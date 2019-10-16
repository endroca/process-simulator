import socketio
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['toolbar'] = 'None'
import time

sio = socketio.Client()

"""
    IO
"""

@sio.on('read', namespace='/controller')
def on_message(data):
    X.append(data)

"""
    Chart definition
"""
plt.ion()
fig, ax = plt.subplots()
fig.canvas.set_window_title('Processo')


"""
    Settings
"""
sampleTime = 0.1
Y = [0, 0]
X = [0, 0]
response = []
count = [0]



if __name__ == '__main__':
    sio.connect('http://localhost:3000', namespaces=['/plant', '/controller'])

    while(True):
        Y.append(1.783*Y[-1] - 0.8187*Y[-2] + 0.004667*X[-1] + 0.004374*X[-2])
        response.append(Y[-1])

        if len(response) > 1:
            count.append(count[-1] + sampleTime)

        # Queue structure
        del Y[0]
        if len(X) > 2:
            del X[0]
        else:
            X[ 1 if X[0] == 0 else 0 ] = 0

        sio.emit('read', response[-1], namespace='/plant')

        ax.clear()
        plt.plot(count, response, color='r')



        ax.set_ylim(response[-1] - 1, response[-1] + 1)

        if len(response) > 100:
            del response[0]
            del count[0]


        # show the plot
        plt.show()
        plt.pause(0.01)
        time.sleep(sampleTime)