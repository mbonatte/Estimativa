import pickle
from Player import Player
from Deck import Deck
import time

class Game:

    def __init__(self,globalID,nPlayers):
        self.globalID = globalID
        self.numberOfPlayers = nPlayers
        self.playersActived = []
        self.matches = []
        self.cards_in_table = []
        self.current_player = None      
        
    def sendScores(self):
        print(f'{self.globalID} - Sending scores')
        time.sleep(1)
        scores = []
        for player in self.playersActived:
            scores.append(f'{player.name} = {player.score}')
        scores = {'SCORES': scores}
        scores = pickle.dumps(scores)
        for player in self.playersActived:
            time.sleep(0.1)
            player.connection.send(scores)
        
    
    def addPlayer(self, player):
        self.playersActived.append(player)
    
    def set_matches(self):
        print(f'{self.globalID} - Setting matcher')
        #from math import trunc
        #n_matches = trunc(52/self.numberOfPlayers)
        n_matches = 4
        self.matches = [i+1 for i in range(n_matches)]
        self.matches += ([i for i in range(n_matches,0,-1)])
        
    
    
    def sendHand(self,player):
        msg = {'HAND': player.hand}
        msg = pickle.dumps(msg)
        player.connection.send(msg)
    
    def deal(self,n_cards):
        print(f'{self.globalID} - Dealing bets')
        time.sleep(1)
        deck = Deck()
        for player in self.playersActived:
            time.sleep(0.1)
            player.hand = deck.deal(n_cards)
            self.sendHand(player)
        
    def setName(self, conn, value):
        print('setting name')
        for player in self.playersActived:
            if player.connection == conn:
                player.name = value
                print('name setted')


    def setBetViaConn(self, conn, value):
        for player in self.playersActived:
            if player.connection == conn:
                player.bet = value
                
    def setPickViaConn(self, conn, value):
        for player in self.playersActived:
            if player.connection == conn:
                self.cards_in_table.append(player.select_card(value))
                self.sendHand(player)
        
    
    def setBets(self):
        print(f'{self.globalID} - Setting bets')
        time.sleep(1)
        self.sendChat('Initiating betting !!!!')
        time.sleep(2)
        print("Bets:")
        for player in self.playersActived:
            time.sleep(0.1)
            msg = {'BET': ''}
            msg = pickle.dumps(msg)
            player.connection.sendall(msg)
            while player.bet == -1:
                print(player.bet)
                time.sleep(1)
            self.sendChat(f"{player.name} bet {player.bet}")
            
        
    
    def sendChat(self, msg):
        msg = {'CHAT': msg}
        msg=pickle.dumps(msg)
        for player in self.playersActived:
            player.connection.send(msg)
        
    
    def sendTable(self):
        msg = {'TABLE': self.cards_in_table}
        msg=pickle.dumps(msg)
        for player in self.playersActived:
            player.connection.send(msg)
    
    def winner_of_turn(self):
        highest_card = self.cards_in_table[0]
        winner = 0
        for i,card in enumerate(self.cards_in_table):
            if card.isHigherThan(highest_card):
                highest_card = card
                winner=i
        self.playersActived[winner].score_in_turn += 1
    
    
    def turn(self,n_cards):
        time.sleep(1)
        for turn in range(n_cards):
            print(f'{self.globalID} - Selecting cards ({turn+1}/{n_cards})')
            time.sleep(1)
            self.cards_in_table = []
            for player in self.playersActived:
                msg = {'PICK': ''}
                msg = pickle.dumps(msg)
                player.connection.send(msg)
                while len(player.hand) == (n_cards-turn):
                    time.sleep(1)
                self.sendTable()
            self.winner_of_turn()
    
    
    def initiateRound(self,n_cards):
        time.sleep(2)
        
        self.deal(n_cards)
        self.setBets()
        
        self.turn(n_cards)
            
        for player in self.playersActived:
            player.check_points()
        
        for player in self.playersActived:
            player.bet = -1

    def run(self):
        print(f'{self.globalID} - Starting game')
        self.set_matches()
        while(len(self.matches)!=0):
            print(f'{self.globalID} - Match {len(self.matches)}')
            self.sendScores()
            self.initiateRound(self.matches.pop(0))
