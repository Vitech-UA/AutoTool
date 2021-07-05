import sqlite3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate

from ui import Ui_MainWindow


def load_data_tools(self):
    """
    Підгружає з бази даних таблицю запчастин
    :param self:
    :return:
    """
    connection = None
    try:
        connection = sqlite3.connect('AutotoolDB.db')
        print("Connect success")
    except sqlite3.Error as e:
        print(f"The error '{e}' occured")

    query = "SELECT * FROM autotool"
    result = connection.execute(query)
    for row_number, row_data in enumerate(result):
        ui.tableWidget.insertRow(row_number)
        for column_number, data in enumerate(row_data):
            ui.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

    connection.close()


def insert_data_tools(self):

    query = """
    INSERT INTO
      autotool (part_name, part_price, part_date, car_milage, info)
    VALUES
      ('{0}','{1}','{2}','{3}','{4}');
    """.format(ui.lineEdit.text(), ui.lineEdit_3.text(), ui.dateEdit.text(), ui.lineEdit_3.text(), ui.lineEdit_4.text(), )
    connection = None
    print(query)
    try:
        connection = sqlite3.connect('AutotoolDB.db')
        print("Connect success")
    except sqlite3.Error as e:
        print(f"The error '{e}' occured")

    result = connection.execute(query)
    connection.commit()
    connection.close()



app = QtWidgets.QApplication(sys.argv)

MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
ui.addBtn.clicked.connect(insert_data_tools)

ui.tableWidget.setHorizontalHeaderLabels(["№", "Назва", "Ціна, грн", "Дата заміни", "Пробіг, км"])
ui.tableWidget.setToolTip("Сюди записуємо дані")
ui.tableWidget.horizontalHeaderItem(0).setToolTip("Номер запису")
ui.tableWidget.horizontalHeaderItem(1).setToolTip("Назва вузла, деталі, витратного матеріалу, що мінявся/ставився")
ui.tableWidget.horizontalHeaderItem(2).setToolTip("Вартість заміненої деталі")
ui.tableWidget.horizontalHeaderItem(3).setToolTip("Тут вказати дату заміни")
ui.tableWidget.horizontalHeaderItem(4).setToolTip("Тут вказати пробіг в км. на момент заміни деталі")

ui.tableWidget.verticalHeader().setVisible(False)

# підгружу поточну дату в DateEdit
date = QDate.currentDate()
ui.dateEdit.setDate(date)

# підгружу дані з бази у таблицю
load_data_tools(ui)
MainWindow.show()

sys.exit(app.exec_())
