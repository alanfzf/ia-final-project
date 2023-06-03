from recog import FaceRecognizer

frg = FaceRecognizer()

list = ['./facetest/face0.jpg', './facetest/face1.jpg', './facetest/face2.jpg']

for img in list:
    results = frg.check_face(img)
    print(results)
