import tensorflow as tf
import numpy as np
import PIL.Image as Image

CLASSES = [0.05, 0.10, 0.25, 0.50, 1.00]

def phase2_classification_inference(model, image):
    #load a saved model
    

    # #make a prediction
    # img = tf.keras.preprocessing.image.load_img(
    #     './real_data/0.50/test (1)_3.jpeg', target_size=(180, 180)
    # )
    #convert cv2 image to PIL image and resize
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(image)
    img = img.resize((180, 180))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    # plt.imshow(img_array.astype(np.uint8))
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    print("Probabily a", CLASSES[np.argmax(score)], "$ with a confidence of", 100 * np.max(score), "%")
    return CLASSES[np.argmax(score)]