#!/usr/bin/env python3

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
from os import system

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, file_to_watch, callback):
        self.file_to_watch = os.path.abspath(file_to_watch)
        self.callback = callback

    def on_modified(self, event):
        print(f"Detected change in: {event.src_path}")  # Debugging log
        if os.path.abspath(event.src_path) == self.file_to_watch:
            print(f"File {self.file_to_watch} has been modified!")
            if self.callback:
                self.callback()

class FileChangeObserver:
    def __init__(self, file_path, on_change_callback):
        self.file_path = os.path.abspath(file_path)
        self.on_change_callback = on_change_callback
        self.observer = Observer()

    def start(self):
        event_handler = FileChangeHandler(self.file_path, self.on_change_callback)
        directory_to_watch = os.path.dirname(self.file_path)
        print(f"Watching directory: {directory_to_watch}")  # Debugging log
        self.observer.schedule(event_handler, path=directory_to_watch, recursive=False)
        self.observer.start()
        print(f"Started monitoring {self.file_path}")

    def stop(self):
        self.observer.stop()
        self.observer.join()
        print(f"Stopped monitoring {self.file_path}")

import sys
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python observer.py <year> <day>")
        sys.exit(1)

    year = sys.argv[1]
    day = sys.argv[2]

    file_to_monitor = f"{year}/day{day}.py"  # Replace with your file path

    # Define a callback function
    def on_file_change():
        print("🔥 File change detected!")
        system(f'python main.py run {year} {day}')

    # Create and start the observer
    observer = FileChangeObserver(file_to_monitor, on_file_change)
    observer.start()
    on_file_change()

    try:
        # Keep the program running to monitor changes
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Stop monitoring on user interrupt
        observer.stop()