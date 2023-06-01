import cv2
from keras.models import load_model
import numpy as np
from keras_vggface import utils
from tensorflow.keras.utils import img_to_array
from folders import get_face_train_file

face_cascade = cv2.CascadeClassifier(f'{cv2.data.haarcascades}haarcascade_frontalface_default.xml')
model = load_model(get_face_train_file())

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

        results = model.predict(prep_img)

        print(img)
        for result in results:
            print(str(result))
