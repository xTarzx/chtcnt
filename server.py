import socket, _thread

class Server(object):
    def __init__(self, ip, port):
        self.connections = []
        self.run(ip, port)

    def on_connect(self, c):
        with c:
            while True:
                data = c.recv(1024)
                if data:
                    self.on_message(data)

    def on_message(self, data):
        for connection in self.connections:
            connection.sendall(data)

    def run(self, ip, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((ip, port))
            print("Listening for conections...")
            s.listen()
            while True:
                try:
                    conn, addr = s.accept()
                    self.connections.append(conn)
                    _thread.start_new_thread(self.on_connect, (conn,))
                except KeyboardInterrupt:
                    break




HOST = "0.0.0.0"
PORT = 4040

Server(HOST, PORT)