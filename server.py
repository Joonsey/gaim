from network import Server
from sys import argv
IP = "0.0.0.0"
PORT = 5555

if __name__ == "__main__":
    args = len(argv) > 1
    if args:
        if argv[1] == '-l':
            IP = "localhost"
    server = Server(IP, PORT)
    server.run()
