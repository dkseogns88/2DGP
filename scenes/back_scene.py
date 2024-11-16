import pygame

class Back_Scene:
    def __init__(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self.background_music = pygame.mixer.Sound('resource/megaman.ogg')
        self.effect_sound = pygame.mixer.Sound('resource/what.ogg')
        self.background_music.set_volume(0.5)

    def start_music(self):
        self.background_music.play(loops=-1)

    def stop_music(self):
        self.background_music.stop()

    def play_effect(self):
        self.effect_sound.play()