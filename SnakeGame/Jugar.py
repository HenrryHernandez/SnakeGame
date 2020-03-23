import pygame
from cliente import Cliente
import time
import os

pygame.init()

jugadores = {}
cabezaX_cambio = 0
cabezaY_cambio = 0
appleX = 0
appleY = 0
movA = True
movD = True
movW = True
movS = True

#cabeza
cabezaImg = pygame.image.load("cabeza.png")


def cabeza(jugadores):
    for jugador in jugadores:
        j = jugadores[jugador]
        screen.blit(cabezaImg, (j["cabezaX"], j["cabezaY"]))


bolitaImg = pygame.image.load("dot.png")


def bolitaPintar():
    global jugadores
    for jugador in jugadores:
        j = jugadores[jugador]
        for i in range(j["numDots"]):
            screen.blit(bolitaImg, (j["bolitaX"][i], j["bolitaY"][i]))


appleImg = pygame.image.load("apple.png")


def pintarManzana(x, y):
    screen.blit(appleImg, (x, y))


#game over mensaje
gameOverTablero = pygame.font.Font('freesansbold.ttf', 100)


def mostrarGameOver():
    gameOverMensaje = gameOverTablero.render("Game Over", True, (255, 0, 0))
    screen.blit(gameOverMensaje, (125, 200))


def gameOver(jugadores, id):
    global movA, movD, movW, movS, cabezaX_cambio, cabezaY_cambio
    if jugadores[id]["gameOver"]:
        cabezaX_cambio = 0
        cabezaY_cambio = 0
        movW = False
        movD = False
        movS = False
        movA = False
        mostrarGameOver()


#marcador texto
scoreTablero = pygame.font.Font('freesansbold.ttf', 25)


def mostrarMarcador(puntaje):
    scoreMensaje = scoreTablero.render("Puntos: " + str(puntaje), True, (0, 0, 0))
    screen.blit(scoreMensaje, (10, 10))


def main(nombre):
    global jugadores, cabezaX_cambio, cabezaY_cambio, appleX, appleY, movA, movD, movW, movS

    # start by connecting to the network

    servidor = Cliente()
    id_actual = servidor.conectar(nombre)
    jugadores, appleX, appleY = servidor.enviar("get")


    running = True
    while running:
        jugador = jugadores[id_actual]

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


        # checamos los limites de nuestra cabeza
        if jugador["cabezaX"] < 0:
            jugador["cabezaX"] = 800
        elif jugador["cabezaX"] == 800:
            jugador["cabezaX"] = -32
        elif jugador["cabezaY"] < 0:
            jugador["cabezaY"] = 608
        elif jugador["cabezaY"] == 608:
            jugador["cabezaY"] = -32


        # cuerpo movimiento
        cabezaX_temp = jugador["cabezaX"]
        cabezaY_temp = jugador["cabezaY"]

        jugador["cabezaX"] += cabezaX_cambio
        jugador["cabezaY"] += cabezaY_cambio

        #empaquetamos info
        datos = "move " + str(jugador["cabezaX"]) + " " + str(jugador["cabezaY"]) + " " + str(cabezaX_temp) + " " \
                + str(cabezaY_temp)

        #enviamos info y recibiremos info tambien
        jugadores, appleX, appleY = servidor.enviar(datos)

        #a continuacion los metodos nos ayudaran a repintar todo y se actualizara la pantalla despues
        gameOver(jugadores, id_actual)
        cabeza(jugadores)
        bolitaPintar()
        pintarManzana(appleX, appleY)
        mostrarMarcador(jugador["score"])

        pygame.display.update()

    servidor.desconectar()
    pygame.quit()
    quit()


while True:
    nombre = input("Nombre: ")
    if 0 < len(nombre) < 20:
        break
    else:
        print("No se puede este nombre, debe ser de un rango entre 0 y 20")


#pantalla
screen = pygame.display.set_mode((800, 608))

#titulo e icono
pygame.display.set_caption("SnakeGame")
icon =pygame.image.load("snake1.png")
pygame.display.set_icon(icon)

#arrancar
main(nombre)

