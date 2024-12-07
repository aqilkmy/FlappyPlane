import pygame, random
from pygame import mixer
from pygame.locals import *
from time import sleep

# TAMBAH ENEMY, TAMBAH COLLIDERNYA, RANDOMIZE POSISINYA, FLIP GAMBARNYA, NUNGGU ROMY (DONE)
# PARALLAX 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

SPEED = 8
GRAVITY = 0.8
GAME_SPEED = 9

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

Building_WIDTH = 80
Building_HEIGHT = 500
Building_GAP = 120

score = 0
record = 0

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.speed = SPEED

        self.current_image = 0 

        self.image = pygame.image.load('plane.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

        self.rect[0] = SCREEN_WIDTH / 2
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
        self.rect[1] += self.speed
        self.speed += GRAVITY

    def bump(self):
        self.speed = -SPEED


class Building(pygame.sprite.Sprite):

    def __init__(self, ypos):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load('gedung.png').convert_alpha(),
                       pygame.image.load('gedung-2.png').convert_alpha()]
        
        self.image = self.images[random.randint (0, 1)].convert_alpha()

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH
    
        self.rect[1] = ypos
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED 

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.speed = SPEED

        self.current_image = 0 

        self.image = pygame.image.load('reverse-plane.png').convert_alpha()
        
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

        self.rect[0] = SCREEN_WIDTH + 10  # X position that the bird starts

        self.rect[1] = random.randint (0, SCREEN_HEIGHT - 200)  # Y position that the bird starts

    def update(self):
        self.rect[0] -= (GAME_SPEED + 10)

class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('floor.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos # x position
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT # y position

    def update(self):
        self.rect[0] -= GAME_SPEED #floor speed

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])  # verify if any sprite is off the screen

#function to count the score after passing Buildings
def info():
    global score, record

    if score > record:
        record = score

time = 4

