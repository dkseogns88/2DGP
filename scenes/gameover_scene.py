import pico2d
import pygame


class GameOverScene:
    def __init__(self, game_scene):
        self.game_scene = game_scene

        if not pygame.mixer.get_init():
            pygame.mixer.init()


        self.bg_image = pico2d.load_image('resource/bloodbackground.jpg')
        self.image = pico2d.load_image('resource/gameoverimg.png')
        self.gameover_music = pygame.mixer.Sound('resource/gameover.ogg')
        self.gameover_music.set_volume(0.5)
        self.gameover_music.play(loops=-1)

    def enter(self):
        print("[GameOverScene] Entered GameOverScene")

    def exit(self):
        print("[GameOverScene] Exiting GameOverScene")
        self.gameover_music.stop()


    def draw(self):
        pico2d.clear_canvas()
        if self.game_scene:
            self.game_scene.draw()

        self.bg_image.draw(512, 512,1024,1024)
        self.image.draw(512, 600)
        pico2d.update_canvas()

    def handle_events(self, events):
        for event in events:
            if event.type == pico2d.SDL_QUIT:
                return 'exit'

            elif event.type == pico2d.SDL_KEYDOWN:
                if event.key == pico2d.SDLK_r:
                    return 'Game_Scene'

    def update(self):
        pass

    def __del__(self):
        self.gameover_music.stop()
        pygame.mixer.quit()


