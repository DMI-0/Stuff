import pygame as pg
from settings import *
from sprites import SpriteSheet
from sprites import Player
from sprites import Wall



brick_list = []
class Game:
   def __init__(self):
      pg.init()
      pg.mixer.init()
      self.screen = pg.display.set_mode((WIDTH, HEIGHT))
      self.clock = pg.time.Clock()
      self.running = True
      self.all_sprites = pg.sprite.Group()
      self.wall_group = pg.sprite.Group()
      # self.char = []

      self.explosion_sheet = SpriteSheet("Sprites/explosion.png")
      self.tilemap = SpriteSheet("Sprites/tilemap.png")
      self.char = SpriteSheet("Sprites/spritesheet_characters.png")

      self.load_images()

   def load_images(self):


      self.bow_img = self.tilemap.get_image(16*11.5, 16*9.5, 16, 16)
      # self.player_img = self.character.get_image(57, 43, 50, 43)
      # self.player_img.set_colorkey(BLACK)
      # self.player  = Player(self.screen, 57, 43, self.char)
      # zombie_img = self.character.get_image(425, 5, 37, 39)
      # grass_img = self.tilemap.get_image(16*11.5, 16*9.5, 16, 16)
      # ground_img = self.tilemap.get_image(5*11,9*6, 15, 15)
      # image = explosion_sheet.get_image(x_loc, y_loc, 64, 64)
      # image.set_colorkey(BLACK) # erases that color
      self.bow_img.set_colorkey(BLACK)
      # player_img.set_colorkey(BLACK)
      # zombie_img.set_colorkey(BLACK)
      # # explosion_list.append(image)
         # explotsion_list[0]
      
      '''load and/or get images'''
      self.tilemap = SpriteSheet("Sprites/tilemap.png")
      self.grass_img = self.tilemap.get_image(16, 1, 16, 16, 3, 3)
      self.grass_img.set_colorkey(BLACK)
      self.player_img = self.char.get_image(57, 43, 50, 43)
      self.player_img.set_colorkey(BLACK)
      self.wall_img = self.tilemap.get_image(16*6.4, 16*11, 16, 16, 4, 5)
      self.wall_img.set_colorkey(BLACK)

      # self.player = self.character.get_image(57, 43, 50, 43)


   def new(self):
      '''create all game objects, sprites, and groups'''
      '''call run() method'''
      self.wall_group = pg.sprite.Group()
      self.all_sprites = pg.sprite.Group()
      self.bow = pg.sprite.Group()
  
      # player = Player()

      self.wall_list = []
      for row_index, row in enumerate(LAYOUT):
         for col_index, tile in enumerate(row):
            y = row_index * TILESIZE
            x = col_index * TILESIZE
            if tile == '1':
               block = Wall(x, y, self.screen, self.wall_img)
               self.wall_group.add(block)
               self.all_sprites.add(block)
            elif tile == ' ':
               grass = Wall(x, y, self.screen, self.grass_img)
               self.all_sprites.add(grass)
            # elif tile == 'a':
      arrow = Wall(300, 200, self.screen, self.bow_img)
      self.bow.add(arrow)
               # self.wall_group.add(arrow)
      self.player = Player(self.screen, 200, 200, self.player_img, self)
      self.all_sprites.add(self.player)
      self.run()


   def  update(self):
      '''run all updates'''
      # self.player.collide_with_wall()
      self.all_sprites.update()
   def draw(self):
      '''fill the screen, draw the objects, and flip'''
      self.screen.fill(WHITE)
      self.all_sprites.draw(self.screen)
      self.bow.draw(self.screen)
      # self.wall_group.draw(self.screen)
      pg.display.flip()
   def events(self):
      '''game loop event'''
      for event in pg.event.get():
         if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            if self.playing:
               self.playing = False
            self.running = False
   def run(self):
      '''contains the main game loop'''
      self.playing = True
      while self.playing:
         self.events()
         # self.load_images()
         self.update()
         self.draw()
         self.clock.tick(FPS)

   def show_start_screen(self):
      '''the screen to start the game'''
      pass
   def game_over(self):
      '''the game over screen'''
      pass




###################################################################
###                          PLAY GAME                          ### 
###################################################################



game = Game()
game.show_start_screen()
while game.running:
   game.new()

pg.quit()

# explosion_sheet = SpriteSheet("Sprites/explosion.png")
# tilemap = SpriteSheet("Sprites/tilemap.png")
# character = SpriteSheet("Sprites/spritesheet_characters.png")
# explosion_list = []
# tilemap_list = []
# player_list = []
# bow_img = tilemap.get_image(16*11.5, 16*9.5, 16, 16)
# player_img = character.get_image(57, 43, 50, 43)
# zombie_img = character.get_image(425, 5, 37, 39)
# grass_img = tilemap.get_image(2, 2, 15, 15)
# ground_img = tilemap.get_image(5*11,9*6, 15, 15)


# for y in range(5):
#    for x in range(5):
#       x_loc = 64 * x
#       y_loc = 64 * y

#       image = explosion_sheet.get_image(x_loc, y_loc, 64, 64)
#       image.set_colorkey(BLACK) # erases that color
#       bow_img.set_colorkey(BLACK)
#       player_img.set_colorkey(BLACK)
#       zombie_img.set_colorkey(BLACK)
#       explosion_list.append(image)
#    # explotsion_list[0]
#       flip = pg.transform.flip(zombie_img, True, False)
# playing = True

# while playing:
#    for event in pg.event.get():
#       if event.type == pg.QUIT:
#          playing = False



#       keys = pg.key.get_pressed()

#       if keys[pg.K_LEFT]:                                         
#             x += -1 * x_speed
#       elif keys[pg.K_RIGHT]:
#             x += x_speed
#       else:
#          x_speed = 0




#   # game logic
#   # clear the screen
#    screen.fill(NIGHT)
#    for i in range(WIDTH):
#       for e in range(HEIGHT):
#          # screen.blit(grass_img, (i, e))
#          screen.blit(ground_img, (i, e))
  
#    # screen.blit(ground_img, (100, 300))
  
#    # screen.blit(explosion_list[0], (100,100))
#    # screen.blit(bow_img, (100,100))
#    screen.blit(player_img, (x, 100))
#    screen.blit(flip, (200, 100))

# # draw code should go here
#    # update the screen with new drawings
#    pg.display.flip()
#    # limit to "FPS" frames per second
#    clock.tick(FPS)
# pg.quit()
