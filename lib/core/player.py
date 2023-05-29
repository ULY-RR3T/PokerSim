class Player:
    def __init__(self,name,hand,chips):
        self.name = name
        self.hand = hand
        self.chips = chips

    def receive_card(self,card):
        self.hand.add_card(card)

    def empty_hand(self):
        self.hand = []

    def decrement_chips(self,amount):
        self.chips -= amount

    def increment_chips(self,amount):
        self.chips += amount