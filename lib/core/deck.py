from .card import Card
from .config import *
import random
class Deck:
    def __init__(self):
        self.deck = []
        for rank in card_ranks:
            for suit in card_suits:
                self.deck.append(Card(rank,suit))
        self.size = len(self.deck)
        assert self.size == 52

    def shuffle(self):
        random.shuffle(self.deck)

    def draw(self):
        card = self.deck.pop()
        self.size -= 1
        return card