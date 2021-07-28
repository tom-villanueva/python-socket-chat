from server import Server
import signal

if __name__ == "__main__":
	server = Server(IP="192.168.1.19",PORT=1234)
	# Correr el servidor 
	server.correr_servidor()
