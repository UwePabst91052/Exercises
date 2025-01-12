# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\pabst\PycharmProjects\Übungen\Übung1.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(289, 300)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(Form)
        self.spinBox.setMaximum(255)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout.addWidget(self.spinBox, 1, 0, 1, 1)
        self.verticalSlider = QtWidgets.QSlider(Form)
        self.verticalSlider.setMaximum(255)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")
        self.gridLayout.addWidget(self.verticalSlider, 2, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.spinBox_2 = QtWidgets.QSpinBox(Form)
        self.spinBox_2.setMaximum(255)
        self.spinBox_2.setObjectName("spinBox_2")
        self.gridLayout_2.addWidget(self.spinBox_2, 1, 0, 1, 1)
        self.verticalSlider_2 = QtWidgets.QSlider(Form)
        self.verticalSlider_2.setMaximum(255)
        self.verticalSlider_2.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_2.setObjectName("verticalSlider_2")
        self.gridLayout_2.addWidget(self.verticalSlider_2, 2, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_2)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)
        self.spinBox_3 = QtWidgets.QSpinBox(Form)
        self.spinBox_3.setMaximum(255)
        self.spinBox_3.setObjectName("spinBox_3")
        self.gridLayout_3.addWidget(self.spinBox_3, 1, 0, 1, 1)
        self.verticalSlider_3 = QtWidgets.QSlider(Form)
        self.verticalSlider_3.setMaximum(255)
        self.verticalSlider_3.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_3.setObjectName("verticalSlider_3")
        self.gridLayout_3.addWidget(self.verticalSlider_3, 2, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_3)

        self.retranslateUi(Form)
        self.verticalSlider.valueChanged['int'].connect(self.spinBox.setValue)
        self.verticalSlider_2.valueChanged['int'].connect(self.spinBox_2.setValue)
        self.verticalSlider_3.valueChanged['int'].connect(self.spinBox_3.setValue)
        self.spinBox.valueChanged['int'].connect(self.verticalSlider.setValue)
        self.spinBox_2.valueChanged['int'].connect(self.verticalSlider_2.setValue)
        self.spinBox_3.valueChanged['int'].connect(self.verticalSlider_3.setValue)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "RED"))
        self.label_2.setText(_translate("Form", "GREEN"))
        self.label_3.setText(_translate("Form", "BLUE"))