# function to start the game
def start_the_game():
    menu = True
    running = False
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption ("Flappy Plane")

    # main song
    mixer.music.load('game.wav')
    mixer.music.play(-1)    
    
    # background image
    BACKGROUND = pygame.image.load('background-day.png')
    BACKGROUND = pygame.transform.scale(BACKGROUND, (
    SCREEN_WIDTH, SCREEN_HEIGHT))  # it transforms the size of the background image to the same size as the screen

    bird_group = pygame.sprite.Group()
    bird = Bird()
    bird_group.add(bird)

    ground_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group ()

    for i in range(2):
        ground = Ground(2 * SCREEN_WIDTH * i)
        ground_group.add(ground)

    enemy = Enemy ()
    enemy_group.add (enemy)

    Building_group = pygame.sprite.Group()
    for i in range(2):
        Buildings = Building(random.randint (140, 200)) # distance between Buildings
        Building_group.add(Buildings)

    clock = pygame.time.Clock()  # Frames Per Second

    global score, record
    score = 0
    time = 30

    running = True

    while running:  # main loop, what keeps the game running
        font = pygame.font.SysFont(pygame.font.get_default_font(), 60)
        time -= 1
        # menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                break
            elif event.type == pygame.MOUSEBUTTONDOWN and menu == True:
                if event.button == 1:
                    screen.blit(BACKGROUND, (0, 0))
                    ground_group.draw(screen)
                    pygame.display.flip()
                    sleep(0.3)
                    screen.blit(font.render('3', True, (255, 255, 255)), (400, 250))
                    pygame.display.flip()
                    sleep(1)
                    screen.blit(BACKGROUND, (0, 0))
                    ground_group.draw(screen)
                    pygame.display.flip()
                    screen.blit(font.render('2', True, (255, 255, 255)), (400, 250))
                    pygame.display.flip()
                    sleep(1)
                    screen.blit(BACKGROUND, (0, 0))
                    ground_group.draw(screen)
                    pygame.display.flip()
                    screen.blit(font.render('1', True, (255, 255, 255)), (400, 250))
                    pygame.display.flip()
                    sleep(1)
                    screen.blit(BACKGROUND, (0, 0))
                    ground_group.draw(screen)
                    pygame.display.flip()
                    menu = False

            if event.type == KEYDOWN and menu == False:
                if event.key == K_SPACE:
                    bird.bump()

        clock.tick(30)
        screen.blit(BACKGROUND,
                    (0, 0))  # takes the surface of the background and draws on the screen from the position (x, y)

        if menu == True:
            # write the message on the first screen
            font = pygame.font.SysFont(pygame.font.get_default_font(), 60)
            ground_group.draw(screen)
            txt = font.render("CLICK TO START", True, (255,255,255))
            screen.blit(txt, (250, 250))
            font = pygame.font.SysFont(pygame.font.get_default_font(), 25)
            ground_group.draw(screen)
            txt = font.render("ONCE GAME STARTS, PRESS SPACE TO MAKE THE PLANE BUMPS", True, (0, 0, 0))
            screen.blit(txt, (150, 300))
        if menu == False:
            if is_off_screen(ground_group.sprites()[0]):
                ground_group.remove(ground_group.sprites()[0]) # removes the ground if it is off the screen
                new_ground = Ground(GROUND_WIDTH - 20)
                ground_group.add(new_ground)

            if is_off_screen(enemy_group.sprites()[0]):
                enemy_group.remove(enemy_group.sprites()[0]) # removes the ground if it is off the screen
                new_enemy = Enemy()
                enemy_group.add(new_enemy)

            for x in Building_group.sprites ():
                if is_off_screen(x):
                    Building_group.remove(x )  # removes the Building if it is off the screen
                    score += 1
            
            if time <= 0:
                time = random.randint (30, 70)
                Buildings = Building(random.randint (140, 200))
                Building_group.add(Buildings)

            bird_group.update()
            ground_group.update()
            enemy_group.update ()
            Building_group.update()
            
            bird_group.draw(screen)
            Building_group.draw(screen)
            ground_group.draw(screen)
            enemy_group.draw(screen)
            
            font = pygame.font.SysFont(pygame.font.get_default_font(), 80)
            if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
                    pygame.sprite.groupcollide(bird_group, Building_group, False, False, pygame.sprite.collide_mask) or
                    pygame.sprite.groupcollide(bird_group, enemy_group, False, False, pygame.sprite.collide_mask)):# "mask" makes that only the pixels that have any color in the bird collide with the pixels of the floor or Building
                # hit sound
                hit_sound = mixer.Sound('hit.wav')
                hit_sound.play()
                # creates the box at the end
                font1 = pygame.font.SysFont("arial", 33)
                pygame.draw.rect(screen, 0x543847, [SCREEN_WIDTH/4, 104, 400, 200 ], 10)
                pygame.draw.rect(screen, 0xDED895, [(SCREEN_WIDTH/4)+5, 108, 390, 190])
                font2 = pygame.font.SysFont("arial", 33)
                screen.blit(font2.render('GAME OVER', True, (255,0,0)), ((SCREEN_WIDTH/2) - 50, 120))
                txt = font1.render("Your Score", 0, (0,0,255))
                screen.blit(txt, ((SCREEN_WIDTH/2) - 80, 150))
                txt = font1.render(str(score), 0, (0,0,0))
                screen.blit(txt, ((SCREEN_WIDTH/2), 180))
                txt = font1.render("Highest Score", 0, (0,0,255))
                screen.blit(txt, ((SCREEN_WIDTH/2) - 80, 220))
                txt = font1.render(str(record), 0, (0,0,0))
                screen.blit(txt, ((SCREEN_WIDTH/2), 250))
                info()
                pygame.display.flip()
                sleep(5)
                start_the_game()
            else:
                # creates the score on the screen during the game
                txt = font.render(str(score), 0, (255, 255, 255))
                screen.blit(txt, (SCREEN_WIDTH/2, 50))
        pygame.display.flip()

start_the_game()