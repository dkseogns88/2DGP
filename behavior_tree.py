import random
import time


class BehaviorTree:
    def __init__(self, enemy, map_bounds):
        self.enemy = enemy
        self.map_bounds = map_bounds
        self.last_action_time = time.time()
        self.action_interval = 3.0
        self.current_action = None
        self.movement_range = (1, 1)
        self.state = 'idle'
        self.move_end_time = None

    def update(self):
        current_time = time.time()
        if self.state == 'idle':
            if current_time - self.last_action_time >= self.action_interval:
                self.decide_next_action()
                self.last_action_time = current_time
                self.state = 'moving'
                self.move_end_time = current_time + 0.5

        elif self.state == 'moving':
            move_amount = random.randint(*self.movement_range)
            if self.current_action == 'move_left':
                next_position = self.enemy.x - move_amount
                if next_position < self.map_bounds[0]:
                    self.current_action = 'move_right'
                    self.enemy.direction = 1
                else:
                    self.enemy.x = next_position
                    self.enemy.direction = -1

            elif self.current_action == 'move_right':
                next_position = self.enemy.x + move_amount
                if next_position > self.map_bounds[1]:
                    self.current_action = 'move_left'
                    self.enemy.direction = -1
                else:
                    self.enemy.x = next_position
                    self.enemy.direction = 1
            if current_time >= self.move_end_time:
                self.state = 'idle'


    def decide_next_action(self):
        actions = ['move_left', 'move_right']
        self.current_action = random.choice(actions)

