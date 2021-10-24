from PyQt5.QtWidgets import QMessageBox
import logging

"""Клас діалогових вікон"""


def message_add_success():

    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Icon.NoIcon)
    msgBox.setText('Запис успішно додано')
    msgBox.setWindowTitle('Успіх!')
    msgBox.setStandardButtons(QMessageBox.Ok)

    return_value = msgBox.exec()
    if return_value == QMessageBox.Ok:
        print('OK clicked')


class Messages:

    def message(self: str):
        """
        Виводить messageBox із переданим повідомленням
        :param self:
        :return:
        """
        logging.info("show_dialog()")
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(self)
        msgBox.setWindowTitle("Невірні дані")
        msgBox.setStandardButtons(QMessageBox.Ok)
        return_value = msgBox.exec()
        if return_value == QMessageBox.Ok:
            logging.info("Натиснено ОК")
