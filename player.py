import pico2d
import pygame
from bullet import Bullet


class Player:
    def __init__(self):

        self.left_idle_images = [
            pico2d.load_image('resource/playercharacter/left_idle1.png'),
            pico2d.load_image('resource/playercharacter/left_idle2.png')
        ]

        self.left_walk_images = [
            pico2d.load_image('resource/playercharacter/left_walk1.png'),
            pico2d.load_image('resource/playercharacter/left_walk2.png'),
            pico2d.load_image('resource/playercharacter/left_walk3.png'),
            pico2d.load_image('resource/playercharacter/left_walk4.png'),
            pico2d.load_image('resource/playercharacter/left_walk5.png'),
            pico2d.load_image('resource/playercharacter/left_walk6.png'),
            pico2d.load_image('resource/playercharacter/left_walk7.png'),
            pico2d.load_image('resource/playercharacter/left_walk8.png')
        ]


        self.right_idle_images = [
            pico2d.load_image('resource/playercharacter/right_idle1.png'),
            pico2d.load_image('resource/playercharacter/right_idle2.png')
        ]

        self.right_walk_images = [
            pico2d.load_image('resource/playercharacter/right_walk1.png'),
            pico2d.load_image('resource/playercharacter/right_walk2.png'),
            pico2d.load_image('resource/playercharacter/right_walk3.png'),
            pico2d.load_image('resource/playercharacter/right_walk4.png'),
            pico2d.load_image('resource/playercharacter/right_walk5.png'),
            pico2d.load_image('resource/playercharacter/right_walk6.png'),
            pico2d.load_image('resource/playercharacter/right_walk7.png'),
            pico2d.load_image('resource/playercharacter/right_walk8.png')
        ]
        self.bullets = []
        self.screen_width = 1024
        self.screen_height = 1024
        self.x = 10
        self.y = 500
        self.speed = 2

        self.gravity = -0.1
        self.vertical_velocity = 0
        self.jump_power = 5
        self.is_jumping = False
        self.is_on_platform = True
        self.jump_count = 0

        self.jump1_sound = pygame.mixer.Sound('resource/player_jump1.wav')
        self.jump2_sound = pygame.mixer.Sound('resource/player_jump2.wav')
        self.fire_sound = pygame.mixer.Sound('resource/player_fire.wav')

        self.frame_index = 0
        self.frame_count = 0
        self.frame_speed = 20

        self.state = 'idle'
        self.key_state = {
            pico2d.SDLK_LEFT: False,
            pico2d.SDLK_RIGHT: False,
        }
        self.scale = 2.0

        self.last_direction = 1
        self.width = int(20 * self.scale)
        self.height = int(20 * self.scale)

    def update(self):
        if not self.is_on_platform:
            self.vertical_velocity += self.gravity
        self.y += self.vertical_velocity

        if self.is_on_platform and self.vertical_velocity <= 0:
            self.is_jumping = False
            self.jump_count = 0
            self.vertical_velocity = 0

        if self.key_state[pico2d.SDLK_LEFT]:
            self.x -= self.speed
            self.state = 'walk'
            self.last_direction = -1
        elif self.key_state[pico2d.SDLK_RIGHT]:
            self.x += self.speed
            self.state = 'walk'
            self.last_direction = 1
        else:
            self.state = 'idle'

        self.x = max(self.width // 2, min(self.x, self.screen_width - self.width // 2))
        self.y = max(self.height // 2, min(self.y, self.screen_height - self.height // 2))

        self.frame_count = (self.frame_count + 1) % self.frame_speed
        if self.frame_count == 0:
            if self.state == 'idle':
                self.frame_index = (self.frame_index + 1) % len(self.right_idle_images)
            elif self.state == 'walk':
                self.frame_index = (self.frame_index + 1) % len(self.right_walk_images)

        for bullet in self.bullets:
            bullet.update()
        self.bullets = [bullet for bullet in self.bullets if bullet.active]

    def handle_events(self, events):
        for event in events:
            if event.type == pico2d.SDL_KEYDOWN:
                if event.key == pico2d.SDLK_SPACE:
                    self.bullets.append(Bullet(self.x, self.y, self.last_direction))
                    self.fire_sound.play()
                if event.key == pico2d.SDLK_UP:
                    if self.jump_count < 2:
                        if self.jump_count == 0:
                            self.vertical_velocity = self.jump_power
                            self.jump1_sound.play()
                        elif self.jump_count == 1:
                            self.vertical_velocity = self.jump_power * 0.7
                            self.jump2_sound.play()

                        self.is_jumping = True
                        self.is_on_platform = False
                        self.jump_count += 1
                elif event.key in self.key_state:
                    self.key_state[event.key] = True

            elif event.type == pico2d.SDL_KEYUP:
                if event.key in self.key_state:
                    self.key_state[event.key] = False

    def get_collision_box(self):
        left = self.x - self.width // 2
        bottom = self.y - self.height // 2
        right = self.x + self.width // 2
        top = self.y + self.height // 2
        return left, bottom, right, top


    def draw(self):
        draw_width = int(20 * self.scale)
        draw_height = int(20 * self.scale)
        for bullet in self.bullets:
            bullet.draw()

        try:
            if self.last_direction == 1:
                if self.state == 'idle':
                    self.right_idle_images[self.frame_index].draw(self.x, self.y, draw_width, draw_height)
                elif self.state == 'walk':
                    self.right_walk_images[self.frame_index].draw(self.x, self.y, draw_width, draw_height)
            else:
                if self.state == 'idle':
                    self.left_idle_images[self.frame_index].draw(self.x, self.y, draw_width, draw_height)
                elif self.state == 'walk':
                    self.left_walk_images[self.frame_index].draw(self.x, self.y, draw_width, draw_height)
        except IndexError:
            self.frame_index = 0



        left, bottom, right, top = self.get_collision_box()
        pico2d.draw_rectangle(left, bottom, right, top)

