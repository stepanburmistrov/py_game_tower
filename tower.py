import pip
pip.main(['install', 'pygame'])
import pygame
import random
import os
from colorsys import hsv_to_rgb as convert

width = 300
height = 500
fps = 30
TOWER_SCREEN_SIZE = 8
direction = 5
level_size = 200
levels = []
current_level = 0
game_over = False
last_left = -1000
last_right = 1000
H = random.randint(1, 359)

def conv_color(h):
    r, g, b = convert(H / 360, 1, 1)
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return (r,g,b)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

bg = pygame.image.load('bg.jpg')
game_over_img = pygame.image.load('game_over.png').convert_alpha()


class Level(pygame.sprite.Sprite):
    def __init__(self, color=conv_color(H), img=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((level_size, 30))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        if current_level <= TOWER_SCREEN_SIZE:
            y = 485 - current_level * 31
        else:
            y = 485 - (TOWER_SCREEN_SIZE + 1) * 31
        self.rect.center = (random.randint(0, 300), y)

    def changeSize(self, newSize, newX):
        self.image = pygame.Surface((newSize, 30))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        if current_level <= TOWER_SCREEN_SIZE:
            y = 485 - current_level * 31
        else:
            y = 485 - TOWER_SCREEN_SIZE * 31
        self.rect.center = (newX, y)

        self.font = pygame.font.SysFont("Arial", 25)
        self.textSurf = self.font.render(str(current_level), 1, (0, 0, 0))
        W = self.textSurf.get_width()
        self.image.blit(self.textSurf, [int(newSize / 2 - W / 2), 1])


all_sprites = pygame.sprite.Group()
levels.append(Level())
all_sprites.add(levels[current_level])


def check_events(e):
    global running, H, direction, level_size, last_left, last_right, levels, current_level, game_over, all_sprites
    for event in e:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            H += 10
            print(H)
            if H > 360:
                H -= 360
            direction = 0
            current_left = levels[current_level].rect.left
            current_right = levels[current_level].rect.right
            new_left = max(last_left, current_left)
            new_right = min(last_right, current_right)
            level_size = new_right - new_left
            if level_size > 0:
                new_x = (new_right + new_left) // 2
                levels[current_level].changeSize(level_size, new_x)
                last_right = new_right
                last_left = new_left
                if current_level > TOWER_SCREEN_SIZE:
                    for i in range(0, current_level):
                        levels[i].rect.y += 31

        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                direction = 5
                level_size = 200
                levels = []
                current_level = 0
                game_over = False
                last_left = -1000
                last_right = 1000
                all_sprites = pygame.sprite.Group()
                levels.append(Level())
                all_sprites.add(levels[current_level])


running = True
while running:
    events = pygame.event.get()
    if events != []:
        # print(events)
        check_events(events)

    levels[current_level].rect.x += direction
    if levels[current_level].rect.x > width or levels[current_level].rect.x < -level_size:
        direction *= -1

    if direction == 0 and level_size > 0:
        current_level += 1
        direction = random.choice([5, -5])
        levels.append(Level(conv_color(H)))
        all_sprites.add(levels[current_level])
    elif level_size <= 0:
        game_over = True

    #screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    all_sprites.draw(screen)
    if game_over:
        screen.blit(game_over_img, (75, 100))

    clock.tick(fps)
    pygame.display.flip()

pygame.quit()
