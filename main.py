import pygame
import random
import math


class Config(object):
    fullscreen = True
    width = 1366
    height = 768
    fps = 60


class Player(pygame.sprite.Sprite):  #player class
    s = (pygame.K_s)
    w = (pygame.K_w)
    d = (pygame.K_d)
    a = (pygame.K_a)

    def __init__(self, startpos=(102, 579)):
        super().__init__()
        self.pos = list(startpos)
        self.image = pygame.image.load('player.png')
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=startpos)
    def shoot(self,pos,angle,bullet_img):
        bullet = Bullet((self.rect.centerx, self.rect.top),angle,bullet_img)
        all_sprites_list.add(bullet)
        bullets.add(bullet)
    def update(self, seconds):
        pressedkeys = pygame.key.get_pressed()
        if pressedkeys[self.s]:
            self.rect.y += 5
        elif pressedkeys[self.w]:
            self.rect.y -= 5
        elif pressedkeys[self.a]:
            self.rect.x -= 5
        elif pressedkeys[self.d]:
            self.rect.x += 5


class Enemy(pygame.sprite.Sprite):  #enemy class

    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(200, Config.width)
        self.rect.y = random.randrange(200, Config.height)
        self.speedy = random.randrange(3, 6)

    def update(self):
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist
        self.rect.x += dx * self.speedy
        self.rect.y += dy * self.speedy
        if self.rect.x < -100:
            self.rect.x = 1400


class Bullet(pygame.sprite.Sprite):  #bullet class

    def __init__(self, pos, angle, img):
        super().__init__()
        #import image.
        self.angle = (180 / math.pi) * -angle - 90
        self.image = pygame.transform.rotate(img, self.angle)
        self.rect = self.image.get_rect()
        speed = 5
        #moves towards the mouse
        self.velocity_x = math.cos(angle) * speed
        self.velocity_y = math.sin(angle) * speed
        self.turn = pygame.transform.rotate(self.image, math.degrees(angle))
        self.pos = list(pos)

    def update(self):
        #move the bullet
        self.pos[0] += self.velocity_x
        self.pos[1] += self.velocity_y
        self.rect.center = self.pos


player = Player()

enemy_img = pygame.image.load('evilpizzaman.png')
bullet_img = pygame.image.load("pbullet.png")

enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
for x in range(0, 10):
    enemy = Enemy(enemy_img)
    enemies.add(enemy)
# sprite handling list
all_sprites_list = pygame.sprite.Group()
allgroup = pygame.sprite.LayeredUpdates()
allgroup.add(player)

for i in enemies:
    all_sprites_list.add(i)


def main():
    shoot_time = 0
    mainloop = True
    while mainloop:  #control handling
        #INTILIZE PYGAME
        pygame.init()
        screen = pygame.display.set_mode((Config.width, Config.height),
                                         pygame.FULLSCREEN)

        font = pygame.font.Font('freesansbold.ttf', 64)

        clock = pygame.time.Clock()

        millisecond = clock.tick(Config.fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
        mouse_x, mouse_y = pygame.mouse.get_pos()

        distance_x = mouse_x - player.rect.x
        distance_y = mouse_y - player.rect.y

        angle = math.atan2(distance_y, distance_x)

        shoot_time += 1
        if shoot_time%20 == 0:
          player.shoot((player.rect.x, player.rect.y), angle,bullet_img)
        #update graphics
        pygame.display.set_caption("basic bullet hell")
        screen.fill((0, 0, 0), )
        for bullet in bullets:
            if bullet.rect.x > Config.width:
                bullets.remove(bullet)
                all_sprites_list.remove(bullet)
        kill_list = pygame.sprite.groupcollide(bullets, enemies, True, True)
        game_over = pygame.sprite.groupcollide(allgroup, enemies, True, True)
        if len(allgroup) == 0:
            game_over_text = font.render("GAME OVER", True, (255, 255, 255))
            screen.blit(game_over_text, (Config.width / 2, Config.height / 2))
            pygame.display.update()
            continue
        elif len(enemies) == 0:
            game_over_text = font.render("YOU WIN", True, (255, 255, 255))
            screen.blit(game_over_text, (Config.width / 2, Config.height / 2))
            pygame.display.update()
            continue
        allgroup.update(millisecond)
        all_sprites_list.update()
        allgroup.draw(screen)
        all_sprites_list.draw(screen)
        pygame.display.update()


print(
    "arrow keys to move, space to shoot. Objective is to kill all enemies on screen"
)
main()
pygame.quit()
