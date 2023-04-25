import pygame
import random
import os
import pyttsx3
import pyaudio

pygame.font.init()
pygame.mixer.init()

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

m = 0
hscore = 0
WIDTH, HEIGHT = 1200, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE INVADER")
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)  # sky blue = 70, 170, 220, gray = 100, 100, 100
RED = (255, 0, 0)
LIVE_FONT = pygame.font.SysFont('comicsans', 15)
SCORE_FONT = pygame.font.SysFont('comicsans', 15)
START_FONT = pygame.font.SysFont('comicsans', 20)
END_FONT = pygame.font.SysFont('comicsans', 20)
ENY_HIT = pygame.USEREVENT + 1
ENEMY_HIT = pygame.USEREVENT + 1
PLAYER_HIT = pygame.USEREVENT + 1
FPS = 60
PIXEL_SPEED = 7
ENEMY_PIXEL_SPEED = 1
ENY_PIXEL_SPEED = 1
PLAYER_MAX_BULLETS = 7
PLAYER_BULLET_PIXEL_SPEED = 9
ENEMY_BULLET_PIXEL_SPEED = 6
PLAYER_SPACESHIP_WIDTH, PLAYER_SPACESHIP_HEIGHT = 75, 60
ENEMY_SPACESHIP_WIDTH, ENEMY_SPACESHIP_HEIGHT = 60, 55
ENY_SPACESHIP_WIDTH, ENY_SPACESHIP_HEIGHT = 45, 35
PLAYER_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('i.s', 'player.png'))
PLAYER_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    PLAYER_SPACESHIP_IMAGE, (PLAYER_SPACESHIP_WIDTH, PLAYER_SPACESHIP_HEIGHT)), 0)
ENEMY_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('i.s', 'enemy.png'))
ENEMY_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    ENEMY_SPACESHIP_IMAGE, (ENEMY_SPACESHIP_WIDTH, ENEMY_SPACESHIP_HEIGHT)), 0)
SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('i.s', 'space.jpg')), (WIDTH, HEIGHT))
SP = pygame.transform.scale(pygame.image.load(
    os.path.join('i.s', 'sp.png')), (WIDTH, HEIGHT))
SI_IMAGE = pygame.image.load(
    os.path.join('i.s', 'si.png'))
SI = pygame.transform.rotate(pygame.transform.scale(
    SI_IMAGE, (400, 350)), 0)
ENY_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('i.s', 'enemy.png'))
PLAYER_BULLET_FIRE_SOUND = pygame.mixer.Sound(
    os.path.join('i.s', 'player gun.mp3'))
E_BULLET_FIRE_SOUND = pygame.mixer.Sound(
    os.path.join('i.s', 'enemy gun.mp3'))
ENY_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    ENY_SPACESHIP_IMAGE, (ENY_SPACESHIP_WIDTH, ENY_SPACESHIP_HEIGHT)), 0)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def draw_window(player, enemy, eny, player_bullets, enemy_bullets,
                eny_bullets, player_live, health_white, health_red, score):
    WIN.blit(SPACE, (0, 0))
    player_live_text = LIVE_FONT.render(
        "Lives: " + str(player_live), True, WHITE)
    score_show_text = SCORE_FONT.render(
        "Scores: " + str(score), True, WHITE)
    WIN.blit(player_live_text, (10, 10))
    WIN.blit(score_show_text, (1120, 10))
    WIN.blit(PLAYER_SPACESHIP, (player.x, player.y))
    WIN.blit(ENEMY_SPACESHIP, (enemy.x, enemy.y))
    pygame.draw.rect(WIN, RED, health_red)
    pygame.draw.rect(WIN, GREEN, health_white)
    WIN.blit(ENY_SPACESHIP, (eny.x, eny.y))
    for bullet in player_bullets:
        pygame.draw.rect(WIN, ORANGE, bullet)
    for bullet in enemy_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in eny_bullets:
        pygame.draw.rect(WIN, GREEN, bullet)
    pygame.display.update()


