import tensorflow as tf
assert tf.__version__.startswith('2')

import PIL.Image as Image

tf.get_logger().setLevel('ERROR')
from absl import logging
logging.set_verbosity(logging.ERROR)
import numpy as np
# from keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from keras.applications.efficientnet import preprocess_input, decode_predictions

CLASSES = ["real","dolar","euro"]
width = 320
height = 320

def phase1_detection_inference(infer, image, threshold=0.3):


    # #make a prediction
    # img = tf.keras.preprocessing.image.load_img(
    #     './data/images/train/test (1).jpeg',
    #     target_size=(320, 320),
    # )
    
    img = Image.fromarray(image)
    img = img.resize((320,320))
    img_array = tf.keras.preprocessing.image.img_to_array(img).astype('uint8')
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    output = infer(images = img_array)
    # output = model(inputs = img_array)

    count = np.squeeze(output['output_3'])
    scores = np.squeeze(output['output_1'])
    classes = np.squeeze(output['output_2'])
    boxes = np.squeeze( output['output_0'] )

    # print("=====================================")
    # print("count: ", count)
    # print("scores: ", scores)
    # print("classes: ", classes)
    # print("boxes: ", boxes)
    # print("=====================================")

    

    results = []
    for i in range(count):
        if scores[i] >= threshold:
            o1, o2, o3, o4,   = boxes[i]

            o1 = o1 / height
            o2 = o2 / width
            o3 = o3 / height
            o4 = o4 / width


            xmin = o2
            xmax = o4
            ymin = o1
            ymax = o3

            result = {
            'bounding_box': [xmax, xmin, ymax, ymin],
            'class_id': classes[i],
            'score': scores[i]
            }
            results.append(result)
    # print (results)
    return results
