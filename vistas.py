from tkinter import *

class VistaDialogo:

	def __init__(self) -> None:
		# widgets de la ventana
		self.window = Tk()
		self.window.geometry('350x200')
		self.window.title("Bienvenido")
		self.__init_widgets__()
		self.usuario = ''
		self.ip = '127.0.0.1'
		self.port = 1234
		self.window.mainloop()

	def clicked(self):
		self.usuario = self.username.get()
		self.ip = self.ipField.get()
		self.port = int(self.portField.get())
		self.window.destroy()

	def __init_widgets__(self) -> None:
		# widgets del formulario de bienvenida 
		self.label = Label(self.window, text="username: ")
		self.label.grid(column=0, row=0)

		self.username = Entry(self.window,width=10)
		self.username.grid(column=1, row=0)

		self.labelIP = Label(self.window, text="IP: ")
		self.labelIP.grid(column=0, row=1)

		self.ipField = Entry(self.window,width=10)
		self.ipField.grid(column=1, row=1)	

		self.labelPort = Label(self.window, text="Puerto: ")
		self.labelPort.grid(column=0, row=2)

		self.portField = Entry(self.window,width=10)
		self.portField.grid(column=1, row=2)

		self.btn = Button(self.window, text="aceptar", command=self.clicked)
		self.btn.grid(column=0, row=3)	

class VistaPrincipal:

	def __init__(self) -> None:
		# widgets de la ventana
		self.window = Tk()
		self.window.geometry('350x200')
		self.window.title("Chatroom Redes")
		self.__init_widgets__()

	def __init_widgets__(self) -> None:
    # widgets del chat
		self.scrollbar = Scrollbar(self.window, orient=VERTICAL)
		self.chat = Listbox(
			self.window,
			borderwidth=2,
			yscrollcommand=self.scrollbar.set
		)
		self.scrollbar.config(command=self.chat.yview)
		self.scrollbar.grid(column=1, row=0)
		self.chat.grid(column=0, row=0)
 
		self.label = Label(self.window, text="Escriba un mensaje")
		self.label.grid(column=0, row=1)

		self.msj = Entry(self.window,width=10)
		self.msj.grid(column=1, row=1)

		self.btn = Button(self.window, text="enviar")
		self.btn.grid(column=2, row=1)	


	def get_mensaje(self) -> str:
		return self.msj.get()