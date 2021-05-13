import socket, _thread


class Client(object):
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def get_messages(self, s):
        while True:
            data = s.recv(1024)
            if data:
                print(data)

    def connect(self, ip, port):
        self.s.connect((ip, port))
        print(f"Connected to {ip}:{port}")
        # _thread.start_new_thread(self.get_messages, (s,))
        # while True:
        #     data = input(">> ").encode()
        #     s.sendall(data)
    
    # def send_message(self, message):
    #     _thread
    
    def cleanup(self):
        # self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()