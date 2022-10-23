import cv2 as cv


#开启摄像头
cap = cv.VideoCapture(0)

#从摄像头获取图片

f,frame = cap.read()
cv.imwrite('car.jpg',frame)
cap.release()