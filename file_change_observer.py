from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, file_to_watch, callback):
        self.file_to_watch = file_to_watch
        self.callback = callback

    def on_modified(self, event):
        if event.src_path == self.file_to_watch:
            print(f"File {self.file_to_watch} has been modified!")
            if self.callback:
                self.callback()

class FileChangeObserver:
    def __init__(self, file_path, on_change_callback):
        self.file_path = file_path
        self.on_change_callback = on_change_callback
        self.observer = Observer()

    def start(self):
        event_handler = FileChangeHandler(self.file_path, self.on_change_callback)
        self.observer.schedule(event_handler, path=self.file_path.rsplit('/', 1)[0], recursive=False)
        self.observer.start()
        print(f"Started monitoring {self.file_path}")

    def stop(self):
        self.observer.stop()
        self.observer.join()
        print(f"Stopped monitoring {self.file_path}")