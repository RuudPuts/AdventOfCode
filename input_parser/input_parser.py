from abc import ABC, abstractmethod

class InputParser(ABC):
    @abstractmethod
    def parse(input):
        pass