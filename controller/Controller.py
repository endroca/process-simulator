import socketio

sio = socketio.Client()

"""
    IO
"""
state = ''
lastError = 0
integral = 0

Kp = 1
Ki = Kp*2
Kd = Kp*1/2
dt = 0.1


def stateController(value):
    global error, state, integral
    if state != value:
        error = [0]
        integral = 0
        state = value



@sio.on('read', namespace='/error')
def on_message(data):
    process(data)


def process(data):
    global lastError, integral, dt

    if data['type'] == 'ma':
        action = data['action']
        stateController('ma')
    else:
        stateController('')
        error = data['action']
        
        integral = integral + Ki * error * dt
        
        derivative = Kd * (error - lastError) / dt
        lastError = error

        pid = (Kp * error) + integral + derivative

        action = pid

    sio.emit('read', action, namespace='/controller')


if __name__ == '__main__':
    sio.connect('http://localhost:3000', namespaces=['/error', '/controller'])
    sio.wait()