import pygame, random, sys
from pygame import mixer
from pygame.locals import *
from time import sleep

#DEKLARASI VARIABEL
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

#CLASS UNTUK PESAWAT KITA, SEBAGAI PLAYER
class Plane(pygame.sprite.Sprite):
    jumpable = True #Untuk mengetahui apakah pesawat ini masih bisa melompat atau tidak
    
    def __init__(self):
        #INISIALISASI, LOADING GAMBAR, DAN SETTING POSISI AWAL
        pygame.sprite.Sprite.__init__(self)

        self.speed = SPEED

        self.image = pygame.image.load('Assets/plane.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

        self.rect[0] = SCREEN_WIDTH / 2
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
        #LOGIC YANG BERJALAN TIAP WAKTU
        #DALAM HAL INI, SET POSISI Y PESAWAT = KECEPATAN JATUH PESAWAT
        self.rect[1] += self.speed
        self.speed += GRAVITY

    def explode (self):
        #PESAWAT MELEDAK, DAN GAMBAR PESAWAT DIGANTI DENGAN EFEK LEDAKAN
        self.image = pygame.image.load('Assets/explode.png').convert_alpha()

    def bump(self):
        #BUAT PESAWAT MELOMPAT
        if self.jumpable:
            self.speed = -SPEED


#CLASS UNTUK GEDUNG
class Building(pygame.sprite.Sprite):
    def __init__(self, ypos):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load('Assets/gedung.png').convert_alpha(),
                       pygame.image.load('Assets/gedung-2.png').convert_alpha()]
        
        self.image = self.images[random.randint (0, 1)].convert_alpha()

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH
    
        self.rect[1] = ypos
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        #GESER KE KIRI SEJAUH GAME_SPEED (DALAM HAL INI, 9 UNIT)
        self.rect[0] -= GAME_SPEED 

#CLASS UNTUK PESAWAT MUSUH
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.speed = SPEED

        self.current_image = 0 

        self.image = pygame.image.load('Assets/reverse-plane.png').convert_alpha()
        
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

        self.rect[0] = SCREEN_WIDTH + 10

        #SET POSISI Y PESAWAT AGAR MENJADI RANDOM
        self.rect[1] = random.randint (0, SCREEN_HEIGHT - 200)

    def update(self):
        #SAMA SEPERTI UPDATE PADA GEDUNG, BEDANYA INI LEBIH CEPAT
        self.rect[0] -= (GAME_SPEED + 10)

#CLASS UNTUK GROUND
class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Assets/new-floor.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT
    def update(self):
        #SAMA SEPERTI GEDUNG, NAMUN GERAKANNYA LEBIH LAMBAT UNTUK MEMBERIKAN EFEK PARALLAX
        self.rect[0] -= GAME_SPEED + 5

