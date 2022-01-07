from dataclasses import dataclass


@dataclass
class StringReader:
    string: str
    offset: int = 0

    def read(self, length):
        data = self.string[self.offset: self.offset + length]
        self.offset += length
        return data
