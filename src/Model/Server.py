import Model.Client as Client
import socket
import threading
import sys
import time
from random import randint

class Server:
    connections = []
    peers = []
    def __init__(self, ip_address, port=4400):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((ip_address, port))
        '''Instrui o sistema operacional para colocar o socket em modo passivo'''
        sock.listen(1)
        print("Server running...")

        while True:
            c,a = sock.accept()
            cThread = threading.Thread(target=self.handler, args=(c,a))
            cThread.daemon = True
            cThread.start()
            self.conections.append(c)
            self.peers.append(a[0])
            '''mostrando o cliente que entra no chat'''
            print(str(a[0]) + ':' + str(a[1]), "connected")
            self.sendPeers()

    def handler(self, c, a):
        while True:
            data = c.recv(1024)
            for connection in self.connections:
                connection.send(data)
            if not data:
                print(str(a[0]) + ':' + str(a[1]), "disconnected")
                self.connections.remove(c)
                self.peers.remove(a[0])
                c.close()
                self.sendPeers()
                break

    def sendPeers(self):
        p = ""
        for peer in self.peers:
            p = p + peer + ","

        for connection in self.connections:
            connection.send(b'\x11' + bytes(p, 'utf-8'))

class P2P:
    peers=['127.390.0.1']

while True:
    try:
        print("Trying to connect...")
        time.sleep(randint(1,5))
        for peer in P2P.peers:
            try:
                client = Client(peer)

            except KeyboardInterrupt:
                sys.exit(0)

            except:
                pass

            try:
                server = Server()
                
            except KeyboardInterrupt:
                sys.exit(0)
                
            except:
                print("Couldn't start the server...")

    except KeyboardInterrupt:
        sys.exit(0)
        
