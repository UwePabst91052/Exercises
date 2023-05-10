# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\pabst\PycharmProjects\Übungen\Übung3.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

RECENT_FILES_MAX = 5

from PyQt5 import QtCore, QtGui, QtWidgets
from Workpackage import *
from ReadWorkpackes import *
from StoreWorkpackages import *
import Zeitraum as ts
import AddWorkday as awd
import datetime as dt
from BerichtAnzeigen import display_report
from BerichtAusdrucken import create_work_dictionary
from BerichtAusdrucken import create_work_merged
from BerichtAusdrucken import report_work_summary
from BerichtAusdrucken import report_work_summary_timespan
from BerichtAusdrucken import report_workday_summary
from BerichtAusdrucken import report_workpackage_summary
from BerichtAusdrucken import report_number_of_workdays
import os

DATA_FILE_PATH = "./Dateien/RecentFiles.txt"

class OverviewSection(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel(self)
        self.table_overview = QtWidgets.QTableWidget(self)
        self.setGeometry(QtCore.QRect(9, 9, 601, 216))
        self.setObjectName("layoutWidget")
        self.verticalLayout.setObjectName("verticalLayout")
        self.label.setObjectName("label")
        self.label.setText("An diesen Arbeitspaketen wird gearbeitet")
        self.verticalLayout.addWidget(self.label)
        self.table_overview.setObjectName("table_overview")
        self.table_overview.setColumnCount(4)
        self.table_overview.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Tätigkeit")
        self.table_overview.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Anfang")
        self.table_overview.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Ende")
        self.table_overview.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Dauer")
        self.table_overview.setHorizontalHeaderItem(3, item)
        self.table_overview.horizontalHeader().setDefaultSectionSize(80)
        self.table_overview.verticalHeader().setDefaultSectionSize(20)
        self.table_overview.setColumnWidth(0, 350)
        self.table_overview.verticalHeader().setVisible(False)
        self.table_overview.setShowGrid(False)
        self.table_overview.itemClicked.connect(self.on_item_clicked)
        self.verticalLayout.addWidget(self.table_overview)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

    def add_workpackage(self, name=""):
        row = self.table_overview.rowCount()
        self.table_overview.insertRow(row)
        if len(name) > 0:
            item = QtWidgets.QTableWidgetItem(name)
            self.table_overview.setItem(row, 0, item)

    def update_times(self, index, start="", stop="", duration=""):
        row = index
        item = QtWidgets.QTableWidgetItem(start)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table_overview.setItem(row, 1, item)
        item = QtWidgets.QTableWidgetItem(stop)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table_overview.setItem(row, 2, item)
        item = QtWidgets.QTableWidgetItem(duration)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table_overview.setItem(row, 3, item)

    def show_daily_worktime(self, daily_worktime):
        row = self.table_overview.rowCount()
        count_wp = len(workpackages)
        if row == count_wp:
            self.table_overview.insertRow(row)
            self.table_overview.setItem(row, 0, QtWidgets.QTableWidgetItem("an diesem Tag gearbeitet:"))
            item = QtWidgets.QTableWidgetItem(daily_worktime)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.table_overview.setItem(row, 3, item)
        else:
            item = self.table_overview.item(row - 1, 3)
            item.setText(daily_worktime)

    def on_item_clicked(self):
        global wp_index
        for item in self.table_overview.selectedItems():
            wp_index = item.row()
            wp = workpackages[wp_index]
            date = ex.layoutDate.get_current_date()
            ex.layoutWorktimes.add_worktimes(date, wp)
            ex.layoutWorkpackage.edit_workpackage.setText(wp.wp_name)
            ex.layoutChanging.update_times(date, wp)

    def delete_all_rows(self):
        while self.table_overview.rowCount() > 0:
            self.table_overview.removeRow(0)

    def update_wp_overview(self, date):
        row = 0
        for wp in workpackages:
            wt_list = get_worktimes_for_date(date, wp)
            ix = len(wt_list) - 1
            if ix >= 0:
                times = wt_list[ix]
                ex.layoutOverview.update_times(row, times[0], times[1], times[2])
            else:
                ex.layoutOverview.update_times(row)
            row += 1
        self.show_daily_worktime(get_daily_worktime(date))


class WorkpackageSection(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(QtCore.QRect(10, 240, 541, 48))
        self.setObjectName("layoutWidget_4")
        self.gridLayout_2 = QtWidgets.QGridLayout(self)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setHorizontalSpacing(24)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.edit_workpackage = QtWidgets.QLineEdit(self)
        self.edit_workpackage.setObjectName("edit_workpackage")
        self.gridLayout_2.addWidget(self.edit_workpackage, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setText("Tätigkeit")
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.button_add_wp = QtWidgets.QPushButton(self)
        self.button_add_wp.setText("Hinzufügen")
        self.button_add_wp.setObjectName("button_add_wp")
        self.button_add_wp.clicked.connect(self.on_click_add_wp)
        self.gridLayout_2.addWidget(self.button_add_wp, 1, 1, 1, 1)
        self.gridLayout_2.setColumnStretch(0, 10)

    def on_click_add_wp(self):
        name = self.edit_workpackage.text()
        wp = Workpackage(name)
        wp.add_workday(dt.date.today().strftime("%d.%m."))
        workpackages.append(wp)
        ex.layoutOverview.add_workpackage(name)


class DateSection(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(QtCore.QRect(10, 300, 331, 56))
        self.setObjectName("layoutWidget_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setHorizontalSpacing(22)
        self.gridLayout_3.setVerticalSpacing(7)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)
        self.cb_workdays = QtWidgets.QComboBox(self)
        self.cb_workdays.setObjectName("cb_workdays")
        self.cb_workdays.activated.connect(self.on_click_item)
        self.gridLayout_3.addWidget(self.cb_workdays, 1, 0, 1, 1)
        self.button_start_stop = QtWidgets.QPushButton(self)
        self.button_start_stop.setCheckable(True)
        self.button_start_stop.setObjectName("button_start_stop")
        self.button_start_stop.clicked[bool].connect(self.on_click_start_stop)
        self.gridLayout_3.addWidget(self.button_start_stop, 1, 1, 1, 1)
        self.button_add_day = QtWidgets.QPushButton(self)
        self.button_add_day.setObjectName("button_add_day")
        self.button_add_day.clicked.connect(self.on_click_add_workday)
        self.gridLayout_3.addWidget(self.button_add_day, 1, 2, 1, 1)
        self.label_3.setText("Anzeigedatum")
        self.button_start_stop.setText("Beginn")
        self.button_add_day.setText("Hinzufügen")

    def on_click_start_stop(self, pressed):
        global wt_index
        if wp_index < 0:
            return
        wp = workpackages[wp_index]
        time = QtCore.QTime.currentTime().toString(QtCore.Qt.TextDate)
        if not pressed:
            wp.finish_working(time)
            worktime = str(wp.cur_workday.cur_worktime)
            times = worktime.split()
            ex.layoutOverview.update_times(wp_index, start=times[0], stop=times[1], duration=times[2])
            ex.layoutWorktimes.add_worktime(times[0], times[1], times[2])
            ex.layoutChanging.set_endtime(times[1], times[2])
            self.button_start_stop.setText("Beginn")
            date = self.get_current_date()
            ex.layoutOverview.show_daily_worktime(get_daily_worktime(date))
        else:
            date = self.get_current_date()
            wp.add_workday(date)
            wp.begin_working(time)
            wt_index = -1
            time = wp.cur_workday.cur_worktime.start_time
            time = str(time)
            ex.layoutOverview.update_times(wp_index, start=time)
            ex.layoutChanging.set_starttime(time)
            ex.layoutChanging.set_endtime("00:00", "")
            self.button_start_stop.setText("Ende")

    def on_click_add_workday(self):
        dialog = QtWidgets.QDialog()
        ui_dialog = awd.Ui_Dialog()
        ui_dialog.setupUi(dialog)
        dialog.exec_()
        new_date = ui_dialog.calendarWidget.selectedDate().toString("dd.MM.yyyy")
        if wp_index >= 0:
            wp = workpackages[wp_index]
            wp.add_workday(new_date)
            create_date_list(wp.workdays)
            self.add_workdays()

    def add_workdays(self):
        self.cb_workdays.clear()
        for date in all_workdays:
            self.cb_workdays.addItem(date)
        date = QtCore.QDate.currentDate().toString(QtCore.Qt.DefaultLocaleShortDate)
        if date not in all_workdays:
            self.cb_workdays.addItem(date)
        self.cb_workdays.setCurrentText(date)

    def on_click_item(self):
        date = self.get_current_date()
        if wp_index >= 0:
            wp = workpackages[wp_index]
            ex.layoutWorktimes.add_worktimes(date, wp)
            ex.layoutChanging.update_times(date, wp)
        ex.layoutOverview.update_wp_overview(date)
        ex.layoutOverview.show_daily_worktime(get_daily_worktime(date))

    def get_current_date(self):
        return self.cb_workdays.currentText()


class WorktimesSection(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(QtCore.QRect(10, 380, 231, 161))
        self.setObjectName("layoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setObjectName("label_4")
        self.label_4.setText("gespeicherte Arbeitszeiten")
        self.verticalLayout_3.addWidget(self.label_4)
        self.table_worktimes = QtWidgets.QTableWidget(self)
        self.table_worktimes.setObjectName("table_worktimes")
        self.table_worktimes.setColumnCount(3)
        self.table_worktimes.setRowCount(0)
        self.table_worktimes.verticalHeader().setVisible(False)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Startzeit")
        self.table_worktimes.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Endezeit")
        self.table_worktimes.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Dauer")
        self.table_worktimes.setHorizontalHeaderItem(2, item)
        self.table_worktimes.horizontalHeader().setDefaultSectionSize(70)
        self.table_worktimes.verticalHeader().setDefaultSectionSize(20)
        self.table_worktimes.setShowGrid(False)
        self.table_worktimes.itemClicked.connect(self.on_item_clicked)
        self.verticalLayout_3.addWidget(self.table_worktimes)

    def add_worktime(self, start, end, duration):
        global wt_index
        row = self.table_worktimes.rowCount()
        self.table_worktimes.insertRow(row)
        item = QtWidgets.QTableWidgetItem(start)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table_worktimes.setItem(row, 0, item)
        item = QtWidgets.QTableWidgetItem(end)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table_worktimes.setItem(row, 1, item)
        item = QtWidgets.QTableWidgetItem(duration)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table_worktimes.setItem(row, 2, item)
        wt_index = row

    def add_worktimes(self, date, workpackage):
        global wt_index
        self.table_worktimes.clearContents()
        wt_index = -1
        while self.table_worktimes.rowCount() > 0:
            self.table_worktimes.removeRow(0)
        date = ex.layoutDate.get_current_date()
        wt_list = get_worktimes_for_date(date, workpackage)
        for times in wt_list:
            self.add_worktime(times[0], times[1], times[2])

    def delete_all_rows(self):
        while self.table_worktimes.rowCount() > 0:
            self.table_worktimes.removeRow(0)

    def on_item_clicked(self):
        global wt_index
        wp = workpackages[wp_index]
        wt_index = self.table_worktimes.currentRow()
        date = ex.layoutDate.get_current_date()
        ex.layoutChanging.update_times(date, wp)


class ChangingSection(QtWidgets.QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(QtCore.QRect(250, 370, 261, 173))
        self.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(0, 4, -1, -1)
        self.gridLayout.setHorizontalSpacing(15)
        self.gridLayout.setVerticalSpacing(16)
        self.gridLayout.setObjectName("gridLayout")
        self.edit_starttime = QtWidgets.QTimeEdit(self)
        self.edit_starttime.setObjectName("edit_starttime")
        self.edit_starttime.setDisplayFormat("HH:mm")
        self.gridLayout.addWidget(self.edit_starttime, 1, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 1, 1, 1)
        self.button_apply = QtWidgets.QPushButton(self)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.button_apply.setFont(font)
        self.button_apply.setObjectName("button_apply")
        self.button_apply.clicked.connect(self.on_click_apply)
        self.gridLayout.addWidget(self.button_apply, 2, 0, 1, 1)
        self.button_note = QtWidgets.QPushButton(self)
        self.button_note.clicked.connect(self.on_click_note)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.button_note.setFont(font)
        self.button_note.setObjectName("button_note")
        self.gridLayout.addWidget(self.button_note, 2, 2, 1, 1)
        self.button_add_worktime = QtWidgets.QPushButton(self)
        self.button_add_worktime.clicked.connect(self.on_click_add)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.button_add_worktime.setFont(font)
        self.button_add_worktime.setObjectName("button_add_worktime")
        self.gridLayout.addWidget(self.button_add_worktime, 3, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 2, 1, 1)
        self.edit_endtime = QtWidgets.QTimeEdit(self)
        self.edit_endtime.setObjectName("edit_endtime")
        self.edit_endtime.setDisplayFormat("HH:mm")
        self.gridLayout.addWidget(self.edit_endtime, 1, 1, 1, 1)
        self.button_delete = QtWidgets.QPushButton(self)
        self.button_delete.clicked.connect(self.on_click_delete)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.button_delete.setFont(font)
        self.button_delete.setObjectName("button_delete")
        self.gridLayout.addWidget(self.button_delete, 3, 2, 1, 1)
        self.display_duration = QtWidgets.QLineEdit(self)
        self.display_duration.setReadOnly(True)
        self.display_duration.setObjectName("display_duration")
        self.gridLayout.addWidget(self.display_duration, 1, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.setTitle("Ändern")
        self.label_6.setText("Endezeit")
        self.button_apply.setText("Übernehmen")
        self.button_note.setText("Notiz")
        self.button_add_worktime.setText("Hinzufügen")
        self.label_7.setText("Dauer")
        self.button_delete.setText("Löschen")
        self.label_5.setText("Startzeit")

    def set_starttime(self, time_str):
        self.edit_starttime.setTime(QtCore.QTime.fromString(time_str))

    def set_endtime(self, endtime, duration):
        self.edit_endtime.setTime(QtCore.QTime.fromString(endtime))
        self.display_duration.setText(duration)

    def update_times(self, date, workpackage):
        global wt_index
        wt_list = get_worktimes_for_date(date, workpackage)
        if wt_index < 0:
            wt_index = len(wt_list) - 1
        if wt_index >= 0:
            times = wt_list[wt_index]
            self.set_starttime(times[0], )
            self.set_endtime(times[1], times[2])
        else:
            self.set_starttime("00:00")
            self.set_endtime("00:00", "")

    def on_click_add(self):
        date = ex.layoutDate.get_current_date()
        if wp_index >= 0:
            wp = workpackages[wp_index]
            start_time = self.edit_starttime.time().toString(QtCore.Qt.TextDate)
            end_time = self.edit_endtime.time().toString(QtCore.Qt.TextDate)
            wp.add_workday(date)
            wp.begin_working(start_time)
            wp.finish_working(end_time)
            ex.layoutOverview.update_wp_overview(date)
            ex.layoutWorktimes.add_worktimes(date, wp)
            self.update_times(date, wp)

    def on_click_apply(self):
        date = ex.layoutDate.get_current_date()
        wt = None
        wp = None
        if wp_index >= 0:
            wp = workpackages[wp_index]
            for wd in wp.workdays:
                if wd.date == date:
                    if wt_index >= 0:
                        wt = wd.worktimes[wt_index]
                    else:
                        wt = wd.cur_worktime
        if wt is not None:
            start = self.edit_starttime.time().toString(QtCore.Qt.TextDate)
            if start != wt.start_time:
                wt.set_start_time(start)
            end = self.edit_endtime.time().toString(QtCore.Qt.TextDate)
            if end != wt.end_time:
                wt.set_end_time(end)
            if end != '00:00:00':
                ex.layoutOverview.update_wp_overview(date)
                ex.layoutWorktimes.add_worktimes(date, wp)
                ex.layoutChanging.update_times(date, wp)
            else:
                ex.layoutOverview.update_times(wp_index, start=str(wt.start_time))

    def on_click_delete(self):
        date = ex.layoutDate.get_current_date()
        if wp_index >= 0 and wt_index >= 0:
            wp = workpackages[wp_index]
            for wd in wp.workdays:
                if wd.date == date:
                    del wd.worktimes[wt_index]
            ex.layoutOverview.update_wp_overview(date)
            ex.layoutWorktimes.add_worktimes(date, wp)
            self.update_times(date, wp)

    def on_click_note(self):
        pass


class UiMainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(UiMainWindow, self).__init__(parent)
        self.central_widget = QtWidgets.QWidget(self)
        self.layoutOverview = OverviewSection(self.central_widget)
        self.layoutWorkpackage = WorkpackageSection(self.central_widget)
        self.layoutDate = DateSection(self.central_widget)
        self.layoutWorktimes = WorktimesSection(self.central_widget)
        self.layoutChanging = ChangingSection(self.central_widget)

        self.menu_bar = QtWidgets.QMenuBar(self)
        self.menuFile = QtWidgets.QMenu("Datei", self)
        self.menuReport = QtWidgets.QMenu("Berichte", self)
        self.status_bar = QtWidgets.QStatusBar(self)
        self.tool_bar = QtWidgets.QToolBar(self)
        self.tool_bar.setObjectName("tool_Bar")
        self.setObjectName("MainWindow")
        self.resize(603, 600)
        self.setWindowTitle("Zeitnachweis")
        self.central_widget.setObjectName("central_widget")
        self.layoutOverview.setObjectName("layoutWidget")
        self.setCentralWidget(self.central_widget)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 658, 21))
        self.menu_bar.setObjectName("menu_bar")

        self.recent_files_actions = [self.open_recent_file0, self.open_recent_file1,
                                     self.open_recent_file2, self.open_recent_file3,
                                     self.open_recent_file4]
        self.recent_files = read_recent_files()
        self.action_new = QtWidgets.QAction("Neu", self)
        self.action_new.triggered.connect(new_file)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./resources/file-new.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_new.setIcon(icon)
        self.actionOpen = QtWidgets.QAction("Öffnen...", self)
        self.actionOpen.triggered.connect(open_file)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./resources/file-open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon1)
        self.actionSave = QtWidgets.QAction("Speichern", self)
        self.actionSave.triggered.connect(save_file)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("./resources/file-save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon2)
        self.actionSaveAs = QtWidgets.QAction("Speichern unter...")
        self.actionSaveAs.triggered.connect(save_file_as)
        self.menuRecentFiles = QtWidgets.QMenu("Zuletzt verwendet", self)
        self.menuFile.addAction(self.action_new)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addSeparator()
        index = 0
        for path, base in self.recent_files:
            recent_action = QtWidgets.QAction(base, self)
            recent_action.triggered.connect(self.recent_files_actions[index])
            self.menuFile.addAction(recent_action)
            index += 1
        self.menu_bar.addAction(self.menuFile.menuAction())

        self.action_proof_of_time = QtWidgets.QAction("Zeitnachweis", self)
        self.action_proof_of_time.triggered.connect(show_report)
        self.action_workpackage = QtWidgets.QAction("Arbeitspaket", self)
        self.action_workpackage.triggered.connect(show_workpackage)
        self.action_workday = QtWidgets.QAction("Arbeitstag", self)
        self.action_workday.triggered.connect(show_workday)
        self.action_balance = QtWidgets.QAction("Gleitzeitsaldo", self)
        self.action_balance.triggered.connect(show_balance)
        self.action_count_days = QtWidgets.QAction("Anzahl Arbeitstage", self)
        self.action_count_days.triggered.connect(show_num_workdays)
        self.menuReport.addAction(self.action_proof_of_time)
        self.menuReport.addAction(self.action_workpackage)
        self.menuReport.addAction(self.action_workday)
        self.menuReport.addAction(self.action_balance)
        self.menuReport.addAction(self.action_count_days)
        self.menu_bar.addAction(self.menuReport.menuAction())
        self.tool_bar.addAction(self.action_new)
        self.tool_bar.addAction(self.actionOpen)
        self.tool_bar.addAction(self.actionSave)

        self.setMenuBar(self.menu_bar)
        self.status_bar.setObjectName("status_bar")
        self.setStatusBar(self.status_bar)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.tool_bar)

        QtCore.QMetaObject.connectSlotsByName(self)

    def open_recent_file0(self):
        self.open_recent_file(0)

    def open_recent_file1(self):
        self.open_recent_file(1)

    def open_recent_file2(self):
        self.open_recent_file(2)

    def open_recent_file3(self):
        self.open_recent_file(3)

    def open_recent_file4(self):
        self.open_recent_file(4)

    def open_recent_file(self, index):
        path, base = self.recent_files[index]
        file_name = path + '/' + base
        open_data_file(file_name)


class ExampleApp(UiMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)


def new_file():
    global  workpackages, all_workdays, filename, wp_index, wt_index
    ex.layoutOverview.delete_all_rows()
    ex.layoutWorktimes.delete_all_rows()
    ex.layoutDate.cb_workdays.clear()
    workpackages = []
    all_workdays = []
    filename = ""
    wp_index = -1
    wt_index = -1
    ex.setWindowTitle("Zeitnachweis")


def open_file():
    global filename
    file_name = QtWidgets.QFileDialog.getOpenFileName(ex, "Öffne Datei", ".\Dateien", "XML Dateien (*.xml)")[0]
    open_data_file(file_name)


def open_data_file(file_name):
    global filename, workpackages
    if len(workpackages) > 0:
        new_file()
    filename = file_name
    file = open(filename, 'r', encoding='utf-8')
    workpackages = read_workpackages(file)
    file.close()
    # add to recent file list
    add_recent_files(filename)
    filename_base = os.path.basename(filename)
    ex.setWindowTitle("Zeitnachweis - " + filename_base)
    for wp in workpackages:
        create_date_list(wp.workdays)
    ex.layoutDate.add_workdays()
    row = 0
    date = ex.layoutDate.get_current_date()
    for wp in workpackages:
        ex.layoutOverview.add_workpackage(wp.wp_name)
        # ex.layoutChanging.update_times(date, wp)
        row += 1
    ex.layoutOverview.update_wp_overview(date)


def save_file():
    if filename == "":
        save_file_as()
    else:
        file = open(filename, 'w', encoding='utf-8')
        for wp in workpackages:
            write_workpackage(file, wp)
        file.close()


def save_file_as():
    global filename
    filename = QtWidgets.QFileDialog.getOpenFileName(ex, "Speichere Datei", ".\Dateien", "XML Dateien (*.xml)")[0]
    file = open(filename, 'w', encoding='utf-8')
    for wp in workpackages:
        write_workpackage(file, wp)
    file.close()


def show_report():
    report = report_work_summary("Otto Normalverbraucher", workpackages)
    display_report(report)


def show_workpackage():
    keylist = create_work_dictionary(workpackages)
    from_date = keylist[0]
    until_date = keylist[len(keylist) - 1]
    wp_name = workpackages[wp_index].wp_name
    report = report_workpackage_summary(wp_name, workpackages, from_date, until_date)
    display_report(report)


def show_workday():
    date = ex.layoutDate.cb_workdays.currentText()
    report = report_workday_summary(date, workpackages)
    display_report(report)

def input_timespan(min_date ,max_date):
    date = Date(min_date)
    from_date = QtCore.QDate(date.year, date.month, date.day)
    date = Date(max_date)
    until_date = QtCore.QDate(date.year, date.month, date.day)
    dialog = QtWidgets.QDialog()
    ui_dialog = ts.Ui_Dialog()
    ui_dialog.setupUi(dialog)
    ui_dialog.calendarWidgetFrom.setSelectedDate(from_date)
    ui_dialog.calendarWidgetUntil.setSelectedDate(until_date)
    dialog.exec_()
    from_date = ui_dialog.fromDate.date().toString("dd.MM.yyyy")
    until_date = ui_dialog.untilDate.date().toString("dd.MM.yyyy")
    return from_date, until_date

def merge_wpckgs(workpackages):
    mergedWorkpackages = []
    mergedWorkpackages.append(Wp.Workpackage("Merged Workpackages"))

    for wp in workpackages:
        for wd in wp.workdays:
            mergedWorkpackages[0].add_workday(str(wd.date))
            for wt in wd.worktimes:
                wt_strings = str(wt).split(" ", 3)
                mergedWorkpackages[0].begin_working(wt_strings[0])
                mergedWorkpackages[0].finish_working(wt_strings[1])
    mergedWorkpackages[0].sort_workdays()
    return mergedWorkpackages

def show_balance():
    workpackageMerged = merge_wpckgs(workpackages)
    keylist = create_work_dictionary(workpackageMerged)
    timespan = input_timespan(keylist[0],
                              keylist[len(keylist) - 1])
    report = report_work_summary_timespan("Otto Normalverbraucher", workpackages, timespan[0], timespan[1])
    display_report(report)

def show_num_workdays():
    keyList = create_work_dictionary(workpackages)
    timespan = input_timespan(keyList[0],
                              keyList[len(keyList) - 1])
    keylist = create_work_merged(workpackages, timespan[0], timespan[1])
    countOffice = 0
    countHome = 0
    countBoth = 0
    evaluation_period = "Auswertungszeitraum vom {0} bis {1}".format(timespan[0], timespan[1])
    for key in keylist.keys():
        value = keylist[key]
        if len(value) > 1:
            result = check_real_worked(key, value[0], value[1])
            if result[0]:
                countBoth += 1
            else:
                if value[result[1]].wp_name == "Homeoffice":
                    countHome += 1
                else:
                    countOffice += 1
        else:
            if value[0].wp_name == "Homeoffice":
                countHome += 1
            else:
                countOffice += 1
    report = report_number_of_workdays(keylist, countHome, countOffice, countBoth, evaluation_period)
    display_report(report)

def get_count_wt(date, wp):
    for wd in wp.workdays:
        if str(wd.date) == date:
            return len(wd.worktimes)

def check_real_worked(date, wp1, wp2):
    countWtWp1 = get_count_wt(date, wp1)
    countWtWp2 = get_count_wt(date, wp2)
    if(countWtWp1 > 0 and countWtWp2 > 0):
        return True, -1
    else:
        if countWtWp1 > 0:
            index = 0
        else:
            index = 1
        return False, index

def get_worktimes_for_date(date, workpackage):
    wd_found = None
    wt_list = []
    for wd in workpackage.workdays:
        if wd.date == date:
            wd_found = wd
            break
    if wd_found is not None:
        for wt in wd_found.worktimes:
            times = str(wt).split()
            wt_list.append(times)
    return wt_list


def create_date_list(workdays):
    for wd in workdays:
        date = str(wd.date)
        if date not in all_workdays:
            all_workdays.append(date)


def get_daily_worktime(date_str):
    daily_duration = 0
    for wp in workpackages:
        daily_duration += wp.get_wpckg_duration_for_date(date_str)
    return Time.convert_seconds_to_time_string(daily_duration)


def add_recent_files(file_name):
    if os.path.exists(DATA_FILE_PATH):
        file = open(DATA_FILE_PATH, 'r', encoding='windows-1252')
        path_list = file.readlines()
        # compare with new filename
        duplicate = False
        for path in path_list:
            base_name = os.path.basename(file_name)
            duplicate |= path.find(base_name) >= 0
        if not duplicate and len(path_list) < RECENT_FILES_MAX:
            file.close()
            file = open(DATA_FILE_PATH, 'a', encoding='windows-1252')
            file.write(filename + '\n')
    else:
        # create data file
        file = open(DATA_FILE_PATH, 'x', encoding='windows-1252')
        file.write(file_name + '\n')

    file.close()


def read_recent_files():
    file_list = []
    if os.path.exists(DATA_FILE_PATH):
        file = open(DATA_FILE_PATH, 'r', encoding='windows-1252')
        path_list = file.readlines()
        for path in path_list:
            dirname = os.path.dirname(path)
            basename = os.path.basename(path).rstrip()
            if len(file_list) < RECENT_FILES_MAX:
                file_list.append((dirname, basename))
    return file_list


workpackages = []
all_workdays = []
filename = ""
wp_index = -1
wt_index = -1
app = QtWidgets.QApplication([])
ex = ExampleApp()
ex.show()
ex.layoutDate.add_workdays()
app.exec_()
