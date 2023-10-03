import random

from PyQt5.QtCore import QUrl, QRectF
from PyQt5.QtGui import QFontDatabase, QPixmap, QPainter
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from game.logic.graphics.Camera import Camera
from game.logic.graphics.LevelTextures import LevelTextures
from game.logic.gui.HUD import HUD
from game.logic.objects.entities.Bullet import Bullet
from game.logic.objects.entities.Hero import Hero
from game.logic.objects.entities.Zombie import Zombie
from game.logic.objects.guns.AssaultRifle import AssaultRifle
from game.logic.objects.guns.Pistol import Pistol
from game.logic.objects.guns.ShootGun import ShootGun


# TODO: ЛОГИКА ПРОХОЖДЕНИЯ

class MainGame:
    def __init__(self):
        self.hero = Hero(1000, 1000)
        self.game_wave = 0
        self.score = 0
        self.alive_zombies = 0
        self.game_font_id = QFontDatabase.addApplicationFont('sprites/fonts/19453.otf')
        self.map_range = 2500, 2500
        self.bg_pixmap: [QPixmap, None] = None
        self.background = []
        self.animated_objects = []
        self.effects = []
        self.bullets = []
        self.garbage = []
        self.camera = Camera(self.hero.x, self.hero.y, self.map_range)

        self.object_init()
        self.sound_init()
        self.background_init()

    def background_init(self):
        self.bg_pixmap = QPixmap(*self.map_range)
        self.background = LevelTextures.draw_background(*self.map_range)
        painter = QPainter(self.bg_pixmap)

        for bg_texture in self.background:
            painter.drawPixmap(bg_texture[0], bg_texture[1], bg_texture[-1])

        painter.end()

    def object_init(self):
        self.animated_objects.append([self.hero, 1])
        self.animated_objects.append([self.hero.current_gun, 2])
        for gun in self.hero.inventory:
            if [gun, 2] not in self.animated_objects:
                self.animated_objects.append([gun, 2])

    def update_wave(self):
        self.hero.hp = 100
        self.game_wave += 1
        for _ in range(random.randrange(2 * self.game_wave, 5 * self.game_wave)):
            self.animated_objects.append(
                [
                    Zombie(
                        random.randrange(0, self.map_range[0]),
                        random.randrange(0, self.map_range[1]),
                        self.game_wave
                    )
                    , 3
                ]
            )
            self.alive_zombies += 1
            self.animated_objects.sort(key=lambda x: x[-1])

    def sound_init(self):
        player = QMediaPlayer()

        player.setMedia(QMediaContent(QUrl.fromLocalFile('audio/fighting/purple_shade.wav')))

        player.play()

        if player.state() == QMediaPlayer.StoppedState:
            print(player.errorString())

    def update(self, mouse_pos):
        if not self.alive_zombies:
            self.update_wave()
        for effect in self.effects:
            if effect[1] == 0:
                self.garbage.append(effect)
        for bullet in self.bullets:
            bullet.update()
            if not bullet.active:
                self.garbage.append(bullet)
        for anim_object in self.animated_objects:
            obj = anim_object[0]
            if type(obj) == Zombie:
                obj.hero_coords = (self.hero.x, self.hero.y)
            if type(obj) in [Pistol, AssaultRifle, ShootGun]:
                for bullet in obj.bullets:
                    if bullet not in self.bullets:
                        self.bullets.append(bullet)

            if type(obj) == Hero:
                obj.set_mouse_pos(*mouse_pos)
                self.hero.current_gun.mouse_pos = mouse_pos

            obj.update()

        self.hero.current_gun.change_coordinate(
            self.hero.x,
            self.hero.y,
            self.hero.current_frame_type[-1]
        )
        self.camera.hero_positions.append([self.hero.x, self.hero.y])
        self.camera.update()

    def collect_garbage(self):
        for animated_object in self.animated_objects:
            if not animated_object[0].active and type(animated_object[0]) not in [Pistol, AssaultRifle, ShootGun]:
                self.garbage.append(animated_object)
        for garbage in self.garbage:
            if type(garbage) is Bullet and garbage in self.bullets:
                self.bullets.remove(garbage)
            elif type(garbage) is list and garbage in self.animated_objects:
                self.animated_objects.remove(garbage)
                self.alive_zombies -= 1
            else:
                if garbage in self.effects:
                    self.effects.remove(garbage)

        self.garbage.clear()

    def check_collisions(self):
        for animated_sprite in self.animated_objects:
            obj = animated_sprite[0]
            if type(obj) == Zombie:
                if self.hero.rect.intersects(obj.rect):
                    self.hero.hp -= obj.damage

                for bullet in self.bullets:
                    if bullet.rect.intersects(obj.rect):
                        bullet.deactivate()
                        self.garbage.append(bullet)
                        obj.hp -= 10
                        effect_x, effect_y = random.randrange(obj.x - 10, obj.x + 140), \
                            random.randrange(obj.y - 10, obj.y + 10)
                        self.effects.append([*LevelTextures.get_OI_effect(), effect_x, effect_y])

        self.hero.x = 0 if self.hero.x < 0 else self.hero.x
        self.hero.y = 0 if self.hero.y < 0 else self.hero.y
        self.hero.x = self.map_range[0] - 100 if self.hero.x + 100 > self.map_range[0] else self.hero.x
        self.hero.y = self.map_range[1] - 200 if self.hero.y + 200 > self.map_range[1] else self.hero.y

    def paint_game(self, parent):
        painter = QPainter(parent)
        window: QPixmap = self.bg_pixmap.copy()
        window_painter = QPainter(window)

        self.repaint_objects(window_painter)
        self.paint_effects(window_painter)

        window_painter.end()
        painter.drawPixmap(
            QRectF(0, 0, self.camera.max_x, self.camera.max_y),
            window,
            QRectF(*self.camera.get_top_left_corner(), self.camera.max_x, self.camera.max_y)
        )

    def repaint_objects(self, painter: QPainter):
        for bullet in self.bullets:
            if bullet.active:
                frame = bullet.current_frames[bullet.current_frame]
                image = QPixmap().fromImage(frame.toqimage())
                painter.drawPixmap(bullet.x, bullet.y, image)

        for anim_object in self.animated_objects:
            obj = anim_object[0]
            if obj.active:
                frame = obj.current_frames[obj.current_frame]
                image = QPixmap().fromImage(frame.toqimage())
                if type(obj) in [Hero, Zombie]:
                    LevelTextures.draw_hero_shadow(obj.x, obj.y, painter)
                    HUD.draw_hp(painter, obj)

                painter.drawPixmap(obj.x, obj.y, image)

    def paint_effects(self, painter):
        for effect in self.effects:
            if effect[1] > 0:
                LevelTextures.paint_effect(effect, painter, self.game_font_id)
                effect[1] -= 1
