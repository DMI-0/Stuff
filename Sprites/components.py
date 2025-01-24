
from settings import *
import pygame as pg


pg.init()

screen = pg.display.set_mode(([WIDTH, HEIGHT]), pg.RESIZABLE)

playing = True
clock = pg.time.Clock()

class Player:
    def __init__(self, x_loc, y_loc, display, right_img, left_img):
        # img = pg.image.load('platformer/character/walk/walk0001.png')
        # self.image = pg.transform.scale(img, (width, height))
        self.right = right_img
        self.left = left_img
        # self.rect = self.image.get_rect()
        self.display = display
        self.velo = 5
        self.x_velo = 5
        self.y_velo = 0
        self.jumping = False
        self.falling = False
        self.landed = True
        self.HP = 100
        self.reset = 0
        self.tel = False
        self.level = False
        self.x = x_loc
        self.y = y_loc
        self.add = False


        self.image = self.right[0]
        self.rect = self.image.get_rect()
        self.rect.x = x_loc
        self.rect.y = y_loc

        self.run_right = False
        self.run_left = False

        self.current_frame = 0
        self.delay = 10
        self.last  = pg.time.get_ticks()

    def draw(self):
        self.display.blit(self.image, self.rect)
    def update(self, surface_list, move_list, moving_list, up_list,
               gate_list, right_list, left_list, collasping_list):
        x_change = 0
        y_change = 0

        # list of key presses
        keys = pg.key.get_pressed()
        mouse = pg.mouse.get_pressed()

        # set x_velo (velocity) based on key presses
        if keys[pg.K_LEFT] and self.HP >= 1:                                                        #  or and self.rect.x > BRICK_WIDTH:    # or self.rect.x != 50:
            self.now = pg.time.get_ticks()
            x_change = -1 * self.velo
            self.run_left = True

            if self.now - self.last > self.delay:
                self.last = self.now
                self.current_frame = (self.current_frame + 1) % len(self.left)
                self.image = self.left[self.current_frame]
        elif keys[pg.K_RIGHT] and self.HP >= 1: # and self.rect.x != WIDTH - 100:
            self.now = pg.time.get_ticks()
            x_change = self.velo
            self.run_right = True

            if self.now - self.last > self.delay:
                self.current_frame = (self.current_frame + 1) % len(self.left)
                self.image = self.right[self.current_frame]
        else:
            x_change = 0
            if self.run_left:
                self.image = self.left[0]
                self.run_left = False
            elif self.run_right:
                self.image = self.right[0]
                self.run_right = False




        # set x_velo (velocity) based on key presses
        if keys[pg.K_a] and self.HP >= 1:                                                        #  or and self.rect.x > BRICK_WIDTH:    # or self.rect.x != 50:
            self.now = pg.time.get_ticks()
            x_change = -1 * self.velo
            self.run_left = True

            if self.now - self.last > self.delay:
                self.last = self.now
                self.current_frame = (self.current_frame + 1) % len(self.left)
                self.image = self.left[self.current_frame]
        elif keys[pg.K_d] and self.HP >= 1: # and self.rect.x != WIDTH - 100:
            self.now = pg.time.get_ticks()
            x_change = self.velo
            self.run_right = True

            if self.now - self.last > self.delay:
                self.current_frame = (self.current_frame + 1) % len(self.left)
                self.image = self.right[self.current_frame]

    # jump on space key
        if keys[pg.K_SPACE] and not self.jumping and self.landed:
            self.jumping = True
            self.landed = False

            self.y_velo = -15
        if not keys[pg.K_SPACE]:
            self.jumping = False

        if keys[pg.K_w] and not self.jumping and self.landed:
            self.jumping = True
            self.landed = False

            self.y_velo = -15
        if not keys[pg.K_w]:
            self.jumping = False

        if keys[pg.K_UP] and not self.jumping and self.landed:
            self.jumping = True
            self.landed = False

            self.y_velo = -15
        if not keys[pg.K_UP]:
            self.jumping = False

        self.y_velo += GRAVITY
        if self.y_velo > 10: # and self.rect.y != 550:
            self.y_velo = 10         # set terminal velocity
        y_change += self.y_velo

    # starts over the game
        if keys[pg.K_RETURN] and self.HP <= 0:
            self.rect.x = self.x
            self.rect.y = self.y
            self.HP = 100
            self.velo = 5
            self.jumping = False
            self.landed = True
            self.y_velo = 0
            self.reset += 1
            
        font = pg.font.SysFont("TimesNewRoman", 35)
        score_text = font.render("HP: " + str(self.HP), True, WHITE)
        screen.blit(score_text, (920, 50))
        # checks for collision 
        for surface in surface_list:
            # vertical collision
            if surface.rect.colliderect(self.rect.x, self.rect.y + y_change, self.rect.width, self.rect.height):
                # if player is going down
                if self.y_velo >= 0:
                    y_change = surface.rect.top - self.rect.bottom
                    self.landed = True
                    self.jumping = False
                    self.y_velo = 0
                # if player is going up
                elif self.y_velo < 0:
                    y_change = surface.rect.bottom - self.rect.top
                    self.y_velo = 0
            # Horizontal collision
            if surface.rect.colliderect(self.rect.x + x_change, self.rect.y, self.rect.width, self.rect.height):
                x_change = 0
        
      
        
        for move in move_list:
            # vertical collision
            if move.rect.colliderect(self.rect.x, self.rect.y + y_change, self.rect.width, self.rect.height):
                # if player is going down
                if self.y_velo >= 0:
                    y_change = move.rect.top - self.rect.bottom
                    self.landed = True
                    self.jumping = False
                    self.rect.x = self.x
                    self.rect.y = self.y
                # if player is going up
                elif self.y_velo < 0:
                    y_change = move.rect.bottom - self.rect.top
                    self.rect.x = self.x
                    self.rect.y = self.y
            if move.rect.colliderect(self.rect.x + x_change, self.rect.y, self.rect.width, self.rect.height):
                self.rect.x = self.x
                self.rect.y = self.y

        for move in moving_list:
            # vertical collision
            if move.rect.colliderect(self.rect.x, self.rect.y + y_change, self.rect.width, self.rect.height):
                self.x_velo = 0
                # if player is going down
                if self.y_velo >= 0:
                    y_change = move.rect.top - self.rect.bottom
                    self.landed = True
                    self.jumping = False
                    self.y_velo = 0
                # if player is going up
                elif self.y_velo < 0:
                    y_change = move.rect.bottom - self.rect.top
                    self.y_velo = 0
            # Horizontal collision
            if move.rect.colliderect(self.rect.x + x_change, self.rect.y, self.rect.width, self.rect.height):
                # self.y_velo = 0
                pass


        for up in up_list:
            # vertical collision
            if up.rect.colliderect(self.rect.x, self.rect.y + y_change, self.rect.width, self.rect.height):
                # if player is going down
                if self.y_velo >= 0:
                    y_change = up.rect.top - self.rect.bottom
                    self.landed = True
                    self.jumping = False
                    self.y_velo = 0
                # if player is going up
                elif self.y_velo < 0:
                    y_change = up.rect.bottom - self.rect.top
                    self.y_velo = 0
            # Horizontal collision
            if up.rect.colliderect(self.rect.x + x_change, self.rect.y, self.rect.width, self.rect.height):
                # self.y_velo = 0
                pass
        for gate in gate_list:
            # vertical collision
            if gate.rect.colliderect(self.rect.x, self.rect.y + y_change, self.rect.width, self.rect.height):
                # if player is going down
                if self.y_velo >= 0:
                    y_change = gate.rect.top - self.rect.bottom
                    self.landed = True
                    self.jumping = False
                    self.y_velo = 0
                # if player is going up
                elif self.y_velo < 0:
                    y_change = gate.rect.bottom - self.rect.top
                    self.y_velo = 0
            # Horizontal collision
            if gate.rect.colliderect(self.rect.x + x_change, self.rect.y, self.rect.width, self.rect.height):
                x_change = 0
        
        for right in right_list:
            # vertical collision
            if right.rect.colliderect(self.rect.x, self.rect.y + y_change, self.rect.width, self.rect.height):
                self.x_velo = 0
            # if player is going down
                if self.y_velo >= 0:
                    y_change = right.rect.top - self.rect.bottom
                    self.landed = True
                    self.jumping = False
                    self.y_velo = 0
                # if player is going up
                elif self.y_velo < 0:
                    y_change = right.rect.bottom - self.rect.top
                    self.y_velo = 0
            # Horizontal collision
            if right.rect.colliderect(self.rect.x + x_change, self.rect.y, self.rect.width, self.rect.height):
                # self.y_velo = 0
                pass
        for left in left_list:
            # vertical collision
            if left.rect.colliderect(self.rect.x, self.rect.y + y_change, self.rect.width, self.rect.height):
                self.x_velo = 0
                # if player is going down
                if self.y_velo >= 0:
                    y_change = left.rect.top - self.rect.bottom
                    self.landed = True
                    self.jumping = False
                    self.y_velo = 0
                # if player is going up
                elif self.y_velo < 0:
                    y_change = left.rect.bottom - self.rect.top
                    self.y_velo = 0
            # Horizontal collision
            if left.rect.colliderect(self.rect.x + x_change, self.rect.y, self.rect.width, self.rect.height):
                # self.y_velo = 0
                pass

    
        for col in collasping_list:
            # vertical collision
            if col.rect.colliderect(self.rect.x, self.rect.y + y_change, self.rect.width, self.rect.height):
                # if player is going down
                if self.y_velo >= 0:
                    y_change = col.rect.top - self.rect.bottom
                    self.landed = True
                    self.jumping = False
                    self.y_velo = 0
                # if player is going up
                elif self.y_velo < 0:
                    y_change = col.rect.bottom - self.rect.top
                    self.y_velo = 0
            # Horizontal collision
            if col.rect.colliderect(self.rect.x + x_change, self.rect.y, self.rect.width, self.rect.height):
                x_change = 0


        if self.rect.y > HEIGHT:
            self.HP = 0
        if self.rect.y < 0:
            self.HP = 0
        if self.rect.x > WIDTH:
            self.HP = 0
        if self.rect.x < -25:
            self.HP = 0

        # print(self.rect.x)
        if self.HP <= 0:
            self.velo = 0
            x_change = 0
            y_change = 0
            self.jumping = False
    # update the player location
        self.rect.x += x_change
        self.rect.y += y_change
        y_change = -1 * self.velo

 
    def re(self):
        font = pg.font.SysFont("TimesNewRoman", 35)
        score_text = font.render("Resets: " + str(self.reset), True, WHITE)
        screen.blit(score_text, (1045, 50))


