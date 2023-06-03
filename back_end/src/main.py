from flask import Flask, request, Response, json
from recog import FaceRecognizer

app = Flask(__name__)
model = FaceRecognizer()

@app.route("/")
def index():
    return "UMG SISTEMAS"

@app.route("/predict", methods = ['POST'])
def predict_image():
    files = request.files
    if len(files) != 1 or 'face' not in files:
        return Response(
            "Invalid request, you must upload the image with a key called 'face'",
            status=400)

    image_stream = request.files['face'].stream
    image_array = bytearray(image_stream.read())
    result = model.predict_face(image_array)

    return Response(json.dumps(result), status=200, mimetype='application/json')

app.run(host="0.0.0.0")
