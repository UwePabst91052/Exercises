import socket
import time

HOST = "127.0.0.1"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print("Connected by", addr)
        try:
            while True:
                data = conn.recv(1024)
                if data:
                    print("Received", repr(data))
                    if data == b'exit':
                        break
                else:
                    time.sleep(0.5)
        except KeyboardInterrupt:
            pass