class Brick:
    def __init__(self, display, color, x, y, width, height, img):
        self.image = pg.transform.scale(img, (width, height))
        self.rect = self.image.get_rect()    
        self.display = display
        self.color = color
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.velo = 1
        self.width = width
        self.height = height
        # self.rect = pg.Rect(x, y, self.width, self.height)
        self.check = False
        self.range = 200
        self.collapsing = False
        self.pick = False
        # self.HP = 1
    def draw_brick(self):
        self.display.blit(self.image, self.rect)
    def collasping_brick(self, player_list):
        self.display.blit(self.image, self.rect)
        for player in player_list:
            # vertical collision
            if player.rect.colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height):
                self.collapsing = True
            # Horizontal collision
            elif player.rect.colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height):
                self.collapsing = True
        
        if self.collapsing == True:
            self.rect.y = -100
    def HP(self, player_list):
        for player in player_list:
            if player.rect.colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height):
                self.pick = True
            if self.pick == True:
                player.HP += 25
                self.pick = False
                self.rect.y = -100
            if player.HP <= 0:
                self.rect.y = self.y
    def lava(self, player_list):
        for player in player_list:
            if player.rect.colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height):
                player.jumping = True
                # player.landed = False

                player.y_velo = -15               
                player.HP -= 50
                

