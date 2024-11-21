import pico2d
import os
import json
import xml.etree.ElementTree as ET


class TiledMap:
    def __init__(self, file_path):
        with open(file_path, 'r') as f:
            self.data = json.load(f)

        self.tile_width = self.data['tilewidth']
        self.tile_height = self.data['tileheight']
        self.map_width = self.data['width']
        self.map_height = self.data['height']
        tileset = self.data['tilesets'][0]
        self.first_gid = tileset['firstgid']
        tileset_source = os.path.join('Tiled', tileset['source'])
        self.tileset_image = pico2d.load_image(self._parse_tileset(tileset_source))
        self.tileset_columns = self.tileset_image.w // self.tile_width
        self.platforms = self._get_platform_tiles()


    def _parse_tileset(self, tileset_source):
        tree = ET.parse(tileset_source)
        root = tree.getroot()
        image_element = root.find('image')
        return os.path.join('Tiled', image_element.get('source'))

    def _get_platform_tiles(self):
        platforms = []
        for layer in self.data['layers']:
            if layer['type'] == 'tilelayer':
                for y in range(self.map_height):
                    for x in range(self.map_width):
                        tile_index = layer['data'][y * self.map_width + x]
                        if tile_index == 2:
                            left = x * self.tile_width
                            bottom = (self.map_height - y - 1) * self.tile_height
                            right = left + self.tile_width
                            top = bottom + self.tile_height
                            platforms.append((left, bottom, right, top))
        return platforms

    def check_collision_with_player(self, player):
        player_left, player_bottom, player_right, player_top = player.get_collision_box()
        player.is_on_platform = False
        for platform in self.platforms:
            platform_left, platform_bottom, platform_right, platform_top = platform
            if player.vertical_velocity > 0 and player_bottom < platform_top:
                continue
            if player_bottom <= platform_top and player_top > platform_top and \
                    player_left < platform_right and player_right > platform_left:
                player.y = platform_top + player.height // 2
                player.vertical_velocity = 0
                player.is_jumping = False
                player.is_on_platform = True
                break

    def draw(self):
        for layer in self.data['layers']:
            if layer['type'] == 'tilelayer':
                for y in range(self.map_height):
                    for x in range(self.map_width):
                        tile_index = layer['data'][y * self.map_width + x] - self.first_gid
                        if tile_index < 0:
                            continue

                        tile_x = (tile_index % self.tileset_columns) * self.tile_width
                        tile_y = (tile_index // self.tileset_columns) * self.tile_height
                        self.tileset_image.clip_draw(
                            tile_x, self.tileset_image.h - tile_y - self.tile_height,
                            self.tile_width, self.tile_height,
                            x * self.tile_width + self.tile_width // 2,
                            (self.map_height - y - 1) * self.tile_height + self.tile_height // 2
                        )
                        if layer['data'][y * self.map_width + x] == 2:
                            left = x * self.tile_width
                            bottom = (self.map_height - y - 1) * self.tile_height
                            right = left + self.tile_width
                            top = bottom + self.tile_height
                            pico2d.draw_rectangle(left, bottom, right, top)

