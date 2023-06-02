# folder access
from folders import get_face_train_file_lite, get_processed_folder

# opencv stuff
import cv2
import numpy as np

# idk
import keras
import tensorflow as tf
from keras import Sequential
from keras.layers import Flatten, Dense, RandomFlip, RandomRotation
from keras_vggface.vggface import VGGFace

W,H = 224, 224
LEARNING_RATE = 0.0001

def do_training():
    # hate verbose stuff
    tf.get_logger().setLevel('ERROR')

    #load the data set
    train_dataset = tf.keras.preprocessing.image_dataset_from_directory(
        get_processed_folder(),
        labels='inferred',
        shuffle=True, 
        batch_size=8, 
        image_size=(W,H))

    class_names = train_dataset.class_names
    size = len(class_names)

    print(f"{class_names}, {size}")


    #load the base face recognition model
    resnet_base = VGGFace(
        model='resnet50', 
        include_top=False, 
        input_shape=(W,H,3))

    data_augmentation = Sequential([
        RandomFlip('horizontal'),
        RandomRotation(0.2) ])

    # freeze the base model
    resnet_base.trainable = False

    # build the new model
    inputs = tf.keras.Input(shape=(W, H,3 ))
    x = data_augmentation(inputs)
    x = resnet_base(x)
    x = Flatten(name='flatten')(x)

    out = Dense(size, name='classifier')(x)
    model = keras.Model(inputs, out)

    # train the model
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy']
    )
    model.fit(train_dataset, epochs=20)

    # save the model
    prob_model = Sequential([
        model,
        tf.keras.layers.Softmax()
    ])

    # model.save(get_face_train_file())
    # create_tf_lite_file(prob_model)
    check_faces(prob_model, class_names)


def check_faces(tf_model, class_name):
    from keras.utils import img_to_array
    from keras_vggface import utils

    face_cascade = cv2.CascadeClassifier(f'{cv2.data.haarcascades}haarcascade_frontalface_default.xml')
    list = ['./facetest/face0.jpg', './facetest/face1.jpg', './facetest/face2.jpg']

    for img in list:
        imgtest = cv2.imread(img, cv2.IMREAD_COLOR)
        image_array = np.array(imgtest, "uint8")
        faces = face_cascade.detectMultiScale(imgtest, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            size = (W, H)
            roi = image_array[y: y + h, x: x + w]
            resized_image = cv2.resize(roi, size)

            prep_img = img_to_array(resized_image)
            prep_img = np.expand_dims(prep_img, axis=0)
            prep_img = utils.preprocess_input(prep_img, version=1)

            results = tf_model.predict(prep_img)
            winner = results[0].argmax()
            print(f"Probability: {results}, {winner}")
            print(f"Predicted face: {class_name[winner]}")



def create_tf_lite_file(tf_model):
    resnet_converter = tf.lite.TFLiteConverter.from_keras_model(tf_model)
    resnet_converter.optimizations = [tf.lite.Optimize.DEFAULT]
    resnet_tflite = resnet_converter.convert()
    # save file
    with open(get_face_train_file_lite(), 'wb') as f:
        f.write(resnet_tflite)

do_training()
