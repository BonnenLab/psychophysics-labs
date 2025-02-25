import numpy as np
from abc import ABC, abstractmethod

class MotionFactory(ABC):
    @abstractmethod
    def generate(self, rng, speed, theta, phi, totFrames):
        pass

class CoherentMotionFactory(MotionFactory):
    def __init__(self, cubeSize, numDots):
        self.cubeSize = cubeSize
        self.numDots = numDots

    def generate(self, rng, speed, theta, phi, totFrames):
        # Generate initial positions uniformly in the cube [-cubeSize, cubeSize]
        x0 = 2 * self.cubeSize * rng.uniform(0, 1, (self.numDots, 1)) - self.cubeSize
        y0 = 2 * self.cubeSize * rng.uniform(0, 1, (self.numDots, 1)) - self.cubeSize
        z0 = 2 * self.cubeSize * rng.uniform(0, 1, (self.numDots, 1)) - self.cubeSize

        # Calculate trajectory steps: an array from 0 to (totFrames-1)*speed
        r = np.arange(0, totFrames * speed, speed).reshape(1, totFrames)

        # Repeat the initial positions for each frame
        x = np.tile(x0, (1, totFrames))
        y = np.tile(y0, (1, totFrames))
        z = z0 + np.tile(r, (self.numDots, 1))

        # Wrap the z coordinates to keep them inside the cube
        z = np.mod(z + self.cubeSize, 2 * self.cubeSize) - self.cubeSize

        # Build the rotation matrices using angles in degrees
        cos_phi = np.cos(np.deg2rad(phi))
        sin_phi = np.sin(np.deg2rad(phi))
        roty = np.array([
            [cos_phi, 0, sin_phi],
            [0,       1, 0],
            [-sin_phi,0, cos_phi]
        ])

        cos_theta = np.cos(np.deg2rad(theta))
        sin_theta = np.sin(np.deg2rad(theta))
        rotz = np.array([
            [cos_theta, -sin_theta, 0],
            [sin_theta,  cos_theta, 0],
            [0,               0,    1]
        ])

        # Apply the rotations to each dot's trajectory
        for i in range(self.numDots):
            pos = np.vstack((x[i, :], y[i, :], z[i, :]))  # 3 x totFrames
            newpos = rotz @ roty @ pos  # Matrix multiplication: first roty then rotz
            x[i, :], y[i, :], z[i, :] = newpos[0, :], newpos[1, :], newpos[2, :]

        return x, y, z
