import socketio

sio = socketio.Client()

"""
    IO
"""
state = ''
y = [0, 0]
x = [0, 0]


def stateController(value):
    global x, state
    if state != value:
        x = [0, 0]
        state = value



@sio.on('read', namespace='/error')
def on_message(data):
    process(data)


def process(data):
    if data['type'] == 'ma':
        action = data['action']
        stateController('ma')
    else:
        stateController('')
        x.append(data['action'])
        y.append(y[-2] + 11.1 * x[-1] - 19.8 * x[-2] + 9.1 * x[-3])

        action = y[-1]

        del x[0]
        del y[0]

    sio.emit('read', action, namespace='/controller')


if __name__ == '__main__':
    sio.connect('http://localhost:3000', namespaces=['/error', '/controller'])
    sio.wait()