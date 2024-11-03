import pico2d
from scenes.scene import Scene


class FT_Scene(Scene):
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        pico2d.clear_canvas()
        pico2d.update_canvas()

    def handle_events(self, events):
        for event in events:
            if event.type == pico2d.SDL_QUIT:
                return 'exit'
            elif event.type == pico2d.SDL_KEYDOWN:
                if event.key == pico2d.SDLK_ESCAPE:
                    return 'BG_Scene'