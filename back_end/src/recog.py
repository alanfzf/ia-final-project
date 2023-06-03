# opencv
import cv2
import pickle
import numpy as np
import tensorflow as tf
# keras
from keras.layers import Softmax
from keras import Sequential
from keras.models import load_model
from keras_vggface import utils
from keras.utils import img_to_array
#folders
from folders import get_dir_for_training_file, get_dir_for_labels_file

class FaceRecognizer:

    def __init__(self):
        self.model = Sequential([
            load_model(get_dir_for_training_file()),
            Softmax()
        ])
        self.face_cascade = cv2.CascadeClassifier(
            f'{cv2.data.haarcascades}haarcascade_frontalface_default.xml')

        # labels
        with open(get_dir_for_labels_file(), "rb") as f: 
            class_dictionary = pickle.load(f)

        self.classes = [value for _, value in class_dictionary.items()]


    def check_face(self, image):
        prediction = {}
        read_image = cv2.imread(image, cv2.IMREAD_COLOR)
        image_array = np.array(read_image, dtype=np.uint8)
        faces = self.face_cascade.detectMultiScale(
            read_image, scaleFactor=1.1, minNeighbors=5)

        if len(faces) != 1:
            return {
                "error": f"Bad amount of faces detected: {len(faces)}",
            }

        for (x,y,w,h) in faces:
            roi = image_array[y: y+h, x: x+w]
            resized_image = cv2.resize(roi, (224, 224))

            prep_image = img_to_array(resized_image)
            prep_image = np.expand_dims(prep_image, axis=0)
            prep_image = utils.preprocess_input(prep_image, version=1)

            results = self.model.predict(prep_image, verbose=0)
            person = tf.argmax(results, axis=1)[0].numpy()
            prob = tf.reduce_max(results, axis=1)[0].numpy()

            prediction = {
                "predicted_face": self.classes[person],
                "probability": prob,
                # "raw": results
            }

        # return the prediction
        return prediction


    def predict_face(self, bytes):
        prediction = {}

        new_array = np.asarray(bytes, dtype=np.uint8)
        read_image = cv2.imdecode(new_array, cv2.IMREAD_COLOR)
        image_array = np.array(read_image, dtype=np.uint8)

        faces = self.face_cascade.detectMultiScale(
            read_image, scaleFactor=1.1, minNeighbors=5)

        if len(faces) != 1:
            return {
                "error": f"Bad amount of faces detected: {len(faces)}",
            }

        for (x,y,w,h) in faces:
            roi = image_array[y: y+h, x: x+w]
            resized_image = cv2.resize(roi, (224, 224))

            prep_image = img_to_array(resized_image)
            prep_image = np.expand_dims(prep_image, axis=0)
            prep_image = utils.preprocess_input(prep_image, version=1)

            results = self.model.predict(prep_image, verbose=0)
            person = tf.argmax(results, axis=1)[0].numpy()
            prob = tf.reduce_max(results, axis=1)[0].numpy()

            prediction = {
                "predicted_face": self.classes[person],
                "probability": str(prob),
                # "raw": results
            }

        # return the prediction
        return prediction


    def real_time_check(self, image):
        results = self.model.predict(image, verbose=0)
        person = tf.argmax(results, axis=1)[0].numpy()
        prob = tf.reduce_max(results, axis=1)[0].numpy()

        prediction = {
            "predicted_face": self.classes[person],
            # we need to serialize it as a string
            "probability": prob,
        }
        return prediction
