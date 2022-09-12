from random import randint

class Player:
    def __init__(self, conn, name=None):
        self.connection = conn
        if name==None:
            from uuid import uuid4
            self.name = uuid4().hex
        else:
            self.name = name
        self.hand = []
        self.bet = -1
        self.score = 0
        self.score_in_turn = 0

    def sendHand(self):
        self.connection.send(b'you hand {self.hand}')
        

    def set_bet(self,bet = None):
        if (bet==None):
            self.bet = input(f"{self.name}, what is your bet? ")
        else:
            self.bet = bet
        print(f'{self.name} = {self.bet}')
            
    
    def select_card(self,value):
        for i,card in enumerate(self.hand):
            if card == value:
                return self.hand.pop(i)
    
    def check_points(self):
        if self.bet == self.score_in_turn:
            if self.bet==0:
                self.score += 1
            else:
                self.score += 2*self.bet
        else:
            self.score -= abs(self.bet-self.score_in_turn)
        self.bet = -1
        self.score_in_turn = 0
            
        
    def print_score(self):
        print(f'{self.name} = {self.score}')