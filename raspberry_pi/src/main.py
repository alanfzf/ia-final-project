import json
import io
import time
from flask import Flask, send_file
from picamera2 import Picamera2



app = Flask(__name__)
app.use_x_send_file = True

@app.route('/')
def index():
    return json.dumps({
        'name': 'alice',
        'email': 'alice@outlook.com'
    })

@app.route('/take_picture')
def take_picture():

    picam2 = Picamera2()
    capture_config = picam2.create_still_configuration()
    picam2.configure(capture_config)
    picam2.start()

    time.sleep(1)
    data = io.BytesIO()
    picam2.capture_file(data, format='jpeg')
    picam2.close()
    data.seek(0)

    return send_file(data, download_name='face.jpeg')

app.run(host="0.0.0.0")
