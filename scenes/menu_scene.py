import pico2d
from scenes.scene import Scene


class Menu_Scene(Scene):
    def __init__(self):
        self.background = pico2d.load_image('resource/menu_background.png')
        self.start_button = pico2d.load_image('resource/start_button.png')
        self.exit_button = pico2d.load_image('resource/exit_button.png')
        self.start_button_pos = (512, 300)
        self.exit_button_pos = (512, 100)

    def draw(self):
        pico2d.clear_canvas()
        self.background.draw(512, 512)
        self.start_button.draw(*self.start_button_pos)
        self.exit_button.draw(*self.exit_button_pos)
        pico2d.update_canvas()

    def handle_events(self, events):
        for event in events:
            if event.type == pico2d.SDL_QUIT:
                return 'exit'
            elif event.type == pico2d.SDL_MOUSEBUTTONDOWN:
                x, y = event.x, 1024 - event.y
                if self.is_button_clicked(self.start_button_pos, x, y):
                    return 'Game_Scene'
                elif self.is_button_clicked(self.exit_button_pos, x, y):
                    return 'exit'

    def is_button_clicked(self, button_pos, x, y):
        bx, by = button_pos
        return bx - 50 < x < bx + 50 and by - 25 < y < by + 25