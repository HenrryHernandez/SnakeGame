import pygame
import random
import math
import time

pygame.init()

#screen
screen = pygame.display.set_mode((800, 608))

#title and icon
pygame.display.set_caption("SnakeGame")
icon =pygame.image.load("snake1.png")
pygame.display.set_icon(icon)

#marcador texto
puntaje = 0
scoreTablero = pygame.font.Font('freesansbold.ttf', 25)


def mostrarMarcador():
    scoreMensaje = scoreTablero.render("Puntos: " + str(puntaje), True, (0, 0, 0))
    screen.blit(scoreMensaje, (10, 10))


#game over mensaje
gameOverTablero = pygame.font.Font('freesansbold.ttf', 100)
restartTablero = pygame.font.Font('freesansbold.ttf', 25)


def mostrarGameOver():
    gameOverMensaje = gameOverTablero.render("Game Over", True, (255, 0, 0))
    screen.blit(gameOverMensaje, (125, 200))
    restartMensaje = restartTablero.render("Presiona Espacio para reiniciar", True, (255, 0, 0))
    screen.blit(restartMensaje, (220, 300))


#cabeza
cabezaImg = pygame.image.load("cabeza.png")
cabezaX = 96
cabezaY = 96
cabezaX_cambio = 0
cabezaY_cambio = 0


def cabeza(x, y):
    screen.blit(cabezaImg, (x, y))


#cargar apple imagen
appleImg = pygame.image.load("apple.png")


def random32X():
    x = random.randint(0, 768)
    while x % 32 != 0:
        x = random.randint(0, 768)

    return x


def random32Y():
    y = random.randint(0, 576)
    while y % 32 != 0:
        y = random.randint(0, 576)

    return y


appleX = random32X()
appleY = random32Y()


def apple(x, y):
    screen.blit(appleImg, (x, y))


#colision
def comerManzana(cabX, cabY, appX, appY):
    distancia = math.sqrt((math.pow(cabX - appX, 2)) + (math.pow(cabY - appY, 2)))
    if distancia < 1:
        return True
    else:
        return False


#cuerpo
bolitaImg = pygame.image.load("dot.png")
bolitaImgs = []
bolitaX =[]
bolitaY = []
numDots = 0


def bolita():
    global numDots
    numDots += 1
    bolitaImgs.append(bolitaImg)
    bolitaX.append(0)
    bolitaY.append(0)


def bolitaPintar(x, y, i):
    screen.blit(bolitaImgs[i], (x, y))


def reiniciarValores():
    global cabezaX
    global cabezaY
    cabezaX = 96
    cabezaY = 96
    global puntaje
    puntaje = 0
    global numDots
    numDots = 0
    global movA
    global movD
    global movS
    global movW
    movA = True
    movD = True
    movW = True
    movS = True
    global appleX
    global  appleY
    appleX = random32X()
    appleY = random32Y()


reiniciar = False
running = True
movA = True
movD = True
movW = True
movS = True
while running:
    time.sleep(.07)
    screen.fill((220, 220, 220))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and movW:
                cabezaY_cambio = -32
                cabezaX_cambio = 0
                movS = False
                movA = True
                movD = True

            if event.key == pygame.K_s and movS:
                cabezaY_cambio = 32
                cabezaX_cambio = 0
                movW = False
                movA = True
                movD = True

            if event.key == pygame.K_a and movA:
                cabezaX_cambio = -32
                cabezaY_cambio = 0
                movD = False
                movW = True
                movS = True

            if event.key == pygame.K_d and movD:
                cabezaX_cambio = 32
                cabezaY_cambio = 0
                movA = False
                movW = True
                movS = True

            if event.key == pygame.K_SPACE and reiniciar:
                reiniciarValores()
                reiniciar = False

    #checamos los limites de nuestra cabeza
    if cabezaX < 0:
        cabezaX = 800
    elif cabezaX == 800:
        cabezaX = -32
    elif cabezaY < 0:
        cabezaY = 608
    elif cabezaY == 608:
        cabezaY = -32

    #checar si se comio la manzana y que al generar manzana no choque con alguna parte del cuerpo
    comido = comerManzana(cabezaX, cabezaY, appleX, appleY)
    if comido:
        enCuerpo = True
        while enCuerpo:
            x = random32X()
            y = random32Y()
            enCuerpo = False
            for i in range(numDots):
                if bolitaX[i] == x and bolitaY[i] == y:
                    enCuerpo = True
                    break

        appleX = x
        appleY = y
        puntaje += 1
        bolita()

    #checar Game Over
    for i in range(numDots):
        if bolitaX[i] == cabezaX and bolitaY[i] == cabezaY:
            cabezaX_cambio = 0
            cabezaY_cambio = 0
            movW = False
            movD = False
            movS = False
            movA = False
            mostrarGameOver()
            reiniciar = True


    #cuerpo movimiento
    cabezaX_temp = cabezaX
    cabezaY_temp = cabezaY

    cabezaX += cabezaX_cambio
    cabezaY += cabezaY_cambio

    for i in range(numDots - 1, -1, -1):
        if i == 0:
            bolitaX[i] = cabezaX_temp
            bolitaY[i] = cabezaY_temp
            continue
        bolitaX[i] = bolitaX[i - 1]
        bolitaY[i] = bolitaY[i - 1]

    cabeza(cabezaX, cabezaY)

    for i in range(numDots):
        bolitaPintar(bolitaX[i], bolitaY[i], i)

    apple(appleX, appleY)
    mostrarMarcador()
    pygame.display.update()