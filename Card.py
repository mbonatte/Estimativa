class Card:
    def __init__(self,value,suit):
        self.value = value
        self.suit = suit
        
    def __str__ (self):
        return f'{self.value}_of_{self.suit}'
    
    def __eq__(self, other):
        return (self.value == other.value and
                self.suit == other.suit)
    
    
    def isHigherThan(self,card):
        if self.suit == card.suit:
            if int(self.value) > int(card.value):
                return True
            else:
                return False
        else:
            if self.suit == 'Clubs':
                return False
            if self.suit == 'Diamonds':
                return True
            if self.suit == 'Spades' and card.suit == 'Hearts':
                return True
            else:
                return False