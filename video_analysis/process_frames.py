import numpy as np
import cv2
from frame import Frame

# string is the name of the video we want to analyze
cap = cv2.VideoCapture('aotl')

frames = []

# fixme - remove the 60 limit later
while(cap.isOpened() and len(frames) <= 60):
    ret, frame = cap.read()

    # stop when no more frames to read
    if ret == False:
        break
        
    frames.append(Frame(frame))

    # Algorithm detection can be put here so that each new frame
    # can be analyzed right after the Frame object is created.
    # This would work well if we're working with streams (Youtube).

general_idxs = []
red_idxs = []

# Start on second frame so you can compare it to first frame
for idx, current_frame in enumerate(frames[1:]):
    previous_frame = frames[idx - 1]

    # general oppositing transition formula
    if general_transition(previous_frame, current_frame):
        # opposing transition found
        general_idxs.append(idx)

    # red opposing transition formula
    if red_transition(previous_frame, current_frame):
        # red transition found
        red_idxs.append(idx)

# TODO: general_idxs and red_idxs now have the indexes where there are potentially
# dangerous flashes. Convert indexes to timestamps to be used in the UI.
# If both lists are empty, video is clean.

# print (general_idxs)
# print (red_idxs)

# Release everything if job is finished
cap.release()
cv2.destroyAllWindows()


def general_transition(previous_frame, current_frame):
    height = previous_frame.raw_array.shape[0]
    width = previous_frame.raw_array.shape[1]

    # fixme - not sure what maximum luminance means
    # # maximum L among all pixels in both frames
    # max_L = 0.0

    general_count = 0
    for x in range(height):
        for y in range(width):
            darker_L = 0
            lighter_L = 0
            if current_frame.L[x][y] < previous_frame.L[x][y]:
                darker_L = current_frame.L[x][y]
                lighter_L = previous_frame.L[x][y]
            else:
                darker_L = previous_frame.L[x][y]
                lighter_L = current_frame.L[x][y]

            if darker_L < 0.8 and lighter_L - darker_L > lighter_L * 0.1:
                general_count = general_count + 1
    if general_count / 36 > previous_frame.raw_array.size:
        # detected
        return True
    return False


def red_transition(previous_frame, current_frame):
    height = previous_frame.raw_array.shape[0]
    width = previous_frame.raw_array.shape[1]

    red_count = 0
    for x in range(height):
        for y in range(width):
            # red opposing transition formula
            # it's possible previous threshold isn't needed - fixme - see algorithm again
            previous_threshold = previous_frame.R[x][y] / \
                                 (previous_frame.R[x][y] + previous_frame.G[x][y] + previous_frame.B[x][y])
            current_threshold = current_frame.R[x][y] / \
                                (current_frame.R[x][y] + current_frame.G[x][y] + current_frame.B[x][y])

            previous_delta = (previous_frame.R[x][y] - previous_frame.G[x][y] - previous_frame.B[x][y]) * 320
            current_delta = (current_frame.R[x][y] - current_frame.G[x][y] - current_frame.B[x][y]) * 320

            # fixme - do this following part pixel by pixel, 
            # then see if total number of detected pixels is greater than 1/36 of total pixels
            if previous_threshold > 0.80 and current_threshold > 0.80 and \
                current_delta - previous_delta > 0:
                # red transition found
                red_count = red_count + 1
    
    if red_count / 36 > previous_frame.raw_array.size:
        return True
    return False

