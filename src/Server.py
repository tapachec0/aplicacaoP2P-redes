# -*- coding: utf-8 -*-
import P2P
from Player import Player
import socket
import threading
import sys
import time
from random import randint

class Server(Player):
    connections = []
    def __init__(self, ip_address, nickname, port=4400):
        super().__init__()
        self.ranking = 'Ranking\n'
        self.round_leader=False
        self.round_on=False
        self.noInput = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((ip_address, port)) #Instrui o sistema operacional para colocar o socket em modo passivo
        self.nickname = nickname
        self.sock.listen(1)
        print("Server running...")
        print("{}:".format(nickname), end=" ")

        iThread1 = threading.Thread(target=self.sendMsg, args=(nickname,))
        iThread1.daemon = True
        iThread1.start()

        while True:
            c,a = self.sock.accept() 

            cThread2 = threading.Thread(target=self.handler, args=(c, a, nickname))
            cThread2.daemon = True
            cThread2.start()

            self.connections.append(c)
            P2P.peers.append(a[0])
            '''mostrando o cliente que entra no chat'''
            print("\n"+str(a[0]), "connected"+"\n{}:".format(nickname), end=" ")
            self.sendPeers()
        
    def sendMsg(self, nickname):
        while True:
            if not self.noInput:
                msg = input("")
                if msg.startswith('/'):
                    Thread3 = threading.Thread(target=self.handle_command, args=(msg,))
                    Thread3.daemon = True
                    Thread3.start()
                else:
                    for connection in self.connections:
                        connection.send(bytes('{}: {}'.format(nickname, msg), 'utf-8'))
                print("{}:".format(nickname), end=" ")

    def handler(self, c, a, nickname):
        while True:
            try:
                data = str(c.recv(1024), 'utf-8')
                if self.round_on and self.round_leader:
                    if "go" in data:
                        command, player_nickname = data.split(":")
                        self.ranking+="{} - Acertou\n".format(player_nickname) if self.handle_command(command) else "{} - Errou\n".format(player_nickname)
                else:
                    for connection in self.connections:
                        if(connection is not c):
                            connection.send(bytes(data, 'utf-8'))
                    print('\n'+data+"\n{}:".format(nickname), end=" ")
            except:
                raise
            if not data:
                print(str(a[0]) + ':' + str(a[1]), "disconnected"+"\n{}:".format(nickname), end=" ")
                self.connections.remove(c)
                P2P.peers.remove(a[0])
                c.close()
                self.sendPeers()
                break

    def sendPeers(self):
        p = ""
        for peer in P2P.peers:
            p = p + peer + ","

        for connection in self.connections:
            connection.send(b'\x11' + bytes(p, 'utf-8'))
    
    def exit(self):
        self.sock.close()