class Enemy:
    def __init__(self, x_loc, y_loc, width, height, color, display, img):
        self.color = color
        self.display = display
        self.velo = 5
        self.image = pg.transform.scale(img, (width, height))
        self.rect = self.image.get_rect()    
        self.HP = 1
        self.rect.x = x_loc
        self.rect.y = y_loc
        self.range = 200
        self.x = x_loc
        self.y = y_loc
        self.range = 200
    def draw_enemy(self):
            self.display.blit(self.image, self.rect)
    def update(self):

        self.rect.x += -self.velo
        if self.rect.x <= 0 and self.HP >= 1:
            self.rect.x += WIDTH

    def upen(self):

        self.rect.y += self.velo
        if self.rect.y >= HEIGHT and self.HP >= 1:
                self.rect.y -= HEIGHT
        
    def rmey(self):

        self.rect.x += self.velo
        if self.rect.x + 55 >= WIDTH:
                self.rect.x -= WIDTH + 55
        

    def right_side(self):
        if self.HP <= 0:
            self.rect.x = -50
        elif self.rect.x <= 0 and self.HP >= 1:
            self.rect.x += WIDTH
        self.left = self.x 
        self.right = self.x + self.range
        self.rect.x += -self.velo
        if self.rect.x <= self.left:
            self.velo = -3
        elif self.rect.x >= self.right or self.rect.x <= 50:
            self.velo = 3


    def left_side(self):
        if self.HP <= 0:
            self.rect.x = 0
        elif self.rect.x + 55 >= WIDTH and self.HP >= 1:
            self.rect.x -= WIDTH + 55
        self.left = self.x 
        self.right = self.x - self.range
        self.rect.x += -self.velo
        if self.rect.x >= self.left:
            self.velo = 3
        elif self.rect.x <= self.right or self.rect.x <= 50:
            self.velo = -3

    def col(self, player_list):
        x_change = 0
        y_change = 0
        for player in player_list:
            if player.rect.colliderect(self.rect.x, self.rect.y + y_change, self.rect.width, self.rect.height):
                player.HP -= 100
                self.rect.x = 1500
                self.rect.y = 1500
                self.velo = 0

                if player.HP <= 0:
                    self.rect.x = self.x
                    self.velo = 0
            elif player.rect.colliderect(self.rect.x + x_change, self.rect.y, self.rect.width, self.rect.height):
                self.rect.x = -100
                player.HP -= 100
                if player.HP <= 0:
                    self.rect.x = self.x
                    self.velo = 0
  


    def reset(self, player_list): 
        keys = pg.key.get_pressed()
        for player in player_list:
            if keys[pg.K_RETURN] and player.HP <= 0:
                self.velo = 5
                self.jumping = False
                self.landed = True
                self.rect.x = self.x
                self.rect.y = self.y

