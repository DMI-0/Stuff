from settings import *
import components as comps
import pygame as pg

screen = pg.display.set_mode([WIDTH, HEIGHT])

index = 11
end_list = []
player_list = []
enemy_list = []
brick_list = []
fake_list = []
teleport_list = []
up_enemy_list = []
freeze_list = []
moving_list = []
reverse_list = []
re_list = []
key_list = []
gate_list = []
right_side_list = []
left_side_list = []
big_enemy_list = []
br_enemy_list = []
colapsing_list = []
rimy_list = []
lemy_list = []
block_list = []

# current_level = level_list[index] 
# current_level = outline 
current_level = LAYOUT 


block_img = pg.image.load('platformer/images/crate.png')
arrow_img = pg.image.load('platformer/images/arrow.png')
key_img = pg.image.load('platformer/images/key_blue.png')
player_img = pg.image.load('platformer/images/Boy face.png')
gate_img = pg.image.load('platformer/images/lock_blue.png')
stone_wall = pg.image.load('platformer/images/stone wall.jpg')
moving_img = pg.image.load('platformer/images/cloud_3.png')
fly_img = pg.image.load('platformer/images/fly_normal.png')
broken_img = pg.image.load('platformer/images/fence_broken.png')
warp_img = pg.image.load('platformer/images/warp.png')
slime_img = pg.image.load('platformer/images/slime_walk.png')
bridge_img = pg.image.load('platformer/images/bridge.png')

def load_levels(level):
    end_list.clear()
    player_list.clear()
    enemy_list.clear()
    brick_list.clear()
    fake_list.clear()
    teleport_list.clear()
    up_enemy_list.clear()
    freeze_list.clear()
    moving_list.clear()
    reverse_list.clear()
    re_list.clear()
    key_list.clear()
    gate_list.clear()
    right_side_list.clear()
    left_side_list.clear()
    big_enemy_list.clear()
    br_enemy_list.clear()
    colapsing_list.clear()
    rimy_list.clear()
    lemy_list.clear()
    block_list.clear()    

    for row in range(len(level)):
        y_loc = row * BRICK_HEIGHT
        for col in range(len(level[0])):
            x_loc = col * BRICK_WIDTH
            if level[row][col] == '1':
                brick = comps.Brick(screen, WHITE, x_loc, y_loc, BRICK_WIDTH, BRICK_HEIGHT, stone_wall)
                brick_list.append(brick)
            elif level[row][col] == '*':
                brick = comps.Brick(screen, WHITE, x_loc, y_loc, 5, 5, block_img)
                brick_list.append(brick)
            elif level[row][col] == '2':
                next_level = comps.Brick(screen, GREEN, x_loc, y_loc, BRICK_WIDTH, BRICK_HEIGHT, arrow_img)
                end_list.append(next_level)
            elif level[row][col] == '3':
                brick = comps.Brick(screen, YELLOW, x_loc, y_loc, wid, hid, block_img)
                brick_list.append(brick)
            elif level[row][col] == 'F':
                tel = comps.Brick(screen, GRAY, x_loc, y_loc, BRICK_WIDTH, BRICK_HEIGHT, broken_img)
                fake_list.append(tel)
            elif level[row][col] == 'T':
                movement = comps.Brick(screen, PINK, x_loc, y_loc, BRICK_WIDTH, BRICK_HEIGHT, warp_img)
                teleport_list.append(movement)
            elif level[row][col] == 'P':
                player = comps.Player(x_loc, y_loc, PLAYER_WIDTH, PLAYER_HEIGHT, BLUE, screen, player_img)
                player_list.append(player)
            elif level[row][col] == 'E':
                enemy = comps.Enemy(x_loc, y_loc, ENEMY_WIDTH, ENEMY_HEIGHT, RED, screen, fly_img)
                enemy_list.append(enemy)
            elif level[row][col] == 'R':
                r_enemy = comps.Enemy(x_loc, y_loc, ENEMY_WIDTH, ENEMY_HEIGHT, RED, screen, fly_img)
                reverse_list.append(r_enemy)
            elif level[row][col] == 'U':
                up = comps.Enemy(x_loc, y_loc, ENEMY_WIDTH, ENEMY_HEIGHT, RED, screen, fly_img)
                up_enemy_list.append(up)   
            elif level[row][col] == '4':
                let = comps.Move(screen, SKY, x_loc, y_loc, BRICK_WIDTH, hid, bridge_img)
                moving_list.append(let)
            elif level[row][col] == '5':
                re = comps.Move(screen, SKY, x_loc, y_loc, BRICK_WIDTH, hid, bridge_img)
                re_list.append(re)
            elif level[row][col] == 'i':
                key = comps.Key(screen, GRASS, x_loc, y_loc, wid, hid, key_img)
                key_list.append(key)
            elif level[row][col] == 'G':
                gate = comps.Gate(screen, WHITE, x_loc, y_loc, BRICK_WIDTH, BRICK_HEIGHT, gate_img)
                gate_list.append(gate)
            elif level[row][col] == 'r':
                side = comps.Move(screen, SKY, x_loc, y_loc, BRICK_WIDTH, hid, bridge_img)
                right_side_list.append(side)
            elif level[row][col] == 'L':
                left_side = comps.Move(screen, SKY, x_loc, y_loc, BRICK_WIDTH, hid, bridge_img)
                left_side_list.append(left_side)
            elif level[row][col] == 'B':
                big_enemy = comps.Enemy(x_loc, y_loc, big_width, ENEMY_HEIGHT, RED, screen, fly_img)
                big_enemy_list.append(big_enemy)
            elif level[row][col] == 'b':
                br_enemy = comps.Enemy(x_loc, y_loc, big_width, ENEMY_HEIGHT, RED, screen, fly_img)
                br_enemy_list.append(br_enemy)
            elif level[row][col] == 'c':
                colapsing_brick = comps.Brick(screen, GRAY, x_loc, y_loc, BRICK_WIDTH, BRICK_HEIGHT, broken_img)
                colapsing_list.append(colapsing_brick)
            elif level[row][col] == '<':
                test = comps.Enemy(x_loc, y_loc, ENEMY_WIDTH, ENEMY_HEIGHT, RED, screen, slime_img)
                rimy_list.append(test)
            elif level[row][col] == '>':
                lemy = comps.Enemy(x_loc, y_loc, ENEMY_WIDTH, ENEMY_HEIGHT, RED, screen, slime_img)
                lemy_list.append(lemy)

            elif level[row][col] == 'g':
                ground = comps.Brick(screen, WHITE, x_loc, y_loc, BRICK_WIDTH, BRICK_HEIGHT, bridge_img)
                block_list.append(ground)

