import pickle
import tensorflow as tf
import keras
from keras import Sequential
from keras.layers import Flatten, Dense, RandomFlip, RandomRotation
from keras_vggface.vggface import VGGFace
import numpy as np
from folders import get_face_train_file, get_face_train_file_lite, get_processed_folder,get_face_labels_file

train_dataset = tf.keras.preprocessing.image_dataset_from_directory(get_processed_folder(),shuffle=True, batch_size=8, image_size=(224, 224))

vggface_resnet_base = VGGFace(model='resnet50', include_top=False, input_shape=(224,224,3))
data_augmentation = Sequential([
    RandomFlip('horizontal'),
    RandomRotation(0.2)
])

# freeze the base model
nb_class = 2
vggface_resnet_base.trainable = False

# build the new model
inputs = tf.keras.Input(shape=(224, 224,3 ))
x = data_augmentation(inputs)
x = vggface_resnet_base(x)
x = Flatten(name='flatten')(x)

out = Dense(nb_class, name='classifier')(x)
model = keras.Model(inputs, out)

# train
base_learning_rate = 0.0001
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=base_learning_rate),
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy']
)

history = model.fit(train_dataset, epochs=20)

# create HDF5 file
model.save(get_face_train_file())

# save pickle file
list = ['./facetest/face0.jpg', './facetest/face1.jpg', './facetest/face2.jpg']

prob_model = Sequential([
    model,
    tf.keras.layers.Softmax()
])



import cv2
import numpy as np
import tensorflow as tf
# 
from keras_vggface import utils
from tensorflow.keras.utils import img_to_array

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

        results = prob_model.predict(prep_img)

        for result in results:
            print(str(result))


# lite tensorflow
vggface_resnet_converter = tf.lite.TFLiteConverter.from_keras_model(model)
vggface_resnet_converter.optimizations = [tf.lite.Optimize.DEFAULT]
vggface_resnet_tflite = vggface_resnet_converter.convert()

with open(get_face_train_file_lite(), 'wb') as f:
    f.write(vggface_resnet_tflite)
