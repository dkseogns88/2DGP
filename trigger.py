class Trigger:
    def __init__(self, x, y, width, height, callback):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.callback = callback
        self.activated = False

    def check_activation(self, player):
        player_left, player_bottom, player_right, player_top = player.get_collision_box()
        trigger_left = self.x
        trigger_bottom = self.y
        trigger_right = self.x + self.width
        trigger_top = self.y + self.height



        if (player_right > trigger_left and
                player_left < trigger_right and
                player_top > trigger_bottom and
                player_bottom < trigger_top and
                not self.activated):
            self.activated = True
            self.callback()
            print("Trigger activated!")