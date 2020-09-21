#py test.py "topic" "{\"channel_id\":\"Bigboss\",\"rtsp\":\"rtsp://ubndxinman.ddns.net:560/av0_0\"}"
import redis


client = redis.Redis(host="10.60.110.163", port=6379)
cameras = 'camera_config_topic'

client.publish(cameras, str({b'action': b'CAMERA_ADD', b'camera': b'AA1234567'}))