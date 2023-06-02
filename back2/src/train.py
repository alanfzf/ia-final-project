# folder access
from folders import clear_training, get_face_train_file_lite, get_processed_folder, get_face_labels_file, get_face_train_file, get_processed_file, get_images

# opencv stuff
import cv2
import numpy as np
import pickle
import uuid

# idk
import keras
import tensorflow as tf
from keras import Sequential
from keras.layers import Flatten, Dense, RandomFlip, RandomRotation, Softmax
from keras_vggface.vggface import VGGFace

W,H = 224, 224
LEARNING_RATE = 0.0001


def prepare_dataset():
    clear_training()

    images = get_images()
    face_classifier = cv2.CascadeClassifier(f'{cv2.data.haarcascades}haarcascade_frontalface_default.xml')

    for _id, label in enumerate(images.keys()):
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
                resized_image = cv2.resize(roi, (W, H))
                img_array = np.array(resized_image, dtype=np.uint8)
                file_name = get_processed_file(label, f"{uuid.uuid4()}.png") 
                cv2.imwrite(file_name, img_array)
    print('Generated faces..!')


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
        Softmax()
    ])

    check_faces(prob_model, class_names)
    model.save(get_face_train_file())
    save_labels(class_names)
    # create_tf_lite_file(prob_model)


def check_faces(tf_model, class_name):
    from keras.utils import img_to_array
    from keras_vggface import utils

    face_cascade = cv2.CascadeClassifier(f'{cv2.data.haarcascades}haarcascade_frontalface_default.xml')
    list = ['./facetest/face0.jpg', './facetest/face1.jpg', './facetest/face2.jpg']

    for img in list:
        image_read = cv2.imread(img, cv2.IMREAD_COLOR)
        image_array = np.array(image_read, "uint8")
        faces = face_cascade.detectMultiScale(image_read, scaleFactor=1.1, minNeighbors=5)

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


def save_labels(labels):
    class_dict = {index: item for index, item in enumerate(labels)}
    with open(get_face_labels_file(),'wb') as f: 
        pickle.dump(class_dict, f)


def save_tf_lite(tf_model):
    resnet_converter = tf.lite.TFLiteConverter.from_keras_model(tf_model)
    resnet_converter.optimizations = [tf.lite.Optimize.DEFAULT]
    resnet_tflite = resnet_converter.convert()

    with open(get_face_train_file_lite(), 'wb') as f:
        f.write(resnet_tflite)

prepare_dataset()
do_training()
