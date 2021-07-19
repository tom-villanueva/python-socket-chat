import socket
import select

cabecera_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234

# AF_INTET es IPv4 y SOCK_STREAM es TCP 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# para reconectar a la misma direccion
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Vincular el socket para informar al SO que usamos esa IP y PUERTO
server_socket.bind((IP, PORT))

# Escuchando por nuevas conexiones
server_socket.listen()

# Creamos una lista de sockets, e incluimos el socket del servidor
lista_sockets = [server_socket]

# Creamos un diccionario de clientes, el socket como key y la cabecera y username como datos
clientes = {}

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
    sockets_lectura, _, sockets_excepcion = select.select(lista_sockets, [], lista_sockets)


    # por cada socket en el que recibimos datos
    for socket_notificado in sockets_lectura:

        # Si el socket es nuestro socket servidor, entonces recibimos una nueva conexion
        if socket_notificado == server_socket:
            client_socket, client_address = server_socket.accept()

            # Recibimos el nombre de usuario del chat
            user = recibir_mensaje(client_socket)

            # Si no hay nada, se desconecto, seguimos con la lista 
            if user is False:
                continue

            # Agregar el socket de cliente a la lista de sockets
            lista_sockets.append(client_socket)

            # Agregar usuario al diccionario de clientes
            clientes[client_socket] = user

            print('Aceptada nueva conexion desde {}:{}, username: {}'.format(*client_address, user['datos'].decode('utf-8')))

        # Si el socket es un cliente, significa que recibimos mensaje del chat
        else:

            mensaje = recibir_mensaje(socket_notificado)

            if mensaje is False:
                print('Cerrada la conexion desde: {}'.format(clientes[socket_notificado]['datos'].decode('utf-8')))
                lista_sockets.remove(socket_notificado)
                del clientes[socket_notificado]
                continue

            # Conseguir usuario del socket notificado, para saber quien mando el mensaje
            user = clientes[socket_notificado]

            print(f'Mensaje recibido desde {user["datos"].decode("utf-8")}: {mensaje["datos"].decode("utf-8")}')

            # Mandamos el mensaje a todos los clientes
            for client_socket in clientes:
                if client_socket != socket_notificado:
                    client_socket.send(user['cabecera'] + user['datos'] + mensaje['cabecera'] + mensaje['datos'])

    # Si hubiese un error en un socket lo eliminamos 
    for socket_notificado in sockets_excepcion:
        lista_sockets.remove(socket_notificado)
        del clientes[socket_notificado]