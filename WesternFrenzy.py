import pygame
import sys
import time
import random
pygame.init()

#colores
#
BLACK = (0,0,0)
WHITE = (255,255,255)
PURPLE = (148,0,111)
BLUE = (0,0,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)
ORANGE = (255,127,0)
RED = (255,0,0)
GREY = (65,65,65)

# Fuente para el texto
font = pygame.font.SysFont(None, 40)

#Espesificaciones de pantalla 
#
sw = 1280
sh = 720
screen_size = (sw,sh)

#Screen
#
screen = pygame.display.set_mode(screen_size)
bg_Floor = pygame.image.load(r"C:\Users\rafal\OneDrive\Escritorio\Progra 2\Proyect W\Assets\Bg-Floor.png").convert()

#fps 
#
clock = pygame.time.Clock()

#Bullet asset
#
Bullet = pygame.image.load(r"C:\Users\rafal\OneDrive\Escritorio\Progra 2\Proyect W\Assets\Bullet.png")

#Player assets 
#
PL_Back = pygame.image.load(r"C:\Users\rafal\OneDrive\Escritorio\Progra 2\Proyect W\Assets\Player - front.png").convert_alpha()
PL_Front = pygame.image.load(r"C:\Users\rafal\OneDrive\Escritorio\Progra 2\Proyect W\Assets\Player - back.png").convert_alpha()
PL_Left = pygame.image.load(r"C:\Users\rafal\OneDrive\Escritorio\Progra 2\Proyect W\Assets\Player - left.png").convert_alpha()
PL_Right = pygame.image.load(r"C:\Users\rafal\OneDrive\Escritorio\Progra 2\Proyect W\Assets\Player - right.png").convert_alpha()
Hearts = pygame.image.load(r"C:\Users\rafal\OneDrive\Escritorio\Progra 2\Proyect W\Assets\heart.png").convert_alpha() 

#bandit assets
#
GB_Front = pygame.image.load(r"C:\Users\rafal\OneDrive\Escritorio\Progra 2\Proyect W\Assets\bandit - front.png").convert_alpha()
GB_Back = pygame.image.load(r"C:\Users\rafal\OneDrive\Escritorio\Progra 2\Proyect W\Assets\bandit - back.png").convert_alpha()
GB_Left = pygame.image.load(r"C:\Users\rafal\OneDrive\Escritorio\Progra 2\Proyect W\Assets\bandit - left.png").convert_alpha()
GB_Right = pygame.image.load(r"C:\Users\rafal\OneDrive\Escritorio\Progra 2\Proyect W\Assets\bandit - right.png").convert_alpha()
     
