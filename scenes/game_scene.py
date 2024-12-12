import pico2d
import pygame
import os
from scenes.scene import Scene
from scenes.back_scene import Back_Scene
from tiled_map import TiledMap
from player import Player
from enemy import Enemy
from behavior_tree import BehaviorTree
from save import Save
from load import Load
from trap import Trap
from movingtrap import MovingTrap
from trigger import Trigger

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 1024

class Game_Scene(Scene):
    def __init__(self, saved_data=None):
        self.back_scene = Back_Scene()
        self.back_scene.start_music()
        self.map = TiledMap('Tiled/Stage1.json')
        self.player = Player()
        self.enemies = []
        self.traps = []
        self.save_instance = Save(self.player, self.enemies, self.traps)
        self.load_instance = Load(self.player, self.enemies,self)
        self.game_over = False
        self.skip_collision_check = False
        self.trap_images = {
            'up': pico2d.load_image('resource/movingtrap_up.png'),
            'down': pico2d.load_image('resource/movingtrap_down.png'),
            'left': pico2d.load_image('resource/movingtrap_left.png'),
            'right': pico2d.load_image('resource/movingtrap_right.png')
        }



        self.init_new_game()


    def enter(self):
        print("[Game_Scene] Entered Game_Scene")

    def exit(self):
        print("[Game_Scene] Exiting Game_Scene")
        if self.back_scene:
            self.back_scene.stop_music()
            self.back_scene = None
        self.enemies.clear()
        self.map = None

    def setup(self):
        map_left = 0
        map_right = self.map.map_width * self.map.tile_width

        map_center_x = (self.map.map_width * self.map.tile_width) // 2
        map_center_y = (self.map.map_height * self.map.tile_height) // 2
        enemy = Enemy(map_center_x, map_center_y)
        enemy.behavior_tree = BehaviorTree(enemy, (map_left, map_right))
        self.enemies.append(enemy)
        def active_trap():
            if self.traps:
                self.traps[0].triggered = True

        # 트리거 생성
        self.triggers = []
        trigger = Trigger(80,80,40,40,active_trap)
        self.triggers.append(trigger)

        # 타일맵 스캔
        for layer in self.map.data['layers']:
            if layer['type'] == 'tilelayer':
                for y in range(self.map.map_height):
                    for x in range(self.map.map_width):
                        gid = layer['data'][y * self.map.map_width + x]

                        if gid == 105:
                            # 정적 함정 위치 계산
                            tile_x = x * self.map.tile_width + self.map.tile_width // 2
                            tile_y = (self.map.map_height - y - 1) * self.map.tile_height + self.map.tile_height // 2
                            # 정적 함정 객체 생성
                            static_trap = Trap(gid, tile_x, tile_y)
                            self.traps.append(static_trap)
                            # 타일맵에서는 제거하지 않음 -> 타일맵이 그대로 그림

                        elif gid == 123:
                            # MovingTrap 기존 로직
                            tile_x = x * self.map.tile_width + self.map.tile_width // 2
                            tile_y = (self.map.map_height - y - 1) * self.map.tile_height + self.map.tile_height // 2

                            direction = "up"
                            speed = 150

                            moving_trap = MovingTrap(gid, tile_x, tile_y, direction, speed, self.moving_trap_image)
                            self.traps.append(moving_trap)
                            # MovingTrap은 맵에서 제거해 타일맵이 그리지 않도록 함
                            layer['data'][y * self.map.map_width + x] = 0


    def init_new_game(self):
        # 새로운 게임 시작 시 기본 설정
        self.player.x = 30
        self.player.y = 1000
        self.player.vertical_velocity = 0
        self.player.is_jumping = False

        # 리스트 초기화
        self.enemies = []
        self.traps = []

        # 맵, 적, 함정 등을 세팅
        self.setup()
        trap_positions = [
            (500, 300, 'up', 150),
            (330, 1000, 'down', 50),
            (700, 500, 'left', 100),
            (800, 200, 'right', 200)
        ]

        for (x, y, direction, speed) in trap_positions:
            image = self.trap_images[direction]
            moving_trap = MovingTrap(None, x, y, direction, speed, image)
            self.traps.append(moving_trap)


    def check_collision(self, obj1, obj2):
        left1, bottom1, right1, top1 = obj1.get_collision_box()
        left2, bottom2, right2, top2 = obj2.get_collision_box()

        return not (right1 < left2 or left1 > right2 or top1 < bottom2 or bottom1 > top2)

    def update(self):
        if self.skip_collision_check:
            self.skip_collision_check = False  # 첫 프레임만 스킵
            return
        self.player.update(self.map)
        self.player.handle_events(pico2d.get_events(),
                                  save_instance=self.save_instance,
                                  load_instance=self.load_instance)
        self.map.check_vertical_collision(self.player)
        self.map.check_horizontal_collision(self.player)

        self.player.clamp_position(SCREEN_WIDTH, SCREEN_HEIGHT)

        # 트리거 체크
        for trig in self.triggers:
            trig.check_activation(self.player)

        dt = 1 / 60  # FPS 기준
        # 트랩 업데이트 및 충돌 체크
        for trap in self.traps:
            if isinstance(trap, MovingTrap):
                # 여기서 MovingTrap의 위치 업데이트 복원
                trap.update(dt, self.map.map_width * self.map.tile_width,
                            self.map.map_height * self.map.tile_height, self.player)

            if trap.check_player_collision(self.player, self.map):
                print("[Game_Scene] Player hit a trap. Triggering GameOver.")
                self.game_over = True
                return 'GameOver_Scene'

        # 비활성화된 트랩 제거
        self.traps = [trap for trap in self.traps if trap.active]

        # 플레이어의 총알과 Save 타일 충돌 체크
        for bullet in self.player.bullets:
            if self.map.check_bullet_collision_with_save_tile(bullet):
                print("[Game_Scene] Bullet hit Save tile. Saving game state.")
                self.save_instance.save_state()
                bullet.active = False  # 충돌한 총알 비활성화

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
        for trap in self.traps:
            if isinstance(trap, MovingTrap):
                trap.draw()

        pico2d.update_canvas()

    def cleanup_save_file(self):
        save_file = "save_state.json"
        if os.path.exists(save_file):
            os.remove(save_file)
            print(f"[Game_Scene] Save file '{save_file}' deleted.")
        else:
            print(f"[Game_Scene] No save file to delete.")

    def handle_events(self, events):
        if self.game_over:
            return 'GameOver_Scene'

        for event in events:
            if event.type == pico2d.SDL_QUIT:
                self.delete_save_on_exit = True  # 종료 시 세이브 파일 삭제
                self.back_scene.stop_music()
                return 'exit'
            elif event.type == pico2d.SDL_KEYDOWN:
                if event.key == pico2d.SDLK_ESCAPE:
                    self.delete_save_on_exit = True  # 메뉴로 나갈 때 세이브 파일 삭제
                    self.back_scene.stop_music()
                    return 'Menu_Scene'

        self.player.handle_events(events)

    def __del__(self):
        # 게임 종료 시 세이브 파일 삭제를 조건부로 설정
        save_file = "save_state.json"
        if hasattr(self, 'delete_save_on_exit') and self.delete_save_on_exit:
            if os.path.exists(save_file):
                os.remove(save_file)
                print(f"[Game_Scene] Save file '{save_file}' deleted.")
            else:
                print(f"[Game_Scene] No save file to delete.")
        if hasattr(self, 'back_scene') and self.back_scene:
            try:
                self.back_scene.stop_music()
            except Exception as e:
                print(f"[Debug] Error stopping music in __del__: {e}")
