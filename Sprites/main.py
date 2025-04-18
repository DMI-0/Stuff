import pygame as pg
from settings import *
from sprites import *

# char width and height: 1474 and 74

brick_list = []
class Game:
   def __init__(self):
      pg.init()
      pg.mixer.init()
      self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
      self.clock = pg.time.Clock()
      self.running = True
      self.all_sprites = pg.sprite.Group()
      self.wall_group = pg.sprite.Group()
      self.coin_group = pg.sprite.Group()
      # self.char = []

      self.explosion_sheet = SpriteSheet("Sprites/explosion.png")
      self.tilemap = SpriteSheet("Sprites/tilemap.png")
      self.char = SpriteSheet("Sprites/spritesheet_characters.png")
      self.char2 = SpriteSheet("Sprites/new_chars.png")
      self.ren = SpriteSheet("Sprites/Ren.png")

      self.load_images()

   def load_images(self):


      # self.bow_img = self.tilemap.get_image(16*11.5, 16*9.5, 16, 16)
      # self.player_img = self.character.get_image(57, 43, 50, 43)
      # self.player_img.set_colorkey(BLACK)
      # self.player  = Player(self.screen, 57, 43, self.char)
      # zombie_img = self.character.get_image(425, 5, 37, 39)
      # grass_img = self.tilemap.get_image(16*11.5, 16*9.5, 16, 16)
      # ground_img = self.tilemap.get_image(5*11,9*6, 15, 15)
      # image = explosion_sheet.get_image(x_loc, y_loc, 64, 64)
      # image.set_colorkey(BLACK) # erases that color
      # self.bow_img.set_colorkey(BLACK)
      # player_img.set_colorkey(BLACK)
      # zombie_img.set_colorkey(BLACK)
      # # explosion_list.append(image)
         # explotsion_list[0]
      
      '''load and/or get images'''
      self.tilemap = SpriteSheet("Sprites/tilemap.png")
      self.grass_img = self.tilemap.get_image(16, 0, 16, 16, 2.2, 2.2) # grass with flowers (green)
      self.grass_img.set_colorkey(BLACK)
      self.grass_plain = self.tilemap.get_image(0, 0, 16, 16, 2.2, 2.2) # grass without flowers
      self.grass_plain.set_colorkey(BLACK)
      self.grass_flower = self.tilemap.get_image(17*2, 0, 16, 16, 2.2, 2.2) # grass with flowers (sunflower)
      self.grass_flower.set_colorkey(BLACK)
      self.player_img = self.char.get_image(57, 43, 50, 43)
      self.player_img.set_colorkey(BLACK)

      self.wall_lower_left = self.tilemap.get_image(0, 16*10.7, 16, 16, 2.2, 2.2) # wall
      self.wall_lower_left.set_colorkey(BLACK)
      self.wall_left_cornor_mid = self.tilemap.get_image(0, 16*9.5, 16, 16, 2.2, 2.2) # wall
      self.wall_left_cornor_mid.set_colorkey(BLACK)
      self.wall_upper_left = self.tilemap.get_image(0, 16*8.5, 16, 16, 2.2, 2.2) # wall
      self.wall_upper_left.set_colorkey(BLACK)
      
      self.wall_lower_mid = self.tilemap.get_image(16, 16*10.7, 16, 16, 2.2, 2.2) # wall
      self.wall_lower_mid.set_colorkey(BLACK)
      self.wall_middle = self.tilemap.get_image(16, 16*9.6, 16, 16, 2.2, 2.2) # wall
      self.wall_middle.set_colorkey(BLACK)
      self.wall_upper_mid = self.tilemap.get_image(16, 16*8.6, 16, 16, 2.2, 2.2) # wall
      self.wall_upper_mid.set_colorkey(BLACK)


      self.wall_lower_right = self.tilemap.get_image(16*2.1, 16*10.7, 16, 16, 2.2, 2.2) # wall lower right
      self.wall_lower_right.set_colorkey(BLACK)
      self.wall_upper_right = self.tilemap.get_image(16*2.1, 16*8.5, 16, 16, 2.2, 2.2) # wall * upper right
      self.wall_upper_right.set_colorkey(BLACK)
      self.wall_right_cornor_mid = self.tilemap.get_image(16*2.1, 16*9.5, 16, 16, 2.2, 2.2) # wall middle right side
      self.wall_right_cornor_mid.set_colorkey(BLACK)
      # self.Ren_img = self.ren.get_image(145, 195, 48, 48) # forward 1
      # self.Ren_img.set_colorkey(BLACK)

      self.right = []
      self.left = []
      self.up = []
      self.down = []
      self.castle_list = []


      self.en_right = []
      self.en_left = []
      self.en_down = []
      self.en_up = []

      for l in range(2):
         for i in range(8, 12):
            locx = l*17
            locy = 17*i
            self.test = self.tilemap.get_image(locx, locy, 16, 16, 2.2, 2.2)
            self.test.set_colorkey(BLACK)
            self.castle_list.append(self.test)



      for i in range(3, 6):
         locx =  i * 48
         locy = 48*4
         self.Ren_down = self.ren.get_image(locx, locy, 48, 48) # down
         self.Ren_down.set_colorkey(BLACK)
         self.down.append(self.Ren_down)


      for i in range(3, 6):
         locx =  i * 48
         locy = 48*7
         self.Ren_up = self.ren.get_image(locx, locy, 48, 48) # up
         self.Ren_up.set_colorkey(BLACK)
         self.up.append(self.Ren_up)

      for i in range(3, 6):
         locx =  i * 48
         locy = 48*5
         self.Ren_left = self.ren.get_image(locx, locy, 48, 48) # left/right
         self.Ren_left.set_colorkey(BLACK)
         self.left.append(self.Ren_left)
         right = pg.transform.flip(self.Ren_left, True, False)
         self.right.append(right)


      



      for i in range(0, 2):
         locx =  i * 48
         locy = 0
         self.en = self.ren.get_image(locx, locy, 48, 48) # down
         self.en.set_colorkey(BLACK)
         self.en_down.append(self.en)


      for i in range(0, 2):
         locx =  i * 48
         locy = 48*3
         self.e_up = self.ren.get_image(locx, locy, 48, 48) # up
         self.e_up.set_colorkey(BLACK)
         self.en_up.append(self.e_up)

      for i in range(0, 2):
         locx =  i * 48
         locy = 48
         self.left_e = self.ren.get_image(locx, locy, 48, 48) # left/right
         self.left_e.set_colorkey(BLACK)
         self.en_left.append(self.left_e)
         right = pg.transform.flip(self.left_e, True, False)
         self.en_right.append(right)



      # self.Ren_img.set_colorkey(BLACK)
      self.wall_img = self.tilemap.get_image(16*6.4, 16*11, 16, 16, 2, 3.5)
      self.wall_img.set_colorkey(BLACK)
      self.coin_img = self.tilemap.get_image(16*9.5, 16*7.5, 16, 16, 2, 2)
      self.coin_img.set_colorkey(BLACK)
      self.ground_img = self.tilemap.get_image(16, 16, 16, 16, 2.2, 2.2) # Grass with dirt center
      self.ground_img.set_colorkey(BLACK)
      
      self.grass_corner_left = self.tilemap.get_image(0, 16, 16, 16, 2.2, 2.2) # upper left side
      self.grass_corner_left.set_colorkey(BLACK)
      self.grass_left_side = self.tilemap.get_image(0, 34, 16, 16, 2.2, 2.2) # middle left side
      self.grass_left_side.set_colorkey(BLACK)
      self.grass_lower_left = self.tilemap.get_image(0, 52, 16, 16, 2.2, 2.2) # lower left corner
      self.grass_lower_left.set_colorkey(BLACK)
      self.grass_middle_lower = self.tilemap.get_image(16, 52, 16, 16, 2.2, 2.2) # middle lower grass
      self.grass_middle_lower.set_colorkey(BLACK)
      
      self.grass_lower_right = self.tilemap.get_image(34, 52, 16, 16, 2.2, 2.2) # right lower grass
      self.grass_lower_right.set_colorkey(BLACK)
      self.grass_corner_right = self.tilemap.get_image(34, 16, 16, 16, 2.2, 2.2) # right upper side
      self.grass_corner_right.set_colorkey(BLACK)
      self.grass_middle_right = self.tilemap.get_image(34, 34, 16, 16, 2.2, 2.2) # Right side middle 
      self.grass_middle_right.set_colorkey(BLACK)

      self.grass_mid_mid = self.tilemap.get_image(16, 16, 16, 16, 2.2, 2.2)
      self.grass_mid_mid.set_colorkey(BLACK)
      self.dirt = self.tilemap.get_image(16, 34, 16, 16, 2.2, 2.2) # dirt block
      self.dirt.set_colorkey(BLACK)




      # self.player = self.character.get_image(57, 43, 50, 43)


   def new(self):
      '''create all game objects, sprites, and groups'''
      '''call run() method'''
      self.wall_group = pg.sprite.Group()
      self.all_sprites = pg.sprite.Group()
      self.coin_group = pg.sprite.Group()
      self.player_sprite = pg.sprite.Group()
  
      # player = Player()
      
      self.wall_list = []
      for row_index, row in enumerate(LAYOUT):
         for col_index, tile in enumerate(row):
            y = row_index * TILESIZE
            x = col_index * TILESIZE
            # if tile == 'd':
            #    self.w = Wall(x, y, self.screen, self.castle_list)
            #    self.all_sprites.add(self.w)
            #    self.wall_group.add(self.w)
            
            if tile == '1':
               block = Wall(x, y, self.screen, self.wall_img)
               self.wall_group.add(block)
               self.all_sprites.add(block)
            elif tile == ' ':
               plain = Wall(x, y, self.screen, self.grass_plain)
               self.all_sprites.add(plain)
            elif tile == 'f':
               flower = Wall(x, y, self.screen, self.grass_flower)
               self.all_sprites.add(flower)
            elif tile == 'g':
               grass = Wall(x, y, self.screen, self.grass_img)
               self.all_sprites.add(grass)
            elif tile == 'r':
               upper_right = Wall(x, y, self.screen, self.grass_corner_right)   
               self.all_sprites.add(upper_right)
            elif tile == '4':
               middle_right = Wall(x, y, self.screen, self.grass_middle_right)  
               self.all_sprites.add(middle_right)
            elif tile == 'R':
               lower_right = Wall(x, y, self.screen, self.grass_lower_right)
               self.all_sprites.add(lower_right)  
            elif tile == 'm':
               middle = Wall(x, y, self.screen, self.grass_mid_mid)   
               self.all_sprites.add(middle)
            elif tile == '3':
               middle_mid = Wall(x, y, self.screen, self.dirt) 
               self.all_sprites.add(middle_mid)
            elif tile == 'M':
               lower_mid = Wall(x, y, self.screen, self.grass_middle_lower) 
               self.all_sprites.add(lower_mid)  
            elif tile == 'l':
               upper_left = Wall(x, y, self.screen, self.grass_corner_left)
               self.all_sprites.add(upper_left)
            elif tile == '2':
               middle_left = Wall(x, y, self.screen, self.grass_left_side)
               self.all_sprites.add(middle_left)   
            elif tile == 'L':
               lower_left = Wall(x, y, self.screen, self.grass_lower_left)
               self.all_sprites.add(lower_left)
            elif tile == 'w':
               lower_mid = Wall(x, y, self.screen, self.wall_lower_mid)
               self.all_sprites.add(lower_mid)
               self.wall_group.add(lower_mid)
            elif tile == '5':
               lower_left = Wall(x, y, self.screen, self.wall_lower_left)
               self.all_sprites.add(lower_left)
               self.wall_group.add(lower_left)
            elif tile == '6':
               upper_right = Wall(x, y, self.screen, self.wall_upper_right)
               self.all_sprites.add(upper_right)
               self.wall_group.add(upper_right)
            elif tile == 'u':
               self.wall_mid = Wall(x, y, self.screen, self.wall_upper_mid)
               self.all_sprites.add(self.wall_mid)
               self.wall_group.add(self.wall_mid)
            elif tile == '8':
               self.wall_mid_mid = Wall(x, y, self.screen, self.wall_middle)
               self.all_sprites.add(self.wall_mid_mid)
               self.wall_group.add(self.wall_mid_mid)
            elif tile == '9':
               self.wall_right_mid = Wall(x, y, self.screen, self.wall_right_cornor_mid)
               self.all_sprites.add(self.wall_right_mid)
               self.wall_group.add(self.wall_right_mid)
            elif tile == '!':
               self.wall_right_down = Wall(x, y, self.screen, self.wall_lower_right)
               self.all_sprites.add(self.wall_right_down)
               self.wall_group.add(self.wall_right_down)
            elif tile == '7':
               self.wall_left_mid = Wall(x, y, self.screen, self.wall_left_cornor_mid)
               self.all_sprites.add(self.wall_left_mid)
               self.wall_group.add(self.wall_left_mid)
            elif tile == 'v':
               self.wall_left_low = Wall(x, y, self.screen, self.wall_upper_left)
               self.all_sprites.add(self.wall_left_low)
               self.wall_group.add(self.wall_left_low)

               
            # elif tile == 'a':
      # self.all_sprites.add(coin)
      
      for x in range(3):
         for y in range(3):

            x = random.randint(67, MAP_WIDTH-112)
            y = random.randint(152, MAP_HEIGHT-196)
            coin = Object(self.screen, x, y, self.coin_img)
            self.coin_group.add(coin)
            self.all_sprites.add(coin)
      # self.wall_group.add(coin)
      locx = random.randint(67, MAP_WIDTH-112)
      locy = random.randint(152, MAP_HEIGHT-196)
      self.player = Player(self.screen, self.left, self.right, self.up, self.down, 190, 190, self)
      self.en = Enemy(self.screen, self.en_left, self.en_right, self.en_up, self.en_down, 200, 200, self)

      # self.player_sprite.add(self.player)
      self.all_sprites.add(self.player)
      self.all_sprites.add(self.en)

      self.game_viewer = Camera(MAP_WIDTH, MAP_HEIGHT)

      self.run()

   def  update(self):
      '''run all updates'''
      # print(f'this is the coins: {len(self.coin_group)}')
      # self.player.collide_with_wall()
      self.all_sprites.update()
      self.game_viewer.update(self.player)
      if len(self.coin_group) <= 3:
         # len(self.coin_group) += 10
         pass

   def draw(self):
      '''fill the screen, draw the objects, and flip'''
      self.screen.fill(WHITE)
      for sprite in self.all_sprites:
         self.screen.blit(sprite.image, self.game_viewer.get_view(sprite))
      

      
      # self.player_sprite.draw(self.screen)
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

# explosion_sheet = SpriteSheet("explosion.png")
# tilemap = SpriteSheet("tilemap.png")
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
