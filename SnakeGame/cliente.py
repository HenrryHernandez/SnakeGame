import socket
import _pickle as pickle


class Cliente:
    def __init__(self):
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "169.254.9.225"
        self.port = 5555
        self.addr = (self.host, self.port)

    def conectar(self, nombre):
        self.cliente.connect(self.addr)
        self.cliente.send(str.encode(nombre))
        valor = self.cliente.recv(8)
        return int(valor.decode())

    def desconectar(self):
        self.cliente.close()

    def enviar(self, datos):
        try:
            self.cliente.send(str.encode(datos))
            respuesta = pickle.loads(self.cliente.recv(2048 * 4))

            return respuesta
        except socket.error as e:
            print(e)
