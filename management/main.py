# from subprocess import *
import subprocess
import redis
import json
import sys
import time
import os
import signal

r = redis.Redis(host="10.60.110.163", port=6379)
key = 'motion_manage_process'
# print(r.smembers('cameras'))
# cameras = r.smembers('cameras')
# for camera in cameras:
#     print(r.hgetall(camera))
# print("------------------------------------------------------------------------------------")
#
# print(r.hgetall(49509))
# print(r.hget(49509, 'camera_config'))
# print(r.smembers('channels_49509'))
# print(r.hgetall('110000000006xyz96619'))
# print(r.hget('110000000006xyz96619', 'channel_config'))
# check = json.loads(r.hget('110000000006xyz96619', 'channel_config'))
# print(check['ffmpeg_opt']['src'])
# print(json.loads(r.hgetall('110000000006xyz96619')))

r = redis.Redis(host = '127.0.0.1', port = 6379)
r.mset({"Croatia": "Zagreb", "Bahamas": "Nassau"})
print(r.get("Bahamas"))
print(r.hgetall("myhash"))
print(r.keys())
restaurant_484272 = {
    "name": "Ravagh",
    "type": "Persian",
    "address": {
        "street": {
            "line1": "11 E 30th St",
            "line2": "APT 1",
        },
        "city": "New York",
        "state": "NY",
        "zip": 10016,
    },
    "cars":[
        {"model": "BMW 230", "mpg": 27.5},
        {"model": "Ford Edge", "mpg": 24.1}
    ]
}
r.set(484272, json.dumps(restaurant_484272))
#print(json.loads(r.get(484272)))
check = json.loads(r.get('cameras'))
#print(check["address"]["street"]["line1"])
print(check["camera_id"])
cars = check["cars"]
for x in cars:
    print(x["model"])
#hello world
p = r.pubsub()
p.subscribe('cameras')
while True:
    message = p.get_message()
    if message and not message['data'] == 1:
        message = message['data'].decode('utf-8')
        if message == 'run_script':
            print('script running in the targeted machine')
        else :
            print(json.loads(message))
            cmd = 'python ./motion-detection/webstreaming.py ' + json.loads(message)['channel_id'] + ' ' + json.loads(message)['rtsp']
            process = subprocess.Popen(cmd)
            print("pid--->",process.pid)
            print("signal--->",signal.SIGINT)
            #print(subprocess.Popen(cmd, shell=True))
            #time.sleep(20)
            #os.kill(process.pid, signal.SIGINT)
            #print("delete")
# =======
# old_process_id = None
# def get_pname(id):
#     p = subprocess.Popen(["ps -o cmd= {}".format(id)], stdout=subprocess.PIPE, shell=True)
#     return str(p.communicate()[0].decode('utf-8'))
#
# p = r.pubsub()
# p.subscribe('camera_config_topic')
# while True:
#     camera = p.get_message()
#     if camera and not camera['data'] == 1:
#         camera = camera['data'].decode('utf-8')
#         print(camera)
#         camera = json.loads(camera)
#         if camera['action'] == 'ADD_ALL':
#             print('add all roi')
#         else:
#             camera_id = camera['camera']
#             if r.hget(key, camera_id) is not None:
#                 old_process_id = int(r.hget(key, camera_id).decode("utf-8"))
#             print("old_pid ====>", old_process_id)
#             print("name_old_process====>", get_pname(old_process_id))
#             if old_process_id is not None and get_pname(old_process_id) != '':
#                 print("delete")
#                 os.kill(old_process_id, signal.SIGINT)
#             print("camera_id----->", camera_id)
#             channels_camera_id = r.hget(camera_id, 'channels_camera_id')
#             channels_camera = r.smembers(channels_camera_id)
#             pick_channel = ''
#             for channel in channels_camera:
#                 pick_channel = channel.decode("utf-8")
#                 if r.hget(pick_channel, 'channel_status').decode("utf-8") == 'connected':
#                     break
#             print("pick_channel------>", pick_channel) # sau nay neu co cau hinh den muc do motion cho channel_id thi su dung bien nay thay cho bien src
#             # channel_config = json.loads(r.hget(pick_channel, 'channel_config'))
#             # src = channel_config['ffmpeg_opt']['src']
#             # print(src)
#             src = r.hget(pick_channel, 'rtsp_server_url').decode("utf-8")
#             print("src----->", src)
#             motion_config = ''
#             motion_config = r.hget(camera_id, 'motion_config')
#             print("motion_config---->", motion_config)
#             cmd = 'python3.6 ../webstreaming.py ' + str(src) + ' ' + str(camera_id) + ' ' + str(motion_config)
#             #cmd = 'python ok.py ' + str(src) + ' ' + str(camera_id) + ' ' + str(motion_config)
#             print("cmd---->", cmd)
#             process = subprocess.Popen(cmd, shell=True)
#             print('new pid-------------->', process.pid)
#             r.hset(key, camera_id, process.pid)
#             # time.sleep(20)
#             # os.kill(process.pid, signal.SIGINT)
#             # print("delete")
# >>>>>>> dee9b37e2098441e6a839d1f9f8a358fb961f3a3
