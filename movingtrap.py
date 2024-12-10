from trap import Trap
import pico2d
class MovingTrap(Trap):
    def __init__(self, trap_tile_gid, x, y, direction, speed):
        super().__init__(trap_tile_gid, x, y)
        self.direction = direction
        self.speed = speed
        self.active = True

    def update(self, dt, screen_width, screen_height):
        if self.direction == "up":
            self.y += self.speed * dt
        elif self.direction == "down":
            self.y -= self.speed * dt
        elif self.direction == "left":
            self.x -= self.speed * dt
        elif self.direction == "right":
            self.x += self.speed * dt

        # 화면 밖으로 나가면 비활성화
        if (
            self.x < 0 or
            self.x > screen_width or
            self.y < 0 or
            self.y > screen_height
        ):
            self.active = False

    def draw(self):
        pico2d.draw_rectangle(
            self.x - 16, self.y - 16,
            self.x + 16, self.y + 16
        )
