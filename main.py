import sqlite3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate

from ui import Ui_MainWindow


def loadData(self):
    connection = sqlite3.connect('AutotoolDB.db')
    query = "SELECT * FROM autotool"
    result = connection.execute(query)
    for row_number, row_data in enumerate(result):
        ui.tableWidget.insertRow(row_number)
        for column_number, data in enumerate(row_data):
            ui.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

    connection.close()


app = QtWidgets.QApplication(sys.argv)

MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

# підгружу поточну дату в DateEdit
date = QDate.currentDate()
ui.dateEdit.setDate(date)

# підгружу дані з бази у таблицю
loadData(ui)

MainWindow.show()

sys.exit(app.exec_())
