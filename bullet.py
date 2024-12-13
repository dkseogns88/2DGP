import pico2d
from utils import resource_path

class Bullet:
    def __init__(self, x, y, direction, speed=10):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.image = pico2d.load_image(resource_path('resource/player_bullet.png'))
        self.width = 20
        self.height = 20
        self.active = True

    def update(self):
        self.x += self.speed * self.direction
        if self.x < 0 or self.x > 1024:
            self.active = False

    def draw(self):
        if self.active:
            self.image.draw(self.x, self.y, self.width, self.height)

    def get_collision_box(self):
        left = self.x - self.width // 2
        bottom = self.y - self.height // 2
        right = self.x + self.width // 2
        top = self.y + self.height // 2
        return left, bottom, right, top
