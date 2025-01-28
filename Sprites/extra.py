import pygame as pg
from settings import *

# Classes
class SpriteSheet():
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
    def get_image(self, x, y, width, height, scale_x=None, scale_y=None, color_key=None):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        if scale_x and scale_y:
            image = pg.transform.scale(image, (width * scale_x, height * scale_y))
        if color_key:
            image.set_colorkey(color_key)
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, display, x, y, img, game):
        pg.sprite.Sprite.__init__(self)
        self.display = display
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x     
        self.rect.y = y 
        self.game = game
        self.x_velo = 0
        self.y_velo = 0
        self.player_speed = 5

    def update(self):
        keys = pg.key.get_pressed()
        self.x_velo, self.y_velo = 0, 0  # Reset velocity each frame

        if keys[pg.K_LEFT]:
            self.x_velo = -self.player_speed
        elif keys[pg.K_RIGHT]:
            self.x_velo = self.player_speed
        if keys[pg.K_UP]:
            self.y_velo = -self.player_speed
        elif keys[pg.K_DOWN]:
            self.y_velo = self.player_speed

        # Update position with collision handling
        self.rect.x += self.x_velo
        self.collide_with_wall('x')

        self.rect.y += self.y_velo
        self.collide_with_wall('y')

    def collide_with_wall(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.wall_group, False)
            if hits:
                if self.x_velo > 0:  # Moving right
                    self.rect.right = hits[0].rect.left
                elif self.x_velo < 0:  # Moving left
                    self.rect.left = hits[0].rect.right
        elif dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.wall_group, False)
            if hits:
                if self.y_velo > 0:  # Moving down
                    self.rect.bottom = hits[0].rect.top
                elif self.y_velo < 0:  # Moving up
                    self.rect.top = hits[0].rect.bottom

class Wall(pg.sprite.Sprite):
    def __init__(self, x, y, display, image):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.display = display