def player_handle_movement(keys_pressed, player, t):
    if keys_pressed[pygame.K_LEFT] and player.x - PIXEL_SPEED > 0:  # left arrow key
        player.x -= PIXEL_SPEED
    if keys_pressed[pygame.K_RIGHT] and player.x + PIXEL_SPEED + player.width < WIDTH:  # right arrow key
        player.x += PIXEL_SPEED
    if keys_pressed[pygame.K_UP] and player.y - PIXEL_SPEED > 0:  # up arrow key
        player.y -= PIXEL_SPEED
    if keys_pressed[pygame.K_DOWN] and player.y + PIXEL_SPEED + player.height < HEIGHT - 15:  # down arrow key
        player.y += PIXEL_SPEED
    w = 75
    w -= t
    health_red = pygame.Rect(player.x, player.y + 60, 75, 10)
    health_white = pygame.Rect(player.x, player.y + 60, w, 10)
    return health_white, health_red


def enemy_handle_movement(enemy, eny, player, player_live):
    if enemy.y <= 700:
        if player.colliderect(enemy):
            player_live -= 1
            lower, upper = 0, 1140
            value = random.randint(lower, upper)
            enemy.y = -75
            enemy.x = value
        else:
            enemy.y += ENEMY_PIXEL_SPEED
        if player.colliderect(eny):
            player_live -= 1
            lower, upper = 0, 1140
            value = random.randint(lower, upper)
            eny.y = -50
            eny.x = value
        else:
            eny.y += ENY_PIXEL_SPEED
    if eny.y == 700:
        player_live -= 1
        lower, upper = 0, 1140
        value = random.randint(lower, upper)
        eny.y = -50
        eny.x = value
    if enemy.y == 700:
        player_live -= 1
        lower, upper = 0, 1140
        value = random.randint(lower, upper)
        enemy.y = -75
        enemy.x = value
    return player_live


def bullet_handle_movement(player, enemy, eny, player_bullets, enemy_bullets, eny_bullets, t, score):
    for bullet in player_bullets:
        bullet.y -= PLAYER_BULLET_PIXEL_SPEED
        if eny.colliderect(bullet):
            score += 2
            pygame.event.post(pygame.event.Event(ENY_HIT))
            player_bullets.remove(bullet)
            lower, upper = 0, 1140
            value = random.randint(lower, upper)
            eny.y = -50
            eny.x = value
        elif enemy.colliderect(bullet):
            score += 1
            pygame.event.post(pygame.event.Event(ENEMY_HIT))
            player_bullets.remove(bullet)
            lower, upper = 0, 1140
            value = random.randint(lower, upper)
            enemy.y = -75
            enemy.x = value
        elif bullet.y <= 0:
            player_bullets.remove(bullet)
    for bullet in eny_bullets:
        bullet.y += ENEMY_BULLET_PIXEL_SPEED
        if player.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PLAYER_HIT))
            eny_bullets.remove(bullet)
            t += 5
            ebullet2 = pygame.Rect(eny.x + 20, eny.y, 7, 14)
            eny_bullets.append(ebullet2)
            E_BULLET_FIRE_SOUND.play()
        elif bullet.y > 2000:
            eny_bullets.remove(bullet)
            ebullet2 = pygame.Rect(eny.x + 20, eny.y, 7, 14)
            eny_bullets.append(ebullet2)
            E_BULLET_FIRE_SOUND.play()
    for bullet in enemy_bullets:
        bullet.y += ENEMY_BULLET_PIXEL_SPEED
        if player.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PLAYER_HIT))
            enemy_bullets.remove(bullet)
            t += 5
            ebullet1 = pygame.Rect(enemy.x + 25, enemy.y, 7, 14)
            enemy_bullets.append(ebullet1)
            E_BULLET_FIRE_SOUND.play()
        elif bullet.y > 2000:
            enemy_bullets.remove(bullet)
            ebullet1 = pygame.Rect(enemy.x + 25, enemy.y, 7, 14)
            enemy_bullets.append(ebullet1)
            E_BULLET_FIRE_SOUND.play()
        return t, score


def first_window(text):
    draw_text = START_FONT.render(text, True, WHITE)
    WIN.blit(draw_text, (500, 620))
    pygame.display.update()
    print()


