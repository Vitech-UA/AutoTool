import logging
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QToolBar, QAction
)

from data import DataBaseImporter, DataBaseExporter
from ui import Ui_MainWindow

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

importer = DataBaseImporter()

# Створюю тулбар
toolbar = QToolBar('my_toolbar')
MainWindow.addToolBar(toolbar)

# Кнопка імпорта нової бази даних
import_action = QAction("Імпорт бази даних")
import_action.setStatusTip("Імпорт вже існуючої бази даних")
import_action.triggered.connect(importer.import_database)
toolbar.addAction(import_action)

# Кнопка експорту наявної бази даних
export_action = QAction("Експорт бази даних")
export_action.setStatusTip("ЕКспорт вже існуючої бази даних")
export_action.triggered.connect(DataBaseExporter.export_database)
toolbar.addAction(export_action)

# Налаштування виведення логів
logging.basicConfig(level=logging.INFO)
MainWindow.setFixedSize(1085, 500)
MainWindow.show()

sys.exit(app.exec_())
