import pico2d
from utils import resource_path
import pygame
from bullet import Bullet


class Player:
    def __init__(self, game_scene):
        self.game_scene = game_scene
        self.width = 50
        self.height = 50

        self.left_idle_images = [
            pico2d.load_image(resource_path('resource/playercharacter/left_idle1.png')),
            pico2d.load_image(resource_path('resource/playercharacter/left_idle2.png'))
        ]

        self.left_walk_images = [
            pico2d.load_image(resource_path('resource/playercharacter/left_walk1.png')),
            pico2d.load_image(resource_path('resource/playercharacter/left_walk2.png')),
            pico2d.load_image(resource_path('resource/playercharacter/left_walk3.png')),
            pico2d.load_image(resource_path('resource/playercharacter/left_walk4.png')),
            pico2d.load_image(resource_path('resource/playercharacter/left_walk5.png')),
            pico2d.load_image(resource_path('resource/playercharacter/left_walk6.png')),
            pico2d.load_image(resource_path('resource/playercharacter/left_walk7.png')),
            pico2d.load_image(resource_path('resource/playercharacter/left_walk8.png'))
        ]


        self.right_idle_images = [
            pico2d.load_image(resource_path('resource/playercharacter/right_idle1.png')),
            pico2d.load_image(resource_path('resource/playercharacter/right_idle2.png'))
        ]

        self.right_walk_images = [
            pico2d.load_image(resource_path('resource/playercharacter/right_walk1.png')),
            pico2d.load_image(resource_path('resource/playercharacter/right_walk2.png')),
            pico2d.load_image(resource_path('resource/playercharacter/right_walk3.png')),
            pico2d.load_image(resource_path('resource/playercharacter/right_walk4.png')),
            pico2d.load_image(resource_path('resource/playercharacter/right_walk5.png')),
            pico2d.load_image(resource_path('resource/playercharacter/right_walk6.png')),
            pico2d.load_image(resource_path('resource/playercharacter/right_walk7.png')),
            pico2d.load_image(resource_path('resource/playercharacter/right_walk8.png'))
        ]
        self.bullets = []
        self.screen_width = 1024
        self.screen_height = 1024
        self.x = 20
        self.y = 1000
        self.speed = 2

        self.gravity = -0.1
        self.vertical_velocity = 0
        self.jump_power = 6
        self.is_jumping = False
        self.is_on_platform = True
        self.jump_count = 0

        self.jump1_sound = pygame.mixer.Sound(resource_path('resource/player_jump1.wav'))
        self.jump2_sound = pygame.mixer.Sound(resource_path('resource/player_jump2.wav'))
        self.fire_sound = pygame.mixer.Sound(resource_path('resource/player_fire.wav'))

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


    def clamp_position(self, screen_width, screen_height):
        half_width = self.width / 2
        half_height = self.height / 2

        # x축 클램핑
        if self.x < half_width:
            self.x = half_width
        elif self.x > screen_width - half_width:
            self.x = screen_width - half_width

        # y축 클램핑
        if self.y < half_height:
            self.y = half_height
            self.vertical_velocity = 0
            self.is_on_platform = True
        elif self.y > screen_height - half_height:
            self.y = screen_height - half_height
            self.vertical_velocity = 0

    def update(self, tiled_map):
        if not self.is_on_platform:
            self.vertical_velocity += self.gravity

        # x축 이동 처리
        prev_x = self.x
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

        # x축 충돌 체크
        tiled_map.check_horizontal_collision(self)

        prev_y = self.y
        self.y += self.vertical_velocity

        # y축 충돌 체크
        tiled_map.check_vertical_collision(self)

        # 점프 상태 초기화
        if self.is_on_platform:
            self.is_jumping = False
            self.jump_count = 0
            self.vertical_velocity = 0

        # 애니메이션 업데이트
        self.frame_count = (self.frame_count + 1) % self.frame_speed
        if self.frame_count == 0:
            if self.state == 'idle':
                self.frame_index = (self.frame_index + 1) % len(self.right_idle_images)
            elif self.state == 'walk':
                self.frame_index = (self.frame_index + 1) % len(self.right_walk_images)

        # 총알 업데이트
        for bullet in self.bullets:
            bullet.update()
        self.bullets = [bullet for bullet in self.bullets if bullet.active]

    def handle_events(self, events, save_instance=None, load_instance=None):
        for event in events:
            if event.type == pico2d.SDL_KEYDOWN:
                # 저장 키 ([)
                if event.key == pico2d.SDLK_LEFTBRACKET and save_instance:
                    save_instance.save_state()

                # 불러오기 키 (])
                elif event.key == pico2d.SDLK_RIGHTBRACKET and load_instance:
                    save_data = save_instance.get_saved_data()
                    if save_data:
                        load_instance.load_state(save_data)

                # 점프 키 (위쪽 화살표)
                elif event.key == pico2d.SDLK_UP:
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

                # 발사 키 (스페이스바)
                elif event.key == pico2d.SDLK_SPACE:
                    new_bullet = Bullet(self.x, self.y, self.last_direction)
                    self.game_scene.bullets.append(new_bullet)
                    self.fire_sound.play()

                # 이동 키 처리 (왼쪽/오른쪽)
                elif event.key in self.key_state:
                    self.key_state[event.key] = True

            elif event.type == pico2d.SDL_KEYUP:
                if event.key in self.key_state:
                    self.key_state[event.key] = False

    def get_collision_box(self):
        left = self.x - self.width // 3.2
        bottom = self.y - self.height // 2
        right = self.x + self.width // 3.2
        top = self.y + self.height // 3.5
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

