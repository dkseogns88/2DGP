import pico2d
from utils import resource_path
from pico2d import load_image
import pygame
import os

class GameOverScene:
    def __init__(self):
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init()
            except Exception as e:
                print(f"[GameOverScene] Error initializing pygame mixer: {e}")

        self.bg_image = load_image(resource_path('resource/bloodbackground.jpg'))
        self.image = load_image(resource_path('resource/gameoverimg.png'))
        self.gameover_music = pygame.mixer.Sound(resource_path('resource/gameover.ogg'))
        self.gameover_music.set_volume(0.5)
        self.gameover_music.play(loops=-1)

    def enter(self):
        print("[GameOverScene] Entered GameOverScene")

    def exit(self):
        print("[GameOverScene] Exiting GameOverScene")
        self.gameover_music.stop()


    def draw(self):
        pico2d.clear_canvas()


        self.bg_image.draw(512, 512,1024,1024)
        self.image.draw(512, 600)
        pico2d.update_canvas()

    def handle_events(self, events):
        for event in events:
            if event.type == pico2d.SDL_QUIT:
                return 'exit'

            elif event.type == pico2d.SDL_KEYDOWN:
                if event.key == pico2d.SDLK_r:
                    print("[GameOverScene] Restarting from last save.")
                    save_file = "save_state.json"
                    if os.path.exists(save_file):
                        print("[GameOverScene] Save file found. Requesting load to SceneManager.")
                        return 'Load_Saved_Game'
                    else:
                        print("[GameOverScene] No save file found. Restart aborted.")
                        return 'Menu_Scene'
                if event.key == pico2d.SDLK_ESCAPE:
                    return 'Menu_Scene'



    def update(self):
        pass

    def __del__(self):
        try:
            if pygame.mixer.get_init():
                self.gameover_music.stop()
                pygame.mixer.quit()
        except Exception as e:
            print(f"[GameOverScene] Error in __del__: {e}")

