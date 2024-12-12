import pico2d
from scenes.scene import Scene

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 1024

class GameClearScene(Scene):
    def enter(self):
        print("[GameClearScene] Entered GameClearScene")

    def exit(self):
        print("[GameClearScene] Exiting GameClearScene")

    def update(self):
        pass

    def draw(self):
        pico2d.clear_canvas()
        pico2d.draw_text(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, "Game Clear!", (255, 255, 255))
        pico2d.update_canvas()


def handle_events(self, events):
        for event in events:
            if event.type == pico2d.SDL_QUIT:
                return 'exit'
            elif event.type == pico2d.SDL_KEYDOWN:
                if event.key == pico2d.SDLK_ESCAPE:
                    return 'Menu_Scene'
        return None
