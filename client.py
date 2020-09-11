import socketio
import sys
sio = socketio.Client()
channel_id = 'id1234'

sio.connect('http://localhost:9090', namespaces=['/motion/' + channel_id])

@sio.on('reply', namespace='/motion/' + channel_id)
def on_message(data):
    print("Get DATA: ", data)
