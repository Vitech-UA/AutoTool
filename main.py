from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5 import QtSql



app = QtWidgets.QApplication([])
ui = uic.loadUi('ui.ui')

ui.show()
app.exec()

db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName('autotool.db')