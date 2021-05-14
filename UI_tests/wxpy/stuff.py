import pickle


class IDCODES:
    CHAT_MESSAGE = 0
    CONNECTED_LIST = 1
    SET_USERNAME = 3
    DISCONNECT = 9


class Message:
    def __init__(self, ID, content, username):
        self.ID = ID
        self.content = content
        self.username = username


def pack_message(ID, content, username = None):
    return pickle.dumps(Message(ID, content, username))

def unpack_message(message) -> Message:
    return pickle.loads(message)