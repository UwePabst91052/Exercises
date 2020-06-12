import socket

HOST = "127.0.0.1"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        try:
            message = bytes(input("Nachricht>"), encoding='utf-8')
        except KeyboardInterrupt:
            s.sendall(b'exit')
            break
        s.sendall(message)

