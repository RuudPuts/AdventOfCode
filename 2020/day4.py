from day import Day
from input_parser import InputParser

import re

class Day4(Day):
    @property
    def title(self):
        return "Passport Processing"

    @property
    def input_parser(self):
        return PassportParser()

    @property
    def example_input(self):
        return """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm
iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929
hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm
hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""

    @property
    def expected_results(self):
        return {
            "task1_example": 1,
            "task1": 226,
            "task2_example": 1,
            "task2": 160
        }

    def task1(self, input):
        valid_entries, _ = self.validate_passports(input)

        return len(valid_entries)

    def validate_height(self, height):
        if height == '' or (not height.endswith('cm') and not height.endswith('in')):
            return False

        value = int(height[0:-2])

        if height[-2:] == "cm":
            return value >= 150 and value <= 193
        elif height[-2:] == "in":
            return value >= 59 and value <= 76

        return False

    def task2(self, input):
        passports, _ = self.validate_passports(input)

        field_validators = {
            'byr': lambda x: int(x) >= 1920 and int(x) <= 2002,
            'iyr': lambda x: int(x) >= 2010 and int(x) <= 2020,
            'eyr': lambda x: int(x) >= 2020 and int(x) <= 2030,
            'hgt': self.validate_height,
            'hcl': lambda x: re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', x),
            'ecl': lambda x: x in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
            'pid': lambda x: re.search(r'^[0-9]{9}$', x),
        }

        valid_passports = []
        invalid_passports = []

        for passport in passports:
            passport_valid = True
            for key, validator in field_validators.items():
                if not validator(passport[key]):
                    passport_valid = False

            if passport_valid:
                valid_passports.append(passport)
            else:
                invalid_passports.append(passport)

        return len(valid_passports)

    def validate_passports(self, input):
        required_fields = [
            "byr", # (Birth Year)
            "iyr", # (Issue Year)
            "eyr", # (Expiration Year)
            "hgt", # (Height)
            "hcl", # (Hair Color)
            "ecl", # (Eye Color)
            "pid", # (Passport ID)
        ]

        optional_fields = [
            "cid" # (Country ID)
        ]

        valid_entries = []
        invalid_entries = []

        for entry in input:
            keys = list(entry.keys())
            [x for x in optional_fields if x not in keys or keys.remove(x)]

            if len(keys) == len(required_fields):
                valid_entries.append(entry)
            else:
                invalid_entries.append(entry)

        return valid_entries, invalid_entries

class PassportParser(InputParser):
    def parse_entry(self, entry):
        regex = r"(\w{3}):(.*?) "
        matches = re.findall(regex, entry)

        return dict(matches)

    def parse(self, input):
        entries = []
        entry = []
        for line in input:
            if line == '':
                entries.append(' '.join(entry) + " ")
                entry = []
            else:
                entry.append(line)

        entries.append(' '.join(entry) + " ")

        return list(map(self.parse_entry, entries))
