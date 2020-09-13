#from subprocess import *
import subprocess
import redis
import json
import sys
import time
import os
import signal


program, environment = sys.argv

r = redis.Redis()
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
check = json.loads(r.get(484272))
#print(check["address"]["street"]["line1"])
print(check["cars"])
cars = check["cars"]
for x in cars:
    print(x["model"])
#hello world
p = r.pubsub()
p.subscribe(environment)   
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


