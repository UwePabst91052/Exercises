import socket
import selectors
import types
from PyQt5 import QtWidgets, QtCore
import ChatServerGui


sel = selectors.DefaultSelector()


class ChatServerWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(ChatServerWindow, self).__init__(parent)
        self.ready_to_send = False
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.monitor_selector)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def await_connection(self):
        host = ui_window.lineEdit.text()
        port = int(ui_window.lineEdit_2.text())
        self.sock.bind((host, port))
        self.sock.listen()
        status = "listening on" + str((host, port))
        ui_window.statusLabel.setText(status)
        self.sock.setblocking(False)
        sel.register(self.sock, selectors.EVENT_READ, data=None)

    def start_stop_monitoring(self, checked):
        if checked:
            ui_window.monitorButton.setText("Überwachung beenden")
            self.timer.start(500)
        else:
            ui_window.monitorButton.setText("Überwachung starten")
            ui_window.monitorButton.setChecked(False)
            self.timer.stop()

    def send_message(self):
        self.ready_to_send = True

    def monitor_selector(self):
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    status = "accepted connection from {}".format(addr)
    ui_window.statusLabel.setText(status)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.inb = recv_data
            message = data.inb.decode('utf-8')
            if message == "exit":
                status = "closing connection to {}".format(data.addr)
                ui_window.statusLabel.setText(status)
                sel.unregister(sock)
                sock.close()
                ex.start_stop_monitoring(False)
            else:
                ui_window.receivedEdit.setPlainText(message)
    if mask & selectors.EVENT_WRITE and ex.ready_to_send:
        if not data.outb:
            message = ui_window.messageEdit.toPlainText()
            data.outb = bytes(message, encoding='utf-8')
        if data.outb:
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]
            ex.ready_to_send = len(data.outb) > 0
            message = data.outb.decode('utf-8')
            ui_window.messageEdit.setPlainText(message)


app = QtWidgets.QApplication([])
ex = ChatServerWindow()
ui_window = ChatServerGui.Ui_MainWindow()
ui_window.setupUi(ex)
ex.await_connection()
ex.show()
app.exec_()
sel.close()
