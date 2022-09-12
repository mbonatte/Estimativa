from Card import Card
from random import randrange

class Deck:
    def __init__(self):
        self.deck = []
        self.suits = ['hearts', 'diamonds', 'clubs', 'spades']
        self.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        self.creat_deck()
        
    def creat_deck(self):
        for suit in self.suits:
            for value in self.values:
                self.deck.append(Card(value,suit))
                
        self.shuffle()
    
    def shuffle(self):
        numberOfCards = len(self.deck)
        for i in range(numberOfCards):
          j = randrange(numberOfCards)
          tmp = self.deck[i]
          self.deck[i] = self.deck[j]
          self.deck[j] = tmp;
    
    def deal(self,n_cards):
        cards = []
        for i in range(n_cards):
            cards.append(self.deck.pop(0))
        return cards