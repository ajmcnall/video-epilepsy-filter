import sys

import numpy as np
import cv2
from frame import Frame

def general_transition(previous_frame, current_frame):
    height = previous_frame.raw_array.shape[0]
    width = previous_frame.raw_array.shape[1]
    
    # fixme - not sure what maximum luminance means
    # # maximum L among all pixels in both frames
    # max_L = 0.0

    # print(np.minimum(current_frame.L, previous_frame.L))
    # print(abs(current_frame.L - previous_frame.L))
    # print(np.maximum(current_frame.L, previous_frame.L) * 0.1)

    selection = current_frame.L[(np.minimum(current_frame.L, previous_frame.L) < 0.8) & \
                (abs(current_frame.L - previous_frame.L) > \
                (np.maximum(current_frame.L, previous_frame.L) * 0.1))]

    if len(selection) > (previous_frame.raw_array.size / 36):
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

            previous_rgb_sum = previous_frame.R[x][y] + previous_frame.G[x][y] + previous_frame.B[x][y]
            # prevent divide by zero error
            if previous_rgb_sum == 0:
                previous_rgb_sum = 1
            previous_threshold = previous_frame.R[x][y] / previous_rgb_sum

            current_rgb_sum = current_frame.R[x][y] + current_frame.G[x][y] + current_frame.B[x][y]
            if current_rgb_sum == 0:
                current_rgb_sum = 1
            current_threshold = current_frame.R[x][y] / current_rgb_sum

            previous_delta = (previous_frame.R[x][y] - previous_frame.G[x][y] - previous_frame.B[x][y]) * 320
            current_delta = (current_frame.R[x][y] - current_frame.G[x][y] - current_frame.B[x][y]) * 320

            # fixme - do this following part pixel by pixel, 
            # then see if total number of detected pixels is greater than 1/36 of total pixels
            if previous_threshold > 0.80 and current_threshold > 0.80 and \
                current_delta - previous_delta > 0:
                # red transition found
                red_count = red_count + 1
    
    if red_count > previous_frame.raw_array.size / 36:
        return True
    return False  
  
  
def process_idxs(idxs):
    # not finished yet - TODO
    print(len(idxs))
    idx_iter = iter(idxs)
    pass
  
  
# string is the name of the video we want to analyze
cap = cv2.VideoCapture('../test_video.avi')
# print cap.get(cv2.CAP_PROP_FRAME_COUNT)

# lists for all the found transitions
general_idxs = []
red_idxs = []

# counter allows us to know during which frame or second a transition is found
frame_counter = 0

# variables to keep track of consequtive frames for comparison purposes
previous_frame = None
current_frame = Frame(cap.read()[1]) # We only care about the frame data for the first part

TRANSITION_THRESHOLD = 7
frame_tuples = []   # a list of tuples that represent the start and end frames of epileptic regions
while(cap.isOpened()):
    ret, raw_frame = cap.read()

    # stop when no more frames to read
    if ret == False:
        break
    
    # frames.append(Frame(frame))

    # Algorithm detection can be put here so that each new frame
    # can be analyzed right after the Frame object is created.
    # This would work well if we're working with streams (Youtube).
    previous_frame = current_frame
    current_frame = Frame(raw_frame)

    if general_transition(previous_frame, current_frame):
        general_idxs.append(frame_counter)
        # Since a transition frame was just found,
        # we want to see if this will make it go beyond the threshold
        # for epilepsy detection. 3.5 flashes (AKA 7 transitions) within 1 second
        transition_counter = 0

        # Lower bound is how far back we can go for it to count in our algorithm
        # Should just be within the previous second
        lower_bound = frame_counter - cv2.cv.CV_CAP_PROP_FPS
        if lower_bound < 0:
            lower_bound = 0

        # Technically not needed
        upper_bound = frame_counter
        if lower_bound >= upper_bound:
            sys.stderr.write('Error: lower_bound is too high.')

        for idx, frame in enumerate(general_idxs):
            if frame < lower_bound:
                general_idxs.pop(idx)
            else:
                break
        transition_counter = len(general_idxs)
        if transition_counter >= TRANSITION_THRESHOLD:
            frame_tuples.append((lower_bound, frame_counter))

    frame_counter += 1

# Now that all the frames have been processed,
# merge the frame intervals and convert to timestamps to be pushed into the database.
# TODO


# print "stop"
# # Start on second frame so you can compare it to first frame
# for idx, current_frame in enumerate(frames):
#     previous_frame = frames[idx - 1]

#     # general oppositing transition formula
#     if general_transition(previous_frame, current_frame):
#         # opposing transition found
#         general_idxs.append(idx)

#     # red opposing transition formula
# #    if red_transition(previous_frame, current_frame):
#         # red transition found
# #        red_idxs.append(idx)

# TODO: general_idxs and red_idxs now have the indexes where there are potentially
# dangerous flashes. Convert indexes to timestamps to be used in the UI.
# If both lists are empty, video is clean.
# process_idxs(general_idxs)
# process_idxs(red_idxs)

print (general_idxs)
print (red_idxs)

# Release everything if job is finished
cap.release()
cv2.destroyAllWindows()

