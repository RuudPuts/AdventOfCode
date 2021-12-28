from abc import ABC, abstractmethod
from PIL import Image, ImageDraw


class Drawable(ABC):
    @property
    @abstractmethod
    def filename(self):
        pass

    @property
    @abstractmethod
    def image_size(self):
        pass

    def draw(self):
        image = Image.new("RGB", self.image_size)
        self.draw_with(ImageDraw.Draw(image))
        image.save(f"{self.filename}.png")

    def draw_with(self, draw):
        pass
