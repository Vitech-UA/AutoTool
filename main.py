import sqlite3
import logging
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate
from dialogs import Dialogs
from ui import Ui_MainWindow
from autotool import Autotool

app = QtWidgets.QApplication(sys.argv)

MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
ui.addBtn.clicked.connect(Autotool.add_btn_handler)



# підгружу поточну дату в DateEdit
date = QDate.currentDate()
ui.part_date_edit.setDate(date)

# підгружу дані з бази у таблицю
MainWindow.show()

sys.exit(app.exec_())
