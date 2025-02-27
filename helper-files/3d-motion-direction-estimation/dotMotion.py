import numpy as np
from abc import ABC, abstractmethod

import numpy as np
from abc import ABC, abstractmethod

def getXYdisparities(x, y, z, screenDist, ipd, eye):
    """
    Calculate x and y offsets for 2D projection from 3D coordinates.
    
    Parameters:
        x (ndarray): Array of x coordinates.
        y (ndarray): Array of y coordinates.
        z (ndarray): Array of z coordinates.
        screenDist (float): Viewing distance from the screen.
        ipd (float): Inter-pupillary distance.
        eye (tuple or list): A 2-element sequence where eye[0] is the x-coordinate
                             and eye[1] is the y-coordinate.
                             
    Returns:
        xloff (ndarray): x offset for the left eye.
        xroff (ndarray): x offset for the right eye.
        yoff (ndarray): y offset.
    """
    yoff = (y - eye[1]) * z / (screenDist - z)
    xroff = (x - eye[0] - ipd / 2) * z / (screenDist - z)
    xloff = (x - eye[0] + ipd / 2) * z / (screenDist - z)
    return xloff, xroff, yoff

class Projector(ABC):
    @staticmethod
    @abstractmethod
    def project(x, y, z, screenDist, ipd, eye):
        """
        Abstract method for projecting 3D coordinates to 2D screen coordinates.
        Should return (lx_p, rx_p, y_p).
        """
        pass

class TrueProjector(Projector):
    @staticmethod
    def project(x, y, z, screenDist, ipd, eye):
        """
        Project 3D coordinates (x, y, z) to 2D screen coordinates.
        
        Parameters:
            x, y, z: arrays or scalars representing the 3D coordinates.
            screenDist (float): Distance from the screen.
            ipd (float): Inter-pupillary distance.
            eye (tuple or list): Eye position (eye_x, eye_y).
            
        Returns:
            lx_p: Projected x coordinate for the left eye.
            rx_p: Projected x coordinate for the right eye.
            y_p: Projected y coordinate.
        """
        # Compute the disparities (offsets) for projection.
        xloff, xroff, yoff = getXYdisparities(x, y, z, screenDist, ipd, eye)
        # Apply the computed offsets.
        y_p = y + yoff
        lx_p = x + xloff
        rx_p = x + xroff
        return lx_p, rx_p, y_p


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
#         z0 = 2 * self.cubeSize * rng.uniform(0, 1, (self.numDots, 1)) - self.cubeSize
        z0 = self.cubeSize

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
