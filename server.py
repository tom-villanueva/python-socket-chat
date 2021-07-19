import socket
import select

'''
cabecera_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234

# AF_INTET es IPv4 y SOCK_STREAM es TCP 
self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# para reconectar a la misma direccion
self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Vincular el socket para informar al SO que usamos esa IP y PUERTO
self.server_socket.bind((IP, PORT))

# Escuchando por nuevas conexiones
self.server_socket.listen()

# Creamos una lista de sockets, e incluimos el socket del servidor
self.lista_sockets = [self.server_socket]

# Creamos un diccionario de self.clientes, el socket como key y la cabecera y username como datos
self.clientes = {}

print(f'Escuchando para conexiones en {IP}:{PORT}...')

# Handles mensaje receiving
def recibir_mensaje(client_socket):

    try:

        # Recibimos el encabezado, que contiene el tamaño del mensaje 
        cabecera_mensaje = client_socket.recv(cabecera_LENGTH)

        # Si no recibimos nada, devolvemos false
        if not len(cabecera_mensaje):
            return False

        # Calculamos el tamaño del mensaje a través de la cabecera
        tamaño_mensaje = int(cabecera_mensaje.decode('utf-8').strip())

        # Devolvemos un diccionario con la cabecera y los datos (mensaje) recibidos
        return {'cabecera': cabecera_mensaje, 'datos': client_socket.recv(tamaño_mensaje)}

    except:
        return False

while True:
    
    La función select recibe tres iterables que contienen descriptores de archivos (sockets):
      - rlist: sockets en espera para lectura
      - wlist: sockets en espera para escritura
      - xlist: esperar a una excepcion
    Y devuelve tres iterables, que son subconjuntos de los parametros
      - lectura:    sockets en los que recibimos datos
      - escritura: sockets listos para enviar datos a traves de ellos
      - errores:   sockets con excepciones
    
    sockets_lectura, _, sockets_excepcion = select.select(self.lista_sockets, [], self.lista_sockets)


    # por cada socket en el que recibimos datos
    for socket_notificado in sockets_lectura:

        # Si el socket es nuestro socket servidor, entonces recibimos una nueva conexion
        if socket_notificado == self.server_socket:
            client_socket, client_address = self.server_socket.accept()

            # Recibimos el nombre de usuario del chat
            user = recibir_mensaje(client_socket)

            # Si no hay nada, se desconecto, seguimos con la lista 
            if user is False:
                continue

            # Agregar el socket de cliente a la lista de sockets
            self.lista_sockets.append(client_socket)

            # Agregar usuario al diccionario de self.clientes
            self.clientes[client_socket] = user

            print('Aceptada nueva conexion desde {}:{}, username: {}'.format(*client_address, user['datos'].decode('utf-8')))

        # Si el socket es un cliente, significa que recibimos mensaje del chat
        else:

            mensaje = recibir_mensaje(socket_notificado)

            if mensaje is False:
                print('Cerrada la conexion desde: {}'.format(self.clientes[socket_notificado]['datos'].decode('utf-8')))
                self.lista_sockets.remove(socket_notificado)
                del self.clientes[socket_notificado]
                continue

            # Conseguir usuario del socket notificado, para saber quien mando el mensaje
            user = self.clientes[socket_notificado]

            print(f'Mensaje recibido desde {user["datos"].decode("utf-8")}: {mensaje["datos"].decode("utf-8")}')

            # Mandamos el mensaje a todos los self.clientes
            for client_socket in self.clientes:
                if client_socket != socket_notificado:
                    client_socket.send(user['cabecera'] + user['datos'] + mensaje['cabecera'] + mensaje['datos'])

    # Si hubiese un error en un socket lo eliminamos 
    for socket_notificado in sockets_excepcion:
        self.lista_sockets.remove(socket_notificado)
        del self.clientes[socket_notificado]
'''

