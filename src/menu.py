# -*- coding: utf-8 -*-
from Client import Client
import P2P
import _utils

def menu_principal():
    print("Vamos começar o jogo!!!")
    ip = input("Insira seu IP:")
    nickname = input("Insira um nickname: ")
    P2P.peers.append('{}:{}'.format(nickname,ip))
    print("\n0 - Sair")
    print("1 - Juntar-se a sala existente")
    print("2 - Criar nova sala")
    print("3 - Sair")
    
    while True:
        command = int(input('{}: '.format(nickname)))
        if command == 0:
            break
        elif command == 1:
            join_room(nickname)
        elif command == 2:
            _utils.set_connection()
        elif command == 3:
            break
    
def join_room(nickname):
    class_ip=input("Insira o IP da sala a qual deseja se juntar: ")
    cliente = Client(ip_address=class_ip, nickname=nickname)

menu_principal()