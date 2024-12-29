#!/usr/bin/env python3

import importlib
import inspect
import os
import re
import sys
import time
import argparse

from file_change_observer import FileChangeObserver

def list_years():
    regex = re.compile(r"20[1|2]\d")

    return list(filter(regex.match, os.listdir('.')))


def list_days(year_module):
    days = []
    for _, obj in inspect.getmembers(year_module):
        if inspect.isclass(obj):
            days.append(obj)

    return sorted(days, key=lambda x: int(str(x).split('.')[-2][3:]))

def find_day_class(year: int, day: int):
    year_module = importlib.import_module(str(year))
    for day_class in list_days(year_module):
        if str(day_class).endswith(f"Day{day}'>"):
            return day_class

    return None


def run_day(day_class):
    day = day_class()
    print(f"Day {day.number} - {day.title}")

    # if day.tests:
    #     print("  Running tests")
    day.test()

    # task1_start = time.perf_counter()
    # task1_input = day.input_parser.parse(day.read_input())
    # task1_result = day.task1(task1_input)
    # task1_end = time.perf_counter()
    # task1_duration = task1_end - task1_start
    # print(f"  Task 1: {task1_result} (took {task1_duration * 1000:0.4f}ms)")

    # task2_start = time.perf_counter()
    # task2_input = day.input_parser.parse(day.read_input())
    # task2_result = day.task2(task2_input)
    # task2_end = time.perf_counter()
    # task2_duration = task2_end - task2_start
    # print(f"  Task 2: {task2_result} (took {task2_duration * 1000:0.4f}ms)")


# Define a CLI argument parser. The first argumnet is a command to run. Either 'run' or 'observe'.
# The second argument is the year to run. The third argument is the day to run.
# If the command is 'observe', the year and day arguments are required.
# If the command is 'run', the year and day arugments are optional.




if __name__ == "__main__":
    def parse_arguments():
        parser = argparse.ArgumentParser(description='Advent of Code CLI')
        parser.add_argument('command', choices=['run', 'observe'], help='Command to run')
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

    if args.command == 'observe':
        print("Advent of Code " + str(year))

        file_to_monitor = f"{year}/day{day}.py"

        def on_day_file_change():
            os.system('cls' if os.name == 'nt' else 'clear')
            run_day(find_day_class(year, day))

        observer = FileChangeObserver(file_to_monitor, lambda: on_day_file_change)
        observer.start()

        run_day(find_day_class(year, day))
        try:
        # Keep the program running to monitor changes
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            # Stop monitoring on user interrupt
            observer.stop()
    else:
        if year and day:
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