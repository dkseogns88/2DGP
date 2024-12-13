import json
import os
class Save:
    def __init__(self, player, enemies, traps, game_scene):
        self.player = player
        self.enemies = enemies
        self.traps = traps
        self.game_scene = game_scene
        self.save_data = None

    def save_state(self, save_file="save_state.json"):
        # 플레이어 상태 저장
        player_state = {
            "x": self.player.x,
            "y": self.player.y,
            "vertical_velocity": self.player.vertical_velocity,
            "is_jumping": self.player.is_jumping,
        }

        # 함정 상태 저장
        traps_state = [
            {"x": trap.x, "y": trap.y, "type": trap.__class__.__name__}
            for trap in self.traps
        ]

        # 적 상태 저장
        enemies_state = [
            {"x": enemy.x, "y": enemy.y, "vertical_velocity": enemy.vertical_velocity}
            for enemy in self.enemies
        ]
        stage_state = self.game_scene.stage
        # 데이터 저장
        self.save_data = {
            "stage": stage_state,
            "player": player_state,
            "enemies": enemies_state,
            "traps": traps_state,
        }

        # 파일로 저장
        with open(save_file, "w") as file:
            json.dump(self.save_data, file)
        print("Game state saved.")


    def get_saved_data(self, save_file="save_state.json"):
        if not os.path.exists(save_file):
            print(f"No save file found at {save_file}.")
            return None

        with open(save_file, "r") as file:
            self.save_data = json.load(file)
        print(f"Loaded save data from {save_file}.")
        return self.save_data