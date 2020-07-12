#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback
from PyQt5 import QtWidgets, QtCore

import libserver
import ChatServerMonitor

sel = selectors.DefaultSelector()


class ChatServerWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(ChatServerWindow, self).__init__(parent)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.monitor_selector)
        self.timer.start(500)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def monitor_selector(self):
        events = sel.select(timeout=1)
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

    def add_new_connection(self, addr, user):
        row = ui_window.tableWidget.rowCount()
        ui_window.tableWidget.insertRow(row)
        item = QtWidgets.QTableWidgetItem(addr[0])
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        ui_window.tableWidget.setItem(row, 0, item)
        item = QtWidgets.QTableWidgetItem(str(addr[1]))
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        ui_window.tableWidget.setItem(row, 1, item)
        item = QtWidgets.QTableWidgetItem(user)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        ui_window.tableWidget.setItem(row, 2, item)

    def remove_closed_connection(self, user):
        items = ui_window.tableWidget.findItems(user, QtCore.Qt.MatchExactly)
        row = items[0].row()
        ui_window.tableWidget.removeRow(row)
        if ui_window.tableWidget.rowCount() == 0:
            ui_window.label_server_status.setText("listening on {0}, {1}".format(host, str(port)))


def accept_wrapper(sock):
    global client_list
    conn, addr = sock.accept()  # Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
    message = libserver.Message(sel, conn, addr, ex)
    client_list.append((conn, addr, message))
    message.client_list = client_list
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=message)
    ui_window.label_server_status.setText("Server is running")


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
sel.register(lsock, selectors.EVENT_READ | selectors.EVENT_WRITE, data=None)

client_list = []
app = QtWidgets.QApplication([])
ex = ChatServerWindow()
ui_window = ChatServerMonitor.Ui_MainWindow()
ui_window.setupUi(ex)
ui_window.label_server_status.setText("listening on {0}, {1}".format(host, str(port)))
ex.show()
app.exec_()
sel.close()
