import pico2d
from utils import resource_path
import pygame
import json
import os
from scenes.scene import Scene
from scenes.back_scene import Back_Scene
from tiled_map import TiledMap
from player import Player
from bullet import Bullet
from save_box import SaveBox
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

}

# 스테이지별 Enemy 데이터
STAGE_ENEMIES = {
    1: [
        {"x": 200, "y": 40},
        {"x": 400, "y": 40},
    ],
    2: [

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
        {"x": 80, "y": 18, "direction": "up", "speed": 500},

    ],


}

class Game_Scene(Scene):
    def __init__(self, saved_data=None, stage=1):
        self.back_scene = Back_Scene()
        self.back_scene.start_music()
        self.stage = stage
        self.map = TiledMap(f'Stage{self.stage}.json')
        self.save_boxes = self._create_save_boxes()
        self.player = Player(self)
        self.enemies = []
        self.traps = []
        self.bullets = []
        self.save_instance = Save(self.player, self.enemies, self.traps, self)
        self.load_instance = Load(self.player, self.enemies, self.traps, self)
        self.game_over = False
        self.skip_collision_check = False
        self.trap_images = {
            'up': pico2d.load_image(resource_path('resource/movingtrap_up.png')),
            'down': pico2d.load_image(resource_path('resource/movingtrap_down.png')),
            'left': pico2d.load_image(resource_path('resource/movingtrap_left.png')),
            'right': pico2d.load_image(resource_path('resource/movingtrap_right.png'))
        }
        self.load_stage_data()
        self.init_new_game()

    def _create_save_boxes(self):
        # 각 스테이지에 맞는 SaveBox 객체를 생성합니다.
        save_boxes = []
        if self.stage == 1:
            save_boxes.append(SaveBox(280, 900, 32, 32))
        elif self.stage == 2:
            save_boxes.append(SaveBox(300, 400, 32, 32))
            # 추가 스테이지에 따라 SaveBox를 더 추가할 수 있습니다.
        return save_boxes

    def update_save_boxes(self):
        self.save_boxes = self._create_save_boxes()

    def load_stage_data(self):
        # 현재 파일의 디렉토리를 기준으로 'Tiled' 폴더 경로 설정
        base_dir = os.path.dirname(os.path.abspath(__file__))
        tiled_dir = os.path.join(base_dir, '..', 'Tiled')  # Adjust if necessary

        stage_file = f'Stage{self.stage}.json'
        stage_file_path = os.path.join(tiled_dir, stage_file)

        if not os.path.exists(stage_file_path):
            print(f"Error: '{stage_file_path}' does not exist.")
            self.stages_data = {}
            return

        with open(stage_file_path, 'r') as f:
            self.stages_data = json.load(f)
        print(f"Loaded stage data from '{stage_file_path}'")

        # 맵 재로드
        self.map = TiledMap(stage_file_path)
        print(f"Map reloaded for Stage {self.stage}")


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
        for layer in self.map.map_data['layers']:
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

        initial_positions = {
            1: (30, 1000),
            2: (10, 50),
            3: (10, 50),
        }
        self.player.x, self.player.y = initial_positions.get(self.stage, (30, 1000))
        self.player.vertical_velocity = 0
        self.player.is_jumping = False

        # 리스트 초기화
        self.enemies = []
        self.traps = []

        # 맵, 적, 함정 등을 세팅
        self.setup()

    def save_game_state(self):
        # Save 클래스의 save_state 메서드 호출
        self.save_instance.save_state()
        print("Game state saved via Save instance.")



    def check_collision(self, obj1, obj2):
        left1, bottom1, right1, top1 = obj1.get_collision_box()
        left2, bottom2, right2, top2 = obj2.get_collision_box()

        return not (right1 < left2 or left1 > right2 or top1 < bottom2 or bottom1 > top2)

    def update(self):
        for bullet in self.bullets:
            bullet.update()
        self.bullets = [bullet for bullet in self.bullets if bullet.active]

        for bullet in self.bullets:
            if self.check_bullet_collision_with_save_boxes(bullet):
                bullet.active = False

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
        for bullet in self.bullets:
            for enemy in self.enemies:
                if self.check_collision(bullet, enemy):
                    print("[Game_Scene] Bullet hit Enemy!")
                    bullet.active = False
                    self.enemies.remove(enemy)
                    break

        # 비활성화된 적 제거
        self.enemies = [enemy for enemy in self.enemies if enemy]

    def check_bullet_collision_with_save_boxes(self, bullet):
        for save_box in self.save_boxes:
            tile_left, tile_bottom, tile_right, tile_top = save_box.get_collision_box()
            bullet_left, bullet_bottom, bullet_right, bullet_top = bullet.get_collision_box()

            print(f"Checking collision with SaveBox at ({save_box.x}, {save_box.y})")
            print(f"Tile boundaries: left={tile_left}, right={tile_right}, bottom={tile_bottom}, top={tile_top}")
            print(
                f"Bullet boundaries: left={bullet_left}, right={bullet_right}, bottom={bullet_bottom}, top={bullet_top}")

            # 충돌 처리
            if (
                    bullet_right > tile_left and
                    bullet_left < tile_right and
                    bullet_top > tile_bottom and
                    bullet_bottom < tile_top
            ):
                print("Collision detected with SaveBox.")
                self.save_game_state()
                return True  # 충돌 발생
        return False

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
        self.map = TiledMap(f'Stage{self.stage}.json')
        self.enemies = []
        self.traps = []
        self.save_instance = Save(self.player, self.enemies, self.traps, self)
        self.load_instance = Load(self.player, self.enemies, self.traps, self)

        # 새로운 스테이지 초기화
        self.init_new_game()

        # SceneManager에 스테이지 전환을 알리기 위해 'Game_Scene'을 반환
        return f'Game_Scene:{self.stage}'

    def draw(self):
        pico2d.clear_canvas()
        self.map.draw()
        self.player.draw()

        for save_box in self.save_boxes:
            save_box.draw()
        for bullet in self.bullets:
            bullet.draw()
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
                elif event.key == pico2d.SDLK_n:
                    self.player.x = 0
                    self.player.y = 50
                    return self.transfer_next_stage()

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
