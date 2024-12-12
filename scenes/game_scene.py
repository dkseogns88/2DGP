import pico2d
import pygame
import json
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

# 스테이지별 Trap GID 데이터
STAGE_TRAP_GIDS = {
    1: [105, 123, 132, 114],
    2: [65, 74, 83, 92],
    3: [1, 2, 3, 4],
}

# 스테이지별 Enemy 데이터
STAGE_ENEMIES = {
    1: [
        {"x": 200, "y": 40},
        {"x": 400, "y": 40},
    ],
    2: [
        {"x": 300, "y": 400},
        {"x": 600, "y": 700},
        {"x": 800, "y": 600},
    ],
    3: [
        {"x": 500, "y": 800},
    ],
}

# 스테이지별 MovingTrap 데이터
STAGE_TRAPS = {
    1: [
        {"x": 180, "y": 0, "direction": "up", "speed": 600},
        {"x": 17, "y": 785, "direction": "right", "speed": 500},
        {"x": 768, "y": 0, "direction": "up", "speed": 1000},

    ],
    2: [
        {"x": 250, "y": 350, "direction": "down", "speed": 500},
        {"x": 550, "y": 650, "direction": "right", "speed": 500},
    ],
    3: [
        {"x": 450, "y": 750, "direction": "up", "speed": 500},
        {"x": 700, "y": 850, "direction": "left", "speed": 500},
    ],
}

class Game_Scene(Scene):
    def __init__(self, saved_data=None, stage=1):
        self.back_scene = Back_Scene()
        self.back_scene.start_music()
        self.stage = stage
        self.map = TiledMap(f'Tiled/Stage{self.stage}.json')
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
        self.load_stage_data()
        self.init_new_game()

    def load_stage_data(self):
        stage_file = f'Stage{self.stage}.json'
        stage_file_path = os.path.join('Tiled', stage_file)

        if not os.path.exists(stage_file_path):
            print(f"Error: '{stage_file_path}' does not exist.")
            self.stages_data = {}
            return

        with open(stage_file_path, 'r') as f:
            self.stages_data = json.load(f)
        print(f"Loaded stage data from '{stage_file_path}'")

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

        stage_data = self.stages_data


        # 스테이지별 Enemy 생성
        for enemy_data in STAGE_ENEMIES.get(self.stage, []):
            enemy = Enemy(
                x=enemy_data["x"],
                y=enemy_data["y"]
            )
            enemy.behavior_tree = BehaviorTree(enemy, (map_left, map_right))
            self.enemies.append(enemy)

        # 스테이지별 MovingTrap 생성
        for trap_data in STAGE_TRAPS.get(self.stage, []):
            moving_trap = MovingTrap(
                trap_tile_gid=None,
                x=trap_data["x"],
                y=trap_data["y"],
                direction=trap_data["direction"],
                speed=trap_data["speed"],
                image=self.trap_images[trap_data["direction"]]
            )
            self.traps.append(moving_trap)


        def active_trap():
            if self.traps:
                self.traps[0].triggered = True

        # 트리거 생성
        self.triggers = []
        trigger = Trigger(80,80,40,40,active_trap)
        self.triggers.append(trigger)

        # 타일맵 스캔
        trap_gids = STAGE_TRAP_GIDS.get(self.stage, [])
        for layer in self.map.data['layers']:
            if layer['type'] == 'tilelayer':
                for y in range(self.map.map_height):
                    for x in range(self.map.map_width):
                        gid = layer['data'][y * self.map.map_width + x]
                        # 현재 스테이지의 Trap GIDs 확인
                        if gid in trap_gids:
                            tile_x = x * self.map.tile_width + self.map.tile_width // 2
                            tile_y = (self.map.map_height - y - 1) * self.map.tile_height + self.map.tile_height // 2
                            static_trap = Trap(gid, tile_x, tile_y)
                            self.traps.append(static_trap)





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

        print(f"[Game_Scene] Player Position: ({self.player.x}, {self.player.y})")

        self.map.check_vertical_collision(self.player)
        self.map.check_horizontal_collision(self.player)

        self.player.clamp_position(SCREEN_WIDTH, SCREEN_HEIGHT)

        # 트리거 체크
        for trig in self.triggers:
            trig.check_activation(self.player)

        if self.check_next_stage():
            scene_change = self.transfer_next_stage()
            if scene_change:
                return scene_change
            return

        dt = 1 / 60  # FPS 기준
        # 트랩 업데이트 및 충돌 체크
        for trap in self.traps:
            if isinstance(trap, MovingTrap):
                # 여기서 MovingTrap의 위치 업데이트 복원
                trap.update(dt, self.map.map_width * self.map.tile_width,
                            self.map.map_height * self.map.tile_height, self.player)

            if trap.active and trap.check_player_collision(self.player, self.map):
                if isinstance(trap, MovingTrap):
                    print("[Game_Scene] Player hit a MovingTrap. Triggering GameOver.")
                else:
                    print("[Game_Scene] Player hit a static Trap. Triggering GameOver.")
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

    def draw_transition_zone(self):
        transition_zone_width = 50
        transition_zone_height = 50
        map_right = self.map.map_width * self.map.tile_width
        map_bottom = 0

        left = map_right - transition_zone_width
        bottom = map_bottom
        right = map_right
        top = map_bottom + transition_zone_height


        pico2d.draw_rectangle_outline(left, bottom, right, top)

    def check_next_stage(self):
        # 스테이지 전환 포탈 범위
        transition_zone_width = 100
        transition_zone_height = 100

        player_x, player_y = self.player.x, self.player.y

        # 스테이지 전환 포탈 위치
        map_right = self.map.map_width * self.map.tile_width
        map_bottom = 35

        # 플레이어가 범위내에있는지 체크
        if (map_right - transition_zone_width <= player_x <= map_right) and (
                map_bottom <= player_y <= transition_zone_height):
            print(f"[Game_Scene] Player at ({player_x}, {player_y}) reached the transition zone.")
            return True
        return False

    def transfer_next_stage(self):
        self.stage += 1  # 스테이지 번호 증가
        total_stages = 3  # 총 스테이지 수

        if self.stage > total_stages:
            print("[Game_Scene] All stages completed! Triggering GameClear_Scene.")
            # 모든 스테이지 클리어시
            # SceneManager를 통해 'GameClear_Scene'으로 전환하도록 반환
            return 'GameClear_Scene'

        print(f"[Game_Scene] Transitioning to Stage {self.stage}")

        # 현재 스테이지 종료 처리
        self.exit()

        # 새로운 스테이지 로드
        self.map = TiledMap(f'Tiled/Stage{self.stage}.json')
        self.enemies = []
        self.traps = []
        self.save_instance = Save(self.player, self.enemies, self.traps)
        self.load_instance = Load(self.player, self.enemies, self)

        # 새로운 스테이지 초기화
        self.init_new_game()

        # SceneManager에 스테이지 전환을 알리기 위해 'Game_Scene'을 반환
        return f'Game_Scene:{self.stage}'

    def draw(self):
        pico2d.clear_canvas()
        self.map.draw()
        self.player.draw()

        for enemy in self.enemies:
            enemy.draw()
        for trap in self.traps:
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
