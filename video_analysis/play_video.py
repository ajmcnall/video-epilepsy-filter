import numpy as np
import cv2

cap = cv2.VideoCapture('aotl')
cap.set(cv2.CAP_PROP_POS_FRAMES, 17)

ret, frame = cap.read()

while(cap.isOpened()):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame',gray)
    print cap.get(cv2.CAP_PROP_POS_FRAMES)

    key = cv2.waitKey(0)
    if key == ord('k'):
        ret, frame = cap.read()
        cv2.imshow('frame',gray)
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
