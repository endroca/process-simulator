import socketio
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['toolbar'] = 'None'
import time

"""
    Settings
"""
sampleTime = 0.1
timer = [0]
Y = [0]
X = [0]


"""
    IO
"""
sio = socketio.Client()

@sio.on('read', namespace='/controller')
def on_message(data):
    X.append(data)

"""
    Chart definition
"""
plt.ion()
fig, ax = plt.subplots()
fig.canvas.set_window_title('Process simulator')

"""
    Index array manager
"""
def index(arr, index):
    try:
        return arr[index]
    except IndexError:
        return 0

if __name__ == '__main__':
    sio.connect('http://localhost:3000', namespaces=['/plant', '/controller'])

    while(True):
        Y.append(1.783*index(Y, -1) - 0.8187*index(Y, -2) + 0.004667*index(X, -1) + 0.004374*index(X, -2))
        if len(X) < len(Y):
            X.append(0)

        timer.append(timer[-1] + sampleTime)

        ax.clear()
        ax.plot(timer, Y, color='b', label="Signal")
        #ax.plot(timer, X, color='r', label="Input")
        ax.set_ylim(Y[-1] - 1, Y[-1] + 1)

        sio.emit('read', Y[-1], namespace='/plant')

        if len(Y) > 100:
            del Y[0]
            del X[0]
            del timer[0]  
        
        # show the plot
        ax.legend()
        ax.set_title("Process simulator")
        plt.xlabel("Time in seconds")
        plt.draw()
        plt.pause(0.01)
        
        time.sleep(sampleTime)