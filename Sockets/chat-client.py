import socket
import selectors
import types
import ChatClientGui
from PyQt5 import QtWidgets, QtCore

sel = selectors.DefaultSelector()


class ChatClientWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(ChatClientWindow, self).__init__(parent)
        self.ready_to_send = False
        self.disconnect = False
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.monitor_selector)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_server(self):
        global gsock
        host = ui_window.lineEdit.text()
        port = int(ui_window.lineEdit_2.text())
        gsock = start_connection(host, int(port))

    def disconnect_server(self):
        self.disconnect = True
        self.ready_to_send = True

    def send_message(self):
        self.ready_to_send = True

    def monitor_selector(self):
        events = sel.select(timeout=None)
        for key, mask in events:
            service_connection(key, mask)
        if self.disconnect:
            self.disconnect = False
            self.timer.stop()
            sel.unregister(gsock)
            sel.close()


def start_connection(host, port):
    server_addr = (host, port)
    print("starting connection to", server_addr)
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.setblocking(False)
    lsock.connect_ex(server_addr)
    levents = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = types.SimpleNamespace(
        msg_total=0,
        message=None,
        outb=b"",
    )
    sel.register(lsock, levents, data=data)
    ex.timer.start(500)
    return lsock


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.inb = recv_data
            message = data.inb.decode('utf-8').strip()
            ui_window.receivedEdit.setPlainText(message)
    if mask & selectors.EVENT_WRITE and ex.ready_to_send:
        if not data.outb:
            if not ex.disconnect:
                message = ui_window.messageEdit.toPlainText()
                data.outb = bytes(message, encoding='utf-8')
            else:
                data.outb = b"exit"
        if data.outb:
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]
            ex.ready_to_send = len(data.outb) > 0
            message = data.outb.decode('utf-8')
            ui_window.messageEdit.setPlainText(message)


gsock = None

app = QtWidgets.QApplication([])
ex = ChatClientWindow()
ui_window = ChatClientGui.Ui_MainWindow()
ui_window.setupUi(ex)
ex.show()
app.exec_()
sel.close()
