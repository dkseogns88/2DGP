import pico2d
import pygame

from scenes.menu_scene import Menu_Scene
from scenes.back_scene import Back_Scene
from scenes.game_scene import Game_Scene
from scenes.gameover_scene import GameOverScene


class SceneManager:
    def __init__(self):
        self.current_scene = Menu_Scene()
        self.previous_scene = None
        self.current_scene.enter()

    def change_scene(self, scene_name):

        if self.current_scene:
            self.current_scene.exit()
            del self.current_scene

        # 새로운 씬 생성
        if scene_name == 'GameOver_Scene':
            self.current_scene = GameOverScene()
        elif scene_name == 'Menu_Scene':
            self.current_scene = Menu_Scene()
            self.previous_scene = None
        elif scene_name == 'Back_Scene':
            self.current_scene = Back_Scene()
        elif scene_name == 'Game_Scene':
            self.current_scene = Game_Scene()
            self.previous_scene = None
        elif scene_name == 'exit':
            pico2d.close_canvas()
            exit()
        elif scene_name == 'Load_Saved_Game':
            from save import Save
            save = Save(None, None)  # 초기화용, load 시 player/enemy 필요없음
            saved_data = save.get_saved_data("save_state.json")
            if saved_data is not None:
                self.current_scene = Game_Scene(saved_data)
                self.previous_scene_name = 'Game_Scene'
                self.previous_scene_data = saved_data
            else:
                self.current_scene = Game_Scene()
                self.previous_scene_name = 'Game_Scene'
                self.previous_scene_data = {}

        # 새로운 씬 초기화
        self.current_scene.enter()
        print(f"[SceneManager] Changing scene to: {scene_name}")

    def run(self):
        while self.current_scene:
            events = pico2d.get_events()
            scene_change = self.current_scene.handle_events(events)
            if scene_change:
                self.change_scene(scene_change)
            self.current_scene.update()
            self.current_scene.draw()
