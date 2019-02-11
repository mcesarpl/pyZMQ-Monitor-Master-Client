import zmq
import threading
import time
from zmq.utils.monitor import recv_monitor_message

#Checking zmq version
print("libzmq-" + zmq.zmq_version())
if zmq.zmq_version_info() < (4, 0):
    raise RuntimeError("version not supported")

#Init Variables
ctx = None
socket = None
monitor = None

# def try_reconnection():
#     print('Try reconnection: \n...')
#     for k in range(0, 4):
#         connect()
#         print('Reconnection trying: {}\n...'.format(str(k)))
#         monitor = socket.get_monitor_socket()
#         evt = recv_monitor_message(monitor)
#         time.sleep(5)
#         print("Event: {}".format(evt['event']))
#         if evt['event'] == 1 or evt['event'] == 2:
#             time.sleep(10)
#             if evt['event'] == 1:
#                 return
#     if (evt['event'] == 128 or evt['event'] == 2):
#         print('Reconnect was unsuccessful.')
#         exit()

def event_monitor():
    global monitor
    global socket
    count = 0
    while monitor.poll():
        evt = recv_monitor_message(monitor)
        print("Event: {}".format(evt['event']))
        if evt['event'] == 512 or evt['event'] == 128:
            print('Trying reconnection...')
            socket.close()
            connect()
        # if evt['event'] == 4:
        #     time.sleep(5)
        #     count+=1
        #     print('Trying reconnection...{}'.format(count))
        # if count>3:
        #     print('Reconnect was Not successful.')
        #     exit()
                

def connect():
    print('Trying connect to Server:\n...')
    try:
        global ctx
        global socket
        global monitor
        ctx = zmq.Context.instance() 
        socket = ctx.socket(zmq.REQ)
        socket.connect('tcp://127.0.0.1:5555') 
        monitor = socket.get_monitor_socket()
        time.sleep(10)
    except Exception as e :
        print('Error:' + str(type(e)) + str(e))
        exit()

def main():

    while True:
        print('Sending request ...')
        socket.send_string('Hello')
        #Get the answer
        message = str(socket.recv())
        print('Received from server : ' + message)
        time.sleep(1)

if __name__ == "__main__":
    connect()
    t = threading.Thread(target=event_monitor, args=())
    t.start()
    main()