class Server:

    HEADER_LENGTH = 10


    def __init__(self, IP, PORT) -> None:
        self.IP = IP 
        self.PORT = PORT 
        self.lista_sockets = []
        # diccionario, el socket como key y la cabecera y username como datos
        self.clientes = {}
        self.server_socket = None


    def __recibir_mensaje__(self, client_socket: socket.socket) -> None:
        ''' se encarga de recibir un mensaje y devolver su cabecera y datos'''
        try:

            # Recibimos el encabezado, que contiene el tamaño del mensaje 
            cabecera_mensaje = client_socket.recv(self.HEADER_LENGTH)

            # Si no recibimos nada, devolvemos false
            if not len(cabecera_mensaje):
                return False

            # Calculamos el tamaño del mensaje a través de la cabecera
            tamaño_mensaje = int(cabecera_mensaje.decode('utf-8').strip())

            # Devolvemos un diccionario con la cabecera y los datos (mensaje) recibidos
            return {'cabecera': cabecera_mensaje, 'datos': client_socket.recv(tamaño_mensaje)}

        except:
            return False


    def __aceptar_conexion__(self) -> bool:
        client_socket, client_address = self.server_socket.accept()

        # Recibimos el nombre de usuario del chat
        user = self.__recibir_mensaje__(client_socket)

        # Si no hay nada, se desconecto
        if user is False:
            client_socket.close()
            return False

        # Agregar el socket de cliente a la lista de sockets
        self.lista_sockets.append(client_socket)

        # Agregar usuario al diccionario de self.clientes
        self.clientes[client_socket] = user

        print('Aceptada nueva conexion desde {}:{}, username: {}'.format(*client_address, user['datos'].decode('utf-8')))

        return True


    def __remover_conexion__(self, socket_notificado: socket.socket) -> None:
        print('Cerrada la conexion desde: {}'.format(self.clientes[socket_notificado]['datos'].decode('utf-8')))
        self.lista_sockets.remove(socket_notificado)
        del self.clientes[socket_notificado]
        socket_notificado.close()


    def __establecer_conexion__(self) -> None:
        # AF_INTET es IPv4 y SOCK_STREAM es TCP 
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # para reconectar a la misma direccion
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Vincular el socket para informar al SO que usamos esa IP y PUERTO
        self.server_socket.bind((self.IP, self.PORT))

        # Escuchando por nuevas conexiones
        self.server_socket.listen()

        # Incluimos el socket del servidor en la lista de sockets
        self.lista_sockets.append(self.server_socket)


    def correr_servidor(self) -> None:
        self.__establecer_conexion__()
        print(f'Escuchando para conexiones en {self.IP}:{self.PORT}...')
        while True:
            '''
            La función select recibe tres iterables que contienen descriptores de archivos (sockets):
            - rlist: sockets en espera para lectura
            - wlist: sockets en espera para escritura
            - xlist: esperar a una excepcion
            Y devuelve tres iterables, que son subconjuntos de los parametros
            - lectura:    sockets en los que recibimos datos
            - escritura: sockets listos para enviar datos a traves de ellos
            - errores:   sockets con excepciones
            '''
            sockets_lectura, _, sockets_excepcion = select.select(self.lista_sockets, [], self.lista_sockets)

            # por cada socket en el que recibimos datos
            for socket_notificado in sockets_lectura:

                # Si el socket es nuestro socket servidor, entonces recibimos una nueva conexion
                if socket_notificado == self.server_socket:
                    exito = self.__aceptar_conexion__()

                    # Si no hay nada, se desconecto, seguimos con la lista 
                    if not exito:
                        continue

                # Si el socket es un cliente, significa que recibimos mensaje del chat
                else:

                    mensaje = self.__recibir_mensaje__(socket_notificado)

                    if not mensaje:
                        self.__remover_conexion__(socket_notificado)
                        continue

                    # Conseguir usuario del socket notificado, para saber quien mando el mensaje
                    user = self.clientes[socket_notificado]

                    print(f'Mensaje recibido desde {user["datos"].decode("utf-8")}: {mensaje["datos"].decode("utf-8")}')

                    # Mandamos el mensaje a todos los self.clientes
                    for client_socket in self.clientes:
                        if client_socket != socket_notificado:
                            client_socket.send(user['cabecera'] + user['datos'] + mensaje['cabecera'] + mensaje['datos'])

            # Si hubiese un error en un socket lo eliminamos 
            for socket_notificado in sockets_excepcion:
                self.__remover_conexion__(socket_notificado)
                # self.lista_sockets.remove(socket_notificado)
                # del self.clientes[socket_notificado]
 