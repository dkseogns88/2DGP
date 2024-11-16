import pico2d

from scenes.menu_scene import Menu_Scene
from scenes.back_scene import Back_Scene
from scenes.game_scene import Game_Scene

class SceneManager:
    def __init__(self):
        self.current_scene = Menu_Scene()
        self.current_scene.enter()

    def change_scene(self, scene_name):
        self.current_scene.exit()
        if scene_name == 'Menu_Scene':
            self.current_scene = Menu_Scene()
        elif scene_name == 'Back_Scene':
            self.current_scene = Back_Scene()
        elif scene_name == 'Game_Scene':
            self.current_scene = Game_Scene()
        elif scene_name == 'exit':
            pico2d.close_canvas()
            exit()
        self.current_scene.enter()

    def run(self):
        while True:
            events = pico2d.get_events()
            scene_change = self.current_scene.handle_events(events)
            if scene_change:
                self.change_scene(scene_change)
            self.current_scene.update()
            self.current_scene.draw()