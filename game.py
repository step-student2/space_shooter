import pygame
import random
from os import path
import constants as c

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image.fill(c.RED)
        self.image = pygame.transform.scale(player_img, (50, 50))
        self.image.set_colorkey(c.BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = c.WIDTH / 2
        self.rect.centery = c.HEIGHT - 50
        self.speedx = 0
        self.speedy = 0
        self.step_speed = 8

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -self.step_speed

        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = self.step_speed

        if keystate[pygame.K_UP] or keystate[pygame.K_w]:
            self.speedy = -self.step_speed

        if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
            self.speedy = self.step_speed


        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.left <= 0:
            self.rect.left = 0

        if self.rect.right >= c.WIDTH:
            self.rect.right = c.WIDTH

        if self.rect.bottom >= c.HEIGHT:
            self.rect.bottom = c.HEIGHT

        if self.rect.top <= 1:
            self.rect.top = 1

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image.fill(c.RED)
        self.image = pygame.transform.scale(mob_img, (40, 40))
        self.image.set_colorkey(c.BLACK)
        self.rect = self.image.get_rect()
        self.determine_coordinates()

    def determine_coordinates(self):
        self.rect.x = random.randrange(c.WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(2, 8)
        self.speedx = random.randrange(-2, 2)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.top > c.HEIGHT + 10 or self.rect.right <= 0 or self.rect.left >= c.WIDTH:
            self.determine_coordinates()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(c.RED)
        self.image = pygame.transform.scale(bullet_img, (10, 20))
        self.image.set_colorkey(c.BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy

        if self.rect.bottom < 0:
            self.kill()



pygame.init()
pygame.mixer.init()  # для звуку
screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

background = pygame.image.load(path.join(c.GRAPHICS, 'game_background.png'))
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(c.GRAPHICS, "space_shuttle.png")).convert()
mob_img = pygame.image.load(path.join(c.GRAPHICS, "meteor_big_00.png")).convert()
bullet_img = pygame.image.load(path.join(c.GRAPHICS, "missile.png")).convert()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

mobs = pygame.sprite.Group()
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

bullets = pygame.sprite.Group()

# Цикл гри
running = True
while running:
    # Тримаємо на певній швидкості
    clock.tick(c.FPS)
    # Введення подій
    for event in pygame.event.get():
        # перевірка закривання вікна
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.update()

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)

    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    hits = pygame.sprite.spritecollide(player, mobs, False)

    if hits:
        running = False


    screen.fill(c.BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()

