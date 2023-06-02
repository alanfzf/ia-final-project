# imports
import pickle
# tensorflow
from keras.layers import Dense, GlobalAveragePooling2D
from keras.applications.mobilenet import preprocess_input
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
from keras_vggface.vggface import VGGFace
# folders
from folders import get_face_labels_file, get_face_train_file, get_processed_folder

W,H = 224,224



train_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
train_generator = train_datagen.flow_from_directory(get_processed_folder(), 
                                                    target_size=(W,H), 
                                                    color_mode='rgb', 
                                                    batch_size=32, 
                                                    class_mode='categorical', 
                                                    shuffle=True)

NO_CLASSES = len(train_generator.class_indices.values())

base_model = VGGFace(include_top=False, model='vgg16', input_shape=(W, H, 3)) 

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
x = Dense(1024, activation='relu')(x)
x = Dense(512, activation='relu')(x)
preds = Dense(NO_CLASSES, activation='softmax')(x)

# create a new model with the base model's original input and the new model's output
model = Model(inputs = base_model.input, outputs = preds)

# don't train the first 19 layers - 0..18
for layer in model.layers[:19]:
    layer.trainable = False

# train the rest of the layers - 19 onwards
for layer in model.layers[19:]:
    layer.trainable = True

model.compile(optimizer='Adam',loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(train_generator, batch_size = 1, verbose = 1, epochs = 20)

# creates a HDF5 file
model.save(get_face_train_file())

# save pickle file
class_dictionary = train_generator.class_indices
class_dictionary = {
    value:key for key, value in class_dictionary.items()
}
print(class_dictionary)

# save the class dictionary to pickle
with open(get_face_labels_file(),'wb') as f: 
    pickle.dump(class_dictionary, f)
