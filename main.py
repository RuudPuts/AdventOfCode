#!/usr/bin/env python3

import importlib
import inspect
import os
import re
import sys
import time

def list_years():
    regex = re.compile(r"20[1|2]\d")

    return list(filter(regex.match, os.listdir('.')))

def list_days(year_module):
    days = []
    for _, obj in inspect.getmembers(year_module):
        if inspect.isclass(obj):
            days.append(obj)

    return days

def run_day(day_class):
    day = day_class()
    print("Day %s - %s" % (day.number(), day.title()))
    day_input = day.read_input()

    task1_start = time.time()
    task1_result = day.task1(day_input)
    task1_end = time.time()
    task1_duration = task1_end - task1_start
    print("  Task 1: %s (took %fms)" % (str(task1_result), task1_duration))

    task2_start = time.time()
    task2_result = day.task2(day_input)
    task2_end = time.time()
    task2_duration = task2_end - task2_start
    print("  Task 2: %s (took %fms)" % (str(task2_result), task2_duration))

if __name__ == "__main__":
    if len(sys.argv) == 3:
        year = sys.argv[1]
        day = sys.argv[2]

        print("Advent of Code " + year)

        year_module = importlib.import_module(year)
        for day_class in list_days(year_module):
            if "Day%s" % day in str(day_class):
                run_day(day_class)
    else:
        years = list_years()

        for year in years:
            print("Advent of Code " + year)

            year_module = importlib.import_module(year)

            for day_class in list_days(year_module):
                print("")

                run_day(day_class)