from server import Server

if __name__ == "__main__":
	server = Server(IP="127.0.0.1",PORT=1234)
	server.correr_servidor()
