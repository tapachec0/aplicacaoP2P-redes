import P2P
import socket
import threading

class Client:
    peers = []
    def __init__(self, ip_address, nickname, port=4400):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((ip_address, port))
        
        iThread1 = threading.Thread(target=self.sendMsg, args=(sock, nickname))
        iThread1.daemon = True
        iThread1.start()

        while True:
            data = sock.recv(1024)
            if not data:
                break
            if data[0:1] == b'\x11':
                self.updatePeers(data[1:])
            else:
                print(str(data, 'utf-8'))

    def sendMsg(self, sock, nickname):
        while True:
            msg = input("{}:".format(nickname))
            sock.send(bytes('{}: {}'.format(nickname, msg), 'utf-8'))

    def updatePeers(self, peerData):
        P2P.peers = str(peerData, "utf-8").split(",")[:-1]
