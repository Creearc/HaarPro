import numpy as np
import cv2, os
import imutils

def HAAR(image):
  cascade = cv2.CascadeClassifier("cascade.xml")
  rects = cascade.detectMultiScale(image, scaleFactor=1.5,
                                     minNeighbors=10, minSize=(30, 30),
                                     flags = cv2.CASCADE_SCALE_IMAGE)
                     
  if len(rects) == 0: return []
  rects[:,2:] += rects[:,:2]
  box = []
  for x1, y1, x2, y2 in rects:
     box.append((x1, y1, x2-x1, y2-y1))
  return box

path = "test_imgs"
for f in os.listdir(path + "/"):
  frame = cv2.imread(path + "/" + f,0)
  boxes = HAAR(frame)
  for box in boxes:
    (x, y, w, h) = [int(v) for v in box]
    cv2.rectangle(frame, (x, y), (x + w, y + h), 0, 3)
    cv2.rectangle(frame, (x, y), (x + w, y + h), 255, 1)
  frame = imutils.resize(frame, height=720, inter=cv2.INTER_NEAREST)
  cv2.imshow('', frame)
  key = cv2.waitKey(0) & 0xFF
  if key == ord("q") or key == 27:
    break

cv2.destroyAllWindows()
