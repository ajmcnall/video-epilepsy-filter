import numpy as np
import cv2 as cv

class Frame:
    """
    A class that contains all important information
    needed for frame comparison and analysis.
    """
    # opencv frame data is in numpy arrays
    # raw_array = np.ndarray(shape=(0,0))

    def __init__(self, frame_input):
        self.raw_array = frame_input
        (self.B, self.G, self.R) = cv.split(self.raw_array)

        # relative luminance values for RGB
        self.R = self.R / 255.0
        if self.R <= 0.03928:
            self.R = self.R / 12.92
        else:
            self.R = ((self.R + 0.055) / 1.055) ** 2.4
