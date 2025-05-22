import pygame as pg
import random
from settings import *


screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)

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

class Tiled_Map(pg.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
    

class Player(pg.sprite.Sprite):
    def __init__(self, display, left, right, x, y, idle, jump, attack, hurt, level_list, game):
        pg.sprite.Sprite.__init__(self)
        self.display = display
        self.level_list = level_list

        self.game = game
        self.vx = 0
        self.vy = 0
        self.player_speed = 3
        self.left = left
        self.right = right
        self.idle = idle
        self.jump = jump
        self.image = self.idle[0]
        self.rect = self.image.get_rect()
        self.hurt = hurt
        self.rect.x = x     
        self.rect.y = y 
        self.x = x
        self.y = y
        self.current_frame = 0
        self.delay = 70
        self.last = pg.time.get_ticks()
        self.HP = True
        self.jumping = False
        self.landed = True
        self.coins = 0
        self.attack = attack
        self.attacking = False
        self.damage = False
        self.restart = False
    


        self.run = None # -1 is left and 1 is right
        # self.left = left_img
        # self.right = right_img

        self.player_mask = pg.mask.from_surface(self.image)
        self.mask_image = self.player_mask.to_surface()

    def update(self):
        keys = pg.key.get_pressed()
        self.vx, self.vy = 0, 0  
        now = pg.time.get_ticks()
        
        if now - self.last > self.delay and not keys[pg.K_LEFT] and not keys[pg.K_RIGHT] and not keys[pg.K_SPACE]:
            self.current_frame = (self.current_frame + 1) % len(self.idle)
            self.image = self.idle[self.current_frame]
            self.last = now

        if keys[pg.K_LEFT] and self.HP == True:
            self.now = pg.time.get_ticks()
            if self.now - self.last > self.delay:
                self.current_frame = (self.current_frame + 1) % len(self.left)
                self.image = self.left[self.current_frame]
                self.last = self.now
            self.vx = -self.player_speed
            self.run = -1

        elif keys[pg.K_RIGHT] and self.HP == True:
            self.now = pg.time.get_ticks()
            if self.now - self.last > self.delay:
                self.current_frame = (self.current_frame +1) % len(self.right)
                self.image = self.right[self.current_frame]
                self.last = self.now
            self.vx = self.player_speed
            self.run = 1
       

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
        
        if keys[pg.K_SPACE] and not self.jumping and self.landed and self.HP == True:
            self.jumping = True
            self.landed = False
            self.now = pg.time.get_ticks()
            if self.now - self.last > self.delay:
                self.current_frame = (self.current_frame + 1) % len(self.jump)
                self.image = self.jump[self.current_frame]
                self.last = self.now
            self.vy = -50
        if not keys[pg.K_SPACE] and self.HP == True:
            self.jumping = False

        if keys[pg.K_w] and not self.jumping and self.landed and self.HP == True:
            self.jumping = True
            self.landed = False

            self.vy = -50
        if not keys[pg.K_w] and self.HP == True:
            self.jumping = False

        if keys[pg.K_UP] and not self.jumping and self.landed and self.HP == True:
            self.jumping = True
            self.landed = False

            self.vy = -50
        if not keys[pg.K_UP] and self.HP == True:
            self.jumping = False


                    # Game
                    # (current_level)

        self.vy += GRAVITY
        if self.vy > 10: # and self.rect.y != 550:
            self.vy = 10         # set terminal velocity
        self.rect.y += self.vy

        self.rect.x += self.vx
        self.rect.y += self.vy
        # print(self.rect.y)
        self.collide_with_wall('x')
        self.collide_with_wall('y')
        self.collide_with_obj()
        self.collide_with_death('y')
        self.collide_with_block('y')
        self.hit()
        self.collide_with_enemy('x')
        self.collide_with_enemy('y')
        self.teleport('x')
        self.teleport('y')

    def hit(self):
        keys = pg.key.get_pressed()
# Start attack animation when key is pressed
        if keys[pg.K_f] and not self.attacking:
            self.attacking = True
            self.current_frame = 0
            self.last = pg.time.get_ticks()
            self.image = self.attack[self.current_frame]

# Update animation if attacking
        if self.attacking:
            self.now = pg.time.get_ticks()
            if self.now - self.last > self.delay:
                self.current_frame += 1
                if self.current_frame >= len(self.attack):
                    self.attacking = False  # Stop animating when done
                else:
                    self.image = self.attack[self.current_frame]
                    self.last = self.now

    def collide_with_wall(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.stop_group, False)
            if hits:
                if self.vx > 0:  
                    self.rect.right = hits[0].rect.left
                elif self.vx < 0:  
                    self.rect.left = hits[0].rect.right
   
   
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.wall_group, False)
            if hits:
                if self.vy > 0:  
                    self.rect.bottom = hits[0].rect.top
                    self.landed = True
                    self.jumping = False
                # elif self.vy < 0:  
                #     self.rect.top = hits[0].rect.bottom
                #     self.landed = True
                #     self.jumping = False

    def collide_with_obj(self):
        hits = pg.sprite.spritecollide(self, self.game.coin_group, True)
        self.coins += 1
  
    def collide_with_death(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.death_zone, False)
            if hits:
                if self.vx > 0:  
                    self.rect.right = hits[0].rect.left
                    self.HP = False
                elif self.vx < 0:  
                    self.rect.left = hits[0].rect.right
                    self.HP = False
      
        elif dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.death_zone, False)
            if hits:
                if self.vy > 0:  
                    self.rect.bottom = hits[0].rect.top
                    self.HP = False
                elif self.vy < 0:  
                    self.rect.top = hits[0].rect.bottom
                    self.HP = False

    def collide_with_block(self, dir):
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.move_sprites, False)
            if hits:
                if self.vy > 0:  
                    self.rect.bottom = hits[0].rect.top
                    self.rect.x += hits[0].rect.x
                    # pg.quit()
                elif self.vy < 0:  
                    self.rect.top = hits[0].rect.bottom
                    # pg.quit()
                    self.rect.x += hits[0].rect.x

    def collide_with_enemy(self, dir):
        if dir == 'x':
            enemy = pg.sprite.spritecollide(self, self.game.enemy_group, False)
            if enemy:
                if enemy[0].rect.colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height):
                    if self.vy >= 0:
                        self.player_speed = enemy[0].rect.top - self.rect.bottom
                        self.landed = True
                        self.jumping = False
                        self.vy = 0
                        self.HP = False

                    # if player is going up
                    elif self.vy < 0:
                        self.player_speed = enemy[0].rect.bottom - self.rect.top
                        self.y_velo = 0
                        self.HP = False


                    # self.now = pg.time.get_ticks()
                    # if self.now - self.last > self.delay:
                    #     self.current_frame = (self.current_frame + 1) % len(self.hurt)
                    #     self.image = self.hurt[self.current_frame]
                    #     self.last = self.now
                if enemy[0].rect.colliderect(self.rect.x + self.player_speed, self.rect.y, self.rect.width, self.rect.height):
                    self.player_speed = 0
                    self.HP = False


        if dir == 'y':
            enemy = pg.sprite.spritecollide(self, self.game.enemy_group, False)
            if enemy:
                if self.vy > 0:  
                    self.HP = False
                elif self.vy < 0:  
                    self.HP = False

    def teleport(self, dir):
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.wall_group, False)
            if hits:
                if self.vy > 0:  
                    self.rect.bottom = hits[0].rect.top
                    self.landed = True
                    self.jumping = False
                # elif self.vy < 0:  
                #     self.rect.top = hits[0].rect.bottom
                #     self.landed = True
                #     self.jumping = False

        # if dir == 'x':
        #     hits = pg.sprite.spritecollide(self, self.game.level_group, False)
        #     if hits:
        #         if self.vx > 0:  
        #             index += 1
        #             if current_level < len(map_list):
        #                 current_level = map_list[index]
        #         elif self.vx < 0:  
        #             index += 1
        #             if current_level < len(map_list):
        #                 current_level = map_list[index]        
        # elif dir == 'y':
        #     hits = pg.sprite.spritecollide(self, self.game.level_group, False)
        #     if hits:
        #         if self.vy > 0:  
        #             index += 1
        #             if current_level < len(map_list):
        #                 current_level = map_list[index]
        #         elif self.vy < 0:  
        #             index += 1
        #             if current_level < len(map_list):
        #                 current_level = map_list[index]
    



