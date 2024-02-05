import re


class DataValidator:

    def validate_milage(self, milage_str: str):
        pattern = re.compile(r'^[1-9]\d{0,3}$')

        if re.match(pattern, milage_str):
            return True
        return False

    def validate_summ(self, summ_str: str):
        pattern = re.compile(r'^\d{2,4}(,\d{1,2})?$')

        if re.match(pattern, summ_str):
            return True
        return False

    def validate_volume(self, volume_str: str):
        pattern = re.compile(r'^\d{1,2}(,\d{1,2})?$')

        if re.match(pattern, volume_str):
            return True
        return False
