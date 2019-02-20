import zmq
import time
from zmq.utils.monitor import recv_monitor_message

#Checking zmq version
print("libzmq-" + zmq.zmq_version())
if zmq.zmq_version_info() < (4, 0):
    raise RuntimeError("version not supported")

#Init Global Variables
socket = None
event = None

def event_monitor():
    global socket
    global event
    evt = {'event': 0}
    monitor = socket.get_monitor_socket()
    try:
        evt = recv_monitor_message(monitor, flags=zmq.NOBLOCK)
        event = evt['event']
    except Exception as e:
        if not isinstance(e, zmq.error.Again):
            print('Error:' + str(type(e)) + str(e))
    if evt['event'] != 0:
        print("Event: {}".format(evt['event']))
    if evt['event'] == 1024:
        print('Error: EVENT_MONITOR_STOPPED\nExiting...')
        exit()
    if evt['event'] == 512 or evt['event'] == 128:
        print('Server got offline...\n')
        for k in range(3):
            socket.close()
            print('Trying to Reconnect:...{}\n'.format(str(k)))
            connect()
            evt = recv_monitor_message(monitor)
            if evt['event'] == 1024:
                print('Error: EVENT_MONITOR_STOPPED\nExiting...')
                exit()
            time.sleep(2)
            print('Event:' + str(evt['event']))
            if evt['event'] == 1 or evt['event'] == 2:
                evt = recv_monitor_message(monitor)
                print('Event IF:' + str(evt['event']))
                if evt['event'] == 1:
                    print('Reconnected...\n')
                    event = 1
                    break
        if evt['event'] != 1 :
            print('Could NOT reconnect sucessfuly...\nExiting...')
            exit()
    time.sleep(1)


def connect():
    global socket
    socket = None
    try:
        ctx = zmq.Context.instance()
        socket = ctx.socket(zmq.DEALER)
        socket.connect('tcp://127.0.0.1:3000')
    except Exception as e :
        print('Error:' + str(type(e)) + str(e))

def main():
    global event
    global socket
    loop = False
    while True:
        count = 0
        event_monitor()
        print('Waiting a message ...')
        #Get a message
        try:
            message = str(socket.recv(flags=zmq.NOBLOCK))
        except Exception as e:
            if type(e) == zmq.error.Again:
                message = None
            else:
                print('Error:' + str(type(e)) + str(e))
        if message != None:
            loop = True
            print('Received from server : ' + message)
            #Send a answer
            while (loop and (count<3)):
                try:
                    loop = False
                    socket.send_string(message, flags=zmq.NOBLOCK, copy=True)
                except Exception as e:
                    if str(e) == 'Operation cannot be accomplished in current state':
                        loop = True
                        count+=1
                        print('looping...')
                    else:
                        loop = False
                        print('Error:' + str(type(e)) + str(e))
        time.sleep(1)

if __name__ == "__main__":
    #Start Conection
    connect()
    print('Trying connect to server...\n')
    main()