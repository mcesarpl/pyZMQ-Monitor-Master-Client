import zmq
import os
import time

process = str(os.getpid())
print ('PID: ' + process)

try:
    ctx = zmq.Context.instance()
    socket = ctx.socket(zmq.REP)
    socket.bind('tcp://127.0.0.1:5555')
    print('Server listening on : 127.0.0.1:5555\n...')

except Exception as e:
    print('Error:'+ str(type(e)) + str(e))
    socket.close()

while True:
    #Wait for next request from client
    message = socket.recv()
    print("Message from client : ", message)
    time.sleep(1)
    print("Sending for client:\nOK ")
    socket.send_string("OK")


