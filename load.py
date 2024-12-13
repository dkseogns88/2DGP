import os
import json
from enemy import Enemy
from trap import Trap
from movingtrap import MovingTrap

class Load:
    def __init__(self, player, enemies, traps, game_scene):
        self.player = player
        self.enemies = enemies
        self.traps = traps
        self.game_scene = game_scene

    def load_state(self, save_file="save_state.json"):
        if not os.path.exists(save_file):
            print("No save file found. Load aborted.")
            return

        try:
            # 저장된 데이터 읽기
            with open(save_file, "r") as file:
                save_data = json.load(file)
        except Exception as e:
            print(f"Error loading save file: {e}")
            return

        #스테이지
        stage_state = save_data.get("stage", 1)
        self.game_scene.stage = stage_state
        print(f"Loaded stage: {stage_state}")
        self.game_scene.load_stage_data()

        self.game_scene.enemies.clear()
        self.game_scene.traps.clear()
        self.game_scene.setup()

        # 플레이어 상태 복구
        player_state = save_data["player"]
        self.player.x = player_state["x"]
        self.player.y = player_state["y"]
        self.player.vertical_velocity = player_state["vertical_velocity"]
        self.player.is_jumping = player_state["is_jumping"]

        # 적 상태 복구
        enemies_state = save_data["enemies"]
        for state in enemies_state:
            enemy = Enemy(x=state["x"], y=state["y"])
            enemy.vertical_velocity = state.get("vertical_velocity", 0)
            self.game_scene.enemies.append(enemy)

            # 함정 상태 복구
            traps_state = save_data.get("traps", [])
            for state in traps_state:
                trap_type = state.get("type", "Trap")
                if trap_type == "MovingTrap":
                    trap = MovingTrap(x=state["x"], y=state["y"], direction="up", speed=500, image=None)  # 필요 시 추가 속성
                else:
                    trap = Trap(x=state["x"], y=state["y"])
                self.game_scene.traps.append(trap)

        # SaveBox 업데이트
        self.game_scene.update_save_boxes()

        print("Game state loaded.")
        self.game_scene.skip_collision_check = True