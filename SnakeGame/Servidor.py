import socket
from _thread import *
import random
import math
import _pickle as pickle
import time

S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#IPS Y ESE PEDO
PUERTO = 5555
NOMBRE_HOST = socket.gethostname()
IP_SERVIDOR = socket.gethostbyname(NOMBRE_HOST)

#INTENTAR CONECTAR AL SERVIDOR
try:
    S.bind((IP_SERVIDOR, PUERTO))
except socket.error as e:
    print(str(e))
    print("[SERVIDOR] No se pudo iniciar")
    quit()

S.listen()

print(f"[SERVER] Servidor iniciado con dirección: {IP_SERVIDOR}")

#variables
jugadores = {}
conexiones = 0
_id = 0
iniciar = False


#COSAS DEL JUEGO
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


def colision(jugadores):
    for jugador in jugadores:
        j = jugadores[jugador]
        for i in range(j["numDots"]):
            if j["bolitaX"][i] == j["cabezaX"] and j["bolitaY"][i] == j["cabezaY"]:
                j["gameOver"] = True
                print(f"[GAME] " + j["nombre"] + " ya valio ")


def comerManzana(cabX, cabY, appX, appY):
    distancia = math.sqrt((math.pow(cabX - appX, 2)) + (math.pow(cabY - appY, 2)))
    if distancia < 1:
        return True
    else:
        return False


def comio(jugadores):
    global appleX
    global appleY
    for jugador in jugadores:
        j = jugadores[jugador]

        comido = comerManzana(j["cabezaX"], j["cabezaY"], appleX, appleY)
        if comido:
            enCuerpo = True
            while enCuerpo:
                x = random32X()
                y = random32Y()
                enCuerpo = False
                for i in range(j["numDots"]):
                    if j["bolitaX"][i] == x and j["bolitaY"][i] == y:
                        enCuerpo = True
                        break

            appleX = x
            appleY = y
            j["score"] += 1
            j["numDots"] += 1
            j["bolitaX"].append(0)
            j["bolitaY"].append(0)


def iniciarHiloNuevo(conn, _id):
    global conexiones, jugadores, appleX, appleY

    id_actual = _id

    # RECIBIR NOMBRE DEL CLIENTE
    datos = conn.recv(16)
    nombre = datos.decode("utf-8")
    print("[LOG]", nombre, "conectado al servidor.")

    bolitaX = []
    bolitaY = []
    numDots = 0
    gameOver = False
    x = 96
    y = 96

    jugadores[id_actual] = {"cabezaX": x,
                            "cabezaY": y,
                            "score": 0,
                            "nombre": nombre,
                            "numDots": numDots,
                            "bolitaX": bolitaX,
                            "bolitaY": bolitaY,
                            "gameOver": gameOver}

    conn.send(str.encode(str(id_actual)))
    while True:
        try:
            datos = conn.recv(32)
            if not datos:
                break

            datos = datos.decode("utf-8")

            if datos.split(" ")[0] == "move":
                split_data = datos.split(" ")
                x = int(split_data[1])
                y = int(split_data[2])
                xTemp = int(split_data[3])
                yTemp = int(split_data[4])
                jugadores[id_actual]["cabezaX"] = x
                jugadores[id_actual]["cabezaY"] = y

                #checar colisiones y ese rollo
                if iniciar:
                    comio(jugadores)
                    colision(jugadores)

                for i in range(jugadores[id_actual]["numDots"] - 1, -1, -1):
                    if i == 0:
                        jugadores[id_actual]["bolitaX"][i] = xTemp
                        jugadores[id_actual]["bolitaY"][i] = yTemp
                        continue
                    jugadores[id_actual]["bolitaX"][i] = jugadores[id_actual]["bolitaX"][i - 1]
                    jugadores[id_actual]["bolitaY"][i] = jugadores[id_actual]["bolitaY"][i - 1]

                send_data = pickle.dumps((jugadores, appleX, appleY))

            else:
                send_data = pickle.dumps((jugadores, appleX, appleY))

            # info retorna a clientes
            conn.send(send_data)

        except Exception as e2:
            print("e2: ", e2)
            break  # desconectar al cliente en caso de errores

        time.sleep(0.001)

    # info de desconecte
    print("[DISCONNECT] Name:", nombre, ", Client Id:", id_actual, "disconnected")

    conexiones -= 1
    del jugadores[id_actual]  # bye bye cliente
    conn.close()  # bye bye conexion


print("[GAME] Cargando...")
print("[SERVER] Esperando conexiones...")


#LOOP ENCARGADO DE ACEPTAR NUEVAS CONEXIONES
while True:

    host, addr = S.accept()
    print("[CONNECTION] Connected to:", addr)

    # start game when a client on the server computer connects
    if addr[0] == IP_SERVIDOR and not (iniciar):
        iniciar = True
        print("[STARTED] Game Started")

    # increment connections start new thread then increment ids
    conexiones += 1
    start_new_thread(iniciarHiloNuevo, (host, _id))
    _id += 1

print("[SERVIDOR] Servidor fuera de servico")