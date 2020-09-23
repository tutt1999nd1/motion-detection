import os
import sys
import time

#import coils
import cv2
import numpy as np
import redis
from datetime import datetime
import imutils
import socketio
import sys
import base64
import ast
import json
import decimal

from util.motion_detection import SingleMotionDetector
from util.images import WriteImage


src = None
motion_config = None
channel = None
pts2 = None
camera_id = '42754'
client = redis.Redis(host='127.0.0.1', port=6379)
if len(sys.argv) == 4:
    progam, src, channel, motion_config = sys.argv

else:
    print('You must to give a camera_id, src, motion_config and channel')

if src:
    rtsp = src
else:
    rtsp = 'rtsp://ubndxinman.ddns.net:560/av0_0'

if channel:
    channel_id = channel
else:
    channel_id = 'hi'

sio = socketio.Client()
sio.connect('http://localhost:9090', namespaces=['/motion'])
width = None
height = None
#width = None if len(sys.argv) <= 1 else int(sys.argv[1])
#height = None if len(sys.argv) <= 2 else int(sys.argv[2])

print("==============================================")
if motion_config and json.loads(motion_config[1:].replace('\\','').replace('"x"',"'x'").replace('"y"',"'y'")) != '[]':
    motion_config = json.loads(motion_config[1:].replace('\\','').replace('"x"',"'x'").replace('"y"',"'y'"))
    print("=========================================================================")
    print("motion_config==========>", motion_config['region_value'])
    print("====================================xxxxxxxxxxxxxx=====================================")
else:
    region = "[[{'x':10,'y':10}, {'x':100, 'y':10}, {'x':100, 'y':100}, {'x':10, 'y':100}]]"
    region_value = ast.literal_eval(region)
pts = []
for i in range(len(region_value)):
    pts.append([])
    for point in region_value[i]:
        pts[i].append((point['x'], point['y']))
# Create video capture object, retrying until successful.
max_sleep = 5.0
cur_sleep = 0.1
print("pts2------------>", pts2)
@sio.on('connect', namespace='/motion')
def on_connect():
    print('channel_id---->',channel_id)
    sio.emit('my message', channel_id, namespace='/motion')
    while True:
        cap = cv2.VideoCapture(rtsp)
        if cap.isOpened():
            break
        global  cur_sleep
        print("cur_sleep---->", cur_sleep)
        print("max_sleep----->", max_sleep)
	    # print('not opened, sleeping {}s'.format(cur_sleep))
        time.sleep(cur_sleep)
        if cur_sleep < max_sleep:
            cur_sleep *= 2
            cur_sleep = min(cur_sleep, max_sleep)
            continue
        cur_sleep = 0.1

    # Create client to the Redis store.
    #store = redis.Redis()

    # Set video dimensions, if given.
    if width: cap.set(3, width)
    if height: cap.set(4, height)

    # Monitor the framerate at 1s, 5s, 10s intervals.
    #fps = coils.RateTicker((1, 5, 10))

    md = SingleMotionDetector(pts)

    total = 0
    fail_count = 0
    frame_count = 0
    recording_event = {
        'event_uuid': '',
        'status': 0,
        'camera_id': camera_id,
        'channel_id': channel_id,
        'event_type': 'motion_detect',
        'event_detail': {},
        'event_description': '',
        'thumbnail_url': '',
        'start_time': '',
        'end_time': ''
    }
    start_time = ''
    end_time = 0

    while True:
        status, frame = cap.read()
        if frame is None:
            fail_count = fail_count + 1
            time.sleep(0.5)
            if fail_count > 2:
                cap.release()
                cap = cv2.VideoCapture(rtsp)
                fail_count = 0
            continue
        frame_count += 1
        # status = cv2.imwrite('images/' + str(1) + '.jpg', frame)
        # print(status)
        # if frame_count % 5 == 0:
        # frame = imutils.resize(frame, width=600)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
            # grab the current timestamp and draw it on the frame
            #timestamp = datetime.now()
        cv2.putText(frame, time.asctime(time.localtime(time.time())), (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

            # if the total number of frames has reached a sufficient
            # number to construct a reasonable background model, then
            # continue to process the frame
        # rect_list = []
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

                    # item = {
                    #     "point1": {
                    #         "x": r['x'],
                    #         "y": r['y']
                    #     },
                    #     "point2": {
                    #         "x": r['x'] + r['w'],
                    #         "y": r['y'] + r['h']
                    #     }
                    # }
                    # rect_list.append(item)
                    # send_data['rect_list'] = rect_list
                    # client.publish(str(send_data))
                    # producer.producer(str(send_data))
                if start_time == '':
                    start_time = datetime.now()
                    date_time = start_time.strftime("%m/%d/%Y_%H:%M:%S")
                    t = WriteImage(date_time, frame)
                    t.write_image()

                    event_uuid = channel_id + "_" + date_time
                    recording_event['event_uuid'] = event_uuid
                    recording_event['start_time'] = str(start_time)
                    recording_event['status'] = 0
                    recording_event['thumbnail_url'] = '/images/' + event_uuid
                    client.publish('recording_event_topic', json.dumps(recording_event))
                    # xml = WriteXml(file)
                    # xml.create_object(minX, minY, maxX, maxY)

                    end_time = 0
            else:
                if start_time != '':
                    if end_time < 5:
                        t = datetime.now() - start_time
                        end_time = decimal.Decimal(t.seconds)
                    else:
                        recording_event['end_time'] = str(datetime.now())
                        recording_event['status'] = 1
                        client.publish('recording_event_topic', json.dumps(recording_event))
                        recording_event['end_time'] = ''
                        end_time = 0
                        start_time = ''

            # update the background model and increment the total number
            # of frames read thus far
        md.update(gray)
        total += 1
        for item in pts:
            pts2 = np.array(item, np.int32)
                #pts2 = pts2.reshape((-1, 1, 2))
            frame = cv2.polylines(frame, [pts2], True, (0, 0, 255), 3)
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

                        # item = {
                        #     "point1": {
                        #         "x": r['x'],
                        #         "y": r['y']
                        #     },
                        #     "point2": {
                        #         "x": r['x'] + r['w'],
                        #         "y": r['y'] + r['h']
                        #     }
                        # }
                        # rect_list.append(item)
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
            for item in pts:
                pts2 = np.array(item, np.int32)
                #pts2 = pts2.reshape((-1, 1, 2))
                frame = cv2.polylines(frame, [pts2], True, (0,0,255),3)
        hello, frame = cv2.imencode('.jpg', frame)

        value = np.array(frame).tobytes()
        image = base64.b64encode(value).decode()
        # print(channel_id)
        sio.emit("hi", image, namespace='/motion')
        # sio.emit(channel_id, image, namespace='/motion')