import socket, _thread
from stuff import pack_message, unpack_message, IDCODES

class Client(object):
    def __init__(self, parent):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.UI_parent = parent
        self.username = ""

    def handler(self):
        while True:
            try:
                data = self.s.recv(1024)
                if data:
                    print("MESSAGE RECEIVED")
                    message = unpack_message(data)
                    if message.ID == IDCODES.CHAT_MESSAGE:
                        self.UI_parent.DisplayMessage(message)
            except OSError as err:
                print(err)
                break
        self.cleanup()

    def connect(self, ip, port, username):
        try:
            self.s.connect((ip, port))
            self.username = username
        except Exception as err:
            print(err)
        else:
            print(f"Connected to {ip}:{port}")
            _thread.start_new_thread(self.handler, ())

    def send_message_handler(self, message):
        _thread.start_new_thread(self.send_message, (message,))

    def send_message(self, message):
        self.s.sendall(pack_message(IDCODES.CHAT_MESSAGE, message, self.username))

    def cleanup(self):
        self.s.close()