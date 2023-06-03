import os
import pathlib
import shutil

# base dir
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# folders
IMG_FOLDER, PROCCESED_FOLDER, TRAINING_FOLDER = 1,2,3

def get_folder(ftype):
    folder = os.path.join(BASE_DIR, "files")
    if ftype == IMG_FOLDER:
        folder = os.path.join(folder, "images")
    elif ftype == PROCCESED_FOLDER:
        folder = os.path.join(folder, "processed")
    elif ftype == TRAINING_FOLDER: 
        folder = os.path.join(folder, "training")
    else:
        return None 

    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
    return folder

def get_images():
    image_dir = get_folder(IMG_FOLDER)
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


def get_dir_for_processed_file(label, filename):
    base_folder = get_folder(PROCCESED_FOLDER)
    # create the folder of the label
    base_folder = os.path.join(base_folder, label)
    pathlib.Path(base_folder).mkdir(parents=True, exist_ok=True)
    # return the file name
    file = os.path.join(base_folder, filename)
    return file

def get_dir_for_labels_file():
    base_folder = get_folder(TRAINING_FOLDER)
    label_file = os.path.join(base_folder, 'face_labels.pickle')
    return label_file

def get_dir_for_training_file():
    base_folder = get_folder(TRAINING_FOLDER)
    training_file = os.path.join(base_folder, 'trained_model_resnet.h5')
    return training_file

def clean_training_files():
    folders = [get_folder(TRAINING_FOLDER), get_folder(PROCCESED_FOLDER)]
    for folder in folders:
        shutil.rmtree(folder)
