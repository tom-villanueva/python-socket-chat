from tkinter import *
from controlador import Controlador
from vistas import VistaPrincipal, VistaDialogo
from cliente import Cliente
import threading

def recibir_mensajes(controlador: Controlador) -> None:
	while True:
		controlador.recibir_mensaje()

if __name__ == "__main__":
	# Creo la ventana de bienvenida, tomo el username 
	ventana_bienvenida = VistaDialogo()
	username = ventana_bienvenida.usuario
	ip = ventana_bienvenida.ip
	puerto = ventana_bienvenida.port

	# Creo la vista principal y el cliente
	ventana = VistaPrincipal()
	cliente = Cliente(ip, puerto)

	# Creo el controlador y establezco la conexion del cliente
	controlador = Controlador(cliente, ventana)
	controlador.establecer_conexion(username)

	# thread para poder recibir mensajes, y aun asi mandar msjs
	threading.Thread(target=recibir_mensajes, args=[controlador]).start()

	controlador.run_main()

