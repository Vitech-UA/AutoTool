import sqlite3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate
from dialogs import Dialogs
from ui import Ui_MainWindow


class autotool:
    def add_btn_handler(self):
        Dialogs.add_success_message()


app = QtWidgets.QApplication(sys.argv)

MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
ui.addBtn.clicked.connect(autotool.add_btn_handler)

ui.part_table.setHorizontalHeaderLabels(["№", "Назва", "Ціна, грн", "Дата заміни", "Пробіг, км"])
ui.part_table.setToolTip("Сюди записуємо дані")
ui.part_table.horizontalHeaderItem(0).setToolTip("Номер запису")
ui.part_table.horizontalHeaderItem(1).setToolTip("Назва вузла, деталі, витратного матеріалу, що мінявся/ставився")
ui.part_table.horizontalHeaderItem(2).setToolTip("Вартість заміненої деталі")
ui.part_table.horizontalHeaderItem(3).setToolTip("Тут вказати дату заміни")
ui.part_table.horizontalHeaderItem(4).setToolTip("Тут вказати пробіг в км. на момент заміни деталі")
ui.part_table.verticalHeader().setVisible(False)

# підгружу поточну дату в DateEdit
date = QDate.currentDate()
ui.part_date_edit.setDate(date)

# підгружу дані з бази у таблицю
MainWindow.show()

sys.exit(app.exec_())
