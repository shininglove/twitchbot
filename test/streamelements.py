import socketio
#from config import JWT_TOKEN as accessToken

sio = socketio.Client()


@sio.event
def message(data):
    print("I recieved a message!")


@sio.event
def connect():
    # sio.emit('authenticate', {'method': 'oauth2', 'token': accessToken});
    # sio.emit('authenticate', {'method': 'jwt', 'token': accessToken});
    print("I'm connected!")


@sio.on("event")
def on_message(data):
    print("There is data", data)


@sio.event
def connect_error(data):
    print("The connection failed", data)


@sio.event
def disconnect():
    print("I'm disconnected")


sio.connect("https://realtime.streamelements.com", transports="websocket")

print("my sid is ", sio.sid)
