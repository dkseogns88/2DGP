import pico2d

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
        self.y = 65
        self.speed = 2

        self.frame_index = 0
        self.frame_count = 0
        self.frame_speed = 20


        self.state = 'idle'
        self.key_state = {
            pico2d.SDLK_LEFT: False,
            pico2d.SDLK_RIGHT: False,
            pico2d.SDLK_UP: False,
            pico2d.SDLK_DOWN: False
        }
        self.scale = 2.0

    def update(self):
        if self.key_state[pico2d.SDLK_LEFT]:
            self.x -= self.speed
            self.state = 'walk'
        elif self.key_state[pico2d.SDLK_RIGHT]:
            self.x += self.speed
            self.state = 'walk'
        elif self.key_state[pico2d.SDLK_UP]:
            self.y += self.speed
            self.state = 'walk'
        elif self.key_state[pico2d.SDLK_DOWN]:
            self.y -= self.speed
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
                if event.key in self.key_state:
                    self.key_state[event.key] = True
            elif event.type == pico2d.SDL_KEYUP:
                if event.key in self.key_state:
                    self.key_state[event.key] = False

    def draw(self):
        draw_width = int(32 * self.scale)
        draw_height = int(32 * self.scale)

        try:
            if self.state == 'idle':
                self.idle_images[self.frame_index].draw(self.x, self.y, draw_width, draw_height)
            elif self.state == 'walk':
                self.walk_images[self.frame_index].draw(self.x, self.y, draw_width, draw_height)
        except IndexError as e:
           self.frame_index = 0