
from cgitb import reset
import pygame
import animation
import random

def drawText(t, x, y):
    text = font.render(t, True, WHITE, GRAY)
    text_rectangle = text.get_rect()
    text_rectangle.topleft = (x,y)
    screen.blit(text,text_rectangle)


# constant variables
SCREEN_SIZE = (700,500)
GRAY = (50,50,50)
WHITE = (255, 255, 255)
RED = (242, 15, 60)




# init
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Sophomore Project')
clock = pygame.time.Clock()
font = pygame.font.Font(pygame.font.get_default_font(), 24)

# game states
game_state = 'title screen'
wait = 0
# player
player_image = pygame.image.load('images/Greg_idle0.png')
player_x = 300

player_y = 0
player_speed = 0
player_acceleration = 0.2
player_colstate = 'hitable'
player_collision = True
player_width = 34
player_hight = 51
mid_player_height = 26

new_player_x = player_x
new_player_y = player_y

player_direction = 'right'
player_state = 'idle' # or walking

player_animations = { 
    'idle' : animation.Animation([
        pygame.image.load('images/Greg_idle0.png'),
        pygame.image.load('images/Greg_idle1.png'),
        pygame.image.load('images/Greg_idle2.png'),
        pygame.image.load('images/Greg_idle3.png'),
        pygame.image.load('images/Greg_idle4.png'),
        pygame.image.load('images/Greg_idle5.png'),
        pygame.image.load('images/Greg_idle6.png'),
        pygame.image.load('images/Greg_idle7.png'),
        pygame.image.load('images/Greg_idle8.png')
        ]),
    'walking' : animation.Animation([
        pygame.image.load('images/Greg_walking0.png'),
        pygame.image.load('images/Greg_walking1.png'),
        pygame.image.load('images/Greg_walking2.png'),
        pygame.image.load('images/Greg_walking3.png'),
        pygame.image.load('images/Greg_walking4.png'),
        pygame.image.load('images/Greg_walking5.png'),
        pygame.image.load('images/Greg_walking6.png'),
        pygame.image.load('images/Greg_walking7.png')
        ]),
    'fall' : animation.Animation([
        pygame.image.load('images/Jump4.png')
    ])
}

if player_speed == 0:
    player_state = 'idle'

player_enemy_collision = True 


# enemies
enemy_state = 'alive'
enemy_direction = 'right'
enemy_image = animation.Animation([
    pygame.image.load('images/spike_monster.png'),
    ])
enemy_width = 50
enemy_hight = 26
enemy_x = 150
enemy_y = 274
enemy_collision = True
enemy_speed = 0.5

# Hearts
lives = 3
Life_images = pygame.image.load('images/heart.png')



# platforms
platforms = [
    # middle
    pygame.Rect(100,300,400,50),
    # left
    pygame.Rect(100,250,50,50),
    # right
    pygame.Rect(450,250,50,50)
    
]

Rplatform = pygame.Rect(450,250,50,50)

Lplatform = pygame.Rect(100,250,50,50)

# coins
coin_image = pygame.image.load('images/coin_0.png')

coins = [
    pygame.Rect(200,250,23,23),
    pygame.Rect(100,200,23,23)
    
]
coin_animations = animation.Animation([
        pygame.image.load('images/coin_0.png'),
        pygame.image.load('images/coin_1.png'),
        pygame.image.load('images/coin_2.png'),
        pygame.image.load('images/coin_3.png'),
        pygame.image.load('images/coin_4.png'),
        pygame.image.load('images/coin_5.png')
    ])

score = 0

#Projectiles
projectile_image = animation.Animation([
    pygame.image.load('images/tempprojectile0.png')
        ])
projectile_state = 'idle'
proj_collide = False


running = True
while running == True:
# game loop

    # -----
    # INPUT
    # -----

    # check for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           running = False 

    if game_state == 'playing':

        new_player_x = player_x
        new_player_y = player_y
        
        # player input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            new_player_x -= 2
            player_state = 'walking'
            player_direction = 'left'
        if keys[pygame.K_RIGHT]:
            new_player_x += 2
            player_state = 'walking'
            player_direction = 'right'
        if keys[pygame.K_UP] and play_on_ground:
            player_speed = -6
            player_state = 'fall'
        if keys[pygame.K_LSHIFT] and keys[pygame.K_RIGHT]:
            new_player_x += 3
        if keys[pygame.K_LSHIFT] and keys[pygame.K_LEFT]:
            new_player_x -= 3
        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_UP]:
            player_state = 'idle'
        if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
            player_state = 'idle'
        if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
            player_state = 'fall'
    
    
        if enemy_state == 'alive' and game_state == 'playing':
            if enemy_state == 'alive':
                enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_hight)
            if new_player_x >= enemy_x:
                enemy_x += enemy_speed
                enemy_direction = 'right'
                if enemy_rect.colliderect(Rplatform):
                        break
            elif new_player_x <= enemy_x:
                enemy_x -= enemy_speed
                enemy_direction = 'left'
                if enemy_rect.colliderect(Lplatform):
                        break
            

