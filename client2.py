import zmq
import threading
import time
from zmq.utils.monitor import recv_monitor_message

#Checking zmq version
print("libzmq-" + zmq.zmq_version())
if zmq.zmq_version_info() < (4, 0):
    raise RuntimeError("version not supported")

#Init Global Variables
socket = None
monitor = None
event = None

def event_monitor():
    global monitor
    global socket
    global event
    evt = {'event': 0}
    print(3)
    monitor = socket.get_monitor_socket()
    try:
        evt = recv_monitor_message(monitor, flags=zmq.NOBLOCK)
        event = evt['event']
    except Exception as e:
        print('Error:' + str(type(e)) + str(e))
    print(6)
    print("Event: {}".format(evt['event']))
    print(7)
    if evt['event'] == 512:
        print('Client Disconected...\n')
        for k in range(10):
            socket.close()
            print('Trying to Reconnect:...{}\n'.format(str(k)))
            connect()
            evt = recv_monitor_message(monitor)
            event = evt['event']
            time.sleep(2)
            if evt['event'] == 1 :
                print('Reconnected...\n')
                event = 1
                break
        if evt['event'] != 1 :
            print('Could NOT reconnect sucessfuly...\nExiting...')
            exit()
    time.sleep(1)


def connect():
    global socket
    try:
        ctx = zmq.Context.instance() 
        socket = ctx.socket(zmq.REQ)
        socket.connect('tcp://127.0.0.1:3000') 
    except Exception as e :
        print('Error:' + str(type(e)) + str(e))

def main():
    global event
    global socket
    message = None
    while True:
        print(1)
        event_monitor()
        print(2)
        if event == 1:
            print('Sending request ...')
            try:
                socket.send_string('Hello', flags=zmq.NOBLOCK, copy=False, track=False)
                message = socket.recv(flags=zmq.NOBLOCK)
            except Exception as e :
                if message:
                    print('Error:' + str(type(e)) + str(e))
            #Get the answer
            print('Received from server : ' + str(message))
        time.sleep(1)

if __name__ == "__main__":
    #Start Conection
    connect()
    print('Trying connect to server...\n')
    main()