import uuid
import cv2
import numpy as np
from folders import get_images, get_processed_file

images = get_images()
face_classifier = cv2.CascadeClassifier(f'{cv2.data.haarcascades}haarcascade_frontalface_default.xml')
IMG_W, IMG_H = 224, 224

for id, label in enumerate(images.keys()):
    imgs = images[label]

    for img in imgs:
        # load the image
        read_image = cv2.imread(img)
        img_array = np.array(read_image, dtype=np.uint8)
        faces = face_classifier.detectMultiScale(read_image, scaleFactor=1.1, minNeighbors=5)

        if len(faces) != 1:
            print(f'Skipped photo: {label}: {img}')
            continue

        for (x, y, w, h) in faces:
            roi = img_array[y: y+h, x: x+w]
            resized_image = cv2.resize(roi, (IMG_W, IMG_H))
            img_array = np.array(resized_image, dtype=np.uint8)
            file_name = get_processed_file(label, f"{uuid.uuid4()}.png") 
            cv2.imwrite(file_name, img_array)
