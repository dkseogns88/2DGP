import json
import os
class Save:
    def __init__(self, player, enemies):
        self.player = player
        self.enemies = enemies
        self.save_data = None

    def save_state(self):
        # 플레이어 상태 저장
        player_state = {
            "x": self.player.x,
            "y": self.player.y,
            "vertical_velocity": self.player.vertical_velocity,
            "is_jumping": self.player.is_jumping,
        }

        # 적 상태 저장
        enemies_state = [
            {"x": enemy.x, "y": enemy.y, "vertical_velocity": enemy.vertical_velocity}
            for enemy in self.enemies
        ]

        # 데이터 저장
        self.save_data = {
            "player": player_state,
            "enemies": enemies_state,
        }

        # 파일로 저장
        with open("save_state.json", "w") as file:
            json.dump(self.save_data, file)
        print("Game state saved.")

    def get_saved_data(self, save_file="save_state.json"):
        # 파일에서 저장된 데이터 읽기
        if not os.path.exists(save_file):
            print(f"No save file found at {save_file}.")
            return None

        with open(save_file, "r") as file:
            self.save_data = json.load(file)
        print(f"Loaded save data from {save_file}.")
        return self.save_data