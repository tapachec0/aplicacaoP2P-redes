# -*- coding: utf-8 -*-
import P2P
import socket
import threading
import sys
import time
from random import randint

class Server:
    connections = []
    peers = []
    def __init__(self, ip_address, nickname, port=4400):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((ip_address, port)) #Instrui o sistema operacional para colocar o socket em modo passivo
        
        iThread1 = threading.Thread(target=self.sendMsg, args=(nickname,))
        iThread1.daemon = True
        iThread1.start()
            
        sock.listen(1)
        print("Server running...")

        while True:
            c,a = sock.accept()

            cThread2 = threading.Thread(target=self.handler, args=(c, a, nickname))
            cThread2.daemon = True
            cThread2.start()
            self.connections.append(c)
            self.peers.append(a[0])
            '''mostrando o cliente que entra no chat'''
            print(str(a[0]), "connected")
            self.sendPeers()
        
    def sendMsg(self, nickname):
        while True:
            msg = input("{}:".format(nickname))
            for connection in self.connections:
                connection.send(bytes('{}: {}'.format(nickname, msg), 'utf-8'))

    def handler(self, c, a, nickname):
        while True:
            data = str(c.recv(1024), 'utf-8')
            for connection in self.connections:
                if(connection is not c):
                    connection.send(data)
            print(data)
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
    
    def getNickname(self):
        pass