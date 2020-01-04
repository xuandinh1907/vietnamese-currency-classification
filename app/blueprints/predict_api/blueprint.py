from flask import Blueprint, render_template, request
from flask import Blueprint, jsonify, request
import tensorflow as tf
import numpy as np
import re
import os
import base64
import uuid

predict_api = Blueprint('predict_api', __name__)
model = tf.keras.models.load_model("models/vnd_classifier.h5")
class_names = np.array(['1000', '2000', '5000', '10000', '20000', 
                        '50000', '100000', '200000', '500000'])

def parse_image(imgData):
    img_str = re.search(b"base64,(.*)", imgData).group(1)
    img_decode = base64.decodebytes(img_str)
    filename = "{}.jpg".format(uuid.uuid4().hex)
    with open('uploads/'+filename, "wb") as f:
        f.write(img_decode)
    return img_decode

def preprocess(image):
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, [192, 192])
    # Use `convert_image_dtype` to convert to floats in the [0,1] range.
    image = tf.image.convert_image_dtype(image, tf.float32)
    image = (image*2) - 1  # normalize to [-1,1] range
    image = tf.image.per_image_standardization(image)
    return image
    
@predict_api.route('/predict/', methods=['POST'])
def predict():
    data = request.get_json()

    # Preprocess the upload image
    img_raw = data['data-uri'].encode()
    image = parse_image(img_raw)
    image = preprocess(image)
    image = tf.expand_dims(image, 0)

    probs = model.predict(image)
    label = np.argmax(probs, axis=1)
    label = class_names[label[0]]
    probs = probs[0].tolist()
    probs = [(probs[i], class_names[i]) for i in range(len(class_names))]

    return jsonify({'label': label, 'probs': probs}) 
