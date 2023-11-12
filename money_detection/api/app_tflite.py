import time
import random
import cv2
import numpy as np
from typing import List


from fastapi import FastAPI, File, UploadFile, Response
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

import tensorflow as tf
from tflite_utils import Make_Inference

#TFLite model is way slower on PC than on Android (https://discuss.tensorflow.org/t/efficientdet-lite0-very-slow-on-windows-intel/7756)
MODEL_PATH = './tflite_detect_model/dataset_0.tflite'
# Load the TFLite model
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()
# Get the model details
signature_fn = interpreter.get_signature_runner()
_, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']


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
    try:

        image = image[0]
        image_data = image.file.read()
        img = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_UNCHANGED)
        #Caso o shape da imagem possua 4 canais, remover o canal alpha
        if img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

        #Getting bounding boxes
        result = Make_Inference((input_height, input_width), signature_fn, img, threshold=0.70)
        
        #Getting the money value
        money_values = [1,0.50,0.25,0.10,0.05] #TODO: implement the second model to get the money value

        bbs = []
        for obj in result:
            # Convert the object bounding box from relative coordinates to absolute
            # coordinates based on the original image resolution
            ymin, xmin, ymax, xmax = obj['bounding_box']
            xmin = int(xmin * img.shape[1])
            xmax = int(xmax * img.shape[1])
            ymin = int(ymin * img.shape[0])
            ymax = int(ymax * img.shape[0])

            obj = {
                'bounding_box': [xmin, ymin, xmax, ymax],
                'class': obj['class_id'],
                'score': obj['score'],
                'value': random.choice(money_values) #TODO: change to 'value': money_values[obj['class_id']]
            }
            bbs.append(obj)

            #FOR WEB ONLY
            # Draw the bounding box and label on the image
            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

            # Find the class index of the current object
            # class_id = int(obj['class_id'])

            # Draw the bounding box and label on the image
            # cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

        api_return = {'data': bbs, 'image': img.tolist()}
        return api_return
    except Exception as e:
        print(e)
        return Response(status_code=500)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app_tflite:app', host='127.0.0.1', port=8080, log_level='info')