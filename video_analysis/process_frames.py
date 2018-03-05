import numpy as np
import cv2
from frame import Frame

cap = cv2.VideoCapture('aotl')
orig_fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
orig_width = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
orig_height = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
print cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)

# Define the codec and create VideoWriter object
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
fourcc = cv2.cv.CV_FOURCC(*'XVID')

# name, fourcc, fps, framesize, [isColor]
out = cv2.VideoWriter('output.avi',fourcc, orig_fps, (orig_width, orig_height))

frames = []

while(cap.isOpened() and len(frames) <= 60):
    ret, frame = cap.read()

    # stop when no more frames to read
    if ret == False:
        break
        
    frames.append(Frame(frame))
    
    # frame = cv2.flip(frame,0)

    # # write the flipped frame
    # out.write(frame)

    # cv2.imshow('frame',frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

# for frame in frames:
#     out.write(cv2.flip(frame.raw_array, 0))

general_idxs = []
red_idxs = []

# Start on second frame so you can compare it to first frame
for idx, current_frame in enumerate(frames[1:]):
    previous_frame = frames[idx - 1]

    darker_L = 0
    lighter_L = 0
    if current_frame.L < previous_frame.L:
        darker_L = current_frame.L
        lighter_L = previous_frame.L
    else:
        darker_L = previous_frame.L
        lighter_L = current_frame.L

    # general oppositing transition formula
    if darker_L < 0.80 and lighter_L - darker_L > lighter_L * 0.10:
        # opposing transition found
        general_idxs.append(idx)

    # red opposing transition formula
    # it's possible previous threshold isn't needed - fixme - see algorithm again
    previous_threshold = previous_frame.R / (previous_frame.R + previous_frame.G + previous_frame.B)
    current_threshold = current_frame.R / (current_frame.R + current_frame.G + current_frame.B)

    previous_delta = (previous_frame.R - previous_frame.G - previous_frame.B) * 320
    current_delta = (current_frame.R - current_frame.G - current_frame.B) * 320

    if previous_threshold > 0.80 and current_threshold > 0.80 and \
        current_delta - previous_delta > 0:
        # red transition found
        red_idxs.append(idx)

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
