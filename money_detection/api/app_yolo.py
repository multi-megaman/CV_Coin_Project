import cv2
import numpy as np
from typing import List

from returnClass import Item, BoundingBoxCoordinate

from utils import (get_bounding_boxes_yolov8, crop_image_by_bounding_boxes)

from fastapi import FastAPI, File, UploadFile, Response
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from ultralytics import YOLO
yoloModel = YOLO("./detect_model/best_0/best.pt")


app = FastAPI()

#CORS, para permitir requisições de outros domínios
origins = [
    # "*",
    "http://localhost:5173", #Frontend do React
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
def read_images(image: UploadFile) -> List[Item]:
    try:

        image_data = image.file.read()
        img = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_UNCHANGED)
        #Caso o shape da imagem possua 4 canais, remover o canal alpha
        if img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

        #Getting bounding boxes
        bounding_boxes=get_bounding_boxes_yolov8(img, yoloModel)
        cropped_images = crop_image_by_bounding_boxes(img, bounding_boxes)

        #Making the predictions on the coins values
        predictions = [1]*len(bounding_boxes) #phase_2_model.inference
        
        #Montando o retorno da API
        coins_return = []
        for i in range(len(predictions)):
            coins_return.append(Item(bb_coordinates= BoundingBoxCoordinate(top_left= {'x' : bounding_boxes[i][0][0][0],
                                                                                        'y' : bounding_boxes[i][0][0][1]},
                                                                            bottom_right= {'x' : bounding_boxes[i][0][1][0], 
                                                                                            'y' : bounding_boxes[i][0][1][1]}), 
                                    label= bounding_boxes[i][1], 
                                    prediction= predictions[i]))
    # for api in api_return:
    #     print(api)
        return coins_return
    except Exception as e:
        print(e)
        return Response(status_code=500)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app_tflite:app', host='127.0.0.1', port=8080, log_level='info')