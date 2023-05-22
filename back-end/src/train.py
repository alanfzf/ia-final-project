import cv2
import numpy as np
import pickle

from PIL import Image
from folder_dirs import get_images, get_pickle_folder, get_recognizer_folder

images = get_images()
pkl_file = get_pickle_folder('face-labels.pickle')
recog_file = get_recognizer_folder()

face_cascade = cv2.CascadeClassifier(f'{cv2.data.haarcascades}haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

label_ids = {}
y_labels = []
x_train = []

for id, label in enumerate(images.keys()):
    imgs = images[label]
    label_ids[id] = label

    for img in imgs:
        # convert to grayscale
        pil_image = Image.open(img).convert("L") 
        image_array = np.array(pil_image, "uint8")
        faces = face_cascade.detectMultiScale(image_array,scaleFactor=1.5, minNeighbors=5)
        # get all faces
        for (x,y,w,h) in faces:
            roi = image_array[y:y+h, x:x+w]
            x_train.append(roi)
            y_labels.append(id)


with open(pkl_file, 'wb') as f:
    pickle.dump(label_ids, f)

recognizer.train(x_train, np.array(y_labels))
recognizer.save(recog_file)
