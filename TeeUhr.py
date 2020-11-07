# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\pabst\PycharmProjects\Übungen\TeeUhr.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(235, 144)
        MainWindow.setWindowTitle("Tee Uhr")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 10, 131, 61))
        font = QtGui.QFont()
        font.setFamily("Impact")
        font.setPointSize(30)
        font.setItalic(False)
        font.setKerning(True)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label.setLineWidth(3)
        self.label.setMidLineWidth(0)
        self.label.setText("00:00")
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.pb_inc_seconds = QtWidgets.QPushButton(self.centralwidget)
        self.pb_inc_seconds.setGeometry(QtCore.QRect(180, 10, 21, 23))
        self.pb_inc_seconds.setObjectName("pb_inc_seconds")
        self.pb_dec_seconds = QtWidgets.QPushButton(self.centralwidget)
        self.pb_dec_seconds.setGeometry(QtCore.QRect(180, 50, 21, 23))
        self.pb_dec_seconds.setObjectName("pb_dec_seconds")
        self.pb_inc_minute = QtWidgets.QPushButton(self.centralwidget)
        self.pb_inc_minute.setGeometry(QtCore.QRect(30, 10, 21, 23))
        self.pb_inc_minute.setObjectName("pb_inc_minute")
        self.pb_dec_minute = QtWidgets.QPushButton(self.centralwidget)
        self.pb_dec_minute.setGeometry(QtCore.QRect(30, 50, 21, 23))
        self.pb_dec_minute.setObjectName("pb_dec_minute")
        self.pb_start_timer = QtWidgets.QPushButton(self.centralwidget)
        self.pb_start_timer.setGeometry(QtCore.QRect(80, 80, 75, 23))
        self.pb_start_timer.setObjectName("pb_start_timer")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 235, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pb_inc_minute.clicked.connect(MainWindow.increment_minutes)
        self.pb_dec_minute.clicked.connect(MainWindow.decrement_minutes)
        self.pb_inc_seconds.clicked.connect(MainWindow.increment_seconds)
        self.pb_dec_seconds.clicked.connect(MainWindow.decrement_seconds)
        self.pb_start_timer.clicked.connect(MainWindow.start_timer)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.pb_inc_seconds.setText(_translate("MainWindow", "+"))
        self.pb_dec_seconds.setText(_translate("MainWindow", "-"))
        self.pb_inc_minute.setText(_translate("MainWindow", "+"))
        self.pb_dec_minute.setText(_translate("MainWindow", "-"))
        self.pb_start_timer.setText(_translate("MainWindow", "Start"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
