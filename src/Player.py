# -*- coding: utf-8 -*-
import time

class Player(object):
    def __init__(self):
        pass
    
    def handle_command(self, message):
        """
        Handles the command given by the user.
        """
        comando = message[1:]
        comando=comando.split(" ")
        if self.round_leader and self.round_on:
            if comando[0]=='go':
                return self.checkAnswer(comando[1])
        if comando[0]=='go' and type(self).__name__=="Client":
            self.sock.send(bytes("{}:{}".format(message,self.nickname), 'utf-8'))
        if comando[0]=='start' and type(self).__name__=="Server":
            self.noInput=True
            self.round_leader = True
            self.start()
        if comando[0]=='exit':
            self.exit()

    def start(self):
        msg = "O jogo está começando!\nLíder da rodada: {}".format(self.nickname)
        for connection in self.connections:
            connection.send(bytes('{}: {}'.format(self.nickname, msg), 'utf-8'))
        print(msg)
        self.start_game()

    def start_game(self):
        palavra = input("Você tem 20 segundos para enviar a palavra. Formato: /word (palavra,pa-la-vra): ")
        msg1 = "Aguardando o líder da rodada enviar a palavra."
        for connection in self.connections:
            connection.send(bytes('{}: {}'.format(self.nickname, msg1), 'utf-8'))
        if palavra:
            palavra = palavra[1:].split(" ")
            if(palavra[0]=='word'):
                palavra_game, self.resposta_game = palavra[1][1:-1].split(',')
                self.round_on=True
                msg2 = "Palavra: \"{}\". Você tem 15 segundos para enviar a resposta. Formato: /go pa-la-vra".format(str.upper(palavra_game))
                for connection in self.connections:
                    connection.send(bytes('{}: {}'.format(self.nickname, msg2), 'utf-8'))
                print("Aguardando respostas.")
                time.sleep(20)
                print("Ranking\n{}".format(self.ranking))
                for connection in self.connections:
                    connection.send(bytes(self.ranking, 'utf-8'))
                self.round_on=False
                self.round_leader=False
                self.noInput=False
            else:
                print('comando errado, tente novamente')
                self.noInput=False
                self.start_game()
        else: 
            print("Você não enviou a palavra.")
    
    def checkAnswer(self, resposta):
        if self.resposta_game:
            if self.resposta_game == resposta:
                return True
            else:
                return False