#Posicion del jugador
#
pp = [sw // 2 - PL_Front.get_width() // 2, sh // 2 - PL_Front.get_height() // 2]
pd = "front" 
LS = 0
bullets = []
hp = 2

#Enemigos
#
bandidos = []  
bls = {}

#Disparo
#
def shoot(direction, player_position):
    if direction == "front":
        bullet_pos = [player_position[0] + PL_Front.get_width() // 2 - Bullet.get_width() // 2, player_position[1] - Bullet.get_height()]
    elif direction == "back":
        bullet_pos = [player_position[0] + PL_Back.get_width() // 2 - Bullet.get_width() // 2, player_position[1] + PL_Back.get_height()]
    elif direction == "left":
        bullet_pos = [player_position[0] - Bullet.get_width(), player_position[1] + PL_Left.get_height() // 2 - Bullet.get_height() // 2]
    elif direction == "right":
        bullet_pos = [player_position[0] + PL_Right.get_width(), player_position[1] + PL_Right.get_height() // 2 - Bullet.get_height() // 2]

    #Nueva bala
    #
    bullet = {
        "pos": bullet_pos,
        "dir": direction
    }
    bullets.append(bullet)

def bandit_shoot(bandit):
    current_time = time.time()
    if current_time - bandit["last_shot"] > bandit["shot_time"]:
        if bandit["dir"] == "front":
            bp = [bandit["pos"][0] + GB_Front.get_width() // 2, bandit["pos"][1] + GB_Front.get_height()]
        elif bandit["dir"] == "back":
            bp = [bandit["pos"][0] + GB_Back.get_width() // 2, bandit["pos"][1] - GB_Back.get_height()]
        elif bandit["dir"] == "left":
            bp = [bandit["pos"][0] - GB_Left.get_width(), bandit["pos"][1] + GB_Left.get_height() // 2]
        elif bandit["dir"] == "right":
            bp = [bandit["pos"][0] + GB_Right.get_width(), bandit["pos"][1] + GB_Right.get_height() // 2]
        bullet = {
            "pos": bp,
            "dir": bandit["dir"]
        }
        bullets.append(bullet)
        bandit["last_shot"] = current_time

def move_bullets():
    global hp
    for bullet in bullets[:]:
        if bullet["dir"] == "front":
            bullet["pos"][1] -= 10
        elif bullet["dir"] == "back":
            bullet["pos"][1] += 10
        elif bullet["dir"] == "left":
            bullet["pos"][0] -= 10
        elif bullet["dir"] == "right":
            bullet["pos"][0] += 10

        #Colisión con el jugador
        #
        if (bullet["pos"][0] >= pp[0] and bullet["pos"][0] <= pp[0] + PL_Front.get_width() and
            bullet["pos"][1] >= pp[1] and bullet["pos"][1] <= pp[1] + PL_Front.get_height()):
            hp -= 1
            bullets.remove(bullet)

        #Eliminar balas fuera del límite
        #
        if bullet["pos"][0] < 0 or bullet["pos"][0] > sw or bullet["pos"][1] < 0 or bullet["pos"][1] > sh:
            bullets.remove(bullet)

def display_lives():
    for i in range(hp):
        screen.blit(Hearts, (10 + i * Hearts.get_width(), sh - Hearts.get_height() - 10))

#Creacion de enemigos
#
def spawn_bandit():
    direction = random.choice(["front", "back", "left", "right"])  
    if direction == "front":
        bandit_pos = [sw // 2 - GB_Front.get_width() // 2, 0]  
    elif direction == "back":
        bandit_pos = [sw // 2 - GB_Back.get_width() // 2, sh - GB_Back.get_height()]  
    elif direction == "right":
        bandit_pos = [0, sh // 2 - GB_Left.get_height() // 2]  
    elif direction == "left":
        bandit_pos = [sw - GB_Right.get_width(), sh // 2 - GB_Right.get_height() // 2] 
    
    bandit = {
        "pos": bandit_pos,
        "dir": direction,
        "health": 1,
        "shot_time": random.uniform(2, 4),  
        "last_shot": time.time(),
    }
    bandidos.append(bandit)
    return bandit

#colision de bala
#
def check_bullet_bandit_collision():
    global bandidos
    for bullet in bullets[:]:
        for bandit in bandidos[:]:
            if (bullet["pos"][0] + Bullet.get_width() > bandit["pos"][0] and bullet["pos"][0] < bandit["pos"][0] + GB_Front.get_width() and
                bullet["pos"][1] + Bullet.get_height() > bandit["pos"][1] and bullet["pos"][1] < bandit["pos"][1] + GB_Front.get_height()):
                bandidos.remove(bandit)
                bullets.remove(bullet)  
                break  

#ataque enemigo
#
def bandit_shoot(bandit):
    current_time = time.time()
    if current_time - bandit["last_shot"] > bandit["shot_time"]:
        if bandit["dir"] == "front":
            bp = [bandit["pos"][0] + GB_Front.get_width() // 2, bandit["pos"][1] + GB_Front.get_height()]
        elif bandit["dir"] == "back":
            bp = [bandit["pos"][0] + GB_Back.get_width() // 2, bandit["pos"][1] - GB_Back.get_height()]
        elif bandit["dir"] == "left":
            bp = [bandit["pos"][0] - GB_Left.get_width(), bandit["pos"][1] + GB_Left.get_height() // 2]
        elif bandit["dir"] == "right":
            bp = [bandit["pos"][0] + GB_Right.get_width(), bandit["pos"][1] + GB_Right.get_height() // 2]

        bullet = {
            "pos": bp,
            "dir": bandit["dir"]
        }
        bullets.append(bullet)
        bandit["last_shot"] = current_time

#Movimiento de bala
#
def move_bullets():
    global hp
    for bullet in bullets[:]:  
        if bullet["dir"] == "front":
            bullet["pos"][1] -= 10
        elif bullet["dir"] == "back":
            bullet["pos"][1] += 10
        elif bullet["dir"] == "left":
            bullet["pos"][0] -= 10
        elif bullet["dir"] == "right":
            bullet["pos"][0] += 10

        if (bullet["pos"][0] >= pp[0] and bullet["pos"][0] <= pp[0] + PL_Front.get_width() and
            bullet["pos"][1] >= pp[1] and bullet["pos"][1] <= pp[1] + PL_Front.get_height()):
            hp -= 1
            bullets.remove(bullet)

        if bullet["pos"][0] < 0 or bullet["pos"][0] > sw or bullet["pos"][1] < 0 or bullet["pos"][1] > sh:
            bullets.remove(bullet)

#Mensaje "game over"
#
def game_over():
    game_over_text = font.render("Game Over! Press Enter to Restart", True, WHITE)
    screen.blit(game_over_text, (sw // 2 - game_over_text.get_width() // 2, sh // 2 - game_over_text.get_height() // 2))

#Menu de inicio
#
def show_start_message():
    start_text = font.render("Press Enter to Start", True, WHITE)
    screen.blit(start_text, (sw // 2 - start_text.get_width() // 2, sh // 2 - start_text.get_height() // 2))
    pygame.display.flip()
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting_for_input = False

show_start_message()

#Bucle de juego
#
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    #Final deljuego
    #
    if hp <= 0:
        game_over()
        pygame.display.flip()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            #Reincio
            #
            hp = 2
            bandidos.clear()
            bullets.clear()
            pp = [sw // 2 - PL_Front.get_width() // 2, sh // 2 - PL_Front.get_height() // 2]
            pd = "front"
            LS = 0
            continue

    #Controles del jugador
    #
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        pd = "front"
    elif keys[pygame.K_s]:
        pd = "back"
    elif keys[pygame.K_a]:
        pd = "left"
    elif keys[pygame.K_d]:
        pd = "right"

    #Disparo
    #
    current_time = time.time()
    if keys[pygame.K_j] and current_time - LS > 1:
        shoot(pd, pp)
        LS = current_time

    #Dibujar fondo y jugador
    #
    screen.blit(bg_Floor, (0, 0))

    if pd == "front":
        screen.blit(PL_Front, pp)
    elif pd == "back":
        screen.blit(PL_Back, pp)
    elif pd == "left":
        screen.blit(PL_Left, pp)
    elif pd == "right":
        screen.blit(PL_Right, pp)

    #Dibujar las balas
    #
    for bullet in bullets:
        screen.blit(Bullet, bullet["pos"])

    #Dibujar los bandidos
    #
    for bandit in bandidos:
        if bandit["dir"] == "right":
            screen.blit(GB_Right, bandit["pos"])
        elif bandit["dir"] == "left":
            screen.blit(GB_Left, bandit["pos"])
        elif bandit["dir"] == "back":
            screen.blit(GB_Back, bandit["pos"])
        elif bandit["dir"] == "front":
            screen.blit(GB_Front, bandit["pos"])

    move_bullets()

    #Spaw bandidos
    #
    if random.random() < 0.01:  
        bandit = spawn_bandit()
        bandit_shoot(bandit)

    
    #Disparo de los bandidos
    #
    for bandit in bandidos:
        bandit_shoot(bandit)  
    
    check_bullet_bandit_collision()

    display_lives()

    #Actualizar pantalla
    #
    pygame.display.flip()
    clock.tick(60)