class Move:
    def __init__(self, display, color, x, y, width, height, img):
        self.display = display
        self.color = color
        self.x = x
        self.y = y
        self.velo = 1
        self.width = width
        self.height = height
        # self.rect = pg.Rect(x, y, self.width, self.height)
        self.check = False
        self.range = 200
        self.image = pg.transform.scale(img, (width, height))
        self.rect = self.image.get_rect()    
        self.display = display
        self.color = color
        self.rect.x = x
        self.rect.y = y
        self.velo = 1
        self.width = width
        self.height = height
        # self.rect = pg.Rect(x, y, self.width, self.height)
        self.check = False
        self.range = 200
    def draw_brick(self):
        self.display.blit(self.image, self.rect)
    def update(self):
        self.up = self.y 
        self.down = self.y + self.range
        self.rect.y += -self.velo
        if self.rect.y <= self.up:
            self.velo = -1
        elif self.rect.y >= self.down or self.rect.y >= HEIGHT - 50:
            self.velo = 1
    def reverse(self):
        self.up = self.y 
        self.down = self.y - self.range
        self.rect.y += -self.velo
        if self.rect.y >= self.up:
            self.velo = 1
        elif self.rect.y <= self.down or self.rect.y <= 100:
            self.velo = -1

    def right_side(self, player_list):
        self.left = self.x 
        self.right = self.x + self.range
        self.rect.x += -self.velo
        if self.rect.x <= self.left:
            self.velo = -1
        elif self.rect.x >= self.right or self.rect.x <= 50:
            self.velo = 1
        for player in player_list:
            if player.rect.colliderect(self.rect):
                player.y_velo = self.velo
            else:
                player.y_velo = player.y_velo

    def left_side(self, player_list):
        self.left = self.x 
        self.right = self.x - self.range
        self.rect.x += -self.velo
        if self.rect.x >= self.left:
            self.velo = 1
        elif self.rect.x <= self.right or self.rect.x <= 50:
            self.velo = -1

        for player in player_list:
            if player.rect.colliderect(self.rect):
                player.x_velo = self.velo
            else:
                player.x_velo = player.x_velo

class Key:
    def __init__(self, display, color, x, y, width, height, img):
        self.image = pg.transform.scale(img, (width, height))
        self.rect = self.image.get_rect()
        self.display = display
        self.rect.x = x
        self.rect.y = y
        self.color = color
        self.width = width
        self.height = height
        self.key = 0
        self.pick_up = False
        self.HP = 1
        self.y = y

    def draw(self):
        self.display.blit(self.image, self.rect)
    def picked_up(self, player_list, gate_list):
        keys = pg.key.get_pressed()
        if keys[pg.K_RETURN] and self.HP <= 0:
            self.HP = 1
            # self.HP = 1
        font = pg.font.SysFont("TimesNewRoman", 35)
        score_text = font.render("Key: " + str(self.key), True, WHITE)
        screen.blit(score_text, (815, 50))

        for gate in gate_list:
            for player in player_list:
                if player.rect.colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height):
                    self.pick_up = True
                    gate.rect.y = -100

                if self.pick_up == True:
                    self.key += 1
                    self.pick_up = False
                    self.rect.y = -100
                if player.HP <= 0:
                    self.rect.y = self.y
                    gate.rect.y = gate.rect.y

    
class Gate:
    def __init__(self, display, color, x, y, width, height, img):
        self.image = pg.transform.scale(img, (width, height))
        self.rect = self.image.get_rect()
        self.display = display
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.key = 0
        self.pick_up = False
        self.HP = 1
        self.y = y
    def draw(self):
        self.display.blit(self.image, self.rect)
    def picked_up(self, player_list, key_list):
        for key in key_list:
            for player in player_list:
                if player.rect.colliderect(key.rect.x, key.rect.y, key.rect.width, key.rect.height):
                    self.pick_up = True
                    key.rect.y = -100

                if self.pick_up == True:
                    key.key += 1
                    self.pick_up = False
                    self.rect.y = -100
                if player.HP <= 0:
                    self.rect.y = self.y
                    key.rect.y = key.rect.y

       
        if self.pick_up == True:
            self.pick_up = False
        if self.HP <= 0:
            self.rect.y = self.y
            self.HP = 1
            self.pick_up = False




# player = 0
# col = 0

# test = pg.time.set_timer(col, 1000)
