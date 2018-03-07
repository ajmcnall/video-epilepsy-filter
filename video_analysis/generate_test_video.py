import numpy as np
import cv2

# Define codec and create VideoWriter object
fourcc = cv2.cv.CV_FOURCC(*'XVID')
out = cv2.VideoWriter('test_video.avi', fourcc, 10.0, (80, 60), True)


