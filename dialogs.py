from PyQt5.QtWidgets import QMessageBox


class Dialogs:
    def add_success_message():
        """
            Виводить messageBox із переданим повідомленням
            :param msg:
            :return:
            """
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Icon.NoIcon)
        msgBox.setText('Запис успішно додано')
        msgBox.setWindowTitle('Успіх!')
        msgBox.setStandardButtons(QMessageBox.Ok)

        return_value = msgBox.exec()
        if return_value == QMessageBox.Ok:
            print('OK clicked')
