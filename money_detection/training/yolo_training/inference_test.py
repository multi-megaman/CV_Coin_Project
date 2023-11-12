from ultralytics import YOLO
import cv2

im2 = cv2.imread("./test1.jpeg")

#load model
model = YOLO('./best.pt')

#inference
results = model(im2)  # save predictions as labels

