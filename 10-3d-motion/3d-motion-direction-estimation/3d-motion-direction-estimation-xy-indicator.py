#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
3D Motion Direction Estimation  —  Lab 10  (xy-plane indicator version)

Participants view a 100% coherent 3D dot cloud rendered as a red-cyan anaglyph
and estimate the direction of motion on the horizontal-depth (xz) plane using
an overhead-view arrow.

Direction convention (matches Bonnen et al. 2020):
    0°   = rightward   (+x)
    90°  = away        (+z, into screen)
    180° = leftward    (-x)
    270° = toward      (-z, out of screen)

Trial structure:
    fixation (0.5 s)  →  dot cloud (0.5 s)  →  arrow response

Anaglyph rendering:
    Red channel   = left-eye image  (seen through red filter)
    Cyan channels = right-eye image (seen through cyan filter)
    Window uses additive blending so red and cyan dots compose correctly.

Response indicator:
    A frontal (xy-plane) clock-face ring centered on screen, with a radial
    line rotating to show perceived direction.  This version is kept as a
    reference; the xz-plane (perspective-projected pizza) version is in
    3d-motion-direction-estimation.py.

Based on:
    Bonnen et al. (2020). Binocular viewing geometry shapes the neural
    representation of the dynamic three-dimensional environment.
    Nature Neuroscience, 23, 113–121.
