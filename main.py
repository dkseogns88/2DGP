import pico2d
from scene_manager import SceneManager

pico2d.open_canvas(1024, 1024)
scene_manager = SceneManager()
scene_manager.run()