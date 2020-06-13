import socket
import selectors
import types

HOST = "127.0.0.1"
PORT = 65432

sel = selectors.DefaultSelector()


def start_connection(host, port):
    server_addr = (host, port)
    print("starting connection to", server_addr)
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.setblocking(False)
    lsock.connect_ex(server_addr)
    levents = selectors.EVENT_WRITE
    data = types.SimpleNamespace(
        msg_total=0,
        message=None,
        outb=b"",
    )
    sel.register(lsock, levents, data=data)
    return lsock


def service_connection(key, mask, message):
    lsock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_WRITE:
        if not data.outb:
            data.outb = bytes(message, encoding='utf-8')
        if data.outb:
            print("sending", repr(data.outb))
            sent = lsock.send(data.outb)
            data.outb = data.outb[sent:]


gsock = start_connection(HOST, int(PORT))

run = True
while run:
    try:
        text = input("Nachricht>")
    except KeyboardInterrupt:
        text = "exit"
        run = False
    events = sel.select(timeout=1)
    if events:
        for l_key, l_mask in events:
            service_connection(l_key, l_mask, text)
sel.unregister(gsock)
sel.close()
