import pygame
import random
from os import path
import constants as c

score = 0

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, c.WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

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
        self.lives = 3

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
        self.image_orig = random.choice(mob_img)
        self.image_orig.set_colorkey(c.BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .90 / 2)
        self.rect.x = random.randrange(0, c.WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(2, 5)
        self.speedx = random.randrange(-3, 3)

        self.rotation = 0
        self.rotation_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_update > 50:
            self.last_update = time_now
            self.rotation = (self.rotation + self.rotation_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if (self.rect.top > c.HEIGHT + 10) or (self.rect.left < -25) or (self.rect.right > c.WIDTH + 20):
            self.rect.x = random.randrange(0, c.WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


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
mob_img = [pygame.image.load(path.join(c.GRAPHICS, "meteor_big_00.png")).convert(),
pygame.image.load(path.join(c.GRAPHICS, "meteor_big_01.png")).convert(),
pygame.image.load(path.join(c.GRAPHICS, "meteor_medium_00.png")).convert(),
pygame.image.load(path.join(c.GRAPHICS, "meteor_medium_01.png")).convert(),
pygame.image.load(path.join(c.GRAPHICS, "meteor_small_00.png")).convert(),
pygame.image.load(path.join(c.GRAPHICS, "meteor_small_01.png")).convert(),
pygame.image.load(path.join(c.GRAPHICS, "meteor_tiny.png")).convert()]
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
        score += 1

    hits = pygame.sprite.spritecollide(player, mobs, True)

    if hits:
        player.lives = player.lives - 1

    if player.lives <= 0:
        running = False

    print(player.lives)

    screen.fill(c.BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, "Score:" + str(score), 20, c.WIDTH / 2, 10) # 10px down from the screen
    draw_text(screen, "lives:" + str(player.lives), 20, c.WIDTH / 3, 10)
    pygame.display.flip()

pygame.quit()

