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
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.all_sprites = pg.sprite.Group()
        self.wall_group = pg.sprite.Group()
        self.coin_group = pg.sprite.Group()
        # self.char = []

        self.player = SpriteSheet("characters.png")
        self.ren = SpriteSheet("Ren.png")
    

        self.load_images()

   def load_images(self):

      '''load and/or get images'''

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
            self.test = self.player.get_image(locx, locy, 16, 16, 2.2, 2.2)
            self.test.set_colorkey(BLACK)
            # self.castle_list.append(self.test)




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
        self.map = pytmx.load_pygame("Maps/Map1.tmx")

        player_list = []
        enemy_list = []
        mult = 1.95
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
                        self.guy = Player(self.screen, self.left, self.right, self.up, self.down, obj.x*mult, obj.y*mult2, self)
                        player_list.append(self.guy)
                        self.all_sprites.add(self.guy)
                        self.player_sprite.add(self.guy)





      
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
    #   self.game_viewer.update(self.guy)
      if len(self.coin_group) <= 3:
         # len(self.coin_group) += 10
         pass

   def draw(self):
        '''fill the screen, draw the objects, and flip'''
        self.screen.fill(BLUE)
        
        
        self.map_sprites.draw(self.screen)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.game_viewer.get_view(sprite))
        # font = pg.font.SysFont("TimesNewRoman", 35)
        # score_text = font.render("HP: " + '100', True, RED)
        # self.screen.blit(score_text, (10, 10))
        

        
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