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

data = DataLoader.from_folder("./real_dataset")
train_data, test_data = data.split(0.9)

model = image_classifier.create(train_data, batch_size=8, train_whole_model=True, epochs=300, validation_data=test_data)
loss, accuracy = model.evaluate(test_data)

model.export(export_dir='./models/', export_format=ExportFormat.SAVED_MODEL)
model.export(export_dir='.', tflite_filename='./models/android.tflite')