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
