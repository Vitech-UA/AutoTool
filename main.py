import sqlite3
import logging
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate
from ui import Ui_MainWindow
from dialogs import Messages


class Autotool:
    insert_part_query = str()

    def __init__(self):
        ui.part_price_edit.setStyleSheet("color: black;")

    def add_data(self):
        if len(ui.part_name_edit.text()) == 0:
            Messages.message("Не введено назву запчастини в поле Назва ЗЧ!")
        else:
            logging.info("Назва ЗЧ:'{}'".format(ui.part_name_edit.text()))
            if len(ui.part_mealege_edit.text()) == 0:
                Messages.message("Не введено пробіг")
            else:
                if not ui.part_mealege_edit.text().isdigit():
                    Messages.message("В поле Пробіг введено не число")
                else:
                    logging.info("Пробіг:'{}', км".format(ui.part_mealege_edit.text()))
                    if len(ui.part_price_edit.text()) == 0:
                        Messages.message("Не введено вартість запчастини")
                    else:
                        if not ui.part_price_edit.text().isdigit():
                            Messages.message("В поле Ціна введено не число")
                        else:
                            logging.info("Ціна:'{}', грн".format(ui.part_price_edit.text()))
                            logging.info("Підготовка sql-запиту")
                            Autotool.insert_part_query = """
                            INSERT INTO
                              autotool (part_name, part_price, part_date, car_mileage, part_note)
                            VALUES
                              ('{0}','{1}','{2}','{3}','{4}');
                            """.format(ui.part_name_edit.text(),
                                       ui.part_price_edit.text(),
                                       ui.part_date_edit.text(),
                                       ui.part_mealege_edit.text(),
                                       ui.part_note_edit.text(), )
                            logging.info("Зформовано SQL запит: '{}'".format(Autotool.insert_part_query))
                            try:
                                connection = sqlite3.connect("AutotoolDB.db")
                                logging.info("DB connect success")
                            except sqlite3.Error as e:
                                logging.info("DB connect error: {}".format(e))
                            cur = connection.cursor()
                            cur.execute(Autotool.insert_part_query)
                            connection.commit()
                            logging.info("Очищаю таблицю для виводу оновлених даних")
                            ui.part_table.clear()
                            # рендеринг даних у таблиці
                            ui.part_table.setHorizontalHeaderLabels(
                                ["№", "Назва", "Ціна, грн", "Дата", "Пробіг, км", "Прим."])

                            for row_number, row_data in enumerate(cur.execute("SELECT * FROM autotool")):
                                ui.part_table.insertRow(row_number)
                                logging.info(row_data)
                                for column_number, data in enumerate(row_data):
                                    ui.part_table.setItem(row_number, column_number,
                                                          QtWidgets.QTableWidgetItem(str(data)))

                            connection.close()

    def lad_data(self):
        # Створюю або відкриваю файл бази даних
        try:
            connection = sqlite3.connect("AutotoolDB.db")
            logging.info("DB connect success")
        except sqlite3.Error as e:
            logging.info("DB connect error: {}".format(e))
        # Створюю необхідну таблицю у відкритій раніше базі даних
        cur = connection.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS autotool(
           ID INTEGER PRIMARY KEY AUTOINCREMENT,
           part_name TEXT,
           part_price INTEGER,
           part_date TEXT,
           car_mileage INTEGER,
           part_note TEXT);
        """)

        # Фіксація змін, якщо це необхідно
        try:
            connection.commit()
            logging.info("Фіксація змін у БД")
        except sqlite3.Error as e:
            logging.info("DB commit error: {}".format(e))

        # рендеринг даних у таблиці
        ui.part_table.verticalHeader().setVisible(False)
        ui.part_table.setHorizontalHeaderLabels(["№", "Назва", "Ціна, грн", "Дата", "Пробіг, км", "Прим."])
        for row_number, row_data in enumerate(cur.execute("SELECT * FROM autotool")):
            ui.part_table.insertRow(row_number)
            logging.info(row_data)
            for column_number, data in enumerate(row_data):
                ui.part_table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        connection.close()


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
ui.addBtn.clicked.connect(Autotool.add_data)
autotool = Autotool()
# Налаштування виведення логів
logging.basicConfig(level=logging.INFO)

# підгружу поточну дату в DateEdit
logging.info('Завантажую системну дату в part_date_edit ')
date = QDate.currentDate()
ui.part_date_edit.setDate(date)

autotool.lad_data()

MainWindow.show()

sys.exit(app.exec_())
