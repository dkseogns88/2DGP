import pico2d
import pygame

class Player:
    def __init__(self):
        self.idle_images = [
            pico2d.load_image('resource/playercharacter/Idle1.png'),
            pico2d.load_image('resource/playercharacter/Idle2.png')
        ]

        self.walk_images = [
            pico2d.load_image('resource/playercharacter/Walk1.png'),
            pico2d.load_image('resource/playercharacter/Walk2.png'),
            pico2d.load_image('resource/playercharacter/Walk3.png'),
            pico2d.load_image('resource/playercharacter/Walk4.png'),
            pico2d.load_image('resource/playercharacter/Walk5.png'),
            pico2d.load_image('resource/playercharacter/Walk6.png'),
            pico2d.load_image('resource/playercharacter/Walk7.png'),
            pico2d.load_image('resource/playercharacter/Walk8.png')
        ]

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

        self.frame_index = 0
        self.frame_count = 0
        self.frame_speed = 20

        self.state = 'idle'
        self.key_state = {
            pico2d.SDLK_LEFT: False,
            pico2d.SDLK_RIGHT: False,
        }
        self.scale = 2.0


        self.width = int(20 * self.scale)
        self.height = int(20 * self.scale)

    def update(self):
        if not self.is_on_platform:
            self.vertical_velocity += self.gravity
        self.y += self.vertical_velocity

        # 플랫폼 도달 시 초기화
        if self.is_on_platform and self.vertical_velocity <= 0:
            self.is_jumping = False
            self.jump_count = 0
            self.vertical_velocity = 0

        if self.key_state[pico2d.SDLK_LEFT]:
            self.x -= self.speed
            self.state = 'walk'
        elif self.key_state[pico2d.SDLK_RIGHT]:
            self.x += self.speed
            self.state = 'walk'
        else:
            self.state = 'idle'

        self.frame_count = (self.frame_count + 1) % self.frame_speed
        if self.frame_count == 0:
            if self.state == 'idle':
                self.frame_index = (self.frame_index + 1) % len(self.idle_images)
            elif self.state == 'walk':
                self.frame_index = (self.frame_index + 1) % len(self.walk_images)

    def handle_events(self, events):
        for event in events:
            if event.type == pico2d.SDL_KEYDOWN:
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

        try:
            if self.state == 'idle':
                self.idle_images[self.frame_index].draw(self.x, self.y, draw_width, draw_height)
            elif self.state == 'walk':
                self.walk_images[self.frame_index].draw(self.x, self.y, draw_width, draw_height)
        except IndexError as e:
            self.frame_index = 0



        left, bottom, right, top = self.get_collision_box()
        pico2d.draw_rectangle(left, bottom, right, top)

