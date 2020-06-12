import socket
import selectors
import types

HOST = "127.0.0.1"
PORT = 65432

sel = selectors.DefaultSelector()


def start_connection(host, port):
    global send_data
    server_addr = (host, port)
    print("starting connection to", server_addr)
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.setblocking(False)
    lsock.connect_ex(server_addr)
    levents = selectors.EVENT_WRITE
    send_data = types.SimpleNamespace(
        msg_total=0,
        recv_total=0,
        message=None,
        outb=b"",
    )
    sel.register(lsock, levents, data=send_data)
    return lsock


def prepare_send_data(sock, message):
    global send_data
    sel.unregister(sock)
    send_data = types.SimpleNamespace(
        msg_total=len(message),
        message=bytes(message, encoding='utf-8'),
        outb=b"",
    )
    sel.register(sock, selectors.EVENT_WRITE, data=send_data)


def service_connection(key, mask):
    lsock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.message:
            data.outb = data.message
        if data.outb:
            print("sending", repr(data.outb))
            sent = lsock.send(data.outb)
            data.outb = data.outb[sent:]


send_data = None
gsock = start_connection(HOST, int(PORT))

run = True
while run:
    try:
        text = input("Nachricht>")
    except KeyboardInterrupt:
        text = "exit"
        run = False
    prepare_send_data(gsock, text)
    events = sel.select(timeout=1)
    if events:
        for l_key, l_mask in events:
            service_connection(l_key, l_mask)
sel.unregister(gsock)
sel.close()