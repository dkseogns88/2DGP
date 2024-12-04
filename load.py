class Load:
    def __init__(self, player, enemies):
        self.player = player
        self.enemies = enemies

    def load_state(self, save_data):
        if save_data is None:
            print("No save data available.")
            return

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
