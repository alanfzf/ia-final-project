from picamera2 import Picamera2
import requests
import time
import io

picam2 = Picamera2()
capture_config = picam2.create_still_configuration()
picam2.configure(capture_config)
picam2.start()

time.sleep(1)
data = io.BytesIO()
picam2.capture_file(data, format='png')
picam2.close()
data.seek(0)

url = 'http://192.168.0.100:5000/predict'
resp = requests.post(url, files={'face': data})
data = resp.json()
print(data)
