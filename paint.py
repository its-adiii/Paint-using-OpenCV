import cv2
import numpy as np

framewidth = 640
frameheight = 480

cap = cv2.VideoCapture(0)
cap.set(3, framewidth)
cap.set(4, frameheight)
cap.set(10, 130)

myColors = [[5,107,0,19,255,255]] #for orange(BGR)
           
#list containing the values of the HSV track bars created in colour detection

myColorValues = [[51,153,255]]

myPoints = [] #[x, y, colorId]


def findColor(img, myColors, myColorValues):
  imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  count = 0 # everytime counter counts we come to know which colour is detected
  newPoints = [] #everytime the newpoints change, it will start with the empty list and then subsequent points are appended
  for color in myColors:

    lower = np.array(myColors[0][0:3])
    upper = np.array(myColors[0][3:6])
    mask = cv2.inRange(imgHSV, lower, upper)
    x,y = getContours(mask)
    cv2.circle(imgResult,(x,y),10, myColorValues[count], 3)
    if x != 0 and y != 0:
      newPoints.append([x,y,count])
    count += 1
    #cv2.imshow(str(color[0]), mask)
  return newPoints

def getContours(img):
  contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
  x,y,w,h = 0,0,0,0
  for cnt in contours:
    area = cv2.contourArea(cnt)

    if area>500:

      cv2.drawContours(imgResult, cnt, -1, (51,153,255), 3)
      peri = cv2.arcLength(cnt, True)
      approx = cv2.approxPolyDP(cnt, 0.02*peri,True)
      x, y, w, h = cv2.boundingRect(approx)
  return x+w//2,y
      
def drawOnCanvas(myPoints, myColorValues):
  for point in myPoints:
    cv2.circle(imgResult,(point[0],point[1]),10, myColorValues[point[2]], 3)


while True:
  success, img = cap.read()
  imgResult = img.copy()
  newPoints = findColor(img, myColors, myColorValues)
  if len(newPoints)!= 0:
    for newP in newPoints:
      myPoints.append(newP) 

      if len(myPoints)!=0:
        drawOnCanvas(myPoints, myColorValues)
      #for loop used because we are getting myPoints as a list and we cannot include list inside another list
  findColor(img, myColors, myColorValues)
  cv2.imshow("Result", imgResult)
  if cv2.waitKey(1) & 0xFF ==ord('q'):
    break