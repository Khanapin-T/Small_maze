#создай игру "Лабиринт"!
from pygame import *
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Лабиринт')
background = transform.scale(image.load('background.jpg'), (win_width, win_height))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (50, 50))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 70:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 70:
            self.rect.y += self.speed

class Enemy(GameSprite):
    direction = 'left'
    def update(self):
        if self.rect.x <= 500:
            self.direction = 'right'
        if self.rect.x >= win_width - 45:
            self.direction = 'left'

        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
player = Player('packman.png', 12, 20, 4)
enemy = Enemy('ghost.png', win_width - 80, 280, 3)
final = GameSprite('treasure.png', 580, 420, 0)
wall_1 = Wall(0, 80, 210, 90, 0, 50, 420)
wall_2 = Wall(0, 80, 210, 215, 70, 50, 450)
wall_3 = Wall(0, 80, 210, 340, 0, 50, 420)
wall_4 = Wall(0, 80, 210, 465, 70, 50, 450)

mixer.init()
mixer.music.load('pacmantheme.ogg')
mixer.music.set_volume(0.4)
mixer.music.play()

fps = 60
clock = time.Clock()

game = True
finish = False

font.init()
font = font.Font(None, 70)
win = font.render('GAME WIN', True, (255, 215, 0))
lose = font.render('GAME END', True, (255, 0, 0))

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')
kick.set_volume(0.2)
kick.set_volume(0.2)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.blit(background, (0, 0))
        player.update()
        enemy.update()

        player.reset()
        enemy.reset()
        final.reset()
        wall_1.draw_wall()
        wall_2.draw_wall()
        wall_3.draw_wall()
        wall_4.draw_wall()

        if sprite.collide_rect(player, enemy) or sprite.collide_rect(player, wall_1) or sprite.collide_rect(player, wall_2) or sprite.collide_rect(player, wall_3) or sprite.collide_rect(player, wall_4):
            finish = True
            window.blit(lose, (200, 200))
            kick.play()

        if sprite.collide_rect(player, final):
            finish = True
            window.blit(win, (200, 200))
            money.play()

    display.update()
    clock.tick(fps)