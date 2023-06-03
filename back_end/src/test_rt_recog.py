import cv2
import numpy as np
from keras.utils import img_to_array
from keras_vggface import utils
from recog import FaceRecognizer

# variables
stream = cv2.VideoCapture(0)
rectangle_color = (48, 201, 59)
label_color = (48, 201, 59)
stroke = 2
rcg = FaceRecognizer()
face_cascade = cv2.CascadeClassifier(f'{cv2.data.haarcascades}haarcascade_frontalface_default.xml')

while(True):
    # Capture frame-by-frame
    _, frame = stream.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Detect the faces
    faces = face_cascade.detectMultiScale(rgb, 
                                          scaleFactor=1.3, 
                                          minNeighbors=5)

    for (x, y, w, h) in faces: 
        roi_rgb = rgb[y:y+h, x:x+w]
        # Draw a rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), 
                      rectangle_color, stroke)

        # prep the image
        resized_image = cv2.resize(roi_rgb, (224,224))
        prep_img = img_to_array(resized_image)
        prep_img = np.expand_dims(prep_img, axis=0)
        prep_img = utils.preprocess_input(prep_img, version=1)
        # predict the image
        prediction = rcg.real_time_check(prep_img)
        name = prediction["predicted_face"]
        prob = prediction["probability"]*100

        # Display the label
        cv2.putText(frame, f'({name}) {prob:.2f}%', (x,y-8), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, 
                    label_color, stroke, cv2.LINE_AA)

    # Show the frame
    cv2.imshow("Image", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break      

# Cleanup
stream.release()
cv2.destroyAllWindows()
