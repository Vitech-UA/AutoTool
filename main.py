import sqlite3
import logging
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate
from ui import Ui_MainWindow
from dialogs import Messages
from style_table import Styles


class AutoDataBase:

    def __init__(self):
        logging.info("Конструктор класа AutoDataBase ")
        self.default_param = 1994

    def update_table(self, table_name: str):
        try:
            connection = sqlite3.connect("AutotoolDB.db")
            logging.info("DB connect success")
        except sqlite3.Error as e:
            logging.info("DB connect error: {}".format(e))

        cur = connection.cursor()

        if table_name == "autotool":
            ui.part_table.clear()
            for row_number, row_data in enumerate(cur.execute("SELECT * FROM autotool")):
                ui.part_table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    ui.part_table.setItem(row_number, column_number,
                                          QtWidgets.QTableWidgetItem(str(data)))
            connection.close()
        if table_name == "autofuel":
            ui.fuel_table.clear()
            for row_number, row_data in enumerate(cur.execute("SELECT * FROM autofuel")):
                ui.fuel_table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    ui.fuel_table.setItem(row_number, column_number,
                                          QtWidgets.QTableWidgetItem(str(data)))
            connection.close()


class AutoPart(AutoDataBase):
    insert_part_query = str()

    def __init__(self):
        super().__init__()
        ui.part_table.setStyleSheet(Styles.table_style)
        ui.part_table.verticalHeader().setVisible(False)
        ui.addBtn.clicked.connect(AutoPart.add_data)
        ui.part_table.setHorizontalHeaderLabels(["№", "Назва", "Ціна, грн", "Дата", "Пробіг, км", "Прим."])
        # підгружу поточну дату в DateEdit
        logging.info('Завантажую системну дату в part_date_edit ')
        date = QDate.currentDate()
        ui.part_date_edit.setDate(date)

    def add_data(self):
        """Метод в якому відбувається додавання інформації у БД"""
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
                            AutoPart.insert_part_query = """
                            INSERT INTO
                              autotool (part_name, part_price, part_date, car_mileage, part_note)
                            VALUES
                              ('{0}','{1}','{2}','{3}','{4}');
                            """.format(ui.part_name_edit.text(),
                                       ui.part_price_edit.text(),
                                       ui.part_date_edit.text(),
                                       ui.part_mealege_edit.text(),
                                       ui.part_note_edit.text(), )
                            logging.info("Зформовано SQL запит: '{}'".format(AutoPart.insert_part_query))
                            try:
                                connection = sqlite3.connect("AutotoolDB.db")
                                logging.info("DB connect success")
                            except sqlite3.Error as e:
                                logging.info("DB connect error: {}".format(e))
                            cur = connection.cursor()

                            cur.execute(AutoPart.insert_part_query)
                            connection.commit()
                            connection.close()
                            AutoDataBase().update_table(table_name="autotool")

    def lad_data(self):
        """Метод у якому відбувається створення (якщо її не було створено раніше) бази даних
        та таблиці autotool в яку записуватиметься інфа по замінах запчастин """
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

        # рендеринг даних у таблиці запчастин
        for row_number, row_data in enumerate(cur.execute("SELECT * FROM autotool")):
            ui.part_table.insertRow(row_number)
            logging.info(row_data)
            for column_number, data in enumerate(row_data):
                ui.part_table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        connection.close()


