import pygame as pg
from settings import *
from components import *
from components import Tiled_Map
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
        self.died = False
        self.start = True
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
        self.slime = SpriteSheet("Platformer/sprites/slime_green.PNG")
        self.slime_pur = SpriteSheet("Platformer/sprites/Slime_Purple.png")
        self.index = 0
        self.count = 0
        self.current_level = map_list[self.index]
        self.next_level = False

        self.load_images()

    def load_images(self):

        '''load and/or get images'''
        self.castle_list = []
########## List for my player movements ##########
        self.player_left_list = []
        self.player_right_list = []
        self.player_idle_list = []
        self.jump_list = []
        self.attack_list = []
        self.hit_list = []
########## List for my player movements ##########

########## List for Objects and platforms ##########

        self.move_list = [] # list for moving platforms
        self.coin_list = [] # list for coins
        self.level_list = []

########## List for my Enemy movements ##########
        self.en_right = []
        self.en_left = []
        self.en_down = []
        self.en_up = []
        self.en_right2 = []
        self.en_left2 = []
########## List for my Enemy movements ##########

        self.platform = self.move.get_image(16, 0, 32, 16)
        self.move_list.append(self.platform)
########## Player ##########
    # Player animation moving left and right
        player_scale = 1.2
        for i in range(1, 8):
            locx = i*32
            locy = 64
            self.player_left = self.player.get_image(locx, locy, 32, 32, player_scale, player_scale)
            self.player_left.set_colorkey(WHITE)
            self.player_left_list.append(self.player_left)
            self.player_right = pg.transform.flip(self.player_left, True, False)
            self.player_right_list.append(self.player_right)
    # player Idle animation
        for i in range(1, 4):
            locx = i*32
            locy = 0
            self.player_idle = self.player.get_image(locx, locy, 32, 32, player_scale, player_scale)
            self.player_idle_list.append(self.player_idle)
            self.player_idle.set_colorkey(WHITE) 
            self.player_idle_left = pg.transform.flip(self.player_idle, True, False)
    # player jumping Animation
        for i in range(6, 7):
            locx = i*32
            locy = 160  
            self.player_jump = self.player.get_image(locx, 160, 32, 32, player_scale, player_scale)
            self.player_jump.set_colorkey(WHITE)
            self.jump_list.append(self.player_jump)
    # player getting hit animation
        locx = 32*2
        locy= 32*6
        self.get_hit = self.player.get_image(locx, locy, 32, 32)
        self.hit_list.append(self.get_hit)
        for i in range(1, 11):
            locx = i*16
            locy = 16
            self.coins = self.coin.get_image(locx, locy, 16, 16, player_scale, player_scale)
            self.coins.set_colorkey(WHITE)
            # self.big_coin = pg.transform.scale(self.coins, (1, 1))
            self.coin_list.append(self.coins)
    # player attacking animation
        for i in range(0, 4):
            locx = i*32
            locy = 0
            self.attack = self.swoosh.get_image(locx, locy, 32, 32)
            self.attack.set_colorkey(BLACK)
            self.attack_list.append(self.attack)
########## Player ##########


########## Enemy ##########
        scale = 1.2
        for i in range(0, 4):
            locx =  i * 24
            locy = 0
            self.left_e = self.slime.get_image(locx, locy, 24, 24, scale, scale) # left/right
            self.left_e.set_colorkey(BLACK)
            self.en_left.append(self.left_e)
            right = pg.transform.flip(self.left_e, True, False)
            self.en_right.append(right)
        for i in range(0, 4):
            locx =  i * 24
            locy = 0
            self.left_e = self.slime_pur.get_image(locx, locy, 24, 24, scale, scale) # left/right
            self.left_e.set_colorkey(BLACK)
            self.en_left2.append(self.left_e)
            right = pg.transform.flip(self.left_e, True, False)
            self.en_right2.append(right)
