import pico2d
class Trap:
    def __init__(self, trap_tile_gid, x, y):
        self.trap_tile_gid = trap_tile_gid
        self.x = x
        self.y = y
        self.active = True
        self.width = 32
        self.height = 32

    def check_player_collision(self, player, tiled_map):
        player_left, player_bottom, player_right, player_top = player.get_collision_box()
        trap_left, trap_bottom, trap_right, trap_top = self.get_collision_box()

        collision = not (
                player_right < trap_left or
                player_left > trap_right or
                player_top < trap_bottom or
                player_bottom > trap_top
        )
        if collision:
            self.active = False
        return collision

    def get_collision_box(self):
        size = 32  # 트랩 크기
        return (
            self.x - size // 2,
            self.y - size // 2,
            self.x + size // 2,
            self.y + size // 2
        )

    def draw(self):
        if self.active:
            pico2d.draw_rectangle(
                self.x - 16, self.y - 16,
                self.x + 16, self.y + 16
            )
