import pygame
import random

WIDTH = 480
HEIGHT = 600
FPS = 60

Background = pygame.image.load("Background.png")
size = WIDTH/Background.get_size()[0]
Background = pygame.transform.scale(Background,(size*Background.get_size()[0],size*Background.get_size()[1]))

BLACK = (0, 0, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
Bgrect = Background.get_rect()
clock = pygame.time.Clock()

gameover = False

class Player(pygame.sprite.Sprite):

    player_img = pygame.image.load("Player.png")

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Player.player_img,(HEIGHT/8,HEIGHT/8))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 50
        self.gravity = 25
        self.speed = 0

    def update(self):
        if self.speed != 0:
            if self.speed > 0:
                self.speed -= 1
            if self.speed < 0:
                self.speed += 1
        self.gravity -= 1
        if self.rect.y - self.gravity > HEIGHT/3:
            self.rect.y -= self.gravity
        else:
            for sprite in all_sprites.sprites():
                sprite.rect.y += self.gravity

        key = pygame.key.get_pressed()

        if key[pygame.K_a]:
            self.speed -= 2
        if key[pygame.K_d]:
            self.speed += 2
        
        self.rect.x += self.speed
        self.rect.x = self.rect.x % WIDTH

class Rock(pygame.sprite.Sprite):

    image = pygame.image.load("Rock.png")

    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Rock.image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 0
        rdi = random.randint(1,200)
        if rdi == 1:
            self.mob = Mob(x,y)
            mobs.add(self.mob)
            all_sprites.add(self.mob)
        elif rdi == 2:
            self.spring = Spring(x,y)
            springs.add(self.spring)
            all_sprites.add(self.spring)

    def update(self):
        self.rect.x += self.speed
        self.rect.x = self.rect.x % WIDTH

        if self.rect.top > HEIGHT:
            while True:
                rx = random.randint(50,430)
                ry = random.randint(-150,-5)
                rock = Rock(rx,ry)
                rock.rect = rock.rect.inflate(0,80)
                if not pygame.sprite.spritecollide(rock,rocks,False):
                    rock.rect = rock.rect.inflate(0,-80)
                    rocks.add(rock)
                    all_sprites.add(rock)
                    break
                else:
                    rock.kill()
            self.kill()

    def kill(self):
        try:
            self.mob.kill()
        except:
            pass
        try:
            self.spring.kill()
        except:
            pass
        super().kill()

class Mob(pygame.sprite.Sprite):

    image = pygame.image.load("Mob.png")

    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Mob.image,(HEIGHT/8,HEIGHT/8))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y - 40

    def update(self):
        if self.rect.top > HEIGHT:
            self.kill()

class Spring(pygame.sprite.Sprite):

    image = pygame.image.load("Spring.png")

    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Spring.image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y - 15

    def update(self):
        if self.rect.top > HEIGHT:
            self.kill()

all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()

rocks = pygame.sprite.Group()
mobs = pygame.sprite.Group()
springs = pygame.sprite.Group()

for _ in range(10):
    while True:
        rx = random.randint(50,430)
        ry = random.randint(50,450)
        rock = Rock(rx,ry)
        rock.rect = rock.rect.inflate(0,80)
        if not pygame.sprite.spritecollide(rock,rocks,False):
            rock.rect = rock.rect.inflate(0,-80)
            rocks.add(rock)
            all_sprites.add(rock)
            break
        else:
            rock.kill()

player = Player()
players.add(player)

stop = True

while not gameover:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                stop = False
                
    if not stop:
        all_sprites.update()
        players.update()

    if pygame.sprite.spritecollide(player,rocks,False):
        if player.gravity < -7:
            player.gravity = 25

    if pygame.sprite.spritecollide(player,mobs,False):
        gameover = True

    if pygame.sprite.spritecollide(player,springs,False):
        if player.gravity < -2:
            player.gravity = 45

    if player.rect.top > HEIGHT:
        gameover = True

    screen.fill(BLACK)
    screen.blit(Background,Bgrect)

    all_sprites.draw(screen)
    players.draw(screen)

    pygame.display.flip()

pygame.quit()