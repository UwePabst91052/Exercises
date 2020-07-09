#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback

import libserver

sel = selectors.DefaultSelector()


def accept_wrapper(sock):
    global client_list
    conn, addr = sock.accept()  # Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
    message = libserver.Message(sel, conn, addr)
    client_list.append((conn, addr, message))
    message.client_list = client_list
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=message)


if len(sys.argv) != 3:
    host, port = '127.0.0.1', 65432
else:
    host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Avoid bind() exception: OSError: [Errno 48] Address already in use
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

client_list = []
try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                message = key.data
                try:
                    message.process_events(mask)
                except Exception:
                    print(
                        "main: error: exception for",
                        f"{message.addr}:\n{traceback.format_exc()}",
                    )
                    message.close()
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()
