import pico2d
from scenes.scene import Scene
from scenes.back_scene import Back_Scene
from tiled_map import TiledMap
from player import Player
from enemy import Enemy


class Game_Scene(Scene):
    def __init__(self):
        self.back_scene = Back_Scene()
        self.back_scene.start_music()
        self.map = TiledMap('Tiled/Stage1.json')
        self.player = Player()
        self.enemies = []  # 적 캐릭터 리스트
        self.setup()

    def setup(self):
        # 맵 중앙에 적 캐릭터 추가
        map_center_x = (self.map.map_width * self.map.tile_width) // 2
        map_center_y = (self.map.map_height * self.map.tile_height) // 2

        enemy = Enemy(map_center_x, map_center_y)
        self.enemies.append(enemy)

    def update(self):
        # 플레이어 업데이트
        self.player.update()
        self.map.check_collision_with_player(self.player)

        # 적 캐릭터 업데이트
        for enemy in self.enemies:
            enemy.update(self.map.platforms)

    def draw(self):
        pico2d.clear_canvas()
        self.map.draw()
        self.player.draw()

        # 적 캐릭터 그리기
        for enemy in self.enemies:
            enemy.draw()

        pico2d.update_canvas()

    def handle_events(self, events):
        for event in events:
            if event.type == pico2d.SDL_QUIT:
                self.back_scene.stop_music()
                return 'exit'
            elif event.type == pico2d.SDL_KEYDOWN:
                if event.key == pico2d.SDLK_ESCAPE:
                    self.back_scene.stop_music()
                    return 'Menu_Scene'
                elif event.key == pico2d.SDLK_SPACE:
                    self.back_scene.play_effect()
        self.player.handle_events(events)

    def __del__(self):
        self.back_scene.stop_music()
