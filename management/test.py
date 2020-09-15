#py test.py "topic" "{\"channel_id\":\"Bigboss\",\"rtsp\":\"rtsp://ubndxinman.ddns.net:560/av0_0\"}"
import redis


client = redis.Redis(host="10.60.110.163", port=6379)
cameras = 'cameras'
client.publish(cameras, '49509')
client.sadd(cameras, '21')

client.publish('49507', str({b'motion_config': b'{"host":"65.18.118.199"}', b'camera_enable': b'true', b'camera_manufacture': b'camera_manufacture', b'channels_camera_id': b'channels_49505', b'camera_config': b'{"host":"65.18.118.199","port":80,"user":"admin","pass":"admin12345"}', b'camera_model': b'camera_model'}))