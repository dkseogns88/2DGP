import pico2d

from scenes.bg_scene import BG_Scene
from scenes.ft_scene import FT_Scene

class SceneManager:
    def __init__(self):
        self.current_scene = BG_Scene()
        self.current_scene.enter()

    def change_scene(self, scene_name):
        self.current_scene.exit()
        if scene_name == 'BG_Scene':
            self.current_scene = BG_Scene()
        elif scene_name == 'FT_Scene':
            self.current_scene = FT_Scene()
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