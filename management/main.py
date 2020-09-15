#from subprocess import *
import subprocess
import redis
import json
import sys
import time
import os
import signal


r = redis.Redis(host="10.60.110.163", port=6379)

# print(r.smembers('cameras'))
# cameras = r.smembers('cameras')
# for camera in cameras:
#     print(r.hgetall(camera))
#
# print(r.hgetall(49509))
# print(r.hget(49509, 'camera_config'))
# print(r.smembers('channels_49509'))
# print(r.hgetall('110000000006xyz96619'))
# print(r.hget('110000000006xyz96619', 'channel_config'))
# check = json.loads(r.hget('110000000006xyz96619', 'channel_config'))
# print(check['ffmpeg_opt']['src'])
# print(json.loads(r.hgetall('110000000006xyz96619')))



p = r.pubsub()
p.subscribe('cameras')
while True:
    camera_id = p.get_message()
    if camera_id and not camera_id['data'] == 1:
        camera_id = camera_id['data'].decode('utf-8')
        if camera_id == 'run_script':
            print('script running in the targeted machine')
        else :
            channels_camera_id = r.hget(camera_id, 'channels_camera_id')
            channels_camera = r.smembers(channels_camera_id)
            pick_channel = ''
            for channel in channels_camera:
                pick_channel = channel
                continue
            channel_config = json.loads(r.hget(pick_channel, 'channel_config'))
            motion_config = ''
            motion_config = r.hget(camera_id, 'motion_config')
            src = channel_config['ffmpeg_opt']['src']
            cmd = 'python ../webstreaming.py ' + str(src) + ' ' + str(motion_config)
            print("cmd---->", cmd)
            # cmd = 'python ./my_file.py ' + str(camera_id) + ' ' + str(src)
            #process = subprocess.Popen(cmd)
            #print("pid--->",process.pid)
            #print("signal--->",signal.SIGINT)
            print(subprocess.Popen(cmd, shell=True))
            #time.sleep(20)
            #os.kill(process.pid, signal.SIGINT)
            #print("delete")


