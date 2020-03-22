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

#cabeza
cabezaImg = pygame.image.load("cabeza.png")
cabezaX_cambio = 0
cabezaY_cambio = 0


def cabeza(jugadores):
    for jugador in jugadores:
        j = jugadores[jugador]
        screen.blit(cabezaImg, (j["cabezaX"], j["cabezaY"]))


bolitaImg = pygame.image.load("dot.png")


def bolitaPintar(jugadores):
    for jugador in jugadores:
        j = jugadores[jugador]
        for i in range(j["numDots"]):
            screen.blit(bolitaImg, (j["bolitaX"][i], j["bolitaY"][i]))


appleImg = pygame.image.load("apple.png")


def pintarManzana(x, y):
    screen.blit(appleImg, (x, y))


def main(nombre):
    global jugadores, cabezaX_cambio, cabezaY_cambio, appleX, appleY

    # start by connecting to the network

    servidor = Cliente()
    id_actual = servidor.conectar(nombre)
    jugadores, appleX, appleY = servidor.enviar("get")

    movA = True
    movD = True
    movW = True
    movS = True
    run = True
    while run:
        jugador = jugadores[id_actual]
        datos = ""

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

        # cuerpo movimiento
        cabezaX_temp = jugador["cabezaX"]
        cabezaY_temp = jugador["cabezaY"]

        jugador["cabezaX"] += cabezaX_cambio
        jugador["cabezaY"] += cabezaY_cambio

        for i in range(jugador["numDots"] - 1, -1, -1):
            if i == 0:
                jugador["bolitaX"][i] = cabezaX_temp
                jugador["bolitaY"][i] = cabezaY_temp
                continue
            jugador["bolitaX"][i] = jugador["bolitaX"][i - 1]
            jugador["bolitaY"][i] = jugador["bolitaY"][i - 1]

        datos = "move " + str(jugador["cabezaX"]) + " " + str(jugador["cabezaY"])

        # send data to server and recieve back all players information
        jugadores, appleX, appleY = servidor.enviar(datos)

        cabeza(jugadores)
        bolitaPintar(jugadores)
        pintarManzana(appleX, appleY)

        # redraw window then update the frame
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


#screen
screen = pygame.display.set_mode((800, 608))

#title and icon
pygame.display.set_caption("SnakeGame")
icon =pygame.image.load("snake1.png")
pygame.display.set_icon(icon)

# start game
main(nombre)

