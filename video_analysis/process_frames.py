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
    print len(frames)
    
    # frame = cv2.flip(frame,0)

    # # write the flipped frame
    # out.write(frame)

    # cv2.imshow('frame',frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

for frame in frames:
    out.write(cv2.flip(frame.raw_array, 0))

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