# -----
# UPDATE
# -----
    
    
        # update player animation
        player_animations[player_state].update()

        # coin animations
        coin_animations.update()

        # horizontal movment

        new_player_rect = pygame.Rect(new_player_x,new_player_y,player_width,player_hight)
        x_collision = False

        #...check against every platfrom
        for p in platforms:
            if p.colliderect(new_player_rect):
                x_collision = True
                break
            
        timer = (wait + 1)
        
        if x_collision == False:
            player_x = new_player_x

        # verical movement
        

        player_speed += player_acceleration
        new_player_y += player_speed
        
        new_player_rect = pygame.Rect(new_player_x,new_player_y,player_width,player_hight)
        y_collision = False
        play_on_ground = False
       
        #...check against every platfrom
        for p in platforms:
            if p.colliderect(new_player_rect):
                y_collision = True
                player_speed = 0
                # if the platfor is below the player
                if p[1] > new_player_y:
                    # stick the player to the platform
                    player_y = p[1] - player_hight
                    play_on_ground = True
                break
        if player_speed == 0.3:
            player_state = 'fall'

        if y_collision == False:
            player_y = new_player_y
        
        if player_speed > .4:
            player_state = 'fall'
        elif player_speed <= -6:
            player_state = 'fall'
        

        # see if any coins have been collected
        player_rect = pygame.Rect(player_x, player_y, player_width, player_hight)
        for c in coins:
            if c.colliderect(player_rect):
                coins.remove(c)
                score += 1
                 #win
                if score >= 3:
                    game_state = 'win'


        # see if player has hit enemy
        if enemy_collision == True:
            if enemy_rect.colliderect(new_player_rect):
                player_colstate = 'iframe'
                lives -= 1
                player_enemy_collision = False
                if player_enemy_collision == False:
                    enemy_collision == False
            #if lives <= 0:
             #   game_state = 'lose'
        
            if player_colstate == 'iframe':
                player_collision = False

            if enemy_state == "ded":
                enemy_collision = False
            
        
    # -----
    # DRAW
    # -----

    

    # background
    screen.fill(GRAY)

    if game_state == 'playing':

        # score
        drawText('score: ' + str(score), 10, 10)

        # lives
        for l in range(lives):
            screen.blit(Life_images, (20 +(l*30), 74))

        # Platforms
        for p in platforms:
            pygame.draw.rect(screen, WHITE, p) 

        # Coins
        for c in coins:
            coin_animations.draw(screen, c.x, c.y, False, False)         

        # Ememy
        if enemy_state == "alive" and game_state == 'playing':
            if enemy_direction == 'right':
                enemy_image.draw(screen, enemy_x, enemy_y, True, False)
            elif enemy_direction == 'left':
                enemy_image.draw(screen, enemy_x, enemy_y, False, False)
        

        # Player
        if player_direction == 'right':
            # pygame.blit(player_x, player_y)
            player_animations[player_state].draw(screen, player_x, player_y, False, False)
        elif player_direction == "left":
            #screen.blit(pygame.transform.flip(player_image, True, False), (player_x, player_y))
            player_animations[player_state].draw(screen, player_x, player_y, True, False)
         
        
        
        if keys[pygame.K_t]:
            projectile_state = 'spawned'
            projectile_x = new_player_x
            projectile_y = new_player_y +25
            projectile_width = 15
            projectile_hight = 5
            new_projectile_rect = pygame.Rect(projectile_x, projectile_y, projectile_width, projectile_hight)
            if player_direction == 'right':
                    projectile_direction = 'right'
            elif player_direction == 'left':
                    projectile_direction = 'left'    
            proj_collide = False
            

        if projectile_state == 'spawned' and proj_collide == False:
            new_projectile_rect = pygame.Rect(projectile_x, projectile_y, projectile_width, projectile_hight)
            new_proj_x = projectile_x
            for p in new_projectile_rect:
                if projectile_direction == 'right':
                    if proj_collide == False:
                        projectile_image.draw(screen, projectile_x, projectile_y, False, False)
                        projectile_x += 3   
                elif projectile_direction == 'left':
                     if proj_collide == False:
                        projectile_image.draw(screen, projectile_x, projectile_y, True, False)
                        projectile_x -= 3
            for p in platforms:
               if p.colliderect(new_projectile_rect):
                projectile_state = 'idle'
            
            
            if enemy_rect.colliderect(new_projectile_rect):
                projectile_state = 'idle'
                enemy_state = 'ded'
                score += 1
    
    if game_state == 'title screen':
        drawText(' Title Screen ', 50, 50)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
            game_state = 'playing'
    
    if game_state == 'win':
        drawText(' YOU WON PRESS R TO RESTART ', 50, 50)
    if game_state == 'lose':
        drawText(' YOU LOST PRESS R TO RESTART', 50, 50)

    
    #reset game
    if keys[pygame.K_r]:
        lives = 3
        enemy_state = 'alive'
        game_state = 'title screen'
        player_x = 300
        player_y = 0
        score = 0
          
     
     # present screen
    pygame.display.flip()

    clock.tick(60)


    

# quit
pygame.quit()