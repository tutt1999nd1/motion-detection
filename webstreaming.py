# USAGE
# python webstreaming.py --ip 0.0.0.0 --port 8000

# import the necessary packages
from util.motion_detection import SingleMotionDetector
# from util.redis import RedisPublish
# from util.kafka import KafkaProduce
from util.images import WriteImage
from util.xml import WriteXml

from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import imutils
import time
import cv2
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import decimal

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful for multiple browsers/tabs
# are viewing tthe stream)

env = 'camera'
topic = 'numtest'
outputFrame = None
lock = threading.Lock()

# client = RedisPublish(env)

# initialize a flask object
app = Flask(__name__)
udp = 'udp://177.0.0.1:5005'

send_data = {
    "link_udp": udp,
    "rect_list": [],
    "time": ''
}

# producer = KafkaProduce(topic)

# initialize the video stream and allow the camera sensor to
# warmup
# vs = cv2.VideoCapture("./videos/example_01.mp4")
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--ip", type=str, required=True,
#                     help="ip address of the device")
# ap.add_argument("-o", "--port", type=int, required=True,
#                     help="ephemeral port number of the server (1024 to 65535)")
# ap.add_argument("-f", "--frame_count", type=int, default=32,
#                     help="# of frames used to construct the background model")
# args = vars(ap.parse_args())



# vs = VideoStream(src=udp).start()
time.sleep(2.0)

start_time = ''
end_time = 0


def find_camera(id):
    cameras = ['rtsp://ubndxinman.ddns.net:560/av0_0',
               'rtsp://ytexinman.ddns.net:554/av0_0',
               'rtsp://root:VTxnk123@27.72.21.11:510/axis-media/media.amp']
    return cameras[int(id)]


def detect_motion(camera_id):
    # grab global references to the video stream, output frame, and
    # lock variables
    global outputFrame, lock, start_time, end_time
    cam = find_camera(camera_id)
    vs = cv2.VideoCapture(cam)

    # initialize the motion detector and the total number of frames
    # read thus far
    md = SingleMotionDetector(accumWeight=0.1)
    total = 0
    file = 0

    # loop over frames from the video stream
    while True:
        # read the next frame from the video stream, resize it,
        # convert the frame to grayscale, and blur it
        ret, frame = vs.read()
        if frame is None:
            break
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
                    cv2.rectangle(frame, (r['x'], r['y']), (r['x']+r['w'], r['y']+r['h']),
                                  (0, 0, 255), 2)

                    item = {
                        "point1": {
                            "x": r['x'],
                            "y": r['y']
                        },
                        "point2": {
                            "x": r['x']+r['w'],
                            "y": r['y']+r['h']
                        }
                    }
                    rect_list.append(item)
                send_data['rect_list'] = rect_list
                # client.publish(str(send_data))
                # producer.producer(str(send_data))
                if start_time == '':
                    start_time = datetime.now()

                    file = file + 1

                    xml = WriteXml(file)
                    # xml.create_object(minX, minY, maxX, maxY)

                    t = WriteImage(file, frame)
                    t.write_image()

            if start_time != '':
                if motion is None:
                    if end_time < 5:
                        t = datetime.now() - start_time
                        end_time = decimal.Decimal(t.seconds)
                    else:
                        # client.publish('End time:' + str(datetime.now()))
                        end_time = 0
                        start_time = ''
                else:
                    end_time = 0

        # update the background model and increment the total number
        # of frames read thus far
        md.update(gray)
        total += 1

        # acquire the lock, set the output frame, and release the
        # lock
        # with lock:
        #     outputFrame = frame.copy()
        success, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")


@app.route("/video_feed/<string:id>", methods=["GET"])
def video_feed(id):
    # return the response generated along with the specific media
    # type (mime type)
    return Response(detect_motion(id),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


# check to see if this is the main thread of execution
if __name__ == '__main__':
    app.run()