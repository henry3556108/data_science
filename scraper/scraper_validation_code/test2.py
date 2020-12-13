import cv2

a = cv2.imread("img0.jpg")
a = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
_, a = cv2.threshold(a,100,255,cv2.THRESH_BINARY)
print(_)
cv2.imshow('',a)
cv2.waitKey(0)