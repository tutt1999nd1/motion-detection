from aiohttp import web
import socketio

#https://python-socketio.readthedocs.io/en/latest/server.html
sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


@sio.on('connect', namespace='/motion')
def connect(sid, environ):
    print("connect 1", sid)


@sio.on('my message', namespace='/motion')
async def message(sid, data):
    #await sio.emit('reply', room=sid)

    @sio.on('connect', namespace='/motion/' + data)
    def connect(sid, environ):
        print("connect 2", sid)

    @sio.on('my message', namespace='/motion/' + data)
    def message(sid, message):
        print(message)
        sio.emit('reply', message, namespace='/motion/' + data)


@sio.on('disconnect', namespace='/motion')
def disconnect(sid):
    print('disconnect ', sid)


@sio.event
async def connect(sid, environ):
    #username = authenticate_user(environ)
    username = 'ok'
    await sio.save_session(sid, {'username': username})


if __name__ == '__main__':
    #web.run_app(app)
    web.run_app(app, host='0.0.0.0', port=9090)