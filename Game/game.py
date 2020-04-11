import pygame
import random
from sprites import *
from attributes import *

pygame.init()
pygame.font.init()



pygame.display.set_caption("Distance Yourself")
bg = pygame.image.load('background.png')

clock = pygame.time.Clock()

run = True

game = "MENU"

time = 0

score = 0

started = True

myfont = pygame.font.SysFont('Monserrat', 30)

def scrollCheck():
    if player.pos.x <= screen_width/4:
        player.pos.x += player.vel.x
    for plat in platforms:
        if plat.type != "GROUND":
            plat.rect.x -= player.vel.x
            if plat.rect.right <= 10:
                plat.kill()

def showMenu():
    global run
    global game
    player.health = 50
    global score
    score = 0
    global time
    time = 0
    global started
    started = True

    buttons = pygame.sprite.Group()
    start = Button(screen_width//2 - 110, screen_height//2 -100, pygame.image.load('start.png'))
    instructions = Button(screen_width//2 - 110, screen_height//2, pygame.image.load('instructions.png'))
    title = Button(screen_width//2 - 80, 50, pygame.image.load('title.png'))
    plat = Platform(0, screen_height - 40, screen_width, 40, 'GROUND')
    buttons.add(title)
    buttons.add(start)
    buttons.add(instructions)
    buttons.add(plat)

    pygame.draw.rect(win, (210, 252, 221), (0,0,screen_width, screen_height))
    background = pygame.transform.scale(bg, (569, 512))
    win.blit(background, (-200,10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            clicked_sprites = [s for s in buttons if s.rect.collidepoint(pos)]
            if clicked_sprites and clicked_sprites[0] == start:
                game = "ON"
            elif clicked_sprites and clicked_sprites[0] == instructions:
                game = "INSTRUCT"

    buttons.update()
    buttons.draw(win)

    #need to refresh the display
    pygame.display.update()
    pygame.display.flip()


def showInstructions():
    global run
    global game
    buttons = pygame.sprite.Group()
    text = Button(5, 10, pygame.image.load('text.png'))
    back = Button(screen_width//2 - 110, screen_height - 150, pygame.image.load('back.png'))
    plat = Platform(0, screen_height - 40, screen_width, 40, 'GROUND')
    buttons.add(text)
    buttons.add(back)
    buttons.add(plat)

    pygame.draw.rect(win, (210, 252, 221), (0,0,screen_width, screen_height))
    background = pygame.transform.scale(bg, (569, 512))
    win.blit(background, (-200,10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            clicked_sprites = [s for s in buttons if s.rect.collidepoint(pos)]
            if clicked_sprites and clicked_sprites[0] == back:
                game = "MENU"

    buttons.update()
    buttons.draw(win)

    #need to refresh the display
    pygame.display.update()
    pygame.display.flip()



def redrawGameWindow():
    global started
    if started:
        #restart by emptying out sprite groups and adding the starters
        global all_sprites
        global player
        global players
        global enemies
        global platforms

        all_sprites = pygame.sprite.Group()
        player = Player(200, screen_height - 64 - 35)
        players = pygame.sprite.Group()
        players.add(player)

        all_sprites.add(player)

        enemies = pygame.sprite.Group()

        platforms = pygame.sprite.Group()
        plat = Platform(0, screen_height - 40, screen_width, 40, 'GROUND')
        plat2 = Platform(100, screen_height - 300, screen_width//2+50, 40, False)
        plat3 = Platform(10, screen_height - 400, 70, 40)
        plat4 = Platform(screen_width, screen_height - 500, 100, 40)
        plat5 = Platform(screen_width, screen_height - 500, 100, 40)
        all_sprites.add(plat)
        platforms.add(plat)
        all_sprites.add(plat2)
        platforms.add(plat2)
        all_sprites.add(plat3)
        platforms.add(plat3)
        all_sprites.add(plat4)
        platforms.add(plat4)
        all_sprites.add(plat4)
        platforms.add(plat4)
        started = False

    global run
    #check for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    checkHealth()

    #need to fill every time so it doesn't streak across the screen
    pygame.draw.rect(win, (210, 252, 221), (0,0,screen_width, screen_height))
    background = pygame.transform.scale(bg, (569, 512))
    win.blit(background, (-200,10))

    #check for collisions
    hit = pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_rect)
    if hit:
        player.hit()

    land = pygame.sprite.spritecollide(player, platforms, False)
    if land:
        ## TODO: fix jump mechanics, finish graphics, add to website
        if land[0].type == "GROUND" or (land[0].rect.top <= player.pos.y and player.pos.x + player.width//2 >= land[0].rect.left):
            player.inAir = False
            player.pos.y = land[0].rect.top
            player.vel.y = 0
            player.rect.midbottom = player.pos

    else:
        player.inAir = True


    for enemy in enemies:
        land = pygame.sprite.spritecollide(enemy, platforms, False)
        if land:
            if land[0].type == "GROUND" or (land[0].rect.top <= enemy.pos.y and enemy.pos.x + enemy.width//2 >= land[0].rect.left):
                enemy.inAir = False
                enemy.pos.y = land[0].rect.top
                enemy.vel.y = 0
                enemy.rect.midbottom = enemy.pos

        else:
            enemy.inAir = True


    #check for scroll
    scrollCheck()

    #spawn new platforms, enemies
    spawn()

    #update all_sprites
    all_sprites.update()

    #draw all all_sprites
    all_sprites.draw(win)
    players.draw(win)
    enemies.draw(win)


    global time
    time += 1

    global score
    score = time//27



    #collision text
    health = player.health
    text = myfont.render("HEALTH: " + str(health), False, (255, 255, 255))
    win.blit(text, (screen_width//2 + 30,screen_height - 30))

    scoreText = myfont.render("SCORE: " + str(score), False, (255, 255, 255))
    win.blit(scoreText, (10,screen_height - 30))







    #need to refresh the display
    pygame.display.update()
    pygame.display.flip()

#main loop

#add everything to sprites

all_sprites = pygame.sprite.Group()
player = Player(200, screen_height - 64 - 35)
players = pygame.sprite.Group()
players.add(player)

all_sprites.add(player)

enemies = pygame.sprite.Group()
enemy = Enemy(20 - 128, 40, 400 + 128)

platforms = pygame.sprite.Group()
plat = Platform(0, screen_height - 40, screen_width, 40, 'GROUND')
plat2 = Platform(100, screen_height - 300, screen_width//2+50, 40, False)
plat3 = Platform(10, screen_height - 400, 70, 40)
plat4 = Platform(screen_width, screen_height - 500, 100, 40)
plat5 = Platform(screen_width, screen_height - 500, 100, 40)
all_sprites.add(plat)
platforms.add(plat)
all_sprites.add(plat2)
platforms.add(plat2)
all_sprites.add(plat3)
platforms.add(plat3)
all_sprites.add(plat4)
platforms.add(plat4)
all_sprites.add(plat4)
platforms.add(plat4)

def spawn():
    while len(platforms) < 6:
        tall = player.height
        width = random.randrange(70, screen_width//2+100)
        p = Platform(random.randrange(screen_width + 10, screen_width*2), random.randrange(tall, screen_height-100), width, 40)
        platforms.add(p)
        all_sprites.add(p)

    while (len(enemies) < (time//27)//3) or (len(enemies) <= 0):
        x = random.randrange(0, screen_width - 64-20)
        y = random.randrange(0, screen_height - 40)
        end = screen_width
        if x + 30 < screen_width - 128:
            end = random.randrange(x + 30, screen_width - 128)
        else:
            end = random.randrange(screen_width-128, x + 30)
        e = Enemy(x,y,end)
        enemies.add(e)
        all_sprites.add(e)



def checkHealth():
    global game
    if player.health <= 0:
        game = "OVER"

overTick = 0
messages = pygame.sprite.Group()
over = Button(screen_width//2-100, screen_height//2+100, pygame.image.load('over.png'))
messages.add(over)

def gameOver():
    global game
    player.health = 50
    global score
    score = 0
    global time
    time = 0
    global started
    started = True
    global overTick
    global run
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    messages.update()

    text = myfont.render("SCORE: " + str(score), False, (255, 0, 0))
    win.blit(text, (screen_width//2,screen_height//2))

    messages.draw(win)

    overTick += 1


    if overTick//27 > 1:
        global game
        game = "MENU"

    pygame.display.update()
    pygame.display.flip()











while run:
    clock.tick(27)

    if game == "ON":
        redrawGameWindow()
    elif game == "OVER":
        gameOver()
    elif game == "INSTRUCT":
        showInstructions()
    else:
        showMenu()



pygame.quit()
