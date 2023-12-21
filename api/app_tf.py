import cv2
import numpy as np
from typing import List


from fastapi import FastAPI, File, UploadFile, Response
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

import tensorflow as tf

from detection.saved_model_detection_inference import phase1_detection_inference
from classification.saved_model_classification_inference import phase2_classification_inference

#TFLite model is way slower on PC than on Android (https://discuss.tensorflow.org/t/efficientdet-lite0-very-slow-on-windows-intel/7756)

CLASSES = ["real","dolar","euro"]
VALUES = ['0.05', '0.10', '0.25', '0.50', '1.00']
#load a saved model
tf.keras.backend.clear_session()
phase1_model = tf.saved_model.load('./detection/saved_model/')
infer = phase1_model.signatures['serving_default']

#phase2
phase2_model = tf.keras.models.load_model('./classification/saved_model/', compile=False)


app = FastAPI()

#CORS, para permitir requisições de outros domínios
origins = [
    "*",
    # "http://localhost:3000", #Frontend do React ou qualquer outro frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/', response_class=HTMLResponse)
def home():
    return '<h1>!Coin Counter!</h1>'


@app.post('/getCoins')
def read_images(image: List[UploadFile]):
    # try:

        image = image[0]
        image_data = image.file.read()
        img = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_UNCHANGED)
        #Caso o shape da imagem possua 4 canais, remover o canal alpha
        if img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        print("Image shape: " + str(img.shape))
        #Getting bounding boxes
        result = phase1_detection_inference(infer, img,0.3)
        
        #Getting the money value

        bbs = []
        for obj in result:
            # Convert the object bounding box from relative coordinates to absolute
            # coordinates based on the original image resolution
            xmax, xmin, ymax, ymin  = obj['bounding_box']
            xmin = int(xmin * img.shape[1])
            xmax = int(xmax * img.shape[1])
            ymin = int(ymin * img.shape[0])
            ymax = int(ymax * img.shape[0])
            # ymax = int(ymax)
            # ymin = int(ymin)
            # xmax = int(xmax)
            # xmin = int(xmin)
            # print("ymin: ", ymin, "ymax: ", ymax, "xmin: ", xmin, "xmax: ", xmax)

            if xmin < 0:
                xmin = 0
            if ymin < 0:
                ymin = 0
            if xmax > img.shape[1]:
                xmax = img.shape[1]
            if ymax > img.shape[0]:
                ymax = img.shape[0]

            if xmin > img.shape[1]:
                xmin = img.shape[1]
            if ymin > img.shape[0]:
                ymin = img.shape[0]
            if xmax < 0:
                xmax = 0
            if ymax < 0:
                ymax = 0
            # print("SUBIMAGE SHAPE: ", img[ymin:ymax, xmin:xmax].shape)

            obj = {
                'bounding_box': [xmin, ymin, xmax, ymax],
                'class': CLASSES[int(obj['class_id'])],
                'score': float(obj['score']),
                'value': float(phase2_classification_inference(phase2_model, img[ymin:ymax, xmin:xmax]))
            }
            bbs.append(obj)


            # Find the class index of the current object
            # class_id = int(obj['class_id'])

            # Draw the bounding box and label on the image
            # cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

        api_return = {'data': bbs}
        return api_return
    # except Exception as e:
    #     print(e)
    #     return Response(status_code=500)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app_tf:app', host='127.0.0.1', port=8080, log_level='info')