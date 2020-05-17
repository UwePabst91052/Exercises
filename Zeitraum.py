# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\pabst\PycharmProjects\Übungen\Zeitraum.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(683, 284)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 401, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.calendarWidgetFrom = QtWidgets.QCalendarWidget(Dialog)
        self.calendarWidgetFrom.setGeometry(QtCore.QRect(0, 40, 321, 191))
        self.calendarWidgetFrom.setObjectName("calendarWidgetFrom")
        self.calendarWidgetUntil = QtWidgets.QCalendarWidget(Dialog)
        self.calendarWidgetUntil.setGeometry(QtCore.QRect(350, 40, 312, 183))
        self.calendarWidgetUntil.setObjectName("calendarWidgetUntil")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 10, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(380, 10, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.fromDate = QtWidgets.QDateEdit(Dialog)
        self.fromDate.setGeometry(QtCore.QRect(140, 10, 110, 22))
        self.fromDate.setObjectName("fromDate")
        self.untilDate = QtWidgets.QDateEdit(Dialog)
        self.untilDate.setGeometry(QtCore.QRect(480, 10, 110, 22))
        self.untilDate.setObjectName("untilDate")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.calendarWidgetFrom.clicked['QDate'].connect(self.fromDate.setDate)
        self.fromDate.dateChanged['QDate'].connect(self.calendarWidgetFrom.setSelectedDate)
        self.calendarWidgetUntil.clicked['QDate'].connect(self.untilDate.setDate)
        self.untilDate.dateChanged['QDate'].connect(self.calendarWidgetUntil.setSelectedDate)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "<html><head/><body><p>Datum von</p></body></html>"))
        self.label_2.setText(_translate("Dialog", "<html><head/><body><p>Datum bis</p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    retCode = app.exec_()
    sys.exit(retCode)
