from day import Day
from input_parser.input_parser import InputParser

import re

class Day4(Day):
    def title(self):
        return "Passport Processing"

    def input_parser(self):
        return PassportParser()

    def task1(self, input):
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

        return len(valid_entries)

    def task2(self, input):
        raise Exception("Task failed")

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