class Wall(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([width, height])
        # self.image.fill(BLUE)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Enemy(pg.sprite.Sprite):
    def __init__(self, display, left, right, up, down, x, y, game):
        pg.sprite.Sprite.__init__(self)
        self.display = display

        self.game = game
        self.vx = 0
        self.vy = 0
        self.velo = 1
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
        # self.x_move = random.randint(340, 400)
        self.pos = 0
        self.x = x
        self.y = y
        self.range = 100
        self.Damage = 25
        self.HP = 2

    def update(self):
        self.move_left = self.x 
        self.move_right = self.x + self.range
        self.rect.x += -self.velo
        if self.rect.x <= self.move_left:
            self.run = 1 
            self.velo = -2
        self.now = pg.time.get_ticks()
        if self.now - self.last > self.delay and self.velo == -2:
            self.current_frame = (self.current_frame +1) % len(self.right)
            self.image = self.right[self.current_frame]
            self.last = self.now
        if self.rect.x >= self.move_right:
            self.run = -1
            self.velo = 2
        self.now = pg.time.get_ticks()
        if self.now - self.last > self.delay and self.velo == 2:
            self.current_frame = (self.current_frame +1) % len(self.left)
            self.image = self.left[self.current_frame]
            self.last = self.now
        self.rect.x += self.vx

        self.vy += GRAVITY
        if self.vy > 10: # and self.rect.y != 550:
            self.vy = 10         # set terminal velocity
        self.collide_with_wall('x')

        self.rect.y += self.vy
        self.collide_with_wall('y')

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

class Reverse_Enemy(pg.sprite.Sprite):
    def __init__(self, display, left, right, up, down, x, y, game):
        pg.sprite.Sprite.__init__(self)
        self.display = display

        self.game = game
        self.vx = 0
        self.vy = 0
        self.velo = 1
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
        # self.x_move = random.randint(340, 400)
        self.pos = 0
        self.x = x
        self.y = y
        self.range = 100
        self.Damage = 25
        self.HP = 2

    def update(self):
        self.move_right = self.x        
        self.move_left = self.x + self.range  

        
        self.rect.x += self.velo

       
        if self.rect.x >= self.move_left:
            self.run = -1
            self.velo = -2  
        elif self.rect.x <= self.move_right:
            self.run = 1
            self.velo = 2   

        
        self.now = pg.time.get_ticks()
        if self.now - self.last > self.delay and self.velo == -2:
            self.current_frame = (self.current_frame +1) % len(self.right)
            self.image = self.right[self.current_frame]
            self.last = self.now
        self.now = pg.time.get_ticks()
        if self.now - self.last > self.delay and self.velo == 2:
            self.current_frame = (self.current_frame +1) % len(self.left)
            self.image = self.left[self.current_frame]
            self.last = self.now

        
        self.rect.x += self.vx

        # Apply gravity and vertical physics
        self.vy += GRAVITY
        if self.vy > 10:
            self.vy = 10  

        self.collide_with_wall('x')
        self.rect.y += self.vy
        self.collide_with_wall('y')



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





class Collectable(pg.sprite.Sprite):
    def __init__(self, display, x, y, img, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self = self
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.display = display

class Object(pg.sprite.Sprite):
    def __init__(self, display, x, y, images, game):
        super().__init__()
        self.game = game
        self.display = display
        self.images = images  # Store the full list of images
        self.current_frame = 0
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.delay = 70 
        self.last = pg.time.get_ticks()

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last > self.delay:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]
            self.last = now

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.clock = pg.time.Clock()
    def get_view(self, sprite_object):
        # all sprite object will be moved on camera position
        return sprite_object.rect.move(self.camera.topleft)
    def update(self, target):
        # Horizontal follow always
        x = -target.rect.x + WIDTH // 2

        # Calculate desired y position
        target_y = -target.rect.y + HEIGHT // 2
        current_y = self.camera.y

        # Vertical follow only if player moves above or below threshold (100 pixels)
        if target_y > current_y + 200:
            y = target_y
            self.clock.tick(FPS)
        elif target_y < current_y - 200:
            y = target_y
            self.clock.tick(FPS)
        else:
            y = current_y  # stay

        
        x = min(0, x)
        x = max(-1 * (self.width - WIDTH), x)
        y = min(0, y)
        y = max(-1 * (self.height - HEIGHT), y)

        self.camera = pg.Rect(x, y, self.width, self.height)


class Left_Right(pg.sprite.Sprite):
    def __init__(self, display, x, y, image, game):
        pg.sprite.Sprite.__init__(self)
        self.display = display

        self.game = game
        self.vx = 0
        self.vy = 0
        self.velo = 3
        self.image = image[0]
        self.rect = self.image.get_rect()
        self.rect.x = x     
        self.rect.y = y 
        self.current_frame = 0
        self.delay = 70
        self.last = pg.time.get_ticks()
        self.run = None
        # self.x_move = random.randint(340, 400)
        self.pos = 0
        self.x = x
        self.y = y
        self.range = 400


    def update(self):
        self.move_left = self.x 
        self.move_right = self.x + self.range
        self.move_up = self.y
        self.move_down = self.y + self.range
        self.rect.x += -self.velo
        if self.rect.x <= self.move_left:
            self.run = 1 
            self.velo = -3
        elif self.rect.x >= self.move_right:
            self.run = -1
            self.velo = 3
        if self.rect.y <= -self.velo:
            self.run = 1

        
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.collide_with_player('x')
        self.collide_with_player('y')


    def collide_with_player(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.player_sprite, False)
            if hits:
                if self.vx > 0:  
                    self.rect.right = hits[0].rect.left
                elif self.vx < 0:  
                    self.rect.left = hits[0].rect.right
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.player_sprite, False)
            if hits:
                if self.vy > 0:  
                    self.rect.bottom = hits[0].rect.top
                elif self.vy < 0:  
                    self.rect.top = hits[0].rect.bottom

