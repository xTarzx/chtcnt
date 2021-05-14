import socket, _thread
from stuff import pack_message, unpack_message, IDCODES

class Server(object):
    def __init__(self, ip, port):
        self.connections = {}
        self.run(ip, port)

    def on_connect(self, conn):
        self.connections[conn] = None
        _thread.start_new_thread(self.handler, (conn,))

    def on_message(self, data):
        for connection in self.connections:
            connection.sendall(data)

    def relay_user_list(self):
        users = [self.connections[conn] for conn in self.connections if self.connections[conn]]
        self.on_message(pack_message(IDCODES.CONNECTED_LIST, users))

    def handler(self, c):
        with c:
            while True:
                try:
                    data = c.recv(4096)
                    if data:
                        message = unpack_message(data)
                        if not self.connections[c] and message.ID == IDCODES.SET_USERNAME:
                            self.connections[c] = message.username
                            self.relay_user_list()
                        if message.ID == IDCODES.CHAT_MESSAGE:
                            self.on_message(data)
                except ConnectionResetError as err:
                    print(err)
                    del self.connections[c]
                    self.relay_user_list()
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