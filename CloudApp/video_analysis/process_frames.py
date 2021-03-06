import sys
import datetime

import numpy as np
import numpy.core.multiarray
import cv2
from Frame import Frame

def general_transition(previous_frame, current_frame):

    relative_max = max(np.amax(previous_frame.L), np.amax(current_frame.L))

    selection = current_frame.L[(np.minimum(current_frame.L, previous_frame.L) < 0.8) & \
                (abs(current_frame.L - previous_frame.L) > \
                relative_max * 0.1)]

    if len(selection) > (previous_frame.raw_array.size / 9):
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


def convert_seconds_to_videotime(seconds_in):
    return str(datetime.timedelta(seconds=seconds_in))
  
def analyze(filename):

    # string is the name of the video we want to analyze
    cap = cv2.VideoCapture(filename)

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
    counter = 0
    while(cap.isOpened()):
        ret, raw_frame = cap.read()
        counter += 1
        # stop when no more frames to read
        if ret == False:
            break
        
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
            lower_bound = frame_counter - cap.get(cv2.CAP_PROP_FPS)
            if lower_bound < 0:
                lower_bound = 0

            for frame in general_idxs[:]:
                if frame < lower_bound - 1: # without the -1, we pop crucial frames
                    general_idxs.remove(frame)
                else:
                    break
            transition_counter = len(general_idxs)
            if transition_counter >= TRANSITION_THRESHOLD:
                # The epileptic range should be:
                # From the first frame within the past second to have been detected
                # To the most recently detected frame
                frame_tuples.append((general_idxs[0], frame_counter))

        frame_counter += 1

    # Now that all the frames have been processed,
    # merge the frame intervals and convert to timestamps to be pushed into the database.

    fps = cap.get(cv2.CAP_PROP_FPS)

    #fps = 12    # FIXME: remove in the future, currently CV_CAP_PROP_FPS is inaccurate
    frame_tuples = [(element[0] / fps, element[1] / fps) for element in frame_tuples]

    # I got this from stackoverflow 15273693
    merged_tuples = []
    for begin, end in frame_tuples:
        if merged_tuples and merged_tuples[-1][1] >= begin - 1:
            merged_tuples[-1][1] = max(merged_tuples[-1][1], end)
        else:
            merged_tuples.append([begin, end])

    # From stackoverflow 775049
    timestamp_tuples = [(element[0], element[1])
                        for element in merged_tuples]

    # Release everything if job is finished
    cap.release()
    cv2.destroyAllWindows()

    return timestamp_tuples