playing = True
clock = pg.time.Clock()
load_levels(current_level)
while playing:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            playing = False
        
    # game logic
  # clear the screen
    if index <= 11:
        screen.fill(BLACK)
    elif index >= 11:
        screen.fill(DARK_RED)
        

    # draw code should go here

    if index == 0:
        font = pg.font.SysFont("TimesNewRoman", 35)
        score_text = font.render("Use '<-' and '->' or 'A' and 'D' to move, 'space bar' or 'w' to Jump",True, WHITE)
        screen.blit(score_text, (200, 350))
    elif index == 11:
        font = pg.font.SysFont("TimesNewRoman", 35)
        text = font.render("CONGRADULATIONS", True, WHITE)
        screen.blit(text, (450, 350)) 
        text2 = font.render("YOU'VE BEATEN THE FIRST 10 LEVELS",True, WHITE)
        screen.blit(text2, (300, 400))

    for block in brick_list:
        block.draw_brick()
    for fake in fake_list:
        fake.draw_brick()
    for port in teleport_list:
        port.draw_brick()
        # port.reverse()
    for freeze in freeze_list:
        freeze.draw()
        freeze.update(player_list)
    for next_level in end_list:
        next_level.draw_brick()
    for char in moving_list:
        char.draw_brick()
        char.update()
    for char in colapsing_list:
        char.collasping_brick(player_list)
    for char in re_list:
        char.draw_brick()
        char.reverse()
    for s in right_side_list:
        s.draw_brick()
        s.right_side()
    for l in left_side_list:
        l.draw_brick()
        l.left_side() 
    for i in key_list:
        i.draw()
        i.picked_up(player_list, gate_list, enemy_list, up_enemy_list, 
                    reverse_list, big_enemy_list, br_enemy_list,
                    rimy_list, lemy_list)
    for g in gate_list:
        g.draw()
        g.picked_up(player_list, key_list, enemy_list, up_enemy_list
                    , reverse_list, big_enemy_list, br_enemy_list,
                    rimy_list, lemy_list)
    for char in enemy_list:
        char.draw_enemy()
        char.update(player_list)
        char.reset()
    for rem in reverse_list:
        rem.draw_enemy()
        rem.rmey(player_list)
        rem.reset()
    for umy in up_enemy_list:
        umy.draw_enemy()
        umy.upen(player_list)
        umy.reset()
    for char in big_enemy_list:
        char.draw_enemy()
        char.update(player_list)
        char.reset()
    for br in br_enemy_list:
        br.draw_enemy()
        br.rmey(player_list)
        br.reset()
    for char in rimy_list:
        char.draw_enemy()
        char.right_side(player_list)
        char.reset()
    for char in lemy_list:
        char.draw_enemy()
        char.left_side(player_list)
        char.reset()



    for play in player_list:
        play.update(brick_list, enemy_list,teleport_list, 
                    up_enemy_list, moving_list, reverse_list, re_list, gate_list,
                    right_side_list, left_side_list, big_enemy_list, br_enemy_list,
                    colapsing_list, rimy_list, lemy_list)
        play.draw()
        play.re()

    if play.rect.colliderect(next_level.rect):
        index += 1
        if index < len(level_list):
            current_level = level_list[index]
            load_levels(current_level)

            

   # update the screen with new drawings
    pg.display.flip()


   # limit to "FPS" frames per second
    clock.tick(FPS)


pg.quit()