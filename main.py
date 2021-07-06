import sqlite3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMessageBox

from ui import Ui_MainWindow


def show_dialog(msg: str):
    """
    Виводить messageBox із переданим повідомленням
    :param msg:
    :return:
    """
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText(msg)
    msgBox.setWindowTitle("Недостатньо даних")
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.buttonClicked.connect(msgButtonClick)

    return_value = msgBox.exec()
    if return_value == QMessageBox.Ok:
        print('OK clicked')


def msgButtonClick(i):
    print("Button clicked is:", i.text())


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
    """.format(ui.lineEdit.text(),
               ui.lineEdit_3.text(),
               ui.dateEdit.text(),
               ui.lineEdit_2.text(),
               ui.lineEdit_4.text(), )
    connection = None
    print(query)
    try:
        connection = sqlite3.connect('AutotoolDB.db')
        print("Connect success")
    except sqlite3.Error as e:
        print(f"The error '{e}' occured")

    if len(ui.lineEdit.text()) >= 3:
        if len(ui.lineEdit_3.text()) >= 1:
            if len(ui.lineEdit_2.text()) >= 3:
                result = connection.execute(query)
                connection.commit()
                connection.close()
            else:
                connection.close()
                show_dialog("Не введено пробіг авто")
        else:
            connection.close()
            show_dialog("Не введено ціну запчастини")
    else:
        connection.close()
        show_dialog("Не введено назву запчастини")


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
