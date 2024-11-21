import pico2d
from behavior_tree import BehaviorTree


class Enemy:
    def __init__(self, x, y, width=32, height=32, gravity=-0.5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.gravity = gravity
        self.vertical_velocity = 0
        self.is_on_platform = False
        self.collision_box_color = (255, 0, 0)
        self.speed = 1
        self.direction = 1
        self.frame_count = 0
        self.frame_index = 0
        self.frame_speed = 20

        self.walk_right_images = [
            pico2d.load_image('resource/enemy/dragon_right_1.png'),
            pico2d.load_image('resource/enemy/dragon_right_2.png')
        ]

        self.walk_left_images = [
            pico2d.load_image('resource/enemy/dragon_left_1.png'),
            pico2d.load_image('resource/enemy/dragon_left_2.png')
        ]

    def update(self, platforms):
        if self.behavior_tree:
            self.behavior_tree.update()

        if not self.is_on_platform:
            self.vertical_velocity += self.gravity
        self.y += self.vertical_velocity

        self.check_collision_with_platforms(platforms)
        self.frame_count = (self.frame_count + 1) % self.frame_speed
        if self.frame_count == 0:
            self.frame_index = (self.frame_index + 1) % len(self.walk_right_images)

    def draw(self):

        if self.direction == 1:
            self.walk_right_images[self.frame_index].draw(self.x, self.y, self.width, self.height)
        elif self.direction == -1:
            self.walk_left_images[self.frame_index].draw(self.x, self.y, self.width, self.height)


        left, bottom, right, top = self.get_collision_box()
        pico2d.draw_rectangle(left, bottom, right, top)

    def check_collision_with_platforms(self, platforms):

        self.is_on_platform = False
        left, bottom, right, top = self.get_collision_box()

        for platform in platforms:
            platform_left, platform_bottom, platform_right, platform_top = platform
            if self.vertical_velocity > 0 and bottom < platform_top:
                continue
            if bottom <= platform_top and top > platform_top and \
                    left < platform_right and right > platform_left:
                self.y = platform_top + self.height // 2
                self.vertical_velocity = 0
                self.is_on_platform = True
                break

    def get_collision_box(self):
        left = self.x - self.width // 2
        bottom = self.y - self.height // 2
        right = self.x + self.width // 2
        top = self.y + self.height // 2
        return left, bottom, right, top
