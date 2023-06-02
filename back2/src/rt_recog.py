import numpy as np
import cv2
import pickle
from keras.models import Sequential, load_model
from folders import get_face_train_file, get_face_labels_file

from keras.layers import Softmax
from keras.utils import img_to_array
from keras_vggface import utils

# for face detection
face_cascade = cv2.CascadeClassifier(f'{cv2.data.haarcascades}haarcascade_frontalface_default.xml')

# resolution of the webcam
screen_width = 1280
screen_height = 720

# size of the image to predict
image_width = 224
image_height = 224

# load the trained model
og_model = load_model(get_face_train_file())
prob_model = Sequential([ og_model, Softmax() ])

# the labels for the trained model
with open(get_face_labels_file(), 'rb') as f:
    og_labels = pickle.load(f)
    labels = {key:value for key,value in og_labels.items()}

# default webcam
stream = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    (grabbed, frame) = stream.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # try to detect faces in the webcam
    faces = face_cascade.detectMultiScale(rgb, scaleFactor=1.3, minNeighbors=5)

    # for each faces found
    for (x, y, w, h) in faces: 
        roi_rgb = rgb[y:y+h, x:x+w]

        # Draw a rectangle around the face
        color = (255, 0, 0) # in BGR
        stroke = 2
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, stroke)

        size = (224, 224)
        resized_image = cv2.resize(roi_rgb, size)

        prep_img = img_to_array(resized_image)
        prep_img = np.expand_dims(prep_img, axis=0)
        prep_img = utils.preprocess_input(prep_img, version=1)

        # predict the image
        predicted_prob = prob_model.predict(prep_img)
        person = predicted_prob[0].argmax()
        print(predicted_prob)


        # Display the label
        color = (255, 0, 255)
        name = labels[person]
        stroke = 2
        cv2.putText(frame, f'({name}) 80%', (x,y-8), cv2.FONT_HERSHEY_SIMPLEX, 1, color, stroke, cv2.LINE_AA)

    # Show the frame
    cv2.imshow("Image", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):    # Press q to break out of the loop
        break      

# Cleanup
stream.release()
cv2.destroyAllWindows()
