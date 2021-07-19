import socket
import sys
import errno

'''
HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
my_username = input("Username: ")
# Conectamos el usuario
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

# Para que recv() no bloquee el programa
client_socket.setblocking(False)

# Codificar el usuario y declarar su tamaño en una cabecera
username = my_username.encode('utf-8')
username_cabecera = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
# Mandamos el nombre de usuario
client_socket.send(username_cabecera + username)

while True:

    # Esperar el input del usuario
    mensaje = input(f'{my_username} > ')

    # If mensaje is not empty - send it
    if mensaje:

        # Encode mensaje to bytes, prepare header and convert to bytes, like for username above, then send
        mensaje = mensaje.encode('utf-8')
        mensaje_cabecera = f"{len(mensaje):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(mensaje_cabecera + mensaje)

    try:
        # recibir mensajes (puede haber mas de uno)
        while True:

            # Recibimos la cabecera con el tamaño del username
            username_header = client_socket.recv(HEADER_LENGTH)

            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()
    
            username_tamaño = int(username_header.decode('utf-8').strip())

            # Recibir y decodificar el username
            username = client_socket.recv(username_tamaño).decode('utf-8')

            # Recibimos y decodificamos el mensaje
            mensaje_cabecera = client_socket.recv(HEADER_LENGTH)
            mensaje_tamaño = int(mensaje_cabecera.decode('utf-8').strip())
            mensaje = client_socket.recv(mensaje_tamaño).decode('utf-8')

            print(f'{username} > {mensaje}')

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()
        continue

    except Exception as e:
        print('Reading error: '.format(str(e)))
        sys.exit()
'''

class Cliente:


    HEADER_LENGTH = 10


    def __init__(self, IP, PORT) -> None:
        self.IP = IP
        self.PORT = PORT
        self.my_username = ''
        self.client_socket = None


    def mandar_mensaje(self, mensaje: str) -> None:
        # Esperar el input del usuario
        # mensaje = input(f'{self.my_username} > ')

        # Si mensaje no esta vacio enviarlo
        if mensaje:

            # Codificar el mensaje en bytes y luego enviarlo
            mensaje = mensaje.encode('utf-8')
            mensaje_cabecera = f"{len(mensaje):<{self.HEADER_LENGTH}}".encode('utf-8')
            self.client_socket.send(mensaje_cabecera + mensaje)
    
    def establecer_conexion(self, username: str) -> None:
        self.my_username = input("Username: ")
        # Conectamos el usuario
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.IP, self.PORT))

        # Para que recv() no bloquee el programa
        self.client_socket.setblocking(False)

        # Codificar el usuario y declarar su tamaño en una cabecera
        username = self.my_username.encode('utf-8')
        username_cabecera = f"{len(username):<{self.HEADER_LENGTH}}".encode('utf-8')

        # Mandamos el nombre de usuario
        self.client_socket.send(username_cabecera + username)

    def recibir_mensajes(self):
        # self.__establecer_conexion__()
        while True:

            # # Esperar el input del usuario
            # mensaje = input(f'{self.my_username} > ')

            # # If mensaje is not empty - send it
            # if mensaje:

            #     # Encode mensaje to bytes, prepare header and convert to bytes, like for username above, then send
            #     mensaje = mensaje.encode('utf-8')
            #     mensaje_cabecera = f"{len(mensaje):<{self.HEADER_LENGTH}}".encode('utf-8')
            #     self.client_socket.send(mensaje_cabecera + mensaje)

            try:
                # recibir mensajes (puede haber mas de uno)
                while True:

                    # Recibimos la cabecera con el tamaño del username
                    username_cabecera = self.client_socket.recv(self.HEADER_LENGTH)

                    if not len(username_cabecera):
                        print('Conexion cerrada por el servidor')
                        sys.exit()
            
                    username_tamaño = int(username_cabecera.decode('utf-8').strip())

                    # Recibir y decodificar el username
                    username = self.client_socket.recv(username_tamaño).decode('utf-8')

                    # Recibimos y decodificamos el mensaje
                    mensaje_cabecera = self.client_socket.recv(self.HEADER_LENGTH)
                    mensaje_tamaño = int(mensaje_cabecera.decode('utf-8').strip())
                    mensaje = self.client_socket.recv(mensaje_tamaño).decode('utf-8')

                    print(f'{username} > {mensaje}')

            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Error lectura: {}'.format(str(e)))
                    sys.exit()
                continue

            except Exception as e:
                print('Error lectura: '.format(str(e)))
                sys.exit()
        