#!/usr/bin/env python3

import importlib
import inspect
import os
import re
import sys
import time
import argparse

def list_years():
    regex = re.compile(r"20[1|2]\d")

    return list(filter(regex.match, os.listdir('.')))

def find_year_module(year: int):
    module = importlib.import_module(str(year))
    importlib.reload(module)

    return module

def list_days(year_module):
    days = []
    for _, obj in inspect.getmembers(year_module):
        if inspect.isclass(obj):
            days.append(obj)

    return sorted(days, key=lambda x: int(str(x).split('.')[-2][3:]))

def find_day_class(year: int, day: int):
    year_module = find_year_module(year)
    return getattr(year_module, f"Day{day}", None)

def run_day(day_class):
    day = day_class()
    print(f"Day {day.number} - {day.title}")
    day.test()

if __name__ == "__main__":
    def parse_arguments():
        parser = argparse.ArgumentParser(description='Advent of Code CLI')
        parser.add_argument('command', choices=['run'], help='Command to run')
        parser.add_argument('year', nargs='?', type=int, help='Year to run')
        parser.add_argument('day', nargs='?', type=int, help='Day to run')

        args = parser.parse_args()

        if args.command == 'observe':
            if args.year is None or args.day is None:
                parser.error("The 'observe' command requires both year and day arguments.")
        return args

    args = parse_arguments()
    print(f"Command: {args.command}, Year: {args.year}, Day: {args.day}")

    year = args.year
    day = args.day

    if year and day:

        print(f"Advent of Code {year} - Day {day}")
        run_day(find_day_class(year, day))
    else:
        if year:
            years = [year]
        else:
            years = list_years()

        for year in years:
            print()
            print("Advent of Code " + year)

            year_module = importlib.import_module(year)

            for day_class in list_days(year_module):
                print("")

                run_day(day_class)

            print()
            print()