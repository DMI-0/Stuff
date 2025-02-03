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
    def __init__(self, display, right, left, x, y, img, game):# left_img, right_img):
        pg.sprite.Sprite.__init__(self)
        self.display = display
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x     
        self.rect.y = y 
        self.game = game
        self.vx = 0
        self.vy = 0
        self.player_speed = 5
        self.x = x
        self.y = y
        self.left = left
        self.right = right
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
                self.current_frame = (self.current_frame +1) % len(self.left)
                self.image = self.left[self.current_frame]
                self.last = self.now
            self.vx = -self.player_speed
            self.x
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
            self.vy = -self.player_speed
        elif keys[pg.K_DOWN]:
            self.vy = self.player_speed

        else:
            self.vx = 0
            if self.run == -1:
                self.image = self.left
            elif self.run == 1:
                self.image = self.right
            self.run = None
     

        self.rect.x += self.vx
        self.collide_with_obj('x')
        self.collide_with_wall('x')

        self.rect.y += self.vy
        # print(f'This is the x: {self.rect.x} and this is the y: {self.rect.y}')
        self.collide_with_wall('y')
        self.collide_with_obj('y')

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
     


    def collide_with_obj(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.obj_group, False)
            if hits:
                self.rect.right = hits[0].rect.left
                self.rect.left = hits[0].rect.right
                hits[0].rect.x = random.randint(64, 600)
                hits[0].rect.y = random.randint(107, 469)
# y 469 and 107
# x 64 600
        elif dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.obj_group, False)
            if hits:
                self.rect.bottom = hits[0].rect.top
                self.rect.top = hits[0].rect.bottom
                hits[0].rect.x = random.randint(64, 600)
                hits[0].rect.y = random.randint(107, 469)
class Wall(pg.sprite.Sprite):
    def __init__(self, x, y, display, image):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.display = display



class Enemy(pg.sprite.Sprite):
    def __init__(self, display, x, y, img, game):
        pg.sprite.Sprite.__init__(self)
        self.display = display
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x     
        self.rect.y = y 
        self.game = game
        self.vx = 0
        self.vy = 0
        self.player_speed = 5
