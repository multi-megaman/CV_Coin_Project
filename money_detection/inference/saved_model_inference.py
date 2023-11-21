import tensorflow as tf
assert tf.__version__.startswith('2')

tf.get_logger().setLevel('ERROR')
from absl import logging
logging.set_verbosity(logging.ERROR)
import numpy as np
# from keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from keras.applications.efficientnet import preprocess_input, decode_predictions

CLASSES = ["real","dolar","euro"]
threshold = 0.3

#load a saved model
tf.keras.backend.clear_session()
model = tf.saved_model.load('../models/saved_model/')
infer = model.signatures['serving_default']
#List signatures
print(infer.structured_outputs)

#make a prediction
img = tf.keras.preprocessing.image.load_img(
    './test.jpeg',
    target_size=(320, 320),
)


img_array = tf.keras.preprocessing.image.img_to_array(img).astype('uint8')
img_array = tf.expand_dims(img_array, 0) # Create a batch

output = infer(images = img_array)
# output = model(inputs = img_array)

count = np.squeeze(output['output_3'])
scores = np.squeeze(output['output_1'])
classes = np.squeeze(output['output_2'])
boxes = np.squeeze( output['output_0'] )

results = []
for i in range(count):
    if scores[i] >= threshold:
        result = {
        'bounding_box': boxes[i],
        'class_id': classes[i],
        'score': scores[i]
        }
        results.append(result)
#list output keys
# print(results)
