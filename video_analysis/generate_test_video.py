import numpy as np
import cv2

# Define codec and create VideoWriter object
fourcc = cv2.cv.CV_FOURCC(*'XVID')
out = cv2.VideoWriter('test_video.avi', fourcc, 10.0, (4, 3), True)

# row, column, RGB
light_frame = np.zeros((4, 3, 3))
dark_frame = np.zeros((4, 3, 3))
dark_frame.fill(255)

# convert to 8bit so it works with VideoWriter.write()
light_frame = np.uint8(light_frame)
dark_frame = np.uint8(dark_frame)

# generate a video that should be flagged
for i in range(0, 20): # 20 loops of 2 frames each = 40 frames; fps=10, so 4 seconds of video
    out.write(light_frame)
    out.write(dark_frame)

out.release()
