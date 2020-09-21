from aiohttp import web
import socketio

# https://python-socketio.readthedocs.io/en/latest/server.html
sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


@sio.on('connect', namespace='/motion')
def connect(sid, environ):
    print("connect ", sid)


@sio.on('my message', namespace='/motion')
async def message(sid, data):
    # await sio.emit('reply', room=sid)
    await sio.emit('reply', data, namespace='/motion')
    @sio.on(data, namespace='/motion')
    async def message(sid, message):
        await sio.emit(data, message, namespace='/motion')
    session = await sio.get_session(sid)


@sio.on('disconnect', namespace='/motion')
def disconnect(sid):
    print('disconnect ', sid)


@sio.event
async def connect(sid, environ):
    # username = authenticate_user(environ)
    username = 'ok'
    await sio.save_session(sid, {'username': username})


if __name__ == '__main__':
    # web.run_app(app)
    web.run_app(app, host='0.0.0.0', port=9090)