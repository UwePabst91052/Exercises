#!/usr/bin/env python3

import socket
import selectors
import traceback
from PyQt5 import QtWidgets, QtCore

import libclient
import ChatClientGui

sel = selectors.DefaultSelector()


class ChatClientWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(ChatClientWindow, self).__init__(parent)
        self.disconnect = False
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.monitor_selector)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_server(self):
        global gsock, message
        host = ui_window.lineEdit.text()
        port = int(ui_window.lineEdit_2.text())
        user = ui_window.lineEdit_3.text()
        gsock = start_connection(host, port)
        message.request = create_request("login", user)
        message.ready_to_send = True
        message.set_selector_events_mask("w")

    def disconnect_server(self):
        global message
        self.disconnect = True
        action = "disconnect"
        message.request = create_request(action, "client")
        message.ready_to_send = True
        message.set_selector_events_mask("w")

    def send_message(self):
        global message
        action = "send"
        value = ui_window.messageEdit.toPlainText()
        message.request = create_request(action, value)
        message.ready_to_send = True
        message.set_selector_events_mask("w")

    def monitor_selector(self):
        events = sel.select(timeout=None)
        message = None
        for key, mask in events:
            message = key.data
            try:
                message.process_events(mask)
            except Exception:
                print(
                    "main: error: exception for",
                    f"{message.addr}:\n{traceback.format_exc()}",
                )
                message.close()
        if self.disconnect:
            self.disconnect = False
            self.timer.stop()
            if message is not None:
                message.close()

    def display_received_message(self, text):
        items = ui_window.listMessages.findItems(text, QtCore.Qt.MatchExactly)
        if len(items) == 0:
            ui_window.listMessages.addItem(text)

    def display_chatters(self, chatters):
        for chatter in chatters:
            items = ui_window.listChatters.findItems(chatter, QtCore.Qt.MatchExactly)
            if len(items) == 0:
                ui_window.listChatters.addItem(chatter)


def create_request(action, value):
    if action in ("send", "login", "logout", "peer2peer", "disconnect"):
        return dict(
            type="text/json",
            encoding="utf-8",
            content=dict(action=action, value=value),
        )
    else:
        return dict(
            type="binary/custom-client-binary-type",
            encoding="binary",
            content=bytes(action + value, encoding="utf-8"),
        )


def start_connection(host, port):
    global message
    addr = (host, port)
    print("starting connection to", addr)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    message = libclient.Message(sel, sock, addr, ex)
    sel.register(sock, events, data=message)
    ex.timer.start(500)
    return sock


gsock = None
message = None

app = QtWidgets.QApplication([])
ex = ChatClientWindow()
ui_window = ChatClientGui.Ui_MainWindow()
ui_window.setupUi(ex)
ex.show()
app.exec_()
sel.close()

