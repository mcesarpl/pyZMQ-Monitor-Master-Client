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
    event = evt['event']
    print("Event: {}".format(evt['event']))
    if evt['event'] == 512:
        print('Client Disconected...\nTrying to Reconnect:\n')
        for k in range(3):
            socket.close()
            connect()
            time.sleep(2)
            if evt['event'] == 1 :
                print('Reconnected...\n')
                event = 1
                break
        if evt['event'] != 1 :
            print('Could NOT reconnect sucessfuly...\nExiting...')
            exit()


def connect():
    global ctx
    global socket
    global monitor
    global evt
    print('Trying connect to Server:\n...')
    try:
        ctx = zmq.Context.instance() 
        socket = ctx.socket(zmq.REQ)
        socket.connect('tcp://127.0.0.1:5555') 
        monitor = socket.get_monitor_socket()
        evt = recv_monitor_message(monitor)
    except Exception as e :
        print('Error:' + str(type(e)) + str(e))

def main():

    while True:
        if event == 1:
            print('Sending request ...')
            socket.send_string('Hello')
            #Get the answer
            message = str(socket.recv())
            print('Received from server : ' + message)
        time.sleep(1)

if __name__ == "__main__":
    #Init Global Variables
    ctx = None
    socket = None
    monitor = None
    event = None
    evt = None
    #Start Conection
    connect()
    t = threading.Thread(target=event_monitor, args=())
    t.start()
    main()