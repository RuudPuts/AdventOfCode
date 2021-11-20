#!/usr/bin/env python3

import importlib
import inspect
import os
import re

def list_years():
    regex = re.compile(r"20[1|2]\d")

    return list(filter(regex.match, os.listdir('.')))

def list_days(year_module):
    days = []
    for _, obj in inspect.getmembers(year_module):
        if inspect.isclass(obj):
            days.append(obj)

    return days

if __name__ == "__main__":
    years = list_years()

    for year in years:
        print("Advent of Code " + year)

        year_module = importlib.import_module(year)

        for day_class in list_days(year_module):
            print("")

            day = day_class()
            print("Day %s - %s" % (day.number(), day.title()))
            day_input = day.read_input()
            print("  Task 1: " + str(day.task1(day_input)))
            print("  Task 2: " + str(day.task2(day_input)))