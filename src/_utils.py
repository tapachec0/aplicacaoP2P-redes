# -*- coding: utf-8 -*-
"Script para escrever funçoes uteis a serem utilizadas no software."

import sys
import time
from random import randint
from Server import Server
from Client import Client
import P2P
from ipaddress import ip_address

def set_connection():
    while True:
        try:
            print("Trying to connect...")
            time.sleep(randint(1,5))
            for peer in P2P.peers:
                nickname=peer.split(':')[0]
                ip_address=peer.split(':')[1]
                print(ip_address, nickname)
                try:
                    client = Client(ip_address=ip_address, nickname=nickname)
                except KeyboardInterrupt:
                    sys.exit(0)
                except:
                    pass

                try:
                    server = Server(ip_address=ip_address, nickname=nickname)
                except KeyboardInterrupt:
                    sys.exit(0)
                except:
                    raise
                    print("Couldn't start the server...")

        except KeyboardInterrupt:
            sys.exit(0)
