import os

class Load:
    def __init__(self, player, enemies):
        self.player = player
        self.enemies = enemies

    def load_state(self, save_file="save_state.json"):
        # 파일 존재 여부 확인
        if not os.path.exists(save_file):
            print("No save file found. Load aborted.")
            return  # 저장 파일이 없으면 아무 작업도 하지 않음
            # 저장된 데이터 읽기
            with open(save_file, "r") as file:
                save_data = json.load(file)

        # 플레이어 상태 복구
        player_state = save_data["player"]
        self.player.x = player_state["x"]
        self.player.y = player_state["y"]
        self.player.vertical_velocity = player_state["vertical_velocity"]
        self.player.is_jumping = player_state["is_jumping"]

        # 적 상태 복구
        enemies_state = save_data["enemies"]
        for enemy, state in zip(self.enemies, enemies_state):
            enemy.x = state["x"]
            enemy.y = state["y"]
            enemy.vertical_velocity = state["vertical_velocity"]

        print("Game state loaded.")
        # 충돌 검사 스킵 플래그 설정
        game_scene = self.player.scene  # Game_Scene 객체를 참조
        game_scene.skip_collision_check = True