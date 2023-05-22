import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_pickle_folder(file):
    folder = os.path.join(BASE_DIR, "pickles")
    file = os.path.join(folder, file)
    return file

def get_recognizer_folder():
    folder = os.path.join(BASE_DIR, "recognizers")
    file = os.path.join(folder, "face-trainner.yml")
    return file


def get_images():
    image_dir = os.path.join(BASE_DIR, "images")
    images = {}

    for root, _, files in os.walk(image_dir):
        for file in files:
            if file.endswith("png") or file.endswith("jpg"):
                path = os.path.join(root, file)
                label = os.path.basename(root).replace(" ", "-").lower()

                if not label in images:
                    images[label] = [path]

                img_list = images[label]
                img_list.append(path)

    return images