"""

import numpy as np
import os
from psychopy import visual, core, data, event, gui
from psychopy.hardware import keyboard as hw_keyboard
import pyglet.gl as gl


# ============================================================
# PARAMETERS
# ============================================================

EXP_NAME = '3d-motion-direction-estimation'

# Physical display
VIEWING_DISTANCE_CM = 57.0   # observer-to-screen distance (typical laptop ~57 cm)
IPD_CM              = 6.5    # interpupillary distance, human average

# Stimulus  (Bonnen et al. 2020, Methods)
N_DOTS              = 20
FIELD_DIAMETER_DEG  = 5.0    # frontoparallel diameter of dot-cloud aperture (deg)
ECCENTRICITY_DEG    = 5.0    # aperture center distance from fixation (deg)
STIM_DURATION_S     = 1.0    # motion display duration (s)
FIXATION_DURATION_S = 0.5    # fixation cross duration (s)
SPEED_CMS           = 5.0    # environmental dot speed (cm/s)
DOT_SIZE_BASE_DEG   = 0.12   # dot diameter at viewing distance (deg); scales with depth
DOT_CONTRAST        = 0.1   # dot luminance as fraction of max (Bonnen et al. 2020 used 0.05)

# Trial structure: 72 directions × 2 visual fields = 144 trials
DIRECTIONS_DEG = np.arange(0, 360, 5)   # 0°, 5°, 10°, …, 355°

# Response arrow rotation per keypress
SLOW_STEP_DEG = 0.5    # left / right arrow keys
FAST_STEP_DEG = 2.5    # up   / down  arrow keys

# Response indicator: frontal clock-face ring centered on screen
INDICATOR_R = 3.0   # radius in degrees

# Colors in PsychoPy rgb space (range −1 to +1)
# Black background required for color-mask anaglyph: masked dots land on black,
# so only the unmasked channel(s) are visible through the corresponding filter lens.
COL_BG    = [ 0,  0,  0]   # mid-gray (Bonnen et al. 2020 background)
COL_WHITE = [ 1,  1,  1]
COL_DIM   = [-0.5, -0.5, -0.5]   # dim gray for labels (visible against mid-gray)
# Dot contrast: Weber contrast relative to mid-gray background
# In PsychoPy's −1 to +1 space, v=0 is mid-gray, so bright/dark are ±DOT_CONTRAST
COL_DOT_BRIGHT = [ DOT_CONTRAST,  DOT_CONTRAST,  DOT_CONTRAST]
COL_DOT_DARK   = [-DOT_CONTRAST, -DOT_CONTRAST, -DOT_CONTRAST]


# ============================================================
# SESSION SETUP
# ============================================================

_thisDir = os.path.dirname(os.path.abspath(__file__))

# Participant info dialog
expInfo = {
    'participant': f"{np.random.randint(0, 999999):06d}",
    'session':     '001',
}
expInfo['date']    = data.getDateStr()
expInfo['expName'] = EXP_NAME

dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=EXP_NAME, alwaysOnTop=True)
if not dlg.OK:
    core.quit()

# Data file (CSV only)
dataDir       = os.path.join(_thisDir, 'data')
os.makedirs(dataDir, exist_ok=True)
data_filename = os.path.join(
    dataDir,
    f"{expInfo['participant']}_{EXP_NAME}_{expInfo['date']}"
)

thisExp = data.ExperimentHandler(
    name=EXP_NAME,
    extraInfo=expInfo,
    savePickle=False,
    saveWideText=True,
    dataFileName=data_filename,
)

# Window — black background, default blending.
# Anaglyph is achieved via OpenGL color masks (glColorMask) rather than additive
# blending: before drawing each eye's dots we restrict writes to only the R channel
# (left eye) or only the G+B channels (right eye).  Dots are white; the mask
# ensures only the appropriate channel reaches the framebuffer.
win = visual.Window(
    size=[1512, 982],
    fullscr=True,
    screen=0,
    monitor='testMonitor',
    color=COL_BG,
    colorSpace='rgb',
    useFBO=True,
    units='deg',
    allowGUI=False,
)
win.mouseVisible = False

frame_rate = win.getActualFrameRate() or 60.0
expInfo['frameRate'] = frame_rate

# Precomputed geometry (world space, cm)
eccentricity_cm = VIEWING_DISTANCE_CM * np.tan(np.deg2rad(ECCENTRICITY_DEG))
sphere_r_cm     = VIEWING_DISTANCE_CM * np.tan(np.deg2rad(FIELD_DIAMETER_DEG / 2.0))


# ============================================================
# STIMULI
# ============================================================

fixation = visual.ShapeStim(
    win=win, vertices='cross', size=(0.4, 0.4),
    fillColor=COL_WHITE, lineColor=COL_WHITE, colorSpace='rgb',
)

# Left-eye and right-eye dot clouds — half bright, half dark (set per trial).
# The correct eye channel is selected at draw time via glColorMask (see draw_dots()).
left_eye_dots = visual.ElementArrayStim(
    win=win, nElements=N_DOTS,
    elementTex=None, elementMask='circle',
    sizes=DOT_SIZE_BASE_DEG,
    colors=COL_DOT_BRIGHT, colorSpace='rgb',
    xys=np.zeros((N_DOTS, 2)),
)
right_eye_dots = visual.ElementArrayStim(
    win=win, nElements=N_DOTS,
    elementTex=None, elementMask='circle',
    sizes=DOT_SIZE_BASE_DEG,
    colors=COL_DOT_BRIGHT, colorSpace='rgb',
    xys=np.zeros((N_DOTS, 2)),
)

# Response indicator — frontal clock-face ring + radial line + dot at each end.
# The line runs from the circle centre to the circle edge; rotating it shows direction.
indicator_circle = visual.Circle(
    win=win, radius=INDICATOR_R,
    lineColor=COL_WHITE, fillColor=None, colorSpace='rgb',
    lineWidth=1.5, edges=64, pos=(0, 0),
)
# Line drawn as a thin rectangle (ShapeStim line); ori rotates it.
indicator_line = visual.ShapeStim(
    win=win,
    vertices=[(-0.04, 0), (0.04, 0), (0.04, INDICATOR_R), (-0.04, INDICATOR_R)],
    fillColor=COL_WHITE, lineColor=COL_WHITE, colorSpace='rgb',
    pos=(0, 0), ori=0,
)
# Small dot at the centre
indicator_dot_center = visual.Circle(
    win=win, radius=0.12,
    fillColor=COL_WHITE, lineColor=COL_WHITE, colorSpace='rgb',
    pos=(0, 0),
)
# Small dot at the outer tip — position is updated each frame from angle
indicator_dot_tip = visual.Circle(
    win=win, radius=0.12,
    fillColor=COL_WHITE, lineColor=COL_WHITE, colorSpace='rgb',
    pos=(0, INDICATOR_R),
)

# Cardinal labels shown during the response phase (overhead-view orientation)
_lbl = dict(win=win, height=0.45, color=COL_DIM, colorSpace='rgb')
lbl_right  = visual.TextStim(**_lbl, text='RIGHT ->',  pos=( 7.0,  0.0))
lbl_away   = visual.TextStim(**_lbl, text='↑ AWAY',   pos=( 0.0,  5.0))
lbl_left   = visual.TextStim(**_lbl, text='← LEFT',   pos=(-7.0,  0.0))
lbl_toward = visual.TextStim(**_lbl, text='TOWARD ↓', pos=( 0.0, -5.0))

response_prompt = visual.TextStim(
    win=win, color=COL_WHITE, colorSpace='rgb',
    height=0.45, pos=(0, -8.0), wrapWidth=26,
    text=(
        'Indicate the 3D direction of motion  (viewed from above)\n'
        'LEFT / RIGHT arrows: rotate slowly      UP / DOWN arrows: rotate quickly\n'
        'ENTER to confirm'
    ),
)

msg = visual.TextStim(
    win=win, color=COL_WHITE, colorSpace='rgb',
    height=0.6, pos=(0, 0), wrapWidth=24,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def init_dot_cloud(n_dots, cx, cy, cz, radius):
    """
    Initialise n_dots as 3D points uniformly distributed within a sphere.
    cx, cy, cz : sphere centre in world coordinates (cm)
    radius     : sphere radius (cm)
    Returns an (n_dots, 3) array of (x, y, z) positions.
    """
    pts = np.empty((n_dots, 3))
    filled = 0
    while filled < n_dots:
        batch    = max((n_dots - filled) * 5, 200)
        cands    = np.random.uniform(-radius, radius, (batch, 3))
        inside   = np.sum(cands ** 2, axis=1) <= radius ** 2
        cands    = cands[inside]
        take     = min(len(cands), n_dots - filled)
        pts[filled:filled + take] = cands[:take]
        filled  += take
    pts[:, 0] += cx
    pts[:, 1] += cy
    pts[:, 2] += cz
    return pts


def step_dots(pts, dx, dz, cx, cy, cz, radius):
    """
    Translate all dots by (dx, 0, dz) in world space, then wrap any dot that
    has exited the sphere back through the sphere centre (cyclic motion).
    """
    pts[:, 0] += dx
    pts[:, 2] += dz
    rel     = pts - np.array([cx, cy, cz])
    outside = np.sum(rel ** 2, axis=1) > radius ** 2
    if np.any(outside):
        pts[outside] -= 2.0 * rel[outside]
    return pts


def project_to_screen(pts, D, ipd):
    """
    Perspective-project 3D world points to 2D screen positions for each eye.

    Eyes are at (−ipd/2, 0, 0) [left] and (+ipd/2, 0, 0) [right].
    The screen plane is at z = D.  Vergence is compensated so that the
    fixation point (0, 0, D) maps to screen centre (0°, 0°) for both eyes.

    Parameters
    ----------
    pts : (N, 3) array  — world positions in cm
    D   : float         — viewing distance / screen depth (cm)
    ipd : float         — interpupillary distance (cm)

    Returns
    -------
    left_xy  : (N, 2)  screen positions in degrees for left  eye
    right_xy : (N, 2)  screen positions in degrees for right eye
    sizes    : (N,)    dot sizes in degrees (looming / recession cue)
    """
    x, y, z = pts[:, 0], pts[:, 1], pts[:, 2]
    eL, eR = -ipd / 2.0,  ipd / 2.0

    # Ray from each eye through the 3D point, intersected with screen plane z = D
    # screen_x = eye_x + D * (world_x − eye_x) / world_z
    sx_L = eL + D * (x - eL) / z
    sx_R = eR + D * (x - eR) / z
    sy   = D * y / z          # same for both eyes (eyes share the same y)

    # Convert screen-plane offsets (cm) to degrees of visual angle
    left_xy  = np.degrees(np.arctan2(np.column_stack([sx_L, sy]),  D))
    right_xy = np.degrees(np.arctan2(np.column_stack([sx_R, sy]),  D))

    # Dot size scales with distance: closer dots subtend a larger angle (looming)
    sizes = np.clip(
        DOT_SIZE_BASE_DEG * D / z,
        DOT_SIZE_BASE_DEG * 0.4,
        DOT_SIZE_BASE_DEG * 2.5,
    )
    return left_xy, right_xy, sizes


def draw_dots(l_xy, r_xy, sizes):
    """
    Draw the anaglyph dot cloud for one frame using OpenGL color masks.

    Left-eye  dots → red   channel only  (gl.glColorMask(True,  False, False, True))
    Right-eye dots → green+blue channels (gl.glColorMask(False, True,  True,  True))

    Both dot arrays are white; the mask routes each to the correct channel.
    The framebuffer must be cleared to black before calling this each frame
    (win.flip() handles the clear).
    """
    left_eye_dots.xys   = l_xy
    left_eye_dots.sizes = sizes
    right_eye_dots.xys  = r_xy
    right_eye_dots.sizes = sizes

    # Red channel only — left eye
    gl.glColorMask(gl.GL_TRUE, gl.GL_FALSE, gl.GL_FALSE, gl.GL_TRUE)
    left_eye_dots.draw()

    # Green + blue channels only — right eye (cyan through cyan filter)
    gl.glColorMask(gl.GL_FALSE, gl.GL_TRUE, gl.GL_TRUE, gl.GL_TRUE)
    right_eye_dots.draw()

    # Restore full color writes for all other stimuli (fixation, arrow, text)
    gl.glColorMask(gl.GL_TRUE, gl.GL_TRUE, gl.GL_TRUE, gl.GL_TRUE)


def quit_experiment():
    thisExp.saveAsWideText(data_filename + '.csv', delim=',')
    thisExp.abort()
    win.close()
    core.quit()


# ============================================================
# INSTRUCTIONS
# ============================================================

msg.text = (
    "3D Motion Direction Estimation\n\n"
    "A brief cloud of dots will appear to your left or right.\n"
    "The dots are moving in 3D — left/right and toward/away.\n\n"
    "After each display, rotate a line to show the direction\n"
    "of motion as seen from ABOVE (bird's-eye view):\n\n"
    "  up = AWAY (into screen)\n"
    "  down = TOWARD (out of screen)\n"
    "  left/right = LEFT/RIGHT\n\n"
    "LEFT / RIGHT arrow keys  —  rotate slowly\n"
    "UP   / DOWN  arrow keys  —  rotate quickly\n"
    "ENTER  —  confirm your response\n\n"
    "Put on your RED-CYAN anaglyph glasses now.\n"
    "  RED filter  —  LEFT eye\n"
    "  CYAN filter —  RIGHT eye\n\n"
    "Press ENTER to begin."
)
msg.draw()
win.flip()
event.waitKeys(keyList=['return'])


# ============================================================
# TRIAL SETUP
# ============================================================

# Every direction shown once in each visual field → 144 trials
trial_list = [
    {'direction': float(d), 'side': side}
    for d    in DIRECTIONS_DEG
    for side in ('left', 'right')
]
np.random.shuffle(trial_list)

n_stim_frames  = int(round(STIM_DURATION_S * frame_rate))
response_clock = core.Clock()
kb             = hw_keyboard.Keyboard()


# ============================================================
# MAIN TRIAL LOOP
# ============================================================

for trial_num, trial in enumerate(trial_list):
    theta_deg = trial['direction']
    side      = trial['side']

    # Dot-cloud centre in world space (cm)
    cx = eccentricity_cm if side == 'right' else -eccentricity_cm
    cy = 0.0
    cz = VIEWING_DISTANCE_CM

    # Per-frame displacement in the xz plane (cm)
    # Convention: cos → x (left-right), sin → z (toward-away)
    theta_rad = np.deg2rad(theta_deg)
    dx = np.cos(theta_rad) * SPEED_CMS / frame_rate
    dz = np.sin(theta_rad) * SPEED_CMS / frame_rate

    # Initialise dot cloud at random positions within the sphere
    dots = init_dot_cloud(N_DOTS, cx, cy, cz, sphere_r_cm)

    # Randomly assign half dots bright, half dark; same assignment for both eyes
    dot_colors = np.array(COL_DOT_BRIGHT * N_DOTS, dtype=float).reshape(N_DOTS, 3)
    dark_idx = np.random.choice(N_DOTS, N_DOTS // 2, replace=False)
    dot_colors[dark_idx] = COL_DOT_DARK
    left_eye_dots.colors  = dot_colors
    right_eye_dots.colors = dot_colors

    # ── Fixation ─────────────────────────────────────────────
    fixation.draw()
    win.flip()
    core.wait(FIXATION_DURATION_S)

    # ── Stimulus ─────────────────────────────────────────────
    for _ in range(n_stim_frames):
        dots = step_dots(dots, dx, dz, cx, cy, cz, sphere_r_cm)
        l_xy, r_xy, sizes = project_to_screen(dots, VIEWING_DISTANCE_CM, IPD_CM)

        fixation.draw()
        draw_dots(l_xy, r_xy, sizes)
        win.flip()

        if event.getKeys(keyList=['escape']):
            quit_experiment()

    # ── Response ─────────────────────────────────────────────
    # Indicator starts at a random angle; participant rotates to match perceived motion.
    # Holding a key down continues rotating each frame.
    angle = float(np.random.uniform(0, 360))
    response_clock.reset()
    rt        = None
    responded = False
    kb.clearEvents()

    while not responded:
        # Check for a confirm or quit keypress (single events)
        for key in event.getKeys(['return', 'escape']):
            if key == 'escape':
                quit_experiment()
            elif key == 'return':
                rt        = response_clock.getTime()
                responded = True

        if not responded:
            # Held-key rotation: getState(key) returns True while key is held down
            left_held, right_held, up_held, down_held = kb.getState(
                ['left', 'right', 'up', 'down']
            )
            if left_held:  angle = (angle + SLOW_STEP_DEG) % 360
            if right_held: angle = (angle - SLOW_STEP_DEG) % 360
            if up_held:    angle = (angle + FAST_STEP_DEG) % 360
            if down_held:  angle = (angle - FAST_STEP_DEG) % 360

            # Indicator orientation
            # PsychoPy ori=0 → pointing up; our 90° = away = up, so ori = (90 − angle)
            ori = (90 - angle) % 360
            indicator_line.ori = ori

            # Tip dot position: angle=0 → right (+x), angle=90 → up (+y, = away)
            rad = np.deg2rad(angle)
            indicator_dot_tip.pos = (INDICATOR_R * np.cos(rad),
                                     INDICATOR_R * np.sin(rad))

            indicator_circle.draw()
            indicator_line.draw()
            indicator_dot_center.draw()
            indicator_dot_tip.draw()
            lbl_right.draw()
            lbl_away.draw()
            lbl_left.draw()
            lbl_toward.draw()
            response_prompt.draw()
            win.flip()

    # Circular angular error: positive = CCW overshoot, negative = CW undershoot
    error_deg = (angle - theta_deg + 180) % 360 - 180

    thisExp.addData('trial_num',              trial_num + 1)
    thisExp.addData('direction_presented_deg', theta_deg)
    thisExp.addData('side',                    side)
    thisExp.addData('response_direction_deg',  angle)
    thisExp.addData('direction_error_deg',     error_deg)
    thisExp.addData('response_time_s',         rt)
    thisExp.nextEntry()


# ============================================================
# END SCREEN
# ============================================================

msg.text = (
    "Experiment complete!\n\n"
    "Thank you for participating.\n\n"
    "Press ENTER to exit."
)
msg.draw()
win.flip()
event.waitKeys(keyList=['return'])

thisExp.close()
win.close()
core.quit()
