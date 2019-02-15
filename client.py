import zmq
import threading
import time
from zmq.utils.monitor import recv_monitor_message

#Checking zmq version
print("libzmq-" + zmq.zmq_version())
if zmq.zmq_version_info() < (4, 0):
    raise RuntimeError("version not supported")

def event_monitor():
    global monitor
    global socket
    global event
    count = 0
    while monitor.poll():
        evt = recv_monitor_message(monitor)
        event = evt['event']
        print("Event: {}".format(evt['event']))
        if evt['event'] == 512 or evt['event'] == 128:
            print('Trying reconnection...')
            socket.close()
            connect()
            time.sleep(2)
            if evt['event'] == 4 or evt['event'] == 128:
                count+=1
                print('Trying reconnection...{}'.format(count))
        if count>10:
            print('Reconnect was Not successful.')
            exit()
                

def connect():
    global ctx
    global socket
    global monitor
    print('Trying connect to Server:\n...')
    try:
        ctx = zmq.Context.instance() 
        socket = ctx.socket(zmq.REQ)
        socket.connect('tcp://127.0.0.1:3000') 
        monitor = socket.get_monitor_socket()
    except Exception as e :
        print('Error: ' + str(type(e)) + str(e))

def main():
    while True:
        for k in range(10):
            message = None
            if event == 1:
                print('Sending request ...')
                try:
                    socket.send_string(str(k), flags=zmq.NOBLOCK)
                except Exception as e:
                    if str(e) != 'Operation cannot be accomplished in current state':
                        print('Error:' + str(type(e)) + str(e))
                try:
                    message = str(socket.recv(flags=zmq.NOBLOCK))
                except Exception as e:
                    if type(e) != zmq.error.Again:
                        print('Error:' + str(type(e)) + str(e))
                if message != None:
                    print('Received from server : ' + message)
            time.sleep(1)

if __name__ == "__main__":
    #Init Global Variables
    ctx = None
    socket = None
    monitor = None
    event = None
    #Start Conection
    connect()
    t = threading.Thread(target=event_monitor, args=())
    t.start()
    main()