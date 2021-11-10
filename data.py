import logging
import os
import shutil

from PyQt5.QtWidgets import QFileDialog

import dialogs


class CommonMethods:
    def __init__(self):
        # Отримую шлях програми і шлях скріпта
        self.program_path = os.path.abspath(os.curdir)
        self.db_folder_name = 'user_data'
        self.db_folder_path = self.program_path + '\\' + self.db_folder_name
        if not os.path.exists(self.db_folder_path):
            logging.info("створюю папку {}".format(self.db_folder_path))
            os.mkdir(self.db_folder_path)
        else:
            logging.info("Папка {} вже створена".format(self.db_folder_path))


class DataBaseImporter(CommonMethods):
    def __init__(self):
        CommonMethods.__init__(self)

    def import_database(self):
        logging.info("Викликано метод import_database")
        logging.info(self.db_folder_path)
        # Отримую шлях до обраного файлу
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilter("Файл бази даних (*.db)")
        dlg.exec_()
        selected_file_path_name = dlg.selectedFiles()[0]
        logging.info("Шлях до обраного файлу: {}".format(selected_file_path_name))

        # Копіюю файл у папку з програмою
        shutil.copy(selected_file_path_name, self.db_folder_path)
        dialogs.Messages.message_import_success()


class DataBaseExporter(CommonMethods):

    def __init__(self):
        CommonMethods.__init__(self)

    def export_database(self):
        logging.info("Викликано метод export_database")