def last_window(tx):
    draw_tx = END_FONT.render(tx, True, WHITE)
    WIN.blit(draw_tx, (520, 480))
    pygame.display.update()


def main():
    start1, end1 = 0, 1140
    start2, end2 = 0, 1140
    valuex1 = random.randint(start1, end1)
    valuex2 = random.randint(start2, end2)
    if valuex1 == valuex2:
        valuex1 = 0
        valuex2 = 1140
    player_bullets = []
    enemy_bullets = []
    eny_bullets = []
    clock = pygame.time.Clock()
    player = pygame.Rect(620, 620, PLAYER_SPACESHIP_WIDTH, PLAYER_SPACESHIP_HEIGHT)
    enemy = pygame.Rect(valuex1, -75, ENEMY_SPACESHIP_WIDTH, ENEMY_SPACESHIP_HEIGHT)
    eny = pygame.Rect(valuex2, -50, ENY_SPACESHIP_WIDTH, ENY_SPACESHIP_HEIGHT)
    ebullet1 = pygame.Rect(enemy.x + 25, enemy.y, 7, 14)
    enemy_bullets.append(ebullet1)
    ebullet2 = pygame.Rect(eny.x + 20, eny.y, 7, 14)
    eny_bullets.append(ebullet2)
    player_live = 6
    score = 0
    n = 1
    t = 0
    z = 0
    run = True
    x = globals()['m']
    if x != 0:
        i = 0
    else:
        i = 1
    while i != 0:
        for event in pygame.event.get():
            if event.type != pygame.KEYDOWN:
                WIN.blit(SP, (0, 0))
                WIN.blit(SI, (400, 20))
                text = "Press any key to start..."
                first_window(text)
                if n == 1:
                    speak("Welcome to Space Invaders")
                    speak("Press any key to start")
                    n = 0
            else:
                i = 0
    E_BULLET_FIRE_SOUND.play()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            if event.type == pygame.KEYDOWN:
                if z == 0:
                    if event.key == pygame.K_SPACE and len(player_bullets) < PLAYER_MAX_BULLETS:
                        bullet = pygame.Rect(player.x + 35, player.y, 10, 18)
                        player_bullets.append(bullet)
                        PLAYER_BULLET_FIRE_SOUND.play()
                    if event.key == pygame.K_a:
                        z = 1
                        speak("Auto shoot activated")
                else:
                    if event.key == pygame.K_s:
                        z = 0
                        speak("Auto shoot deactivated")
        if z == 1:
            if len(player_bullets) < PLAYER_MAX_BULLETS:
                bullet = pygame.Rect(player.x + 35, player.y, 10, 18)
                player_bullets.append(bullet)
                PLAYER_BULLET_FIRE_SOUND.play()
        keys_pressed = pygame.key.get_pressed()
        health_white, health_red = player_handle_movement(keys_pressed, player, t)
        player_live = enemy_handle_movement(enemy, eny, player, player_live)
        t, score = bullet_handle_movement(player, enemy, eny, player_bullets,
                                          enemy_bullets, eny_bullets, t, score)
        draw_window(player, enemy, eny, player_bullets, enemy_bullets,
                    eny_bullets, player_live, health_white, health_red, score)
        if player_live == 0:
            if globals()['hscore'] < score:
                globals()['hscore'] = score
            pygame.time.delay(2000)
            WIN.blit(SP, (0, 0))
            WIN.blit(SI, (400, 20))
            tx = f"Highest score: {globals()['hscore']}"
            last_window(tx)
            speak(f"Highest Score is {globals()['hscore']}")
            pygame.time.delay(5000)
            run = False
            globals()['m'] = 1
        if t == 80:
            if globals()['hscore'] < score:
                globals()['hscore'] = score
            pygame.time.delay(2000)
            WIN.blit(SP, (0, 0))
            WIN.blit(SI, (400, 20))
            tx = f"Highest score: {globals()['hscore']}"
            last_window(tx)
            speak(f"Highest Score is {globals()['hscore']}")
            pygame.time.delay(5000)
            run = False
            globals()['m'] = 1
    main()


if __name__ == "__main__":
    main()