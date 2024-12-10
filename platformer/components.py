from settings import *
import pygame as pg


pg.init()

screen = pg.display.set_mode(([WIDTH, HEIGHT]), pg.RESIZABLE)

playing = True
clock = pg.time.Clock()

class Player:
    def __init__(self, x_loc, y_loc, width, height, color, display, img):
        self.image = pg.transform.scale(img, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x_loc
        self.rect.y = y_loc
        self.color = color
        self.display = display
        self.velo = 5
        self.x_velo = 5
        self.y_velo = 0
        self.jumping = False
        self.falling = False
        self.landed = True
        self.HP = True
        self.reset = 0
        self.tel = False
        self.level = False
        self.x = x_loc
        self.y = y_loc

    def draw(self):
        self.display.blit(self.image, self.rect)
    def update(self, surface_list, enemy_list, move_list, up_enemy_list,
               moving_list, rem_list, up_list, gate_list, right_list, left_list,
               big_enemy_list, br_enemy_list, collasping_list, rimy_list, lemy_list):
        x_change = 0
        y_change = 0

        # list of key presses
        keys = pg.key.get_pressed()
        mouse = pg.mouse.get_pressed()

        # set x_velo (velocity) based on key presses
        if keys[pg.K_LEFT] and self.HP == True:                                                        #  or and self.rect.x > BRICK_WIDTH:    # or self.rect.x != 50:
            x_change = -1 * self.velo
        elif keys[pg.K_RIGHT] and self.HP == True: # and self.rect.x != WIDTH - 100:
            x_change = self.velo

        # set x_velo (velocity) based on key presses
        if keys[pg.K_a] and self.HP == True:                                                        #  or and self.rect.x > BRICK_WIDTH:    # or self.rect.x != 50:
            x_change = -1 * self.velo
        elif keys[pg.K_d] and self.HP == True: # and self.rect.x != WIDTH - 100:
            x_change = self.velo

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

        # if pg.mouse.get_pressed() and not self.jumping and self.landed:
        #     self.jumping = True
        #     self.landed = False
        #     self.y_velo = -15
        # if not pg.mouse.get_pressed():
        #     self.jumping = False
        self.y_velo += GRAVITY
        if self.y_velo > 10: # and self.rect.y != 550:
            self.y_velo = 10         # set terminal velocity
        y_change += self.y_velo

    # starts over the game
        if keys[pg.K_RETURN] and not self.HP:
            self.rect.x = self.x
            self.rect.y = self.y
            self.HP = True
            self.velo = 5
            self.jumping = False
            self.landed = True
            self.y_velo = 0
            self.reset += 1
            

                        # resets += 1
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
        
        for enemy in enemy_list:
            # vertical collision
            if enemy.rect.colliderect(self.rect.x, self.rect.y + y_change, self.rect.width, self.rect.height):
                # if player is going down
                if self.y_velo >= 0:
                    self.HP = False
                # if player is going up
                elif self.y_velo < 0:
                    self.HP = False
            # Horizontal collision
            elif enemy.rect.colliderect(self.rect.x + x_change, self.rect.y, self.rect.width, self.rect.height):
                self.HP = False
            if self.rect.y > HEIGHT:
                    self.HP = False
        
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
        for upenemy in up_enemy_list:
            # vertical collision
            if upenemy.rect.colliderect(self.rect.x, self.rect.y + y_change, self.rect.width, self.rect.height):
                # if player is going down
                if self.y_velo >= 0:
                    self.HP = False
                # if player is going up
                elif self.y_velo < 0:
                    self.HP = False
            # Horizontal collision
            elif upenemy.rect.colliderect(self.rect.x + x_change, self.rect.y, self.rect.width, self.rect.height):
                self.HP = False       
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

        for rem in rem_list:
            # vertical collision
            if rem.rect.colliderect(self.rect.x, self.rect.y + y_change, self.rect.width, self.rect.height):
                # if player is going down
                if self.y_velo >= 0:
                    self.HP = False
                # if player is going up
                elif self.y_velo < 0:
                    self.HP = False
            # Horizontal collision
            elif rem.rect.colliderect(self.rect.x + x_change, self.rect.y, self.rect.width, self.rect.height):
                self.HP = False
            if self.rect.y > HEIGHT:
                    self.HP = False
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

        for big_enemy in big_enemy_list:
            # vertical collision
            if big_enemy.rect.colliderect(self.rect.x, self.rect.y + y_change, self.rect.width, self.rect.height):
                # if player is going down
                if self.y_velo >= 0:
                    self.HP = False
                # if player is going up
                elif self.y_velo < 0:
                    self.HP = False
            # Horizontal collision
            elif big_enemy.rect.colliderect(self.rect.x + x_change, self.rect.y, self.rect.width, self.rect.height):
                self.HP = False
            if self.rect.y > HEIGHT:
                    self.HP = False
        for br_enemy in br_enemy_list:
            # vertical collision
            if br_enemy.rect.colliderect(self.rect.x, self.rect.y + y_change, self.rect.width, self.rect.height):
                # if player is going down
                if self.y_velo >= 0:
                    self.HP = False
                # if player is going up
                elif self.y_velo < 0:
                    self.HP = False
            # Horizontarl collision
            elif br_enemy.rect.colliderect(self.rect.x + x_change, self.rect.y, self.rect.width, self.rect.height):
                self.HP = False
            if self.rect.y > HEIGHT:
                    self.HP = False
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

        for rimy in rimy_list:
            # vertical collision
            if rimy.rect.colliderect(self.rect.x, self.rect.y + y_change, self.rect.width, self.rect.height):
                # if player is going down
                if self.y_velo >= 0:
                    self.HP = False
                # if player is going up
                elif self.y_velo < 0:
                    self.HP = False
            # Horizontal collision
            elif rimy.rect.colliderect(self.rect.x + x_change, self.rect.y, self.rect.width, self.rect.height):
                self.HP = False
            if self.rect.y > HEIGHT:
                    self.HP = False
    
        for lemy in lemy_list:
            # vertical collision
            if lemy.rect.colliderect(self.rect.x, self.rect.y + y_change, self.rect.width, self.rect.height):
                # if player is going down
                if self.y_velo >= 0:
                    self.HP = False
                # if player is going up
                elif self.y_velo < 0:
                    self.HP = False
            # Horizontal collision
            elif lemy.rect.colliderect(self.rect.x + x_change, self.rect.y, self.rect.width, self.rect.height):
                self.HP = False
            if self.rect.y > HEIGHT:
                    self.HP = False

        if self.rect.y > HEIGHT:
            self.HP = False
        if self.rect.y < 0:
            self.HP = False
        if self.rect.x > WIDTH:
            self.HP = False
        if self.rect.x < -25:
            self.HP = False

        # print(self.rect.x)
        if self.HP == False:
            font = pg.font.SysFont("TimesNewRoman", 35)
            text = font.render("GAME OVER", True, SKY)
            screen.blit(text, ((WIDTH/2)-100, HEIGHT/2))
            start = font.render("Click 'Return' or 'Enter' to start over", True, SKY)
            screen.blit(start, ((WIDTH/2)-250, (HEIGHT/2)+50))
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
        screen.blit(score_text, (1020, 50))

class Brick:
    def __init__(self, display, color, x, y, width, height, img):
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
        self.collapsing = False
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


class Enemy:
    def __init__(self, x_loc, y_loc, width, height, color, display, img):
        self.color = color
        self.display = display
        self.velo = 5
        self.x_velo = 0
        self.y_velo = 0
        self.image = pg.transform.scale(img, (width, height))
        self.rect = self.image.get_rect()    
        self.HP = True
        self.rect.x = x_loc
        self.rect.y = y_loc
        self.range = 200
        self.x = x_loc
        self.y = y_loc
        self.range = 200
    def draw_enemy(self):
            self.display.blit(self.image, self.rect)
    def update(self, player_list):
        x_change = 0
        y_change = 0
        self.rect.x += -self.velo
        if self.HP == False:
            self.rect.x = -50
        elif self.rect.x <= 0 and self.HP == True:
            # self.rect.x = 0
            self.rect.x += WIDTH

        for player in player_list:
            # vertical collision
            if player.rect.colliderect(self.rect.x, self.rect.y + y_change, self.rect.width, self.rect.height):
                self.HP = False
            # Horizontal collision
            elif player.rect.colliderect(self.rect.x + x_change, self.rect.y, self.rect.width, self.rect.height):
                self.HP = False
        
        keys = pg.key.get_pressed()
        if keys[pg.K_RETURN] and not self.HP:
            self.rect.x = self.rect.x
            self.rect.y = self.rect.y
            self.HP = True
            self.velo = 5
            self.jumping = False
            self.landed = True
            self.y_velo = 0

    def upen(self, player_list):
        x_change = 0
        y_change = 0
        self.rect.y += self.velo
        if self.HP == False:
            self.rect.y = HEIGHT - HEIGHT + 100
        elif self.rect.y >= HEIGHT and self.HP == True:
            self.rect.y -= HEIGHT
        # print(self.rect.y)

        for player in player_list:
            # vertical collision
            if player.rect.colliderect(self.rect.x, self.rect.y + y_change, self.rect.width, self.rect.height):
                self.HP = False
            # Horizontal collision
            elif player.rect.colliderect(self.rect.x + x_change, self.rect.y, self.rect.width, self.rect.height):
                self.HP = False
        
    def rmey(self, player_list):
        x_change = 0
        y_change = 0
        self.rect.x += self.velo

        if self.HP == False:
            self.rect.x = 0
        elif self.rect.x + 55 >= WIDTH and self.HP == True:
            self.rect.x -= WIDTH + 55

        for player in player_list:
            # vertical collision
            if player.rect.colliderect(self.rect.x, self.rect.y + y_change, self.rect.width, self.rect.height):
                self.HP = False
            # Horizontal collision
            elif player.rect.colliderect(self.rect.x + x_change, self.rect.y, self.rect.width, self.rect.height):
                self.HP = False
        

    def right_side(self, player_list):
        if self.HP == False:
            self.rect.x = -50
        elif self.rect.x <= 0 and self.HP == True:
            self.rect.x += WIDTH
        x_change = 0
        y_change = 0
        self.left = self.x 
        self.right = self.x + self.range
        self.rect.x += -self.velo
        if self.rect.x <= self.left:
            self.velo = -3
        elif self.rect.x >= self.right or self.rect.x <= 50:
            self.velo = 3

        for player in player_list:
            # vertical collision
            if player.rect.colliderect(self.rect.x, self.rect.y + y_change, self.rect.width, self.rect.height):
                self.HP = False
            # Horizontal collision
            elif player.rect.colliderect(self.rect.x + x_change, self.rect.y, self.rect.width, self.rect.height):
                self.HP = False
        
    def left_side(self, player_list):
        if self.HP == False:
            self.rect.x = 0
        elif self.rect.x + 55 >= WIDTH and self.HP == True:
            self.rect.x -= WIDTH + 55
        x_change = 0
        y_change = 0
        self.left = self.x 
        self.right = self.x - self.range
        self.rect.x += -self.velo
        if self.rect.x >= self.left:
            self.velo = 3
        elif self.rect.x <= self.right or self.rect.x <= 50:
            self.velo = -3

        for player in player_list:
            # vertical collision
            if player.rect.colliderect(self.rect.x, self.rect.y + y_change, self.rect.width, self.rect.height):
                self.HP = False
            # Horizontal collision
            elif player.rect.colliderect(self.rect.x + x_change, self.rect.y, self.rect.width, self.rect.height):
                self.HP = False




    def reset(self): 
        keys = pg.key.get_pressed()

        if keys[pg.K_RETURN] and not self.HP:
            self.HP = True
            self.velo = 5
            self.jumping = False
            self.landed = True
            self.y_velo = 0 
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

    def right_side(self):
        self.left = self.x 
        self.right = self.x + self.range
        self.rect.x += -self.velo
        if self.rect.x <= self.left:
            self.velo = -1
        elif self.rect.x >= self.right or self.rect.x <= 50:
            self.velo = 1
    def left_side(self):
        self.left = self.x 
        self.right = self.x - self.range
        self.rect.x += -self.velo
        if self.rect.x >= self.left:
            self.velo = 1
        elif self.rect.x <= self.right or self.rect.x <= 50:
            self.velo = -1

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
        self.HP = True
        self.y = y

    def draw(self):
        self.display.blit(self.image, self.rect)
    def picked_up(self, player_list, gate_list, enemy_list, up_enemy_list,
                  rem_list, big_enemy_list, br_enemy_list,
                  rimy_list, lemy_list):
        keys = pg.key.get_pressed()
        if keys[pg.K_RETURN] and self.HP == False:
            self.HP = True
            # self.HP = True
        font = pg.font.SysFont("TimesNewRoman", 35)
        score_text = font.render("Key: " + str(self.key), True, WHITE)
        screen.blit(score_text, (900, 50))
        for player in player_list:
            # vertical collision
            if player.rect.colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height):
            #    self.key = 1
               self.pick_up = True
            # Horizontal collision
            elif player.rect.colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height):
                self.pick_up = True
                
        for gate in gate_list:
            # vertical collision
            if gate.rect.colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height):
                pass           
         # Horizontal collision
            elif player.rect.colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height):
                pass
       
        for enemy in enemy_list:
            if enemy.rect.colliderect(player.rect.x, player.rect.y, player.rect.width, player.rect.height):
                if player.y_velo >= 0:
                    self.HP = False
                elif player.y_velo < 0:
                    self.HP = False
            elif enemy.rect.colliderect(player.rect.x, player.rect.y, player.rect.width, player.rect.height):
                self.HP = False
                if player.rect.y > HEIGHT:
                    self.HP = False

        for upenemy in up_enemy_list:
            if upenemy.rect.colliderect(player.rect.x, player.rect.y, player.rect.width, player.rect.height):
                if player.y_velo >= 0:
                    self.HP = False
                elif player.y_velo < 0:
                    self.HP = False
            elif upenemy.rect.colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height):
                self.HP = False       
        
        for rem in rem_list:
            # vertical collision
            if rem.rect.colliderect(player.rect.x, player.rect.y, player.rect.width, player.rect.height):
                # if player is going down
                if player.y_velo >= 0:
                    self.HP = False
                # if player is going up
                elif player.y_velo < 0:
                    self.HP = False
            # Horizontal collision
            elif rem.rect.colliderect(player.rect.x, player.rect.y, player.rect.width, player.rect.height):
                self.HP = False
            if player.rect.y > HEIGHT:
                    self.HP = False
        
        for big_enemy in big_enemy_list:
            # vertical collision
            if big_enemy.rect.colliderect(player.rect.x, player.rect.y, player.rect.width, player.rect.height):
                # if player is going down
                if player.y_velo >= 0:
                    self.HP = False
                # if player is going up
                elif player.y_velo < 0:
                    self.HP = False
            # Horizontal collision
            elif big_enemy.rect.colliderect(player.rect.x, player.rect.y, player.rect.width, player.rect.height):
                self.HP = False
            if player.rect.y > HEIGHT:
                    self.HP = False
        
        for br_enemy in br_enemy_list:
            # vertical collision
            if br_enemy.rect.colliderect(player.rect.x, player.rect.y, player.rect.width, player.rect.height):
                if player.y_velo >= 0:
                    self.HP = False
                elif player.y_velo < 0:
                    self.HP = False
            elif br_enemy.rect.colliderect(player.rect.x , player.rect.y, player.rect.width, player.rect.height):
                self.HP = False
            if player.rect.y > HEIGHT:
                    self.HP = False
    

        for rimy in rimy_list:
            if rimy.rect.colliderect(player.rect.x, player.rect.y, player.rect.width, player.rect.height):
                if player.y_velo >= 0:
                    self.HP = False
                elif player.y_velo < 0:
                    self.HP = False
                elif rimy.rect.colliderect(player.rect.x, player.rect.y, player.rect.width, player.rect.height):
                    self.HP = False
                    if player.rect.y > HEIGHT:
                        self.HP = False
    
        for lemy in lemy_list:
            if lemy.rect.colliderect(player.rect.x, player.rect.y, player.rect.width, player.rect.height):
                if player.y_velo >= 0:
                    self.HP = False
                elif player.y_velo < 0:
                        self.HP = False
                elif lemy.rect.colliderect(player.rect.x, player.rect.y, player.rect.width, player.rect.height):
                    self.HP = False
                    if player.rect.y > HEIGHT:
                        self.HP = False        

        if self.pick_up == True:
            gate.rect.y = -100
            self.key += 1
            self.rect.y = -100
            self.pick_up = False
        if self.HP == False and self.key >= 1:
            gate.rect.y = gate.rect.y
            self.rect.y = self.y
            self.key += -1
            self.HP = True
            self.pick_up = False


                        # resets += 1
    
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
        self.HP = True
        self.y = y
    def draw(self):
        self.display.blit(self.image, self.rect)
    def picked_up(self, player_list, key_list, enemy_list, up_enemy_list,
                  rem_list, big_enemy_list, br_enemy_list,
                  rimy_list, lemy_list):
        for key in key_list:
            for player in player_list:
                if player.rect.colliderect(key.rect.x, key.rect.y, key.rect.width, key.rect.height):
                    self.pick_up = True
                elif player.rect.colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height):
                    self.pick_up = True
            for enemy in enemy_list:
                # vertical collision
                if enemy.rect.colliderect(player.rect.x, player.rect.y, player.rect.width, player.rect.height):
                    # if player is going down
                    if player.y_velo >= 0:
                        self.HP = False
                    # if player is going up
                    elif player.y_velo < 0:
                        self.HP = False
                # Horizontal collision
                elif enemy.rect.colliderect(player.rect.x, player.rect.y, player.rect.width, player.rect.height):
                    self.HP = False
                    if player.rect.y > HEIGHT:
                        self.HP = False

            for upenemy in up_enemy_list:
                # vertical collision
                if upenemy.rect.colliderect(player.rect.x, player.rect.y, player.rect.width, player.rect.height):
                    # if player is going down
                    if player.y_velo >= 0:
                        self.HP = False
                    # if player is going up
                    elif player.y_velo < 0:
                        self.HP = False
                # Horizontal collision
                elif upenemy.rect.colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height):
                    self.HP = False       
            
            for rem in rem_list:
                # vertical collision
                if rem.rect.colliderect(player.rect.x, player.rect.y, player.rect.width, player.rect.height):
                    # if player is going down
                    if player.y_velo >= 0:
                        self.HP = False
                    # if player is going up
                    elif player.y_velo < 0:
                        self.HP = False
                # Horizontal collision
                elif rem.rect.colliderect(player.rect.x, player.rect.y, player.rect.width, player.rect.height):
                    self.HP = False
                if player.rect.y > HEIGHT:
                        self.HP = False
            
            for big_enemy in big_enemy_list:
                # vertical collision
                if big_enemy.rect.colliderect(player.rect.x, player.rect.y, player.rect.width, player.rect.height):
                    # if player is going down
                    if player.y_velo >= 0:
                        self.HP = False
                    # if player is going up
                    elif player.y_velo < 0:
                        self.HP = False
                # Horizontal collision
                elif big_enemy.rect.colliderect(player.rect.x, player.rect.y, player.rect.width, player.rect.height):
                    self.HP = False
                if player.rect.y > HEIGHT:
                        self.HP = False
            
            for br_enemy in br_enemy_list:
                if br_enemy.rect.colliderect(player.rect.x, player.rect.y, player.rect.width, player.rect.height):
                    if player.y_velo >= 0:
                        self.HP = False
                    elif player.y_velo < 0:
                        self.HP = False
                elif br_enemy.rect.colliderect(player.rect.x , player.rect.y, player.rect.width, player.rect.height):
                    self.HP = False
                if player.rect.y > HEIGHT:
                    self.HP = False


            for rimy in rimy_list:
                if rimy.rect.colliderect(player.rect.x, player.rect.y, player.rect.width, player.rect.height):
                    if player.y_velo >= 0:
                        self.HP = False
                    elif player.y_velo < 0:
                        self.HP = False
                    elif rimy.rect.colliderect(player.rect.x, player.rect.y, player.rect.width, player.rect.height):
                        self.HP = False
                        if player.rect.y > HEIGHT:
                            self.HP = False
        
            for lemy in lemy_list:
                if lemy.rect.colliderect(player.rect.x, player.rect.y, player.rect.width, player.rect.height):
                    if player.y_velo >= 0:
                        self.HP = False
                    elif player.y_velo < 0:
                            self.HP = False
                    elif lemy.rect.colliderect(player.rect.x, player.rect.y, player.rect.width, player.rect.height):
                        self.HP = False
                        if player.rect.y > HEIGHT:
                            self.HP = False

  
       
        if self.pick_up == True:
            self.pick_up = False
        if self.HP == False:
            self.rect.y = self.y
            self.HP = True
            self.pick_up = False

