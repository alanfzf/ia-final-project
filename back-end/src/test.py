# other shit
import cv2
import pickle
import numpy as np
# keras
from keras_vggface import utils
from tensorflow.keras.utils import img_to_array
from tensorflow.keras.models import load_model
# folders
from folders import get_face_labels_file, get_face_train_file

# dimension of images
img_w, img_h = 224, 224

# load labels
with open(get_face_labels_file(), "rb") as f: 
    class_dictionary = pickle.load(f)

class_list = [value for _, value in class_dictionary.items()]
print(class_list)

# face detection
facecascade = cv2.CascadeClassifier(f'{cv2.data.haarcascades}haarcascade_frontalface_default.xml')
model = load_model(get_face_train_file())

for i in range(3): 
    test_image_filename = f'./facetest/face{i}.jpg'
    # load the image
    imgtest = cv2.imread(test_image_filename, cv2.IMREAD_COLOR)
    image_array = np.array(imgtest, "uint8")

    # get the faces detected in the image
    faces = facecascade.detectMultiScale(imgtest, scaleFactor=1.1, minNeighbors=5)

    # if not exactly 1 face is detected, skip this photo
    if len(faces) != 1: 
        print(f'Photo skipped..')
        continue

    for (x_, y_, w, h) in faces:
        # draw the face detected
        face_detect = cv2.rectangle(imgtest, (x_, y_), (x_+w, y_+h), (255, 0, 255), 2)

        # resize the detected face to 224x224
        size = (img_w, img_h)
        roi = image_array[y_: y_ + h, x_: x_ + w]
        resized_image = cv2.resize(roi, size)

        # prepare the image for prediction
        prep_img = img_to_array(resized_image)
        prep_img = np.expand_dims(prep_img, axis=0)
        prep_img = utils.preprocess_input(prep_img, version=1)

        # making prediction
        predicted_prob = model.predict(prep_img)
        print(predicted_prob)
        # print(predicted_prob[0].argmax())
        # print("Predicted face: " + class_list[predicted_prob[0].argmax()])
