import socket

HOST = input("Server IP > ")
PORT = 4040

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))