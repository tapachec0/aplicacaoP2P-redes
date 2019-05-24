from Views import *

def menu_principal():
    print("Vamos começar o jogo!!!")
    ip = input("Insira seu IP:")
    print("\n0 - Sair")
    print("1 - Juntar-se a sala existente")
    print("2 - Criar nova sala")
    print("3 - Ajustar configurações")
    
    while True:
        command = int(input('{}: '.format(ip)))
        if command == 0:
            break
        elif command == 1:
            cliente = join_room()
            return cliente
        elif command == 2:
            servidor = create_room()
            servidor.start()
            return servidor
    
    def join_room():
        class_ip=input("Insira o IP da sala à qual deseja se juntar: ")
        class_port=input("Insira o nº da porta da sala à qual deseja se juntar: ")
        cliente = Client(class_ip, class_port)

    def create_room():
        servidor = Server(ip)