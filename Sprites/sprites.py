import pygame as pg
from settings import *

pg.init()

screen = pg.display.set_mode(([WIDTH, HEIGHT]))

class SpriteSheet():
    def __init__(self, filename):

        self.spritesheet = pg.image.load(filename).convert()
    def get_image(self, x, y, width, height, scale_x=None, scale_y=None, color_key=None):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x,y, width, height))
        if scale_x and scale_y != None:
            image = pg.transform.scale(image, (width*scale_x, height*scale_y))
        if color_key:
            color = image.get_at((0,0))
            image.set_colorkey(color)
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
        self.wall_sprites = pg.sprite.Group()
        self.x_velo = 5
        self.player_speed = 5
        self.x = 0
        self.y = 0
        self.vx, self.vy = 0, 0

    def update(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.rect.x += -self.player_speed
            self.vy = 0
        elif keys[pg.K_RIGHT]:
            self.rect.x += self.player_speed
            self.vy = 0
        elif keys[pg.K_UP]:
            self.rect.y += -self.player_speed
            self.vx = 0
        elif keys[pg.K_DOWN]:
            self.rect.y += self.player_speed
        self.rect.x += self.vx
        self.collide_with_wall('x')

        # self.rect.y += self.vy
        # self.rect.x += self.x
        # self.rect.y += self.y
        # self.collide_with_wall('y')
       

    def collide_with_wall(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self.game, self.game.wall_sprites, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vy < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self.game, self.game.wall_sprites, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vx = 0
                self.rect.y = self.y
    
    
class Wall(pg.sprite.Sprite):
    def __init__(self, x, y, display, image):
        pg.sprite.Sprite. __init__(self)

        self.self = self
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.display = display
    