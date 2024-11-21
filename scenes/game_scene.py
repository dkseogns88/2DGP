import pico2d
import pygame
from scenes.scene import Scene
from scenes.back_scene import Back_Scene
from tiled_map import TiledMap
from player import Player
from enemy import Enemy
from behavior_tree import BehaviorTree


class Game_Scene(Scene):
    def __init__(self):
        self.back_scene = Back_Scene()
        self.back_scene.start_music()
        self.map = TiledMap('Tiled/Stage1.json')
        self.player = Player()
        self.enemies = []
        self.game_over = False
        self.setup()

    def setup(self):
        map_left = 0
        map_right = self.map.map_width * self.map.tile_width

        map_center_x = (self.map.map_width * self.map.tile_width) // 2
        map_center_y = (self.map.map_height * self.map.tile_height) // 2
        enemy = Enemy(map_center_x, map_center_y)
        enemy.behavior_tree = BehaviorTree(enemy, (map_left, map_right))
        self.enemies.append(enemy)

    def enter(self):
        print("[Game_Scene] Entered Game_Scene")

    def exit(self):
        print("[Game_Scene] Exiting Game_Scene")
        if self.back_scene:
            self.back_scene.stop_music()
            self.back_scene = None
        self.enemies.clear()
        self.map = None

    def check_collision(self, obj1, obj2):
        left1, bottom1, right1, top1 = obj1.get_collision_box()
        left2, bottom2, right2, top2 = obj2.get_collision_box()

        return not (right1 < left2 or left1 > right2 or top1 < bottom2 or bottom1 > top2)

    def update(self):
        self.player.update()
        self.map.check_collision_with_player(self.player)

        # 플레이어와 적 충돌 체크
        for enemy in self.enemies:
            if self.check_collision(self.player, enemy):
                print("[Game_Scene] Player collided with Enemy. Triggering GameOver.")
                self.game_over = True
                return 'GameOver_Scene'

            # 적 행동 업데이트
            enemy.behavior_tree.update()
            enemy.update(self.map.platforms)

        # 플레이어 총알과 적 충돌 체크
        for bullet in self.player.bullets:
            for enemy in self.enemies:
                if self.check_collision(bullet, enemy):
                    print("[Game_Scene] Bullet hit Enemy!")
                    bullet.active = False
                    self.enemies.remove(enemy)
                    break

        # 비활성화된 적 제거
        self.enemies = [enemy for enemy in self.enemies if enemy]

    def draw(self):
        pico2d.clear_canvas()
        self.map.draw()
        self.player.draw()

        for enemy in self.enemies:
            enemy.draw()

        pico2d.update_canvas()

    def handle_events(self, events):
        if self.game_over:
            return 'GameOver_Scene'

        for event in events:
            if event.type == pico2d.SDL_QUIT:
                self.back_scene.stop_music()
                return 'exit'
            elif event.type == pico2d.SDL_KEYDOWN:
                if event.key == pico2d.SDLK_ESCAPE:
                    self.back_scene.stop_music()
                    return 'Menu_Scene'
                elif event.key == pico2d.SDLK_y:
                    print("[Debug] GameOver triggered")
                    self.back_scene.stop_music()
                    return 'GameOver_Scene'
        self.player.handle_events(events)

    def __del__(self):
        if hasattr(self, 'back_scene') and self.back_scene:
            try:
                self.back_scene.stop_music()
            except Exception as e:
                print(f"[Debug] Error stopping music in __del__: {e}")
