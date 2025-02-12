import pygame as pg
import random
from settings import *

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
    def __init__(self, display, left, right, up, down, x, y, game):# left_img, right_img):
        pg.sprite.Sprite.__init__(self)
        self.display = display

        self.game = game
        self.vx = 0
        self.vy = 0
        self.player_speed = 5
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.image = self.down[0]
        self.rect = self.image.get_rect()
        self.rect.x = x     
        self.rect.y = y 
        self.current_frame = 0
        self.delay = 70
        self.last = pg.time.get_ticks()

        self.run = None # -1 is left and 1 is right
        # self.left = left_img
        # self.right = right_img

    def update(self):
        keys = pg.key.get_pressed()
        self.vx, self.vy = 0, 0  

        if keys[pg.K_LEFT]:
            self.now = pg.time.get_ticks()
            if self.now - self.last > self.delay:
                self.current_frame = (self.current_frame + 1) % len(self.left)
                self.image = self.left[self.current_frame]
                self.last = self.now
            self.vx = -self.player_speed
            self.run = -1

        elif keys[pg.K_RIGHT]:
            self.now = pg.time.get_ticks()
            if self.now - self.last > self.delay:
                self.current_frame = (self.current_frame +1) % len(self.right)
                self.image = self.right[self.current_frame]
                self.last = self.now
            self.vx = self.player_speed
            self.run = 1
       
        if keys[pg.K_UP]:
            self.now = pg.time.get_ticks()
            if self.now - self.last > self.delay:
                self.current_frame = (self.current_frame +1) % len(self.up)
                self.image = self.up[self.current_frame]
                self.last = self.now
            self.vy = -self.player_speed
            self.run = -2
       
        elif keys[pg.K_DOWN]:
            self.now = pg.time.get_ticks()
            if self.now - self.last > self.delay:
                self.current_frame = (self.current_frame +1) % len(self.down)
                self.image = self.down[self.current_frame]
                self.last = self.now
            self.vy = self.player_speed
            self.run = 2


        elif self.vx == 0 and self.vy == 0:
            self.vx = 0
            if self.run == -1:
                self.image = self.left[0]
            elif self.run == 1:
                self.image = self.right[0]
            elif self.run == 2:
                self.image = self.down[0]
            elif self.run == -2:
                self.image = self.up[0]
            self.run = None
     

        self.rect.x += self.vx
        self.collide_with_obj()
        self.collide_with_wall('x')

        self.rect.y += self.vy
        self.collide_with_wall('y')
        self.collide_with_obj()

    def collide_with_wall(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.wall_group, False)
            if hits:
                if self.vx > 0:  
                    self.rect.right = hits[0].rect.left
                elif self.vx < 0:  
                    self.rect.left = hits[0].rect.right
        elif dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.wall_group, False)
            if hits:
                if self.vy > 0:  
                    self.rect.bottom = hits[0].rect.top
                elif self.vy < 0:  
                    self.rect.top = hits[0].rect.bottom


    def collide_with_obj(self):
        hits = pg.sprite.spritecollide(self, self.game.coin_group, True)

class Wall(pg.sprite.Sprite):
    def __init__(self, x, y, display, image):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.display = display


class Tile(pg.sprite.Sprite):
    def __init__(self, x, y, display, image, image_list):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.display = display
        self.list = image_list
        self.last = pg.time.get_ticks()
    def update(self):
            self.current_frame = (self.current_frame + 1) % len(self.list)
            self.image = self.current_frame


class Enemy(pg.sprite.Sprite):
    def __init__(self, display, left, right, up, down, x, y, game):
        pg.sprite.Sprite.__init__(self)
        self.display = display

        self.game = game
        self.vx = 0
        self.vy = 0
        self.velo = 2
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.image = self.right[0]
        self.rect = self.image.get_rect()
        self.rect.x = x     
        self.rect.y = y 
        self.current_frame = 0
        self.delay = 70
        self.last = pg.time.get_ticks()
        self.run = None
    def update(self):
        self.now = pg.time.get_ticks
        if MAP_HEIGHT > self.rect.x:
            if self.now - self.last > self.delay:
                    self.current_frame = (self.current_frame +1) % len(self.right)
                    self.image = self.right[self.current_frame]
                    self.last = self.now
            self.run = 1
            self.rect.x += self.velo

        elif self.vx == 0 and self.vy == 0:
            self.vx = 0
            if self.run == 1:
                self.image = self.right[0]
        else:
            self.velo = 0


class Object(pg.sprite.Sprite):
    def __init__(self, display, x, y, img):
        pg.sprite.Sprite.__init__(self)
        self = self
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.display = display

class Bullet(pg.sprite.Sprite):
    def __init__(self, player):
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
    def get_view(self, sprite_object):
        # all sprite object will be moved on camera position
        return sprite_object.rect.move(self.camera.topleft)
    def update(self, target):
        # shift map in opp direction
        # add half window size
        x = -target.rect.x + WIDTH//2
        y = -target.rect.y + HEIGHT//2

        # stop scrolling at end of the tilemap
        # if the target moves too far left, or up, make x/y stay = 0
        x = min(0, x)
        y = min(0, y)
        # if the target moves too far right or down make the target
        # at the width of the tilemap minus the of the window
        x = max(-1 * (self.width - WIDTH), x)
        y = max(-1 * (self.height - HEIGHT), y)
        self.camera = pg.Rect(x, y, self.width, self.height)
