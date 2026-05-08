#!/usr/bin/env bash
# TODO: Test this and see if this would work as expected
# TODO: Need to test it in a windows environment to ensure that it would install and check for python correctly.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REQ_FILE="${REQ_FILE:-$SCRIPT_DIR/requirements.txt}"
VENV_DIR="${VENV_DIR:-$SCRIPT_DIR/.venv}"
CONDA_ENV_NAME="${CONDA_ENV_NAME:-psychophysics-labs}"
KERNEL_NAME="${KERNEL_NAME:-psychophysics-labs}"
KERNEL_DISPLAY_NAME="${KERNEL_DISPLAY_NAME:-Python (psychophysics-labs)}"
REGISTER_KERNEL="${REGISTER_KERNEL:-1}"

if [ ! -f "$REQ_FILE" ]; then
  echo "Could not find requirements file: $REQ_FILE" >&2
  exit 1
fi

detect_os() {
  local uname_s
  uname_s="$(uname -s 2>/dev/null || echo unknown)"
  case "$uname_s" in
    Darwin*) echo "macos" ;;
    Linux*) echo "linux" ;;
    CYGWIN*|MINGW*|MSYS*) echo "windows" ;;
    *) echo "unknown" ;;
  esac
}

version_ok() {
  "$@" -c 'import sys; raise SystemExit(0 if sys.version_info[:2] >= (3, 9) else 1)' >/dev/null 2>&1
}

version_text() {
  "$@" -c 'import sys; print(".".join(map(str, sys.version_info[:3])))'
}

choose_conda() {
  local candidate
  for candidate in micromamba mamba conda; do
    if command -v "$candidate" >/dev/null 2>&1; then
      CONDA_CMD=("$candidate")
      ENV_KIND="conda"
      return 0
    fi
  done
  return 1
}

choose_python() {
  if [ -n "${PYTHON_BIN:-}" ]; then
    if version_ok "$PYTHON_BIN"; then
      PYTHON_CMD=("$PYTHON_BIN")
      ENV_KIND="venv"
      return
    fi
    echo "PYTHON_BIN=$PYTHON_BIN is not Python >=3.9." >&2
    exit 1
  fi

  local candidate
  for candidate in python3.13 python3.12 python3.11 python3.10 python3.9 python3 python; do
    if command -v "$candidate" >/dev/null 2>&1 && version_ok "$candidate"; then
      PYTHON_CMD=("$candidate")
      ENV_KIND="venv"
      return
    fi
  done

  if command -v py >/dev/null 2>&1; then
    local spec
    for spec in -3.11 -3.10 -3.9; do
      if version_ok py "$spec"; then
        PYTHON_CMD=(py "$spec")
        ENV_KIND="venv"
        return
      fi
    done
  fi

  if choose_conda; then
    return
  fi

  cat >&2 <<'EOF'
Could not find a compatible Python interpreter.

The analysis notebooks require Python >=3.9.
Install Python 3.11 or 3.10, or install conda/mamba, then rerun this script.
EOF
  exit 1
}

conda_env_exists() {
  "${CONDA_CMD[@]}" env list 2>/dev/null | awk '{print $1}' | grep -Fx "$CONDA_ENV_NAME" >/dev/null 2>&1
}

print_os_hints() {
  local os_name="$1"
  case "$os_name" in
    macos)
      echo "Detected OS: macOS"
      if command -v brew >/dev/null 2>&1; then
        echo "If Python >=3.9 is missing, install it with: brew install python"
      fi
      ;;
    linux)
      echo "Detected OS: Linux"
      echo "If Python venv setup fails, install your distro's Python venv package."
      if command -v apt-get >/dev/null 2>&1; then
        echo "Ubuntu/Debian hint: sudo apt-get install python3-venv python3-pip"
      elif command -v dnf >/dev/null 2>&1; then
        echo "Fedora hint: sudo dnf install python3 python3-pip"
      elif command -v pacman >/dev/null 2>&1; then
        echo "Arch hint: sudo pacman -S python python-pip"
      fi
      ;;
    windows)
      echo "Detected OS: Windows Bash"
      echo "This script supports Git Bash/MSYS/Cygwin-style Bash. In PowerShell, use the same Python commands manually."
      ;;
    *)
      echo "Detected OS: unknown"
      echo "Continuing with standard Python venv setup."
      ;;
  esac
}

OS_NAME="$(detect_os)"
print_os_hints "$OS_NAME"

PYTHON_CMD=()
CONDA_CMD=()
ENV_KIND=""
choose_python

if [ "$ENV_KIND" = "venv" ]; then
  echo "Using Python: $("${PYTHON_CMD[@]}" -c 'import sys; print(sys.executable)') ($(version_text "${PYTHON_CMD[@]}"))"

  if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment: $VENV_DIR"
    "${PYTHON_CMD[@]}" -m venv "$VENV_DIR"
  else
    echo "Using existing virtual environment: $VENV_DIR"
  fi

  if [ "$OS_NAME" = "windows" ]; then
    ENV_PYTHON="$VENV_DIR/Scripts/python.exe"
    ACTIVATE_CMD="source \"$VENV_DIR/Scripts/activate\""
  else
    ENV_PYTHON="$VENV_DIR/bin/python"
    ACTIVATE_CMD="source \"$VENV_DIR/bin/activate\""
  fi

  if [ ! -x "$ENV_PYTHON" ]; then
    echo "Could not find virtual environment Python at: $ENV_PYTHON" >&2
    exit 1
  fi

  RUN_PYTHON=("$ENV_PYTHON")
else
  echo "No compatible Python was found on PATH; using ${CONDA_CMD[0]} to create/use conda environment: $CONDA_ENV_NAME"
  echo "This can download Python into a conda environment, but it does not install conda itself."
  if ! conda_env_exists; then
    "${CONDA_CMD[@]}" create -y -n "$CONDA_ENV_NAME" "python=3.11" pip
  else
    echo "Using existing conda environment: $CONDA_ENV_NAME"
  fi
  RUN_PYTHON=("${CONDA_CMD[@]}" run -n "$CONDA_ENV_NAME" python)
  ACTIVATE_CMD="${CONDA_CMD[0]} activate $CONDA_ENV_NAME"
  echo "Using Python: $("${RUN_PYTHON[@]}" -c 'import sys; print(sys.executable)') ($(version_text "${RUN_PYTHON[@]}"))"
fi

echo "Upgrading installer tools..."
"${RUN_PYTHON[@]}" -m pip install --upgrade pip wheel

echo "Installing lab packages from: $REQ_FILE"
"${RUN_PYTHON[@]}" -m pip install ${PIP_EXTRA_ARGS:-} -r "$REQ_FILE"

if [ "$REGISTER_KERNEL" = "1" ]; then
  echo "Registering Jupyter kernel: $KERNEL_DISPLAY_NAME"
  "${RUN_PYTHON[@]}" -m ipykernel install --user --name "$KERNEL_NAME" --display-name "$KERNEL_DISPLAY_NAME"
fi

cat <<EOF

Environment setup complete.

Activate it with:
  $ACTIVATE_CMD

Open notebooks with:
  jupyter lab

In Jupyter, choose the kernel:
  $KERNEL_DISPLAY_NAME
EOF
