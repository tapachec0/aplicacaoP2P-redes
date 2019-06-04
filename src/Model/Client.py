import Model.Server as Server
import socket
import threading
import sys
import time
from random import randint

class Client:
    peers = []
    def __init__(self, ip_address, port=4400):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip_address, port))

        iThread = threading.Thread(target=self.sendMsg, args=(sock,))
        iThread.daemon = True
        iThread.start()

        while True:
            data = sock.recv(1024)
            if not data:
                break
            if data[0:1] == b'\x11':
                self.updatePeers(data[1:])
            else:
                print(str(data, 'utf-8'))
                
                
    def sendMsg(self, sock):
        while True:
            sock.send(bytes(input(""), 'utf-8'))

    def updatePeers(self, peerData):
        self.peers = str(peerData, "utf-8").split(",")[:-1]

class P2P:
    peers=['127.390.0.1']
    
def set_connection():
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
        
