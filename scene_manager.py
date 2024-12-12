import pico2d
import pygame

from scenes.menu_scene import Menu_Scene
from scenes.back_scene import Back_Scene
from scenes.game_scene import Game_Scene
from scenes.gameover_scene import GameOverScene
from scenes.game_clear_scene import GameClearScene


class SceneManager:
    def __init__(self):
        self.current_scene = Menu_Scene()
        self.current_scene.enter()

    def change_scene(self, scene_name):
        if self.current_scene:
            self.current_scene.exit()
            del self.current_scene

        # 새로운 씬 생성
        if scene_name.startswith('Game_Scene'):
            parts = scene_name.split(':')
            stage = int(parts[1]) if len(parts) > 1 else 1
            self.current_scene = Game_Scene(stage=stage)
        elif scene_name == 'GameOver_Scene':
            self.current_scene = GameOverScene()
        elif scene_name == 'Menu_Scene':
            self.current_scene = Menu_Scene()
        elif scene_name == 'Back_Scene':
            self.current_scene = Back_Scene()
        elif scene_name == 'GameClear_Scene':
            self.current_scene = GameClearScene()
        elif scene_name == 'Load_Saved_Game':
            from save import Save
            from load import Load
            save = Save(None, None, [])
            saved_data = save.get_saved_data("save_state.json")
            self.current_scene = Game_Scene()
            if saved_data is not None:
                # Load 인스턴스에 Game_Scene을 전달
                self.current_scene.load_instance = Load(
                    self.current_scene.player,
                    self.current_scene.enemies,
                    self.current_scene
                )
                self.current_scene.load_instance.load_state("save_state.json")
            else:
                print("[SceneManager] No save file found. Starting a new game.")
        elif scene_name == 'exit':
            pico2d.close_canvas()
            exit()
        else:
            print(f"[SceneManager] Unknown scene: {scene_name}")
            self.current_scene = Menu_Scene()

        self.current_scene.enter()
        print(f"[SceneManager] Changing scene to: {scene_name}")

    def run(self):
        while self.current_scene:
            events = pico2d.get_events()
            scene_change = self.current_scene.handle_events(events)
            if scene_change:
                self.change_scene(scene_change)
                continue

            update_result = self.current_scene.update()
            if update_result:
                self.change_scene(update_result)
                continue


            self.current_scene.draw()
