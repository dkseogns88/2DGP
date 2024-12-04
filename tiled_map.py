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

        # 여러 타일셋 로드
        self.tilesets = self._load_tilesets()
        self.platforms = self._get_platform_tiles()

    def _load_tilesets(self):
        tilesets = []
        for tileset in self.data['tilesets']:
            first_gid = tileset['firstgid']
            tileset_source = os.path.join('Tiled', tileset['source'])
            tileset_info = self._parse_tileset(tileset_source)

            tileset_image = pico2d.load_image(tileset_info['image'])
            columns = (tileset_image.w - tileset_info['margin'] * 2) // (self.tile_width + tileset_info['spacing'])

            tilesets.append({
                "first_gid": first_gid,
                "image": tileset_image,
                "columns": columns,
                "margin": tileset_info['margin'],
                "spacing": tileset_info['spacing']
            })
        return tilesets

    def check_bullet_collision_with_save_tile(self, bullet):
        for layer in self.data['layers']:
            if layer['type'] == 'tilelayer':
                for y in range(self.map_height):
                    for x in range(self.map_width):
                        gid = layer['data'][y * self.map_width + x]

                        # GID가 49 이상인지 확인
                        if gid >= 49:
                            # 타일셋 범위 계산
                            tile_id = gid - 49  # 49이 `firstgid`인 타일셋의 타일 ID

                            # 충돌 박스 계산
                            tile_left = x * self.tile_width
                            tile_bottom = (self.map_height - y - 1) * self.tile_height
                            tile_right = tile_left + self.tile_width
                            tile_top = tile_bottom + self.tile_height
                            bullet_left, bullet_bottom, bullet_right, bullet_top = bullet.get_collision_box()

                            # 충돌 여부 확인
                            if (
                                    bullet_right > tile_left and
                                    bullet_left < tile_right and
                                    bullet_top > tile_bottom and
                                    bullet_bottom < tile_top
                            ):
                                print("Collision detected with Save tile.")
                                return True  # 충돌 발생
        return False

    def _parse_tileset(self, tileset_source):
        tree = ET.parse(tileset_source)
        root = tree.getroot()
        image_element = root.find('image')
        margin = int(root.get('margin', 0))  # 기본값 0
        spacing = int(root.get('spacing', 0))  # 기본값 0

        return {
            "image": os.path.join('Tiled', image_element.get('source')),
            "margin": margin,
            "spacing": spacing
        }

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

    def _get_tileset_for_gid(self, gid):
        # GID에 해당하는 타일셋 반환
        for tileset in reversed(self.tilesets):
            if gid >= tileset['first_gid']:
                return tileset
        return None

    def check_collision_with_player(self, player):
        # 플레이어의 충돌 박스 가져오기
        player_left, player_bottom, player_right, player_top = player.get_collision_box()
        player.is_on_platform = False  # 플랫폼 위 상태 초기화

        for platform in self.platforms:
            platform_left, platform_bottom, platform_right, platform_top = platform

            # 플랫폼 상단 충돌 처리 (발판 역할)
            if (
                    player_bottom <= platform_top <= player_top  # 플레이어 발이 플랫폼 높이에 접근
                    and player.vertical_velocity <= 0  # 아래로 떨어지는 중
                    and player_right > platform_left
                    and player_left < platform_right
            ):
                # 플레이어를 플랫폼 위에 위치
                player.y = platform_top + player.height // 2
                player.vertical_velocity = 0
                player.is_jumping = False
                player.is_on_platform = True
                continue

            # 플랫폼 하단 충돌 처리 (머리 충돌)
            if (
                    platform_bottom <= player_top <= platform_top  # 플레이어 머리가 플랫폼 하단에 접근
                    and player.vertical_velocity > 0  # 위로 점프 중
                    and player_right > platform_left
                    and player_left < platform_right
            ):

                player.y = platform_bottom - player.height // 2
                player.vertical_velocity = 0
                return

            # X축 충돌 처리
            if (
                    player_top > platform_bottom
                    and player_bottom < platform_top
            ):
                # 왼쪽 벽 충돌
                if player_right > platform_left > player_left:
                    player.x = platform_left - player.width // 2

                # 오른쪽 벽 충돌
                elif player_left < platform_right < player_right:
                    player.x = platform_right + player.width // 2

    def draw(self):
        for layer in self.data['layers']:
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

