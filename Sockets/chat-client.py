import socket
import selectors
import types
import ChatClientGui
from PyQt5 import QtWidgets

sel = selectors.DefaultSelector()


class ChatClientWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(ChatClientWindow, self).__init__(parent)

    def connect_server(self):
        global gsock
        host = ui_window.lineEdit.text()
        port = int(ui_window.lineEdit_2.text())
        gsock = start_connection(host, int(port))

    def disconnect_server(self):
        text = "exit"
        events = sel.select(timeout=1)
        if events:
            for l_key, l_mask in events:
                service_connection(l_key, l_mask, text)
        sel.unregister(gsock)
        sel.close()

    def send_message(self):
        text = ui_window.messageEdit.toPlainText()
        events = sel.select(timeout=1)
        if events:
            for l_key, l_mask in events:
                service_connection(l_key, l_mask, text)


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
            sent = lsock.send(data.outb)
            data.outb = data.outb[sent:]

gsock = None

app = QtWidgets.QApplication([])
ex = ChatClientWindow()
ui_window = ChatClientGui.Ui_MainWindow()
ui_window.setupUi(ex)
ex.show()
app.exec_()
