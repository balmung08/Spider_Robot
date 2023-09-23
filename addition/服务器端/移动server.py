import socket
import time
import threading

status = "doing"
send_code = 0
mode = 0
#1177
def socket_portA():
    global status,send_code,mode
    HOST = '---------'  # 服务器的私网IP
    PORT = 1177
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(1)
    num = 0

    while True:
        connection, address = sock.accept()
        connection.settimeout(5)  # 5s
        try:
            code = None
            code = connection.recv(2)
            if code == b'up':
                send_code = str(connection.recv(2).decode())
            if code == b'mp':
                mode = str(connection.recv(2).decode())
            if code == b'do':
                connection.send(send_code.encode())
            if code == b'mo':
                connection.send(mode.encode())
        except Exception as e:
            connection.send("error".encode())

def socket_portB():
    global status,send_code,mode
    HOST = '----------'  # 服务器的私网IP
    PORT = 1178
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(1)
    num = 0

    while True:
        connection, address = sock.accept()
        connection.settimeout(5)  # 5s
        try:
            code = None
            code = connection.recv(2)
            if code == b'up':
                send_code = str(connection.recv(2).decode())
            if code == b'mp':
                mode = str(connection.recv(2).decode())
            if code == b'do':
                connection.send(send_code.encode())
            if code == b'mo':
                connection.send(mode.encode())
        except Exception as e:
            connection.send("error".encode())

class myThread (threading.Thread):
    def __init__(self, threadID, name,function):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.function = function
        #self.lock = threading.RLock()
    def run(self):
        #self.lock.acquire()
        self.function()
        #self.lock.acquire()


threads = []

# 创建新线程
thread1 = myThread(1, "Thread-1", socket_portA)
thread2 = myThread(2, "Thread-2", socket_portB)
# 开启新线程
thread1.start()
thread2.start()

threads.append(thread1)
threads.append(thread2)




