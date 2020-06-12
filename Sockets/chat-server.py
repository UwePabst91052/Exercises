import socket
import time
import selectors
import types

HOST = "127.0.0.1"
PORT = 65432


sel = selectors.DefaultSelector()


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.inb = recv_data
            if data.inb == b'exit':
                print("closing connection to", data.addr)
                sel.unregister(sock)
                sock.close()
                return -1
            else:
                print("Received: ", data.inb)
    return 0


lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((HOST, PORT))
lsock.listen()
print(("listening on", (HOST, PORT)))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

while True:
    ret = 0
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            ret = service_connection(key, mask)
    if ret < 0:
        break

sel.close()
