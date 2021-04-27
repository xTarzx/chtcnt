import socket, _thread


class Client(object):
    def __init__(self, ip, port):
        self.connect(ip, port)
    
    def get_messages(self, s):
        while True:
            data = s.recv(1024)
            if data:
                print(data)


    def connect(self, ip, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            print(f"Connected to {ip}:{port}")
            _thread.start_new_thread(self.get_messages, (s,))
            while True:
                data = input(">> ").encode()
                s.sendall(data)

HOST = input("Server IP > ")
PORT = 4040

Client(HOST, PORT)