class AutoFuel(AutoDataBase):
    insert_refuel_query = str()

    def __init__(self):
        ui.fuel_table.setStyleSheet(Styles.table_style)
        ui.fuel_table.verticalHeader().setVisible(False)
        ui.fuel_table.horizontalHeader().setVisible(True)
        ui.add_refill_button.clicked.connect(AutoFuel.add_data)
        ui.fuel_table.setHorizontalHeaderLabels(["№", "Тип палива", "Пробіг, км", "Варт., грн",
                                                 "Об'єм, л", "Прим.", "Ціна, грн/л", "Дата"])
        ui.fuel_type_combobox.addItems(["Газ", "Бензин", "Дизель"])
        date = QDate.currentDate()
        ui.fuel_date_edit.setDate(date)

    def add_data(self):
        """Метод в якому відбувається перевірка введеної інформаці та додавання її у БД"""
        logging.info("Тип пального: {}".format(ui.fuel_type_combobox.currentText()))
        if len(ui.fuel_mealege_edit.text()) == 0:
            Messages.message("Не введено пробіг на момент заправки в поле Пробіг!")
        else:
            if not ui.fuel_mealege_edit.text().isdigit():
                Messages.message("В поле Пробіг введено не число!")
            else:
                logging.info("Пробіг: {}".format(ui.fuel_mealege_edit.text()))
                if len(ui.fuel_price_edit.text()) == 0:
                    Messages.message("Не введено вартість заправки в поле Вартість!")
                else:
                    if not ui.fuel_price_edit.text().isdigit():
                        Messages.message("В поле Вартість введено не число!")
                    else:
                        logging.info("Вартість заправки {}".format(ui.fuel_price_edit.text()))
                        if len(ui.fuel_cap_edit.text()) == 0:
                            Messages.message("Не введено к-ть літрів в поле Об'єм!")
                        else:
                            logging.info("К-ть літрів: {}".format(ui.fuel_cap_edit.text()))
                            if not ui.fuel_cap_edit.text().isdigit():
                                Messages.message("В поле Об'єм введено не число!")
                            else:
                                price = float(ui.fuel_price_edit.text())
                                capacity = float(ui.fuel_cap_edit.text())
                                cost_format = "{0:.2f}"
                                ui.fuel_cost_edit.setText(cost_format.format(price / capacity))
                                logging.info("Ціна грн/л: {}".format(cost_format.format(price / capacity)))
                                AutoFuel.insert_refuel_query = """
                                INSERT
                                INTO
                                autofuel(fuel_type, fuel_mileage, fuel_price, fuel_capacity,
                                         fuel_note, fuel_cost,fuel_data )
                                VALUES
                                ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}');
                                """.format(ui.fuel_type_combobox.currentText(),
                                           ui.fuel_mealege_edit.text(),
                                           ui.fuel_price_edit.text(),
                                           ui.fuel_cap_edit.text(),
                                           ui.fuel_note_edit.text(),
                                           ui.fuel_cost_edit.text(),
                                           ui.fuel_date_edit.text())
                                logging.info("Зформовано SQL запит: '{}'".format(AutoFuel.insert_refuel_query))
                                # з'єднуюсь з БД для запису заправки
                                try:
                                    connection = sqlite3.connect("AutotoolDB.db")
                                    logging.info("DB connect success")
                                except sqlite3.Error as e:
                                    logging.info("DB connect error: {}".format(e))
                                cur = connection.cursor()
                                cur.execute(AutoFuel.insert_refuel_query)
                                connection.commit()
                                logging.info("Очищаю таблицю для виводу оновлених даних")
                                ui.fuel_table.clear()
                                logging.info("Завантаження оновлених даних у таблицю")
                                AutoDataBase().update_table(table_name="autofuel")

    def load_data(self):
        """Метод у якому відбувається створення (якщо її не було створено раніше) бази даних
        та таблиці autofuel в яку записуватиметься інфа по заправках """
        try:
            connection = sqlite3.connect("AutotoolDB.db")
            logging.info("DB connect success")
        except sqlite3.Error as e:
            logging.info("DB connect error: {}".format(e))

        # Створюю необхідну таблицю у відкритій раніше базі даних
        cur = connection.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS autofuel(
                       ID INTEGER PRIMARY KEY AUTOINCREMENT,
                       fuel_type TEXT,
                       fuel_mileage INTEGER,
                       fuel_price TEXT,
                       fuel_data INTEGER,
                       fuel_capacity TEXT,
                       fuel_note TEXT,
                       fuel_cost TEXT);
                    """)
        connection.close()
        self.render_table


app = QtWidgets.QApplication(sys.argv)

MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
# Налаштування виведення логів
logging.basicConfig(level=logging.INFO)

autofuel = AutoFuel()
autotool = AutoPart()
autotool.update_table(table_name="autotool")
autofuel.update_table(table_name="autofuel")
MainWindow.setFixedSize(1085, 500)
MainWindow.show()

sys.exit(app.exec_())
