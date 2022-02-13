from asyncio.constants import DEBUG_STACK_DEPTH
from pickle import FALSE
from pydoc import render_doc
import random
import pygame, sys

pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('graphics\Player\player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('graphics\Player\player_walk_2.png').convert_alpha()
        self.player_jump = pygame.image.load('graphics\Player\jump.png').convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_walk_index = 0
        self.image = self.player_walk[self.player_walk_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0
        self.animationProgressRemain = 16
        self.jump_sound = pygame.mixer.Sound('audio\jump.mp3')
        self.jump_sound.set_volume(.5)
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
        # APPLY GRAVITY
        self.gravity += 1
        self.rect.bottom += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def player_animation(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.animationProgressRemain -= 1
            if self.animationProgressRemain == 0:
                self.player_walk_index += 1
                if self.player_walk_index == 2:
                    self.player_walk_index = 0
                self.image = self.player_walk[self.player_walk_index]
                self.animationProgressRemain = 16
        
    def update(self):
        self.player_input()
        self.player_animation()

class Enemy(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == 'fly':
            eagle_frame1 = pygame.image.load('graphics\Fly\Fly1.png').convert_alpha()
            eagle_frame2 = pygame.image.load('graphics\Fly\Fly2.png').convert_alpha()
            self.frame = [eagle_frame1, eagle_frame2]
            y_pos = 210
        else:
            slime_frame1 = pygame.image.load('graphics\snail\snail1.png').convert_alpha()
            slime_frame2 = pygame.image.load('graphics\snail\snail2.png').convert_alpha()
            self.frame = [slime_frame1, slime_frame2]
            y_pos = 300
        self.animationIndex = 0
        self.image = self.frame[self.animationIndex]
        self.rect = self.image.get_rect(midbottom = (random.randint(900,1200),y_pos))
        self.animationProgressRemain = 8

    def enemy_animation(self):
        self.animationProgressRemain -= 1
        if self.animationProgressRemain == 0:
            self.animationIndex += 1
            if self.animationIndex == len(self.frame):
                self.animationIndex = 0
            self.image = self.frame[self.animationIndex]
            self.animationProgressRemain = 8

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.enemy_animation()
        self.rect.x -= 5
        self.destroy()


# INITIAL VAR
size = width, height = 800,400
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
font_hero = pygame.font.Font('font\Pixeltype.ttf',60)
font_title = pygame.font.Font('font\Pixeltype.ttf',90)
mouse = pygame.mouse
player_gravity = 0
gameActive = False
restartTime = 0
score = 0
bg_music = pygame.mixer.Sound('audio\music.wav').play()
# animationProgressRemain = 16

# INIT SURFACE BACKGROUND
pygame.display.set_caption('Runner Py')
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()


# INIT SURFACE ENEMY
# slime_frame1 = pygame.image.load('graphics\snail\snail1.png').convert_alpha()
# slime_frame2 = pygame.image.load('graphics\snail\snail2.png').convert_alpha()
# slime_frame = [slime_frame1, slime_frame2]
# slime_frame_index = 0
# slime_surface = slime_frame[slime_frame_index]

# eagle_frame1 = pygame.image.load('graphics\Fly\Fly1.png').convert_alpha()
# eagle_frame2 = pygame.image.load('graphics\Fly\Fly2.png').convert_alpha()
# eagle_frame = [eagle_frame1, eagle_frame2]
# eagle_frame_index = 0
# eagle_surface = eagle_frame[eagle_frame_index]

# enemy_list = []

# PLAYER SURFACE
# player_walk1 = pygame.image.load('graphics\Player\player_walk_1.png').convert_alpha()
# player_walk2 = pygame.image.load('graphics\Player\player_walk_2.png').convert_alpha()
# player_jump = pygame.image.load('graphics\Player\jump.png').convert_alpha()
# player_walk = [player_walk1, player_walk2]
# player_walk_index = 0
# player_surface = player_walk[player_walk_index]
# player_rect = player_surface.get_rect(midbottom =(80,300))


# TITLE SURFECE
hero_surface = pygame.image.load('graphics\Player\player_stand.png').convert_alpha()
hero_surface = pygame.transform.rotozoom(hero_surface, 0,2)
hero_rect = hero_surface.get_rect(center=(400,200))
title_text = font_title.render('RUNNER',False, '#0d0d0d')
title_rect = title_text.get_rect(center=(400,60))
start_text = font_hero.render('Press SPACE to Start',False, '#0d0d0d')
start_rect = start_text.get_rect(center=(400,350))

# TIMER
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer,1500)

# slime_timer = pygame.USEREVENT + 2
# pygame.time.set_timer(slime_timer, 500)

# eagle_timer = pygame.USEREVENT + 3
# pygame.time.set_timer(eagle_timer, 100)


# GROUP
player = pygame.sprite.GroupSingle()
player.add(Player())
enemy = pygame.sprite.Group()

# FUNCTION +
def displayScore():
    cur_score = pygame.time.get_ticks() - restartTime
    score_surface = font_hero.render(f'{cur_score//1000}', False, '#000000')
    score_rect = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface,score_rect)
    return cur_score

# def enemySpawn(enemyList):
#     if enemyList:
#         for enemy in enemyList:
#             enemy.left -= 5
#             if enemy.bottom >= 300:
#                 screen.blit(slime_surface,enemy)
#             else:
#                 screen.blit(eagle_surface,enemy)

#         enemyList = [enemy for enemy in enemyList if enemy.left > -100]
#         return enemyList
#     else:
#         return []

# def enemyCollide(playerRect, enemyList):
#     if enemyList:
#         for enemy in enemyList:
#             if playerRect.colliderect(enemy):
#                 return False
#     return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, enemy, False):
        enemy.empty()
        return False
    else: return True

# def playerAnimation():
#     global player_surface, player_walk_index, animationProgressRemain
#     if player_rect.bottom < 300:
#         player_surface = player_jump
#     else:
#         animationProgressRemain -= 1
#         print(len(player_walk))
#         if animationProgressRemain == 0:
#             player_walk_index += 1
#             if player_walk_index == 2:
#                 player_walk_index = 0
#             player_surface = player_walk[player_walk_index]
#             animationProgressRemain = 16

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

            # KEYBOARD AND MOUSE INPUT (GAME ACTIVE)
        if gameActive:
            # if event.type == pygame.KEYDOWN and player_rect.bottom >= 300:
            #     if event.key == pygame.K_SPACE:
            #         player_gravity = -20
            #         isGround = False
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if player_rect.collidepoint(event.pos):
            #         player_gravity = -20
            #         isGround = False

            # ENEMY TIMER
            if gameActive:
                if event.type == enemy_timer:
                    enemy.add(Enemy(random.choice(['fly','snail','snail','snail'])))
                    # if random.randint(0,2):
                    #     enemy_list.append(slime_surface.get_rect(midbottom = (random.randint(800,1200),300)))
                    # else:
                    #     enemy_list.append(eagle_surface.get_rect(midbottom = (random.randint(800,1200),210)))
                # if event.type == slime_timer:
                #     slime_frame_index += 1
                #     if slime_frame_index >= len(slime_frame):
                #         slime_frame_index = 0
                #     slime_surface = slime_frame[slime_frame_index]
                # if event.type == eagle_timer:
                #     eagle_frame_index += 1
                #     if eagle_frame_index >= len(eagle_frame):
                #         eagle_frame_index = 0
                #     eagle_surface = eagle_frame[eagle_frame_index]

        # RESTART GAME WHEN DIE
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                gameActive = True
                restartTime = pygame.time.get_ticks()

    if gameActive:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        score = displayScore() //1000
        # playerAnimation()

        player.draw(screen)
        player.update()

        enemy.draw(screen)
        enemy.update()

        # screen.blit(player_surface,player_rect)
        # enemy_list = enemySpawn(enemy_list)

        # COLLISION 
        gameActive = collision_sprite()
        # for enemy in enemy_list:
        #     if player_rect.colliderect(enemy):
        #         gameActive = False
        # gameActive = enemyCollide(player_rect, enemy_list)

        # player_gravity += 1
        # player_rect.y += player_gravity
        # if player_rect.bottom >= 300:
        #     player_rect.bottom = 300
    else:
        screen.fill('#eaeaea')
        screen.blit(start_text,start_rect)
        screen.blit(hero_surface, hero_rect)
        if(score == 0):
            screen.blit(title_text,title_rect)
        else:
            score_text = font_hero.render(f'Your Score : {score}',False, '#0d0d0d')
            score_rect = score_text.get_rect(center=(400,50))
            screen.blit(score_text,score_rect)

        # player_rect.midbottom=(80,300)
        # player.rect.bottom = 300
        player_gravity = 0

    pygame.display.update()
    clock.tick(60)