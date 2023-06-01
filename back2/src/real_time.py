import cv2
import numpy as np

from folders import get_face_train_file
from tensorflow.keras.models import load_model
from keras_vggface import utils
from tensorflow.keras.utils import img_to_array

# open cv stuff
face_cascade = cv2.CascadeClassifier(f'{cv2.data.haarcascades}haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

## xd
model = load_model(get_face_train_file())

while(True):

    # Capture frame-by-frame
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = face_cascade.detectMultiScale(rgb, scaleFactor=1.5, minNeighbors=5)

    image_array = np.array(frame, "uint8")
    faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)


    for (x, y, w, h) in faces:
        size = (224, 224)
        roi = image_array[y: y + h, x: x + w]
        resized_image = cv2.resize(roi, size)

        prep_img = img_to_array(resized_image)
        prep_img = np.expand_dims(prep_img, axis=0)
        prep_img = utils.preprocess_input(prep_img, version=1)

        results = model.predict(prep_img)

        for result in results:
            print(str(result))

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
