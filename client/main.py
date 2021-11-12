import cv2
import time
import base64
import json
import numpy as np
import HandTracking as htm
import ctypes
from ordered_set import OrderedSet

import sys
sys.path.append('..')

from client.Redis import ClientRedisConnection
from client.RedisListener import ClientRedisListener

redis_connection = ClientRedisConnection()

overlayList = []

pTime = 0

detector = htm.handDetector(detectionCon=0.85)

tipIds = [4, 8, 12, 16, 20]

gestures = {
        'fist': 0,
        'hello': 0,
        'ok': 0,
        'rock': 0,
        'like': 0

}
filteredGestures = OrderedSet()
configs = redis_connection.read_configs()

def image_handler(image):
    global configs
    raw_image = base64.b64decode(image['data'])
    image = np.frombuffer(raw_image, dtype=np.uint8)
    frame = np.array(cv2.imdecode(image, 1))
    img = detector.findHands(frame)
    runtime_configs = redis_connection.read_configs()
    if runtime_configs != None and runtime_configs != configs:
        configs = runtime_configs

    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingers = []

        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = fingers.count(1)
        if(totalFingers == 0):
            gestures['fist'] += 1
            if gestures['fist'] >= 50:
                filteredGestures.add('fist')
        if(totalFingers == 5):
            gestures['hello'] += 1
            if gestures['hello'] >= 50:
                filteredGestures.add('hello')
        if (fingers == [1, 0, 1, 1, 1]):
            gestures['ok'] += 1
            if gestures['ok'] >= 50:
                filteredGestures.add('ok')
        if (fingers == [1, 1, 0, 0, 1] or fingers == [0, 1, 0, 0, 1]):
            gestures['rock'] += 1
            if gestures['rock'] >= 50:
                filteredGestures.add('rock')
        if(fingers == [0, 0, 0, 1, 1] or fingers == [0, 0, 1, 1, 1]):
            gestures['like'] += 1
            if gestures['like'] >= 50:
                filteredGestures.add('like')

    # filteredGestures = list(filter(lambda gesture: gestures[gesture] > 50, gestures))
    #ctrl.send_data(str({"gestures": filteredGestures}))
    if filteredGestures == {'like', 'fist', 'hello'}:
        data = {"type": "camera_events", "event": "Лампочка гори!", "gestures": filteredGestures}
        # client.send_data(json.dumps(data))
        # exit()

    # cTime = time.time()
    # fps = 1 / (cTime - pTime)
    # pTime = cTime
    print(len(img))
    cv2.imshow("Image", img)
    cv2.waitKey(1)

redis_listener = ClientRedisListener(redis_connection, image_handler)