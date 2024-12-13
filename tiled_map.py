import pico2d
from utils import resource_path
import os
import json
from save_box import SaveBox
import xml.etree.ElementTree as ET



class TiledMap:

    def __init__(self, filename):
        file_path = resource_path(os.path.join('Tiled', filename))
        try:
            with open(file_path, 'r') as f:
                self.map_data = json.load(f)
        except FileNotFoundError:
            print(f"Cannot find the map file: {file_path}")
            raise

        self.tile_width = self.map_data['tilewidth']
        self.tile_height = self.map_data['tileheight']
        self.map_width = self.map_data['width']
        self.map_height = self.map_data['height']

        self.tilesets = self._load_tilesets()
        self.platforms = self._get_platform_tiles()


    def _load_tilesets(self):
        tilesets = []
        for tileset in self.map_data['tilesets']:
            first_gid = tileset['firstgid']
            tileset_source = tileset['source']
            tileset_info = self._parse_tileset(os.path.join('Tiled', tileset_source))

            tileset_image = pico2d.load_image(resource_path(os.path.join('Tiled', tileset_info['image'])))
            columns = (tileset_image.w - tileset_info['margin'] * 2) // (self.tile_width + tileset_info['spacing'])

            tilesets.append({
                "first_gid": first_gid,
                "image": tileset_image,
                "columns": columns,
                "margin": tileset_info['margin'],
                "spacing": tileset_info['spacing']
            })
        return tilesets

    def _create_save_boxes(self):
        # 맵에 직접 SaveBox를 배치합니다.
        # 예시: Stage1과 Stage2에 각각 SaveBox를 생성
        save_boxes = []
        if "Stage1.json" in self.map_data['filename']:
            save_boxes.append(SaveBox(100, 200, 50, 50))
        if "Stage2.json" in self.map_data['filename']:
            save_boxes.append(SaveBox(300, 400, 50, 50))

        return save_boxes

    def check_bullet_collision_with_save_tile(self, bullet):
        for save_box in self.save_boxes:
            tile_left, tile_bottom, tile_right, tile_top = save_box.get_collision_box()
            bullet_left, bullet_bottom, bullet_right, bullet_top = bullet.get_collision_box()

            # 충돌 처리
            if (
                    bullet_right > tile_left and
                    bullet_left < tile_right and
                    bullet_top > tile_bottom and
                    bullet_bottom < tile_top
            ):
                print("Collision detected with SaveBox.")
                self.save_game_state()  # 저장 기능 호출
                return True  # 충돌 발생
        return False

    def _parse_tileset(self, tileset_source):
        tileset_path = resource_path(tileset_source)
        try:
            tree = ET.parse(tileset_path)
            root = tree.getroot()
            image_element = root.find('image')
            margin = int(root.get('margin', 0))
            spacing = int(root.get('spacing', 0))

            return {
                "image": image_element.get('source'),
                "margin": margin,
                "spacing": spacing
            }
        except FileNotFoundError:
            print(f"Cannot find the tileset file: {tileset_path}")
            raise

    def _get_platform_tiles(self):
        platforms = []
        for layer in self.map_data['layers']:
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

    def _get_tileset_for_gid(self, gid):
        # GID에 해당하는 타일셋 반환
        for tileset in reversed(self.tilesets):
            if gid >= tileset['first_gid']:
                return tileset
        return None

    def check_horizontal_collision(self, player):
        player_left, player_bottom, player_right, player_top = player.get_collision_box()

        for platform in self.platforms:
            p_left, p_bottom, p_right, p_top = platform

            # 수평 충돌은 플레이어의 높이가 플랫폼 범위 안에 있고,
            # 수평 방향으로 겹쳤을 때 처리
            if player_top > p_bottom and player_bottom < p_top:
                # 왼쪽 벽 충돌
                if player_right > p_left and player_left < p_left:
                    player.x = p_left - player.width // 2
                # 오른쪽 벽 충돌
                elif player_left < p_right and player_right > p_right:
                    player.x = p_right + player.width // 2

    def check_vertical_collision(self, player):
        player_left, player_bottom, player_right, player_top = player.get_collision_box()
        player.is_on_platform = False

        for platform in self.platforms:
            p_left, p_bottom, p_right, p_top = platform

            # 수직 충돌 처리 (발 아래/위)
            # 바닥 충돌
            if player_bottom <= p_top <= player_top and player.vertical_velocity <= 0 and player_right > p_left and player_left < p_right:
                player.y = p_top + player.height // 2
                player.vertical_velocity = 0
                player.is_on_platform = True
            # 천장 충돌
            if p_bottom <= player_top <= p_top and player.vertical_velocity > 0 and player_right > p_left and player_left < p_right:
                player.y = p_bottom - player.height // 2
                player.vertical_velocity = 0

    def draw(self):
        for layer in self.map_data['layers']:
            if layer['type'] == 'tilelayer':
                for y in range(self.map_height):
                    for x in range(self.map_width):
                        gid = layer['data'][y * self.map_width + x]
                        if gid == 0:
                            continue

                        tileset = self._get_tileset_for_gid(gid)
                        if not tileset:
                            continue

                        tile_id = gid - tileset['first_gid']
                        margin = tileset['margin']
                        spacing = tileset['spacing']
                        columns = tileset['columns']

                        tile_x = margin + (tile_id % columns) * (self.tile_width + spacing)
                        tile_y = margin + (tile_id // columns) * (self.tile_height + spacing)

                        tileset["image"].clip_draw(
                            tile_x, tileset["image"].h - tile_y - self.tile_height,
                            self.tile_width, self.tile_height,
                            x * self.tile_width + self.tile_width // 2,
                            (self.map_height - y - 1) * self.tile_height + self.tile_height // 2
                        )


