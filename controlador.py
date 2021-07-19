from cliente import Cliente
from vistas import VistaPrincipal

class Controlador:
  # Variable de clase para posicionar en el chat
	i = 0

	def __init__(self, cliente: Cliente, vista: VistaPrincipal) -> None:
		self.cliente = cliente
		self.vista = vista
		self.vista.btn.configure(command=self.mandar_mensaje)


	def mandar_mensaje(self) -> None:
		''' 
		Se encarga de mandar el mensaje a través del modelo
		y de insertarlo en la vista (widget chat)
		'''
		mensaje = self.vista.get_mensaje()
		self.cliente.mandar_mensaje(mensaje)
		self.vista.chat.insert(self.i, f'tú: {mensaje}')
		self.i += 1
		self.vista.msj.delete(0, 'end')


	def establecer_conexion(self, username: str) -> None:
		''' Se encarga de establecer la conexion del socket'''
		self.cliente.establecer_conexion(username)


	def recibir_mensaje(self) -> None:
		''' Se encarga de recibir los mensajes de otros usuarios'''
		mensaje = self.cliente.recibir_mensaje()
		if mensaje:
			self.vista.chat.insert(self.i, mensaje)
			self.i += 1


	def run_main(self) -> None:
		''' Se encarga de ejecutar la ventana '''
		self.vista.window.mainloop()