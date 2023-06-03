from flask import Flask
from recog import FaceRecognizer

app = Flask(__name__)
recognizer = FaceRecognizer()

@app.route("/")
def hello_world():
    return ""

@app.route("/predict")
def predict_image():
    return ""

app.run(host="0.0.0.0")
