import pico2d
import pygame
from scene_manager import SceneManager


pygame.init()

pico2d.open_canvas(1024, 1024)
scene_manager = SceneManager()

try:
    scene_manager.run()
finally:
    pygame.quit()