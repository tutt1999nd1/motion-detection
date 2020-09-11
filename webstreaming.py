import os
import sys
import time

import coils
import cv2
import numpy as np
import redis
from datetime import datetime
import imutils
from util.motion_detection import SingleMotionDetector
import socketio
import sys
import base64


channel_id = 'id1234'
rtsp = 'rtsp://ubndxinman.ddns.net:560/av0_0'

sio = socketio.Client()
sio.connect('http://localhost:9090', namespaces=['/motion'])

width = None if len(sys.argv) <= 1 else int(sys.argv[1])
height = None if len(sys.argv) <= 2 else int(sys.argv[2])
region = [
    [(300, 300), (500, 450), (1000, 399), (222, 300)],
    [(700, 300), (340, 450), (100, 399), (222, 300)]
]
pts = [(300, 300), (500, 450), (1000, 399), (222, 300)]

# Create video capture object, retrying until successful.
max_sleep = 5.0
cur_sleep = 0.1

# @sio.on('connect', namespace='/motion')
# def on_connect():
#     sio.emit('my message', channel_id, namespace='/motion')


@sio.on('connect', namespace='/motion')
def on_connect():
    sio.emit('my message', channel_id, namespace='/motion')
    while True:
        cap = cv2.VideoCapture(rtsp)
        if cap.isOpened():
            break
        print('not opened, sleeping {}s'.format(cur_sleep))
        time.sleep(cur_sleep)
        if cur_sleep < max_sleep:
            cur_sleep *= 2
            cur_sleep = min(cur_sleep, max_sleep)
            continue
        cur_sleep = 0.1

    # Create client to the Redis store.
    store = redis.Redis()

    # Set video dimensions, if given.
    if width: cap.set(3, width)
    if height: cap.set(4, height)

    # Monitor the framerate at 1s, 5s, 10s intervals.
    fps = coils.RateTicker((1, 5, 10))

    md = SingleMotionDetector(region)
    total = 0
    while True:
        hello, frame = cap.read()
        if frame is None:
            time.sleep(0.5)
            continue
        frame = imutils.resize(frame, width=600)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        # grab the current timestamp and draw it on the frame
        timestamp = datetime.now()
        cv2.putText(frame, timestamp.strftime(
            "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        # if the total number of frames has reached a sufficient
        # number to construct a reasonable background model, then
        # continue to process the frame
        rect_list = []

        if total > 0:
            # detect motion in the image
            motion = md.detect(gray)
            # cehck to see if motion was found in the frame
            if motion is not None:
                # unpack the tuple and draw the box surrounding the
                # "motion area" on the output frame
                (thresh, rect) = motion
                for r in rect:
                    cv2.rectangle(frame, (r['x'], r['y']), (r['x'] + r['w'], r['y'] + r['h']),
                                  (0, 0, 255), 2)

                    item = {
                        "point1": {
                            "x": r['x'],
                            "y": r['y']
                        },
                        "point2": {
                            "x": r['x'] + r['w'],
                            "y": r['y'] + r['h']
                        }
                    }
                    rect_list.append(item)
                # send_data['rect_list'] = rect_list
                # # client.publish(str(send_data))
                # # producer.producer(str(send_data))
                # if start_time == '':
                #     start_time = datetime.now()
                #
                #     file = file + 1
                #
                #     xml = WriteXml(file)
                #     # xml.create_object(minX, minY, maxX, maxY)
                #
                #     t = WriteImage(file, frame)
                #     t.write_image()

            # if start_time != '':
            #     if motion is None:
            #         if end_time < 5:
            #             t = datetime.now() - start_time
            #             end_time = decimal.Decimal(t.seconds)
            #         else:
            #             # client.publish('End time:' + str(datetime.now()))
            #             end_time = 0
            #             start_time = ''
            #     else:
            #         end_time = 0

        # update the background model and increment the total number
        # of frames read thus far
        md.update(gray)
        total += 1

        hello, frame = cv2.imencode('.jpg', frame)
        value = np.array(frame).tobytes()
        image = base64.b64encode(value)
        sio.emit(channel_id, image, namespace='/motion')