from trap import Trap
import pico2d

class MovingTrap(Trap):
    def __init__(self, trap_tile_gid, x, y, direction, speed, image):
        super().__init__(None, x, y)
        self.direction = direction
        self.speed = speed
        self.active = True
        self.image = image
        self.triggered = False

    def update(self, dt, screen_width, screen_height, player):
        # 매 프레임 플레이어와 거리 체크
        dx = abs(player.x - self.x)
        dy = abs(player.y - self.y)


        if self.direction == "up" and dx <= 100:
            self.triggered = True
        elif self.direction == "down" and dx <= 50:
            self.triggered = True
        elif self.direction == "left" and dy <= 50:
            self.triggered = True
        elif self.direction == "right" and dy <= 100:
            self.triggered = True

        # 트리거가 작동시 이동
        if self.triggered:
            move_x = 0
            move_y = 0

            if self.direction == "up":
                move_y = self.speed * dt
            elif self.direction == "down":
                move_y = -self.speed * dt
            elif self.direction == "left":
                move_x = -self.speed * dt
            elif self.direction == "right":
                move_x = self.speed * dt

            self.x += move_x
            self.y += move_y

            # 화면 나가면 비활성화
            if self.x < 0 or self.x > screen_width or self.y < 0 or self.y > screen_height:
                self.active = False

    def draw(self):
        self.image.draw(self.x, self.y)
