import zmq
import os
import time

process = str(os.getpid())
print ('PID: ' + process)

try:
    ctx = zmq.Context.instance()
    #socket = ctx.socket(zmq.REP)
    socket = ctx.socket(zmq.DEALER)
    socket.bind('tcp://127.0.0.1:4000')
    print('Server listening on : 127.0.0.1:4000\n...')

except Exception as e:
    print('Error:'+ str(type(e)) + str(e))
    socket.close()

while True:

    for k in range(1,10):
        #Waiting for request
        message = socket.recv()
        print("Request from client: ", message)
        time.sleep(1)
        #Sending answer
        print("Sending to client:\n")
        socket.send_string("{}".format(str(k)))
