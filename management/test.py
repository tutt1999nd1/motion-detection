#py test.py "topic" "{\"channel_id\":\"Bigboss\",\"rtsp\":\"rtsp://ubndxinman.ddns.net:560/av0_0\"}"
import redis
import sys
import json
client = redis.Redis(host = '127.0.0.1', port = 6379)
camera_id = {
    'channels_camera_id':1,
    'camera_config':2
}
camera_id_dumps = json.dumps(camera_id)
client.publish('cameras', '[1,2,3,4]')
client.publish('1', camera_id_dumps)
client.publish('chanels_1', '[1,2,3,4]')
client.publish('1', '{rtsp_server_url: rtsp://ubndxinman.ddns.net:560/av0_0}')