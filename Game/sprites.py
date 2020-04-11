import pygame
from attributes import *
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.transform.flip(image, True, False) for image in walkRight]
movement_acc = 0.5
vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = walkRight[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = (self.rect.topright[0] -  self.rect.x)
        self.height = (self.rect.bottomleft[1] -  self.rect.y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.pos = vec(self.rect.center,self.rect.center)
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.standing = True
        self.inAir = True
        self.walkCount = 0
        self.health = 50

    def jump(self):
        if not(self.inAir):
            self.vel.y = -55
            self.inAir = True



    def update(self):

        if self.inAir:
            self.acc = vec(0,7)
        if self.walkCount + 1 >= 9:
            self.walkCount = 0
        if not(self.standing):
            if self.left:
                self.image = walkLeft[self.walkCount]
                self.walkCount += 1
            elif self.right:
                self.image = walkRight[self.walkCount]
                self.walkCount += 1
        else:
                if self.right:
                    self.image = walkRight[0]
                else:
                    self.image = walkLeft[0]


        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.vel.x = -10
            self.left = True
            self.right = False
            self.standing = False
        elif keys[pygame.K_RIGHT]:
            self.vel.x = 10
            self.right = True
            self.left = False
            self.standing = False
        elif keys[pygame.K_SPACE]:
            self.jump()
        else:
            self.vel.x = 0
            self.walkCount = 0
            self.standing = True

        #physics
        self.vel += self.acc
        self.pos += self.vel

        if self.pos.x < 0:
            self.rect.x = 0

        if self.pos.x + self.vel.x > screen_width:
            self.pos.x = screen_width - (self.width//8)
        elif self.pos.x - self.vel.x < 0:
            self.pos.x = (self.width//2)

        self.rect.midbottom = self.pos

    def hit(self):
        if self.left:
            if self.pos.x - 20 > 0:
                self.rect.x -= 20
            else:
                self.pos.x = 0
        else:
                self.pos.x += 20
        self.health -= 1



class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, end):
        pygame.sprite.Sprite.__init__(self)
        self.walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
        self.walkLeft = [pygame.transform.flip(image, True, False) for image in self.walkRight]
        self.image = walkLeft[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = (self.rect.topright[0] -  self.rect.x)
        self.height = (self.rect.bottomleft[1] -  self.rect.y)
        self.end = end
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.pos = vec(self.rect.center,self.rect.center)
        self.walkCount = 0
        self.inAir = False
        self.path = [x, self.end]

    def update(self):
        self.move()
        if self.inAir:
            self.acc = vec(0,3.5)

        if self.walkCount + 1 >= 33:
            self.walkCount = 0
        if self.vel.x > 0:
            self.image = self.walkRight[self.walkCount//3]
            self.walkCount += 1
        else:
            self.image = self.walkLeft[self.walkCount//3]
            self.walkCount += 1



    def move(self):
        if self.vel.x > 0:
            if self.rect.x < self.path[1]:
                self.vel.x = 15
            else:
                self.vel.x = -15
                self.walkCount = 0
        else:
            if self.rect.x > self.path[0]:
                self.vel.x = -15
            else:
                self.vel.x = 15
                self.walkCount = 0

        self.vel += self.acc
        self.pos += self.vel

        self.rect.midbottom = self.pos


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, type="normal"):
        pygame.sprite.Sprite.__init__(self)
        self.image = (pygame.image.load("Grass.png"))
        self.width = width
        self.height = height
        self.getImg(self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = type

    def getImg(self, width, height):
        self.image = self.image.subsurface(pygame.Rect((0,0), (self.width, self.height)))


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
