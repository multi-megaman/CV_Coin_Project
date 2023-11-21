import tensorflow as tf
import numpy as np

CLASSES = ['0.05', '0.10', '0.25', '0.50', '1.00']

#load a saved model
model = tf.keras.models.load_model('./saved_model/')

#make a prediction
img = tf.keras.preprocessing.image.load_img(
    './dataset/0.50/test (1)_3.jpeg', target_size=(180, 180)
)
img_array = tf.keras.preprocessing.image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0) # Create a batch

predictions = model.predict(img_array)
score = tf.nn.softmax(predictions[0])

print("Probabily a", CLASSES[np.argmax(score)], "$ with a confidence of", 100 * np.max(score), "%")