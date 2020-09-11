import socketio
import sys
sio = socketio.Client()
channel_id = 'id1234'

sio.connect('http://localhost:9090', namespaces=['/motion'])

@sio.on('reply', namespace='/motion')
async def on_message(data):
    await print("Get DATA: ", data)


@sio.on('id1234', namespace='/motion')
def on_message(message):
        print("image:", message)