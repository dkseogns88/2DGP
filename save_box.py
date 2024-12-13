from pico2d import load_image
from utils import resource_path

class SaveBox:
    def __init__(self, x, y, width, height, image_path="resource/Savebox.png"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = load_image(resource_path(image_path))

    def get_collision_box(self):
        return (
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.x + self.width // 2,
            self.y + self.height // 2
        )

    def draw(self):
        self.image.clip_draw(0, 0, self.width, self.height, self.x, self.y)
