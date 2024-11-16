import os
import json
import xml.etree.ElementTree as ET
import pico2d

class TiledMap:
    def __init__(self, file_path):
        print(f"Loading JSON file from: {file_path}")
        with open(file_path, 'r') as f:
            self.data = json.load(f)
        print("JSON data loaded successfully!")


        self.tile_width = self.data['tilewidth']
        self.tile_height = self.data['tileheight']
        self.map_width = self.data['width']
        self.map_height = self.data['height']
        print(f"Map dimensions: {self.map_width}x{self.map_height}, Tile size: {self.tile_width}x{self.tile_height}")


        tileset = self.data['tilesets'][0]
        self.first_gid = tileset['firstgid']
        tileset_source = os.path.join('Tiled', tileset['source'])
        print(f"Loading tileset from: {tileset_source}")
        tileset_image_path = self._parse_tileset(tileset_source)
        print(f"Tileset image path: {tileset_image_path}")


        self.tileset_image = pico2d.load_image(tileset_image_path)
        print("Tileset image loaded successfully!")


        self.tileset_columns = self.tileset_image.w // self.tile_width

    def _parse_tileset(self, tileset_source):

        print(f"Parsing .tsx file: {tileset_source}")
        tree = ET.parse(tileset_source)
        root = tree.getroot()
        image_element = root.find('image')
        image_path = os.path.join('Tiled', image_element.get('source'))
        return image_path

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
