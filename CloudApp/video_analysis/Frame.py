import numpy as np
import numpy.core.multiarray
import cv2 as cv

class Frame:
    """
    A class that contains all important information
    needed for frame comparison and analysis.
    All numeric values from w3.org
    """
    # opencv frame data is in numpy arrays
    # raw_array = np.ndarray(shape=(0,0))

    def __init__(self, frame_input):
        self.raw_array = frame_input
        (self.B, self.G, self.R) = cv.split(self.raw_array)

        # relative luminance values for RGB
        self.R = calculate_channel(self.R)
        self.G = calculate_channel(self.G)
        self.B = calculate_channel(self.B)
        self.L = 0.2126 * self.R + \
                 0.7152 * self.G + \
                 0.0722 * self.B


def calculate_channel(c):
    """
    Converts sRGB values to RGB values used for relative luminance.
    All numeric values from w3.org
    """

    # get the dimensions of the numpy array
    # reminder - numpy arrays are 
    # arr[row][col] == arr[x down][y right] == arr[height][width]
    # do calculations for each pixel in frame (AKA each value in array)

    c = c / 255.0

    c[c<=0.03928] /= 12.92
    c[c>0.03928] = ((c[c>0.03928] + 0.055) / 1.055) ** 2.4

    return c
