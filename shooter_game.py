from pygame import *
from random import randint

#constants
windowWidth = 1000
windowHeight = 700


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, img_x, img_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (img_x, img_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):

    def update(self):

        global bulletmim

        self.rect.y += self.speed
        if self.rect.y<=-10:
            self.kill()
            bulletmim+=1

class Player(GameSprite):

    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_RIGHT] and self.rect.x < windowWidth-65:
            self.rect.x += self.speed
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed

    def fire(self):
        bullets.add(Bullet("sword.png", self.rect.centerx, self.rect.top, -4, 20, 100))

lost = 0

class UFO(sprite.Sprite):

    def __init__(self, player_image, player_x, player_y, player_speed, img_x, img_y,  bias_x):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (img_x, img_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.bias_x = bias_x


    def update(self):

        global lost

        if self.rect.y <= windowHeight:
            self.rect.y += self.speed
        else:
            self.rect.x = randint(0, windowWidth-60)
            self.rect.y = randint(-200, 0)
            lost+=1

        if self.rect.x<=0 or self.rect.x >= windowWidth-70:
            self.bias_x *= -1
        self.rect.x += self.bias_x


window = display.set_mode((windowWidth, windowHeight))
display.set_caption("Русы против ящеров")
background = transform.scale(image.load("fon.jpg"), (windowWidth, windowHeight))


clock = time.Clock()
FPS = 60
clock.tick(FPS)


player1 = Player("rus.png", windowWidth/2, windowHeight-100, 10, 90, 100)
ufos = sprite.Group()
bullets = sprite.Group()
for i in range(6):
    ufos.add(UFO("iasher.png", randint(0, windowWidth-60), randint(-400, 0), randint(1, 3), 70, 50, randint(-2, 2)))

font.init()
font1 = font.SysFont('Arial', 30)

game = True
finish = False

killufos=0
bulletcolvo=-0
bulletmim=0


while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #firesound.play()
                bulletcolvo+=1
                player1.fire()


    if finish != True:

        sprites_list = sprite.groupcollide(ufos, bullets, True, True)
        for i in sprites_list:
            killufos+=1
            ufos.add(UFO("iasher.png", randint(0, windowWidth-60), randint(-400, 0), 1, 70, 50, randint(-2, 2)))

        window.blit(background, (0, 0))

        lostsch = font1.render("Пропущено ящеров: " + str(lost), 1 , (130, 130, 130))
        window.blit(lostsch, (20, 80))
        killufo = font1.render("Убито ящеров: " + str(killufos), 1 , (210, 210, 210))
        window.blit(killufo, (20, 110))
        bulletcount = font1.render("Брошено мечей: " + str(bulletcolvo), 1 , (130, 130, 130))
        window.blit(bulletcount, (20, 20))
        bulletmimo = font1.render("Мечей промазанно: " + str(bulletmim), 1 , (210, 210, 210))
        window.blit(bulletmimo, (20, 50))

        player1.reset()

        ufos.draw(window)
        bullets.draw(window)

        player1.update()
        ufos.update()
        bullets.update()

        display.update()

