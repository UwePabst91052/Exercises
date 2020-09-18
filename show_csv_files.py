import csv
import os
import sys
import CsvImport
from PyQt5.QtWidgets import *
from PyQt5 import QtCore


class ShowCsvContent(QMainWindow):
    def __init__(self, parent=None):
        super(ShowCsvContent, self).__init__(parent)
        self.file = None
        self.table = {}
        self.headline = None

    def init_ui(self):
        ui_window.action_open.triggered.connect(self.open_file)
        self.setWindowTitle("Kontoauszug")

    def open_file(self, filename=None):
        if filename is None:
            filename = QFileDialog.getOpenFileName(ex, "Öffne Datei", base_dir, "CSV Dateien (*.csv)")[0]
        self.setWindowTitle("Kontoauszug - " + os.path.basename(filename))
        self.file = open(filename, 'r')
        self.import_file()
        self.file.close()
        self.fill_header()
        self.fill_data()

    def import_file(self):
        data_lines = []
        reader = csv.reader(self.file)
        for row in reader:
            row_joined = ",".join(row)
            if reader.line_num == 1:
                self.headline = row_joined.split(';')
            else:
                data_lines.append(row_joined.split(';'))
        for n in range(0, len(self.headline)):
            column = []
            for i in range(0, len(data_lines)):
                column.insert(0, data_lines[i][n])
            self.table.update({self.headline[n]: column})

    def fill_header(self):
        ui_window.tableWidget.setColumnCount(len(self.headline))
        ui_window.tableWidget.setRowCount(0)
        col = 0
        for header in self.headline:
            item = QTableWidgetItem(header.strip('\"'))
            ui_window.tableWidget.setHorizontalHeaderItem(col, item)
            if col in (2, 6, 7, 10):
                ui_window.tableWidget.setColumnHidden(col, True)
            if col == 3:
                ui_window.tableWidget.setColumnWidth(col, 150)
            elif col == 4:
                ui_window.tableWidget.setColumnWidth(col, 250)
            elif col == 5:
                ui_window.tableWidget.setColumnWidth(col, 200)
            col += 1

    def fill_data(self):
        col = 0
        for header in self.headline:
            column = self.table[header]
            row = 0
            for cell in column:
                if col == 0:
                    ui_window.tableWidget.insertRow(row)
                item = QTableWidgetItem(cell.strip('\"'))
                if col == 8:
                    item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
                ui_window.tableWidget.setItem(row, col, item)
                row += 1
            col += 1


base_dir = "C:\\Users\\pabst\\OneDrive\\Dokumente\\Kontoauszüge"
app = QApplication([])
ui_window = CsvImport.Ui_MainWindow()
ex = ShowCsvContent()
ui_window.setupUi(ex)
ex.init_ui()
if len(sys.argv) > 1:
    ex.open_file(sys.argv[1])
ex.show()
app.exec()