########## Enemy ##########
      # self.player = self.character.get_image(57, 43, 50, 43)


    def new(self):
    
        '''create all game objects, sprites, and groups'''
        '''call run() method'''
        self.wall_group = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.coin_group = pg.sprite.Group()
        self.player_sprite = pg.sprite.Group()
        self.enemy_group = pg.sprite.Group()
        self.map_sprites = pg.sprite.Group()
        self.move_sprites = pg.sprite.Group()
        self.level_group = pg.sprite.Group()
        self.stop_group = pg.sprite.Group()

        self.map = pytmx.load_pygame(self.current_level)
        
        # self.map_sprites.add(self.map2)
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
                                          obj.x*mult, obj.y*mult2,self.player_idle_list, self.jump_list, 
                                          self.attack_list, self.hit_list, self.level_list, self)
                        player_list.append(self.guy)
                        self.all_sprites.add(self.guy)
                        self.player_sprite.add(self.guy)
                    elif obj.name == "Col":
                        Be = Wall(obj.x*mult, obj.y*mult, obj.width*mult, obj.height*mult)
                        self.wall_group.add(Be)
                        self.all_sprites.add(Be)
                    elif obj.name == "Wall":
                        Be = Wall(obj.x*mult, obj.y*mult, obj.width*mult, obj.height*mult)
                        self.stop_group.add(Be)
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
                        self.coin2 = Object(self.screen, obj.x*mult, obj.y*mult, self.coin_list, self)
                        self.all_sprites.add(self.coin2)
                        self.coin_group.add(self.coin2)
                    elif obj.name == 'Enemy':
                      self.enemy = Enemy(self.screen, self.en_left, self.en_right, self.en_up, self.en_down, obj.x*mult, obj.y*mult2, self)
                      self.all_sprites.add(self.enemy)
                      self.enemy_group.add(self.enemy)
                      enemy_list.append(self.enemy)    

                    elif obj.name == 'Enemy2':
                      self.enemys = Reverse_Enemy(self.screen, self.en_left2, self.en_right2, self.en_up, self.en_down, obj.x*mult, obj.y*mult2, self)
                      self.all_sprites.add(self.enemys)
                      self.enemy_group.add(self.enemys)
                      enemy_list.append(self.enemys)                
                    elif obj.name == 'Port':
                        # print("PI")
                        self.level = Object(self.screen, obj.x*mult, obj.y*mult, self.attack_list, self)
                        self.level_group.add(self.level)
                        # self.wall_group.add(self.level)
                        self.all_sprites.add(self.level)
                        self.level_list.append(self.level)
                    self.coin3 =  Object(self.screen, obj.x*mult, obj.y*mult, self.coin_list, self)





      
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

    def update(self):
        '''run all updates'''
        self.all_sprites.update()
        
        # Check for level transition
        for level in self.level_list:
            if level.rect.colliderect(self.guy.rect):
                self.index += 1
                if self.index < len(map_list):
                    self.current_level = map_list[self.index]
                    self.new()  # Reload the level with new map
                else:
                    # Game completed - loop back to first level
                    self.index = 0
                    self.current_level = map_list[self.index]
                    self.new()
        self.game_viewer.update(self.guy)
        if len(self.coin_group) <= 3:
            # len(self.coin_group) += 10
            pass

    def draw(self):
        '''fill the screen, draw the objects, and flip'''
        # if self.guy.rect.colliderect(self.level):
        #     current_level += 1

        
        # self.player_sprite.draw(self.screen)
        # if self.guy.rect.colliderect(self.level.rect.x, self.level.rect.y, self.level.rect.width, self.level.rect.height):
        #     print("Works")
        # for level in self.level_list:
        #     if level.rect.colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height):
        #         print("Works")
        if self.guy.HP == True and self.start == False:
            self.map_sprites.draw(self.screen)
            for sprite in self.all_sprites:
                self.screen.blit(sprite.image, self.game_viewer.get_view(sprite))
        elif self.guy.HP == False and self.start == False:
            self.game_over()   
        else:
            self.show_start_screen()    
        # Draw coin icon
        # if self.guy.rect.colliderect(self.coin2.rect):
        #     self.count += 1
        # self.screen.blit(self.coin3, (20, 20))

        # Draw coin number
        # font = pg.font.SysFont('Arial', 24)
        # coin_text = font.render(self.count, True, (255, 255, 255))
        # self.screen.blit(coin_text, (60, 25))

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
            self.update()
            self.draw()
            self.game_over()
            self.clock.tick(FPS)

    def show_start_screen(self):
        '''the screen to start the game'''
        if self.start == True:
            self.screen.fill(BLACK)
            font_small = pg.font.SysFont("TimesNewRoman", 35)
            instruction = font_small.render("Press Return or Enter to start the game", True, WHITE)

            self.screen.blit(instruction, (WIDTH//2-270, HEIGHT//2)) 
            keys = pg.key.get_pressed()
            if keys[pg.K_RETURN] and self.start == True:
                # print("FINE")
                self.start = False
                self.new()
    
    def game_over(self):
        '''the game over screen'''
        self.died = True
        self.screen.fill(BLACK)
        font_large = pg.font.SysFont("TimesNewRoman", 72)
        font_small = pg.font.SysFont("TimesNewRoman", 30)
        
        title = font_large.render("GAME OVER", True, RED)
        instruction = font_small.render("Press Return or Enter to restart or ESC to quit", True, WHITE)
        
        self.screen.blit(title, (WIDTH//2 - 225, HEIGHT//2 - 100))
        self.screen.blit(instruction, (WIDTH//2-260, HEIGHT//2)) 
        if self.died == True:
            keys = pg.key.get_pressed()
            if keys[pg.K_RETURN] and self.died == True and self.guy.HP == False:
                # print("FINE")
                self.died = False
                self.guy.HP = True
                self.new()


###################################################################
###                          PLAY GAME                          ###
###################################################################



game = Game()
game.show_start_screen()
while game.running:
   game.new()
   game.show_start_screen()
   game.game_over()

pg.quit()