import zmq
import time

try:
    ctx = zmq.Context.instance()
    socket = ctx.socket(zmq.REQ)
    socket.connect('tcp://127.0.0.1:5555')
except Exception as e :
    print('Error:' + str(type(e)) + str(e))
    socket.close()

#Doing requests to server
while True:
    print('Sending request ...')
    socket.send_string('Hello')
    #Get the answer
    message = str(socket.recv())
    print('Received from server : ' + message)
    time.sleep(2)
