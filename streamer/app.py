import base64
import cv2
import zmq

import sys
sys.path.append('..')

from streamer.Redis import ImageSender

camera = cv2.VideoCapture(0)
sender = ImageSender()

while True:
    try:
        ret, frame = camera.read()
        frame = cv2.resize(frame, (640, 480))
        encoded, buf = cv2.imencode('.jpg', frame)
        image = base64.b64encode(buf)
        sender.send_image(image)
    except KeyboardInterrupt:
        camera.release()
        cv2.destroyAllWindows()
        break