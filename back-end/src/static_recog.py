from folders import get_face_train_file, get_face_labels_file
from keras import Sequential
from keras.models import load_model
from keras_vggface import utils
from keras.utils import img_to_array

import cv2
import pickle
import numpy as np
import tensorflow as tf

face_cascade = cv2.CascadeClassifier(f'{cv2.data.haarcascades}haarcascade_frontalface_default.xml')
model = load_model(get_face_train_file())
prob_model = Sequential([ model, tf.keras.layers.Softmax() ])

# load labels
with open(get_face_labels_file(), "rb") as f: 
    class_dictionary = pickle.load(f)

class_list = [value for _, value in class_dictionary.items()]

def check_faces(tf_model):
    face_cascade = cv2.CascadeClassifier(f'{cv2.data.haarcascades}haarcascade_frontalface_default.xml')
    list = ['./facetest/face0.jpg', './facetest/face1.jpg', './facetest/face2.jpg']

    for img in list:
        imgtest = cv2.imread(img, cv2.IMREAD_COLOR)
        image_array = np.array(imgtest, "uint8")
        faces = face_cascade.detectMultiScale(imgtest, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            size = (224, 224)
            roi = image_array[y: y + h, x: x + w]
            resized_image = cv2.resize(roi, size)

            prep_img = img_to_array(resized_image)
            prep_img = np.expand_dims(prep_img, axis=0)
            prep_img = utils.preprocess_input(prep_img, version=1)

            results = tf_model.predict(prep_img)

            winner = results[0].argmax()
            print(f"Photo: {img}")
            print(f"Probability: {results}, {winner}")
            print(f"Predicted face: {class_list[winner]}")

check_faces(prob_model)
