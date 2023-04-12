import cv2


cap = cv2.VideoCaputre(0) 

img=cap.read()

cv2.imshow("Image",img)