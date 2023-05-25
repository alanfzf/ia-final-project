import os
import pathlib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# base images folder
def get_images():
    image_dir = os.path.join(BASE_DIR, "images")
    images = {}

    for root, _, files in os.walk(image_dir):
        for file in files:
            if file.endswith(('.png', '.jpg')):
                path = os.path.join(root, file)
                label = os.path.basename(root).replace(" ", "-").lower()
                if not label in images:
                    images[label] = [path]
                else:
                    images[label].append(path)
    return images

# processed images folders
def get_processed_folder():
    folder = os.path.join(BASE_DIR, "processed")
    return folder

def get_processed_file(label, file):
    folder = os.path.join(BASE_DIR, "processed")
    label_folder = os.path.join(folder, label)
    pathlib.Path(label_folder).mkdir(parents=True, exist_ok=True)
    pfile = os.path.join(label_folder, file)
    return pfile

# training stuff folders
def get_training_folder():
    folder = os.path.join(BASE_DIR, "training")
    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
    return folder

def get_face_labels_file():
    folder = get_training_folder()
    flabels = os.path.join(folder, 'face_labels.pickle')
    return flabels

def get_face_train_file():
    folder = get_training_folder()
    ftrain = os.path.join(folder, 'transfer_learning_trained_face_cnn_model.h5')
    return ftrain