#CLASS UNTUK KERETA YANG MELEWAT (HANYA KOSMETIK SAJA)
class Train(pygame.sprite.Sprite):
    flip = 0
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.flip = random.randint (0, 1)
        self.image = pygame.image.load('Assets/train.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        #SETTING POSISI AWAL KERETA, DARI ARAH KANAN ATAU KIRI
        if self.flip == 0:
            self.rect[0] = SCREEN_WIDTH + 100
        else:
            self.rect[0] = -(SCREEN_WIDTH + 100)
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        #UPDATE JALAN KERETA SESUAI ARAH GERAKNYA
        if self.flip == 0:
            self.rect[0] -= GAME_SPEED + 15
        else:
            self.rect[0] += GAME_SPEED - 2

#FUNGSI UNTUK MENGECEK, APAKAH SUATU SPRITE DILUAR LAYAR ATAU TIDAK
def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

#PROSEDUR UNTUK SKOR DAN HIGH SCORE
def info():
    global score, record

    if score > record:
        record = score

#VARIABEL UNTUK TIMER KERETA DAN GEDUNG, NANTINYA AKAN DIRANDOMIZE
time = 4
train_time = 50

#PROSEDUR UNTUK MEMULAI GAME
def start_the_game():
    menu = True
    running = False
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption ("Flappy Plane")

    #Play musik secara loop
    mixer.music.load('Sounds/Bonetrousle.mp3')
    mixer.music.play(-1)    
    
    BACKGROUND = pygame.image.load('Assets/new-background.png')

    plane_group = pygame.sprite.Group()
    plane = Plane()
    plane_group.add(plane)

    #Buat group, karena nantinya tidak hanya 1 sprite yang dibuat
    ground_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group ()
    train_group = pygame.sprite.Group ()
    Building_group = pygame.sprite.Group()

    #BUAT 2 GROUND SEKALIGUS, AGAR TIDAK TERPUTUS PUTUS
    for i in range(2):
        ground = Ground(2 * SCREEN_WIDTH * i)
        ground_group.add(ground)

    #ground = Ground(2 * SCREEN_WIDTH)
    #ground_group.add(ground)

    enemy = Enemy ()
    enemy_group.add (enemy)

    train = Train ()
    train_group.add (train)

    Buildings = Building(random.randint (140, 200) + 50)
    Building_group.add(Buildings)

    clock = pygame.time.Clock()

    global score, record
    score = 0
    time = 30
    train_time = 50

    running = True

    #Logic yang akan berjalan terus menerus
    while running:
        #Loading font, dan kurangi time dan train_time agar dapat di spawn lagi nantinya
        font = pygame.font.SysFont(pygame.font.get_default_font(), 60)
        time -= 1
        train_time -= 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #Keluar game
                running = False
                pygame.quit()
                sys.exit ()
                break
            elif event.type == pygame.MOUSEBUTTONDOWN and menu == True:
                if event.button == 1:
                    #Mulai timer, dan start game
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
                    #Buat pesawat meloncat ketika user menekan tombol space
                    plane.bump()

        #Update game dengan 30 fps, dan render background
        clock.tick(30)
        screen.blit(BACKGROUND,
                    (0, 0))

        if menu == True:
            #Kondisi ketika menu = True, maka render menu dulu
            font = pygame.font.SysFont(pygame.font.get_default_font(), 60)
            ground_group.draw(screen)
            txt = font.render("CLICK TO START", True, (255,255,255))
            font.bold = True
            screen.blit(txt, (SCREEN_WIDTH/3.5, 200))
            
            ground_group.draw(screen)
        if menu == False:
            #Kondisi ketika menu = False, game dimulai sampai game over

            #Kondisi ketika ground sudah di luar layar, maka hapus yang diluar layar, tambahkan yang baru
            if is_off_screen(ground_group.sprites()[0]):
                ground_group.remove(ground_group.sprites()[0])
                new_ground = Ground(GROUND_WIDTH - 20)
                ground_group.add(new_ground)

            #Kondisi ketika enemy sudah di luar layar, maka hapus yang diluar layar, tambahkan yang baru
            if is_off_screen(enemy_group.sprites()[0]):
                enemy_group.remove(enemy_group.sprites()[0])
                new_enemy = Enemy()
                enemy_group.add(new_enemy)

            #Kondisi ketika gedung sudah di luar layar, maka hapus yang diluar layar, tambahkan score
            for x in Building_group.sprites ():
                if is_off_screen(x):
                    Building_group.remove(x)
                    mixer.Sound('Sounds/Score.mp3').play ()
                    score += 1

            #Kondisi ketika kereta sudah di luar layar, maka hapus yang diluar layar
            for x in train_group.sprites ():
                if x.rect [0] < -(SCREEN_WIDTH * 2) or x.rect [0] > SCREEN_WIDTH * 2:
                    train_group.remove(x)
                    
            #Kondisi ketika time = 0, maka spawn gedung baru, dan setting time menjadi random
            if time <= 0:
                time = random.randint (50, 90)
                Buildings = Building(random.randint (140, 200) + 50)
                Building_group.add(Buildings)
            
            #Kondisi ketika train_time = 0, spawn kereta baru, dan setting train_time menjadi random
            if train_time <= 0:
                train_time = random.randint (100, 200)
                train = Train ()
                train_group.add (train)

            #Update ground, enemy, kereta, dan gedung, lalu tampilkan di layar
            ground_group.update()
            enemy_group.update ()
            train_group.update ()
            Building_group.update()
              
            
            Building_group.draw(screen)
            train_group.draw(screen)
            ground_group.draw(screen)
            enemy_group.draw(screen)
            
            font = pygame.font.SysFont(pygame.font.get_default_font(), 80)

            #Mekanisme game over baru = Ketika pesawat sudah di atas layar, maka matikan input sehingga tidak bisa meloncat lagi
            if plane_group.sprites ()[0].rect[1] <= 0:
                plane.jumpable = False

            #Kalau pesawat kita bertabrakan dengan ground, musuh, atau gedung, maka game over
            if (pygame.sprite.groupcollide(plane_group, ground_group, False, False, pygame.sprite.collide_mask) or
                    pygame.sprite.groupcollide(plane_group, Building_group, False, False, pygame.sprite.collide_mask) or
                    pygame.sprite.groupcollide(plane_group, enemy_group, False, False, pygame.sprite.collide_mask)):
                mixer.music.stop ()
                hit_sound = mixer.Sound('Sounds/hit.wav')
                hit_sound.play()

                #Duar
                plane.explode ()
                plane_group.update()
                plane_group.draw(screen)
                pygame.display.update ()

                #Kasih timer 1 detik, kalau pesawatnya itu benar benar meledak
                sleep (1)

                #Tampilkan game over dan skor
                gameover = mixer.Sound('Sounds/Lose sound effects.mp3')
                gameover.play()
                font1 = pygame.font.SysFont("arial", 33)
                pygame.draw.rect(screen, 0x543847, [SCREEN_WIDTH/4, 104, 400, 200 ], 10)
                pygame.draw.rect(screen, 0xDED895, [(SCREEN_WIDTH/4)+5, 108, 390, 190])
                font2 = pygame.font.SysFont("arial", 33)
                font2.bold = True
                screen.blit(font2.render('GAME OVER', True, (0, 0, 0)), ((SCREEN_WIDTH/2) - 80, 120))
                txt = font1.render("Your Score", 0, (0,0,255))
                screen.blit(txt, ((SCREEN_WIDTH/2) - 100, 170))
                txt = font1.render(str(score), 0, (0,0,0))
                screen.blit(txt, ((SCREEN_WIDTH/2) + 100, 170))
                txt = font1.render("Highest Score", 0, (0,0,255))
                screen.blit(txt, ((SCREEN_WIDTH/2) - 100, 220))
                txt = font1.render(str(record), 0, (0,0,0))
                screen.blit(txt, ((SCREEN_WIDTH/2) + 100, 220))
                info()
                pygame.display.flip()

                #Restart game setelah 5 detik
                sleep(5)
                start_the_game()
            else:
                txt = font.render(str(score), 0, (255, 255, 255))
                screen.blit(txt, (100, 50))

            #Update logic pesawat kita, karena semua logic harus di update sebelum di render
            #Khusus pesawat saja, ditaruh di paling akhir
            plane_group.update ()
            plane_group.draw(screen)
        pygame.display.update()

#   FUNGSI UTAMA, UNTUK MENJALANKAN GAMENYA
start_the_game()