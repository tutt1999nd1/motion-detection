#py test.py "topic" "{\"channel_id\":\"Bigboss\",\"rtsp\":\"rtsp://ubndxinman.ddns.net:560/av0_0\"}"
import redis
import sys
if len(sys.argv) == 3:
    program, environment, action = sys.argv
    client = redis.Redis(host = '127.0.0.1', port = 6379)
    client.publish(environment, action)
else:
    print('You must give an environment, and an action!')