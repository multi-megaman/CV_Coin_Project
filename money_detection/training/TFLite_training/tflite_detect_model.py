from tflite_model_maker.config import ExportFormat, QuantizationConfig
from tflite_model_maker import model_spec
from tflite_model_maker import object_detector

from tflite_support import metadata

import tensorflow as tf
assert tf.__version__.startswith('2')

tf.get_logger().setLevel('ERROR')
from absl import logging
logging.set_verbosity(logging.ERROR)

#------------------------------------------------------------
train_data = object_detector.DataLoader.from_pascal_voc(
    './tf_data/images/train',
    './tf_data/labels/train',
    ['real','dolar','euro']
)

val_data = object_detector.DataLoader.from_pascal_voc(
    './tf_data/images/val',
    './tf_data/labels/val',
     ['real','dolar','euro']
)
#------------------------------------------------------------

"""
Model           	Size(MB)*	Latency(ms)**	Average Precision***
EfficientDet-Lite0	4.4	            37	            25.69%
EfficientDet-Lite1	5.8	            49	            30.55%
EfficientDet-Lite2	7.2	            69	            33.97%
EfficientDet-Lite3	11.4	        116	            37.70%
EfficientDet-Lite4	19.9	        260	            41.96%
"""

spec = model_spec.get('efficientdet_lite0')

model = object_detector.create(train_data, model_spec=spec, batch_size=8, train_whole_model=True, epochs=200, validation_data=val_data)
model.evaluate(val_data)

#save model as savedmodel
model.export(export_dir='.', export_format=ExportFormat.SAVED_MODEL)
# model.evaluate_saved_model('saved_model', val_data)




model.export(export_dir='.', tflite_filename='android.tflite')
print("=======TFLITE MODEL=======")
print(model.evaluate_tflite('android.tflite', val_data))
