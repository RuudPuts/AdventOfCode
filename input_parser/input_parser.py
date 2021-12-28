from abc import ABC, abstractmethod

class InputParser(ABC):
    @abstractmethod
    def parse(self, input):
        pass
