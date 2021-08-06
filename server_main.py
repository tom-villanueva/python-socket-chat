from server import Server
import signal

if __name__ == "__main__":
	ip = input("IP: ")
	port = input("Puerto: ")
	port = int(port)

	server = Server(IP=ip,PORT=port)
	# Correr el servidor 
	server.correr_servidor()
