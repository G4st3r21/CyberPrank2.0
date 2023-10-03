import random

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QPixmap, QTransform, QColor, QBrush, QPen, QFontDatabase, QFont


class LevelTextures:
    @staticmethod
    def draw_background(range_x, range_y):
        bg_textures = []
        for i in range(0, range_y, 48):
            for j in range(0, range_x, 48):
                texture = QPixmap(random.choice([
                    'sprites/tiles/tile_0000.png',
                    'sprites/tiles/tile_0001.png'
                ]))
                texture = texture.scaled(texture.width() * 3, texture.height() * 3)
                bg_textures.append((j, i, texture))

        flower_texture = QPixmap('sprites/tiles/tile_0002.png')
        stone_texture = QPixmap('sprites/tiles/tile_0043.png')
        grass_texture = QPixmap('sprites/tiles/tile_0017.png')
        mushroom_texture = QPixmap('sprites/tiles/tile_0029.png')
        log_texture = QPixmap('sprites/tiles/tile_0106.png')
        LevelTextures.add_layer(bg_textures, flower_texture, (60, 120), range_x, range_y)
        LevelTextures.add_layer(bg_textures, stone_texture, (30, 60), range_x, range_y)
        LevelTextures.add_layer(bg_textures, grass_texture, (25, 50), range_x, range_y)
        LevelTextures.add_layer(bg_textures, mushroom_texture, (25, 50), range_x, range_y)
        LevelTextures.add_layer(bg_textures, log_texture, (5, 10), range_x, range_y)
        # LevelTextures.footpaths_layer(bg_textures)

        return bg_textures

    @staticmethod
    def add_layer(bg_textures, texture, frequency, range_x, range_y):
        texture = texture.scaled(texture.width() * 3, texture.height() * 3)
        for _ in range(random.randrange(*frequency)):
            x, y = random.randrange(0, range_x), random.randrange(0, range_y)
            bg_textures.append((x, y, texture))
            # bg_textures.append((x + 48, y + 48, texture))
            # bg_textures.append((x - 48, y - 48, texture))
            # bg_textures.append((x + 48, y - 48, texture))
            # bg_textures.append((x - 48, y + 48, texture))
            # bg_textures.append((x - 48, y, texture))
            # bg_textures.append((x + 48, y, texture))
            # bg_textures.append((x, y + 48, texture))
            # bg_textures.append((x, y - 48, texture))

    @staticmethod
    def get_OI_effect():
        return "ОЙ", 12

    @staticmethod
    def draw_hero_shadow(x, y, painter):
        ellipse = QRectF(x + 30, y + 100, 68, 40)
        fill_color = QColor(26, 26, 26, 150)
        brush = QBrush(fill_color, Qt.SolidPattern)
        painter.setBrush(brush)
        stroke_color = QColor(26, 26, 26, 150)
        pen = QPen(stroke_color)
        painter.setPen(pen)
        painter.drawEllipse(ellipse)

    @staticmethod
    def paint_effect(effect, painter, game_font_id):
        x, y = effect[-2], effect[-1]
        font_family = QFontDatabase.applicationFontFamilies(game_font_id)[0]
        font = QFont(font_family, 20)

        painter.setFont(font)
        pen = QPen(QColor('black'))
        pen.setWidth(6)
        painter.setPen(pen)
        painter.drawText(x, y, effect[0])

        font = QFont(font_family, 18)
        pen = QPen(QColor('white'))
        pen.setWidth(3)
        painter.setFont(font)
        painter.setPen(pen)
        painter.drawText(x, y, effect[0])
