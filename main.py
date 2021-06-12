from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5 import QtSql



app = QtWidgets.QApplication([])
ui = uic.loadUi('ui.ui')
ui.setWindowTitle('Autotool v 1.0 06/2021')

def addBtnHandler():
    print('Add Button pressed')

def delBtnHandler():
    print('Del Button pressed')

ui.addBtn.clicked.connect(addBtnHandler)
ui.delBtn.clicked.connect(delBtnHandler)

db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName('autotool.db')

ui.tableWidget.setColumnCount(4)
ui.tableWidget.setRowCount(4)





ui.show()
app.exec()