class Up_Down(pg.sprite.Sprite):
    def __init__(self, display, x, y, image, game):
        pg.sprite.Sprite.__init__(self)
        self.display = display

        self.game = game
        self.vx = 0
        self.vy = 0
        self.velo = 3
        self.image = image[0]
        self.rect = self.image.get_rect()
        self.rect.x = x     
        self.rect.y = y 
        self.current_frame = 0
        self.delay = 70
        self.last = pg.time.get_ticks()
        self.run = None
        # self.x_move = random.randint(340, 400)
        self.pos = 0
        self.x = x
        self.y = y
        self.range = 400


    def update(self):
        self.move_up = self.y
        self.move_down = self.y + self.range
        self.rect.y += -self.velo
        if self.rect.y <= self.move_up:
            self.run = 1 
            self.velo = -3
        elif self.rect.y >= self.move_down:
            self.run = -1
            self.velo = 3


        
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.collide_with_player('x')
        self.collide_with_player('y')


    def collide_with_player(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.player_sprite, False)
            if hits:
                if self.vx > 0:  
                    self.rect.right = hits[0].rect.left
                elif self.vx < 0:  
                    self.rect.left = hits[0].rect.right
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.player_sprite, False)
            if hits:
                if self.vy > 0:  
                    self.rect.bottom = hits[0].rect.top
                elif self.vy < 0:  
                    self.rect.top = hits[0].rect.bottom
