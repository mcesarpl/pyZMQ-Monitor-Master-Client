import zmq
import time
from zmq.utils.monitor import recv_monitor_message

#Checking zmq version
print("libzmq-" + zmq.zmq_version())
if zmq.zmq_version_info() < (4, 0):
    raise RuntimeError("version not supported")

EVENT_MAP = {}
print("Event names:")
for name in dir(zmq):
    if name.startswith('EVENT_'):
        value = getattr(zmq, name)
        print("%21s : %4i" % (name, value))
        EVENT_MAP[value] = name

def try_reconnection(socket):
    for k in range(0, 2):
        print('Reconnection trying: {}\n...'.format(str(k)))
        socket.connect('tcp://127.0.0.1:5555')
        evt = recv_monitor_message(monitor)
        evt.update({'description': EVENT_MAP[evt['event']]})
        if evt['event'] == zmq.EVENT_CONNECTED:
            break
        time.sleep(2)
        
    if  (evt['event'] == zmq.EVENT_DISCONNECTED or evt['event'] == zmq.EVENT_CONNECT_DELAYED)
        print('Reconnect was unsuccessful.')
        exit()

def event_monitor(monitor, socket):
    evt = recv_monitor_message(monitor)
    evt.update({'description': EVENT_MAP[evt['event']]})
    print("Event: {}".format(evt))
    if evt['event'] == zmq.EVENT_DISCONNECTED:
        try_reconnection(socket)

try:
    ctx = zmq.Context.instance()
    socket = ctx.socket(zmq.REQ)
    socket.connect('tcp://127.0.0.1:5555')
    monitor = socket.get_monitor_socket()

except Exception as e :
    print('Error:' + str(type(e)) + str(e))
    socket.close()

#Doing requests to server
while True:
   # print('Sending request ...')
   # socket.send_string('Hello')
    #Get the answer
   # message = str(socket.recv())
   # print('Received from server : ' + message)
    event_monitor(monitor, socket)
    time.sleep(5)

