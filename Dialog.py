# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\pabst\PycharmProjects\Übungen\Dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(513, 595)
        font = QtGui.QFont()
        font.setPointSize(10)
        Dialog.setFont(font)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(9, 560, 481, 24))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(250, 370, 261, 173))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(0, 4, -1, -1)
        self.gridLayout.setHorizontalSpacing(15)
        self.gridLayout.setVerticalSpacing(16)
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 2, 1, 1)
        self.edit_starttime = QtWidgets.QTimeEdit(self.groupBox)
        self.edit_starttime.setObjectName("edit_starttime")
        self.gridLayout.addWidget(self.edit_starttime, 1, 0, 1, 1)
        self.edit_endtime = QtWidgets.QTimeEdit(self.groupBox)
        self.edit_endtime.setObjectName("edit_endtime")
        self.gridLayout.addWidget(self.edit_endtime, 1, 1, 1, 1)
        self.display_duration = QtWidgets.QLineEdit(self.groupBox)
        self.display_duration.setReadOnly(True)
        self.display_duration.setObjectName("display_duration")
        self.gridLayout.addWidget(self.display_duration, 1, 2, 1, 1)
        self.button_apply = QtWidgets.QPushButton(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.button_apply.setFont(font)
        self.button_apply.setObjectName("button_apply")
        self.gridLayout.addWidget(self.button_apply, 2, 0, 1, 1)
        self.button_note = QtWidgets.QPushButton(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.button_note.setFont(font)
        self.button_note.setObjectName("button_note")
        self.gridLayout.addWidget(self.button_note, 2, 2, 1, 1)
        self.button_add_worktime = QtWidgets.QPushButton(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.button_add_worktime.setFont(font)
        self.button_add_worktime.setObjectName("button_add_worktime")
        self.gridLayout.addWidget(self.button_add_worktime, 3, 0, 1, 1)
        self.button_delete = QtWidgets.QPushButton(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.button_delete.setFont(font)
        self.button_delete.setObjectName("button_delete")
        self.gridLayout.addWidget(self.button_delete, 3, 2, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(9, 9, 501, 216))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.tableWidget = QtWidgets.QTableWidget(self.widget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.verticalLayout.addWidget(self.tableWidget)
        self.widget1 = QtWidgets.QWidget(Dialog)
        self.widget1.setGeometry(QtCore.QRect(10, 240, 491, 48))
        self.widget1.setObjectName("widget1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget1)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget1)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.edit_workpackage = QtWidgets.QLineEdit(self.widget1)
        self.edit_workpackage.setObjectName("edit_workpackage")
        self.gridLayout_2.addWidget(self.edit_workpackage, 1, 0, 1, 1)
        self.button_add_wp = QtWidgets.QPushButton(self.widget1)
        self.button_add_wp.setObjectName("button_add_wp")
        self.gridLayout_2.addWidget(self.button_add_wp, 1, 1, 1, 1)
        self.widget2 = QtWidgets.QWidget(Dialog)
        self.widget2.setGeometry(QtCore.QRect(10, 300, 231, 56))
        self.widget2.setObjectName("widget2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget2)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setHorizontalSpacing(22)
        self.gridLayout_3.setVerticalSpacing(7)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_3 = QtWidgets.QLabel(self.widget2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)
        self.edit_workday = QtWidgets.QDateEdit(self.widget2)
        self.edit_workday.setObjectName("edit_workday")
        self.gridLayout_3.addWidget(self.edit_workday, 1, 0, 1, 1)
        self.button_start_stop = QtWidgets.QPushButton(self.widget2)
        self.button_start_stop.setCheckable(True)
        self.button_start_stop.setObjectName("button_start_stop")
        self.gridLayout_3.addWidget(self.button_start_stop, 1, 1, 1, 1)
        self.widget3 = QtWidgets.QWidget(Dialog)
        self.widget3.setGeometry(QtCore.QRect(10, 380, 231, 161))
        self.widget3.setObjectName("widget3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.widget3)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.table_worktimes = QtWidgets.QTableWidget(self.widget3)
        self.table_worktimes.setObjectName("table_worktimes")
        self.table_worktimes.setColumnCount(3)
        self.table_worktimes.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_worktimes.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_worktimes.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_worktimes.setHorizontalHeaderItem(2, item)
        self.table_worktimes.horizontalHeader().setDefaultSectionSize(70)
        self.verticalLayout_3.addWidget(self.table_worktimes)
        self.label_5.setBuddy(self.edit_starttime)
        self.label_6.setBuddy(self.edit_endtime)
        self.label_7.setBuddy(self.display_duration)
        self.label_2.setBuddy(self.edit_workpackage)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Tätigkeitsnachweis"))
        self.groupBox.setTitle(_translate("Dialog", "Ändern"))
        self.label_5.setText(_translate("Dialog", "Startzeit"))
        self.label_6.setText(_translate("Dialog", "Endezeit"))
        self.label_7.setText(_translate("Dialog", "Dauer"))
        self.button_apply.setText(_translate("Dialog", "Übernehmen"))
        self.button_note.setText(_translate("Dialog", "Notiz"))
        self.button_add_worktime.setText(_translate("Dialog", "Hinzufügen"))
        self.button_delete.setText(_translate("Dialog", "Löschen"))
        self.label.setText(_translate("Dialog", "An diesen Arbeitspaketen wird gearbeitet"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Tätigkeit"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Anfang"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Ende"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Dauer"))
        self.label_2.setText(_translate("Dialog", "Tätigkeit"))
        self.button_add_wp.setText(_translate("Dialog", "Hinzufügen"))
        self.label_3.setText(_translate("Dialog", "Anzeigedatum"))
        self.button_start_stop.setText(_translate("Dialog", "Beginn"))
        self.label_4.setText(_translate("Dialog", "gespeicherte Arbeitszeiten"))
        item = self.table_worktimes.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Startzeit"))
        item = self.table_worktimes.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Endezeit"))
        item = self.table_worktimes.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Dauer"))
