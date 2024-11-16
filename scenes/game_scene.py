import pico2d
from scenes.scene import Scene
from scenes.back_scene import Back_Scene
from tiled_map import TiledMap
from player import Player

class Game_Scene(Scene):
    def __init__(self):
        self.back_scene = Back_Scene()
        self.back_scene.start_music()
        self.map = TiledMap('Tiled/Stage1.json')
        self.player = Player()
        self.setup()

    def setup(self):
        pass

    def update(self):
        self.player.update()


    def draw(self):
        pico2d.clear_canvas()
        self.map.draw()
        self.player.draw()
        pico2d.update_canvas()

    def handle_events(self, events):
        for event in events:
            if event.type == pico2d.SDL_QUIT:
                self.back_scene.stop_music()
                return 'exit'
            elif event.type == pico2d.SDL_KEYDOWN:
                if event.key == pico2d.SDLK_ESCAPE:
                    self.back_scene.stop_music()
                    return 'Menu_Scene'
                elif event.key == pico2d.SDLK_SPACE:
                    self.back_scene.play_effect()
        self.player.handle_events(events)



    def __del__(self):
        self.back_scene.stop_music()