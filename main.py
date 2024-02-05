from datetime import date

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from ui import Ui_MainWindow
import sys
from data_validator import DataValidator
from json_worker import JsonWorker
from enums.enum_fuel_type import EnumFuelType


class AutoToolApp:
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow)
        self.json_worker = JsonWorker()
        self.validator = DataValidator()
        self.ui.MilageEdit.textEdited.connect(self.get_milage)
        self.ui.SummEdit.textEdited.connect(self.get_sum)
        self.ui.VolumeEdit.textEdited.connect(self.get_volume)
        self.ui.dateEdit.dateChanged.connect(self.update_date)
        self.ui.FuelTypeComboBox.currentIndexChanged.connect(self.update_fuel_type)
        self.ui.AddButton.clicked.connect(self.add_fuel_record)

        self.ui.dateEdit.setDate(QtCore.QDate.currentDate())
        self.update_date()
        self.update_fuel_type()

        self.milage = 0
        self.summ = 0
        self.volume = 0
        self.milage_valid_flag = False
        self.volume_valid_flag = False
        self.summ_valid_flag = False

        self.fuel_json_data = JsonWorker.convert_xlsx_to_json('fuel_data.xlsx')

        MainWindow.show()
        sys.exit(app.exec_())

    def get_milage(self):
        if self.validator.validate_milage(milage_str=self.ui.MilageEdit.text()):
            self.milage = self.ui.MilageEdit.text()
            print('Пробіг: {} км.'.format(self.milage))
            self.milage_valid_flag = True

    def get_sum(self):
        if self.validator.validate_summ(summ_str=self.ui.SummEdit.text()):
            self.summ = self.ui.SummEdit.text()
            print('Сума: {} грн.'.format(self.summ))
            self.summ_valid_flag = True

    def get_volume(self):
        if self.validator.validate_volume(volume_str=self.ui.VolumeEdit.text()):
            self.volume = self.ui.VolumeEdit.text()
            print("Об'єм: {} л.".format(self.volume))
            self.volume_valid_flag = True

    def update_date(self):
        self.date = date(self.ui.dateEdit.date().year(), self.ui.dateEdit.date().month(),
                         self.ui.dateEdit.date().day())
        print('Дата: {}'.format(self.date))

    def update_fuel_type(self):
        self.fuel_type = EnumFuelType(self.ui.FuelTypeComboBox.currentIndex()).name
        print(self.fuel_type)

    def add_fuel_record(self):

        if self.volume_valid_flag and self.summ_valid_flag and self.milage_valid_flag:
            self.fuel_json_data = self.json_worker.add_item_to_json(json_data=self.fuel_json_data,
                                                                    fuel_type=self.fuel_type,
                                                                    milege=self.milage,
                                                                    volume=self.volume,
                                                                    sum=self.summ,
                                                                    date_add=self.date)
            record_count = 0
            for key in self.fuel_json_data.keys():
                record_count += 1
                print('[{}] {}:{}'.format(record_count, key, self.fuel_json_data[key]))


application = AutoToolApp()
