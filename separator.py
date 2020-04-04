import os
import cv2
import numpy as np
import imutils

import time

ix,iy = -1,-1
s = 50
r = 2

# mouse callback function
def draw_circle(event,x,y,flags,param):
  global ix, iy, s, r, img
  ix,iy = x, y
  if event == cv2.EVENT_LBUTTONUP:
    print('click!')
    cv2.imwrite('Dirt_Good/' + str(time.time()) + '.png',
                img[y - s // 2 + 2 : y + s // 2 - 2, x - s // 2 + 2: x + s // 2 - 2])
    for i in range(-r, r + 1):
      for j in range(-r, r + 1):
        if i == j: continue
        cv2.imwrite('Dirt_Bad/' + str(time.time()) + '.png',
                    img[y - s // 2 + 2 + j * s: y + s // 2 - 2 + j * s, x - s // 2 + 2  + i * s: x + s // 2 - 2 + i * s])
  if event == cv2.EVENT_RBUTTONUP:
    print('declick!')
    cv2.imwrite('Dirt_Bad/' + str(time.time()) + '.png',
                img[y - s // 2 + 2 : y + s // 2 - 2, x - s // 2 + 2: x + s // 2 - 2])
  elif event == cv2.EVENT_MOUSEWHEEL:
    if flags > 0:
      s += 1
    else:
      s -= 1
  elif event == cv2.EVENT_MOUSEHWHEEL:
    s += 1

def setka(img, x, y, s):
  global r
  for i in range(-r, r + 1):
    for j in range(-r, r + 1):
      cv2.rectangle(img, (x - s // 2 + i * s, y - s // 2 + j * s),
                    (x + s // 2 + i * s, y + s // 2 + j * s), (0, 0, 255), 1)
  cv2.rectangle(img, (x - s // 2, y - s // 2),
                (x + s // 2, y + s // 2), (0, 255, 0), 2)
  return img

# Create a black image, a window and bind the function to window
img = np.zeros((512,512,3), np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)

path = 'Data'
fls = os.listdir(path)
counter = 0

while(1):
  img = cv2.imread(path + '/' +fls[counter])
  img = imutils.resize(img, height=720, inter=cv2.INTER_NEAREST)
  img = setka(img, ix, iy, s)
  
  cv2.imshow('image',img)
  k = cv2.waitKey(1) & 0xFF
  if k == 27:
    break
  elif k == ord('a'):
    counter += 1
  elif k == ord('2'):
    r += 1
  elif k == ord('1'):
    r -= 1
  elif k == ord('['):
    s -= 10
  elif k == ord(']'):
    s += 10
cv2.destroyAllWindows()
