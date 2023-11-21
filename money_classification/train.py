import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
import tensorflow as tf

from tensorflow import keras
from keras import layers
from keras.models import Sequential

DATASET_PATH = './real_dataset'
IMAGE_EXTENSION = '.jpeg'

batch_size = 16
img_height = 180
img_width = 180
epochs = 300

# Load dataset ================================================================
import pathlib
data_dir = pathlib.Path(DATASET_PATH)
# Count images
image_count = len(list(data_dir.glob(f'*/*{IMAGE_EXTENSION}')))

# Train dataset ===============================================================
print("=============Train dataset=============")
train_ds = tf.keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="training",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

# Validation dataset ==========================================================
print("=============Validation dataset=============")
val_ds = tf.keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="validation",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

# Class names ================================================================
print("=============Class names=============")
class_names = train_ds.class_names
print(class_names)


AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

normalization_layer = layers.Rescaling(1./255)

# Create the model ============================================================
num_classes = len(class_names)

data_augmentation = keras.Sequential(
  [
    layers.RandomFlip("horizontal",
                      input_shape=(img_height,
                                  img_width,
                                  3)),
    layers.RandomFlip("vertical",
                      input_shape=(img_height,
                                  img_width,
                                  3)),
    layers.RandomRotation((-0.95,0.95)),
    layers.RandomZoom((0.1,0.5)),
    layers.RandomCrop(img_height, img_width),
    layers.RandomContrast((0.7,2)),
  ]
)

model = Sequential([
    data_augmentation,
    layers.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
    layers.Conv2D(16, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(32, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Dropout(0.2), #Dropout layer to avoid overfitting
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(num_classes, activation='softmax')
])

# Compile the model ===========================================================
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# # Model summary ===============================================================
# model.summary()

# Train the model ==============================================================


history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=epochs
)

# Save the model ===============================================================
model.save('./models/saved_model/')

#to TFLite ====================================================================
# Convert the model.
converter = tf.lite.TFLiteConverter.from_saved_model('./models/saved_model/')
tflite_model = converter.convert()
# Save the model.
with open('./modelsmodel.tflite', 'wb') as f:
  f.write(tflite_model)

# Visualize training results ===================================================
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()


