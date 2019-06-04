# -*- coding: utf-8 -*-

from Player import Player
import P2P
import socket
import threading

class Client(Player):
    def __init__(self, ip_address, nickname, port=4400):
        self.ranking = ''
        self.round_leader=False
        self.round_on=False
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.connect((ip_address, port))
        self.nickname = nickname
        
        print("{}:".format(nickname), end=" ")
        iThread1 = threading.Thread(target=self.sendMsg, args=(self.sock, nickname))
        iThread1.daemon = True
        iThread1.start()

        while True:
            try:
                data = self.sock.recv(1024)
            except:
                break
            if not data:
                break
            if data[0:1] == b'\x11':
                self.updatePeers(data[1:])
            else:
                print("\n"+str(data, 'utf-8')+"\n{}:".format(nickname), end=" ")

    def sendMsg(self, sock, nickname):
        while True:
            msg = input("")
            if msg.startswith('/'):
                self.handle_command(msg[0:])
            else:
                sock.send(bytes('{}: {}'.format(nickname, msg), 'utf-8'))
            print("\n{}:".format(nickname), end=" ")

    def updatePeers(self, peerData):
        P2P.peers = str(peerData, "utf-8").split(",")[:-1]
        
    def exit(self):
        self.sock.close()
