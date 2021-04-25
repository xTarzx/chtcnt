import socket

HOST = "0.0.0.0"
PORT = 4040

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    print("Connected", addr)
    