import pygame as pg
from settings import *
from components import *
from Levels import Tiled_Map
import pytmx

# char width and height: 1474 and 74

brick_list = []
class Game:
   def __init__(self):
        pg.init()
        pg.mixer.init()
        pg.mixer.music.load("platformer/music/time_for_adventure.mp3")
        pg.mixer.music.play(-1)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.all_sprites = pg.sprite.Group()
        self.wall_group = pg.sprite.Group()
        self.coin_group = pg.sprite.Group()
        self.death_zone = pg.sprite.Group()
        # self.char = []

        self.player = SpriteSheet("Knight2.PNG")
        self.move = SpriteSheet("Platformer/sprites/platforms.png")
        self.coin = SpriteSheet("coin2.PNG")
        self.swoosh = SpriteSheet("swoosh.png")
        self.ren = SpriteSheet("Ren.png")

        self.load_images()

   def load_images(self):

      '''load and/or get images'''

      self.castle_list = []
      self.player_left_list = []
      self.player_right_list = []
      self.player_idle_list = []
      self.jump_list = []
      self.attack_list = []


      self.move_list = []
      self.coin_list = []


      self.en_right = []
      self.en_left = []
      self.en_down = []
      self.en_up = []

      self.platform = self.move.get_image(16, 0, 32, 16)
      self.move_list.append(self.platform)

      for i in range(1, 8):
          locx = i*32
          locy = 64
          self.player_left = self.player.get_image(locx, locy, 32, 32) # Player animation moving left
          self.player_left.set_colorkey(WHITE)
          self.player_left_list.append(self.player_left)
          self.player_right = pg.transform.flip(self.player_left, True, False) # player animation moving right
          self.player_right_list.append(self.player_right)

      for i in range(1, 4):
          locx = i*32
          locy = 0
          self.player_idle = self.player.get_image(locx, locy, 32, 32)
          self.player_idle_list.append(self.player_idle)
          self.player_idle.set_colorkey(WHITE) 
      for i in range(6, 7):
        locx = i*32
        locy = 160  
        self.player_jump = self.player.get_image(locx, 160, 32, 32)
        self.player_jump.set_colorkey(WHITE)
        self.jump_list.append(self.player_jump)
      
      
      for i in range(1, 11):
          locx = i*16
          locy = 16
          self.coins = self.coin.get_image(locx, locy, 16, 16)
          self.coins.set_colorkey(WHITE)
          self.coin_list.append(self.coins)

      for i in range(0, 4):
          locx = i*32
          locy = 0
          self.attack = self.swoosh.get_image(locx, locy, 32, 32)
          self.attack.set_colorkey(BLACK)
          self.attack_list.append(self.attack)




# for my enemy
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


      # self.player = self.character.get_image(57, 43, 50, 43)


   def new(self):
        '''create all game objects, sprites, and groups'''
        '''call run() method'''
        self.wall_group = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.coin_group = pg.sprite.Group()
        self.player_sprite = pg.sprite.Group()
        self.enemy_sprite = pg.sprite.Group()
        self.map_sprites = pg.sprite.Group()
        self.move_sprites = pg.sprite.Group()
        self.map = pytmx.load_pygame("Maps/Map1.tmx")

        player_list = []
        enemy_list = []
        mult = 2
        mult2 = 1.95





        for layer in self.map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, surf in layer.tiles():
                    pos = (x*TILESIZE, y*TILESIZE)
                    surf = pg.transform.scale(surf, (TILESIZE, TILESIZE))
                    Tiled_Map(pos, surf, self.all_sprites)

            elif isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if obj.name == 'Player':
                        self.guy = Player(self.screen, self.player_right_list, self.player_left_list, 
                                          obj.x*mult, obj.y*mult2,self.player_idle_list, self.jump_list, self.attack_list, self)
                        player_list.append(self.guy)
                        self.all_sprites.add(self.guy)
                        self.player_sprite.add(self.guy)
                    elif obj.name == "Col":
                      Be = Wall(obj.x*mult, obj.y*mult, obj.width*mult, obj.height*mult)
                      self.wall_group.add(Be)
                      self.all_sprites.add(Be)
                    elif obj.name == "pi":
                      Be = Wall(obj.x*mult2, obj.y*mult, obj.width*mult, obj.height*mult)
                      self.wall_group.add(Be)
                      self.all_sprites.add(Be)
                    elif obj.name == 'Down':
                        self.down = Up_Down(self.screen, obj.x*mult, obj.y*mult, self.move_list, self)
                        self.all_sprites.add(self.down)
                        self.wall_group.add(self.down)
                        self.move_sprites.add(self.down)
                    elif obj.name == 'death':
                        ded = Wall(obj.x*mult, obj.y*mult, obj.width*mult, obj.height*mult)
                        self.all_sprites.add(ded)
                        self.death_zone.add(ded)
                    elif obj.name == 'coin':
                        # print("YES")
                        coin = Object(self.screen, obj.x*mult, obj.y*mult, self.coin_list, self)
                        self.all_sprites.add(coin)
                        self.coin_group.add(coin)
                    elif obj.name == 'Test':
                      enemy = Enemy(self.screen, self.en_left, self.en_right, self.en_up, self.en_down, obj.x*mult, obj.y*mult2, self)
                      self.all_sprites.add(enemy)
                      self.enemy_sprite.add(enemy)
                      enemy_list.append(enemy)                    





      
        self.wall_list = []
        
        for x in range(3):
            for y in range(3):

                x = random.randint(67, MAP_WIDTH-112)
                y = random.randint(152, MAP_HEIGHT-196)
                # coin = Object(self.screen, x, y, self.coin_img)
                # self.coin_group.add(coin)
                # self.all_sprites.add(coin)
        # self.wall_group.add(coin)
        locx = random.randint(67, MAP_WIDTH-112)
        locy = random.randint(152, MAP_HEIGHT-196)
        # self.player = Player(self.screen, self.left, self.right, self.up, self.down, 190, 190, self)
        # self.en = Enemy(self.screen, self.en_left, self.en_right, self.en_up, self.en_down, 200, 200, self)

        # self.player_sprite.add(self.player)
        # self.all_sprites.add(self.player)
        # self.all_sprites.add(self.en)

        self.game_viewer = Camera(MAP_WIDTH*TILESIZE, MAP_HEIGHT*TILESIZE)

        self.run()

   def  update(self):
      '''run all updates'''
      # print(f'this is the coins: {len(self.coin_group)}')
      # self.player.collide_with_wall()
      self.all_sprites.update()
      self.game_viewer.update(self.guy)
      if len(self.coin_group) <= 3:
         # len(self.coin_group) += 10
         pass

   def draw(self):
        '''fill the screen, draw the objects, and flip'''
        self.screen.fill(BLACK)
        self.player_sprite.draw(self.screen)
        
        self.map_sprites.draw(self.screen)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.game_viewer.get_view(sprite))
        font = pg.font.SysFont("TimesNewRoman", 35)
        score_text = font.render("HP: " + '100', True, RED)
        self.screen.blit(score_text, (10, 10))
        

        
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