import socket, _thread
from stuff import pack_message, unpack_message, IDCODES

class Client(object):
    def __init__(self, parent):
        self.UI_parent = parent
        self.username = ""

    def handler(self):
        while True:
            try:
                data = self.s.recv(4096)
                if data:
                    message = unpack_message(data)
                    if message.ID == IDCODES.CHAT_MESSAGE:
                        self.UI_parent.DisplayMessage(message)
                    elif message.ID == IDCODES.CONNECTED_LIST:
                        self.UI_parent.UpdateConnected(message)
            except OSError as err:
                print(err)
                break
        self.cleanup()

    def connect(self, ip, port, username):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((ip, port))
            self.username = username
            self.send_message("", IDCODES.SET_USERNAME)
        except Exception as err:
            print(err)
            return False
        else:
            print(f"Connected to {ip}:{port}")
            _thread.start_new_thread(self.handler, ())
            return True

    def send_message(self, message, ID=IDCODES.CHAT_MESSAGE):
        self.s.sendall(pack_message(ID, message, self.username))

    def cleanup(self):
        self.s.close()