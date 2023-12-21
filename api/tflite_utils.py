import tensorflow as tf
import numpy as np
import cv2
import time

def preprocess_image(loaded_image, input_size):
    """Preprocess the input image to feed to the TFLite model"""

    resized_img = cv2.resize(loaded_image, input_size)
    resized_img = resized_img[tf.newaxis, :]
    #   resized_img = tf.cast(resized_img, dtype=tf.uint8)
    return resized_img

def detect_objects(signature_fn, image, threshold):
    """Returns a list of detection results, each a dictionary of object info."""
    

    start_time = time.time()

    # Feed the input image to the model
    output = signature_fn(images=image)

    end_time = time.time()
    elapsed_time = end_time - start_time
    # print("Elapsed time to infer: " + str(elapsed_time))

    # Get all outputs from the model
    count = int(np.squeeze(output['output_0']))
    scores = np.squeeze(output['output_1'])
    classes = np.squeeze(output['output_2'])
    boxes = np.squeeze(output['output_3'])
    
    # print("count", count)
    # print("scores", scores)
    # print("classes", classes)
    # print("boxes", boxes)

    results = []
    for i in range(count):
        if scores[i] >= threshold:
            result = {
                'bounding_box': boxes[i].tolist(),
                'class_id': classes[i].tolist(),
                'score': scores[i].tolist()
            }
            results.append(result)
    return results

def Make_Inference(input_size, signature_fn, loaded_image, threshold=0.70):
    # Load the input image and preprocess it
    preprocessed_image = preprocess_image(
        loaded_image,
        input_size
        )

    # Run object detection on the input image
    results = detect_objects(signature_fn, preprocessed_image, threshold=threshold)
    return results



# def preprocess_image(loaded_image, input_size):
#   """Preprocess the input image to feed to the TFLite model"""

#   img = tf.image.convert_image_dtype(loaded_image, tf.uint8)
#   original_image = img
#   resized_img = tf.image.resize(img, input_size)
#   resized_img = resized_img[tf.newaxis, :]
#   resized_img = tf.cast(resized_img, dtype=tf.uint8)
#   return resized_img, original_image