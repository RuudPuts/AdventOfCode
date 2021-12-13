from utils.ocr.ocr_characters import OCRCharacter


class OCR:
    CHAR_WIDTH = 5
    CHAR_HEIGHT = 6

    def __init__(self, data):
        self.data = data
    
    def text(self):
        if len(self.data) > self.CHAR_HEIGHT:
            raise Exception(f"Invalid row count. expected {self.CHAR_HEIGHT}, got {len(self.data)}!")
        if len(self.data[0]) % self.CHAR_WIDTH != 0:
            raise Exception(f"Invalid length, {len(self.data)} not divisable by {self.CHAR_WIDTH}!")

        result_len = len(self.data[0]) / self.CHAR_WIDTH

        text = []
        while len(text) < result_len:
            character = self.character_at(len(text) * self.CHAR_WIDTH)
            text.append(OCRCharacter.recognize(character))

        return text

    def character_at(self, index):
        return ["".join(x[index: index + self.CHAR_WIDTH]) for x in self.data]