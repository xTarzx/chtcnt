import socket, _thread
from stuff import pack_message, unpack_message, IDCODES

class Server(object):
    def __init__(self, parent):
        self.connections = {}
        self.UI_parent = parent

    def on_connect(self, conn, addr):
        self.connections[conn] = None
        _thread.start_new_thread(self.handler, (conn, addr))

    def on_message(self, data):
        for connection in self.connections:
            connection.sendall(data)

    def on_disconnect(self, c, addr):
        self.UI_parent.DisplayLog(f"{self.connections[c]} ({addr[0]}) disconnected from the server")
        del self.connections[c]

    def relay_user_list(self):
        users = [self.connections[conn] for conn in self.connections if self.connections[conn]]
        self.on_message(pack_message(IDCODES.CONNECTED_LIST, users))


    def handler(self, c, addr):
        with c:
            while True:
                try:
                    data = c.recv(4096)
                    if data:
                        message = unpack_message(data)
                        if not self.connections[c] and message.ID == IDCODES.SET_USERNAME:
                            self.connections[c] = message.username
                            self.UI_parent.DisplayLog(f"{self.connections[c]} has connected to server from {addr[0]}")
                            self.relay_user_list()
                        if message.ID == IDCODES.CHAT_MESSAGE:
                            self.on_message(data)
                except (ConnectionResetError, ConnectionAbortedError) as err:
                    self.on_disconnect(c, addr)
                    break
        self.relay_user_list()
        
    def run(self, ip, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((ip, port))
        self.UI_parent.DisplayLog(f"Listening for conections on port {self.s.getsockname()[1]}")
        self.s.listen()
        while True:
            try:
                conn, addr = self.s.accept()
                self.on_connect(conn, addr)
            except OSError:
                break

    def start_server(self, port, ip="0.0.0.0"):
        _thread.start_new_thread(self.run, (ip, port))

    def stop_server(self):
        for conn in self.connections:
            conn.close()
            print(conn, "Closed")
        self.connections.clear()
        self.s.close()