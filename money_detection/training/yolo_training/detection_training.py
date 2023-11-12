from ultralytics import YOLO

# model = YOLO('yolov8.yaml')

#Worked
model = YOLO('yolov8n.pt')

# model = YOLO('yolov8x.yaml').load('yolov8n.pt') # build from YAML and transfer weights

#training
result = model.train(data='./yolo.yaml', task ='detect', mode ='train', epochs=10, batch=2, imgsz=320, flipud=0.0, fliplr=0.0 )

#val
model.val()
