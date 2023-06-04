import requests
import io
from picamera2 import Picamera2
from requests import RequestException

URL = 'http://192.168.0.100:8000/insert/'

class RaspCam:

    def __init__(self):
        self.cam = Picamera2()
        self.conf = self.cam.create_still_configuration()
        # start the camera
        self.cam.configure(self.conf)
        self.cam.start()

    def send_info(self, card):
        json_resp = None
        # generate the bytes
        img_bytes = io.BytesIO()
        self.cam.capture_file(img_bytes, format='png')
        # self.cam.close()
        img_bytes.seek(0)

        # send the bytes along with the card
        try:
            resp = requests.post(URL, files={'face': img_bytes}, data={'tag': card})
            json_resp = resp.json()
        except RequestException as e:
            return e

        return json_resp
