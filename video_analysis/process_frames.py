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

    # darker_L = 0
    # lighter_L = 0
    # if current_frame.L < previous_frame.L:
    #     darker_L = current_frame.L
    #     lighter_L = previous_frame.L
    # else:
    #     darker_L = previous_frame.L
    #     lighter_L = current_frame.L

    # general oppositing transition formula
    # fixme - this following part should be in a loop
    # and pixels should be considered epileptic individually before seeing if
    # total # epileptic pixels > all pixels in the frame/36
    if (current_frame.L < 0.8 or previous_frame < 0.8) and \
       current_frame.L - previous_frame.L > lighter_L * 0.10:
        # opposing transition found
        general_idxs.append(idx)

    # red opposing transition formula
    # it's possible previous threshold isn't needed - fixme - see algorithm again
    previous_threshold = previous_frame.R / (previous_frame.R + previous_frame.G + previous_frame.B)
    current_threshold = current_frame.R / (current_frame.R + current_frame.G + current_frame.B)

    previous_delta = (previous_frame.R - previous_frame.G - previous_frame.B) * 320
    current_delta = (current_frame.R - current_frame.G - current_frame.B) * 320

    # fixme - do this following part pixel by pixel, 
    # then see if total number of detected pixels is greater than 1/36 of total pixels
    if previous_threshold > 0.80 and current_threshold > 0.80 and \
        current_delta - previous_delta > 0:
        # red transition found
        red_idxs.append(idx)

# print (general_idxs)
# print (red_idxs)

# Release everything if job is finished
cap.release()
cv2.destroyAllWindows()