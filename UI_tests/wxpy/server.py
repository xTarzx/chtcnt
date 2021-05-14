import socket, _thread
from stuff import pack_message, unpack_message, IDCODES

class Server(object):
    def __init__(self, ip, port):
        self.connections = []
        self.run(ip, port)

    def on_connect(self, conn):
        self.connections.append(conn)
        _thread.start_new_thread(self.handler, (conn,))

    def on_message(self, data):
        for connection in self.connections:
            connection.sendall(data)

    def handler(self, c):
        with c:
            while True:
                try:
                    data = c.recv(1024)
                    if data:
                        message = unpack_message(data)
                        if message.ID == IDCODES.CHAT_MESSAGE:
                            self.on_message(data)
                except ConnectionResetError as err:
                    print(err)
                    self.connections.remove(c)
                    break
    def run(self, ip, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((ip, port))
            print("Listening for conections...")
            s.listen()
            while True:
                try:
                    conn, addr = s.accept()
                    print(f"Connection from {addr}", conn)
                    self.on_connect(conn)
                    
                except KeyboardInterrupt:
                    break




HOST = "0.0.0.0"
PORT = 4040

Server(HOST, PORT)