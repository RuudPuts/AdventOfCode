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
    print(f"Day {day.number} - {day.title}")

    if day.tests:
        print("  Running tests")
        day.test()

    task1_start = time.perf_counter()
    task1_input = day.input_parser.parse(day.read_input())
    task1_result = day.task1(task1_input)
    task1_end = time.perf_counter()
    task1_duration = task1_end - task1_start
    print(f"  Task 1: {task1_result} (took {task1_duration * 1000:0.4f}ms)")

    task2_start = time.perf_counter()
    task2_input = day.input_parser.parse(day.read_input())
    task2_result = day.task2(task2_input)
    task2_end = time.perf_counter()
    task2_duration = task2_end - task2_start
    print(f"  Task 2: {task2_result} (took {task2_duration * 1000:0.4f}ms)")


if __name__ == "__main__":
    if len(sys.argv) == 3:
        year = sys.argv[1]
        day = sys.argv[2]

        print("Advent of Code " + year)

        year_module = importlib.import_module(year)
        for day_class in list_days(year_module):
            if str(day_class).endswith(f"Day{day}'>"):
                run_day(day_class)
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