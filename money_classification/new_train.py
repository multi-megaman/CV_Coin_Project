import os

import numpy as np

import tensorflow as tf
assert tf.__version__.startswith('2')

from tflite_model_maker import model_spec
from tflite_model_maker import image_classifier
from tflite_model_maker.config import ExportFormat
from tflite_model_maker.config import QuantizationConfig
from tflite_model_maker.image_classifier import DataLoader

import matplotlib.pyplot as plt

image_path = "./real_dataset"
data = DataLoader.from_folder(image_path)
train_data, rest_data = data.split(0.8)
validation_data, test_data = rest_data.split(0.5)

model = image_classifier.create(train_data, validation_data=validation_data,model_spec=model_spec.get('efficientnet_lite0'), epochs=1000)
print(model.evaluate(test_data))
# loss, accuracy = model.evaluate(test_data)
model.export(export_dir='./models', export_format=ExportFormat.SAVED_MODEL)
model.export(export_dir='./models')