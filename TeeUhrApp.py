from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtMultimedia as mm
import TeeUhr

RESOURCE_PATH = "C:/Users/pabst/AppData/Local/Programs/Python/Python38-32/Lib/site-packages/arcade/resources"


class ExampleApp(QMainWindow):
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.raw_time = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.count_down)
        self.effect = mm.QSoundEffect()
        self.effect.setSource(QtCore.QUrl.fromLocalFile(f"{RESOURCE_PATH}/Sounds/gameover1.wav"))
        self.effect.setLoopCount(10)

    def count_down(self):
        if self.raw_time > 0:
            self.raw_time -= 1
        else:
            self.timer.stop()
            self.effect.play()
        self.display_time()

    def display_time(self):
        minutes = self.raw_time // 60
        seconds = self.raw_time % 60
        time_str = "{0:02d}:{1:02d}".format(minutes, seconds)
        ui_window.label.setText(time_str)

    def increment_minutes(self):
        self.raw_time += 60
        self.display_time()

    def increment_seconds(self):
        self.raw_time += 10
        self.display_time()

    def decrement_minutes(self):
        if self.raw_time > 60:
            self.raw_time -= 60
        self.display_time()

    def decrement_seconds(self):
        if self.raw_time > 10:
            self.raw_time -= 10
        self.display_time()

    def start_timer(self):
        self.timer.start(1000)


app = QApplication([])
ui_window = TeeUhr.Ui_MainWindow()
ex = ExampleApp()
ui_window.setupUi(ex)
ex.show()
app.exec_()
