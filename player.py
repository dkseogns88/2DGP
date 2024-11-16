import pico2d

class Player:
    def __init__(self):
        self.image = pico2d.load_image('resource/Character_nonbg.png')
        self.x = 512
        self.y = 384
        self.speed = 2
        self.key_state = {
            pico2d.SDLK_LEFT: False,
            pico2d.SDLK_RIGHT: False,
            pico2d.SDLK_UP: False,
            pico2d.SDLK_DOWN: False
        }

    def update(self):
        if self.key_state[pico2d.SDLK_LEFT]:
            self.x -= self.speed
        if self.key_state[pico2d.SDLK_RIGHT]:
            self.x += self.speed
        if self.key_state[pico2d.SDLK_UP]:
            self.y += self.speed
        if self.key_state[pico2d.SDLK_DOWN]:
            self.y -= self.speed

    def handle_events(self, events):
        for event in events:
            if event.type == pico2d.SDL_KEYDOWN:
                if event.key in self.key_state:
                    self.key_state[event.key] = True
            elif event.type == pico2d.SDL_KEYUP:
                if event.key in self.key_state:
                    self.key_state[event.key] = False

    def draw(self):
        self.image.clip_draw(
            0, self.image.h - 80,
            100, 80,
            self.x, self.y
        )
