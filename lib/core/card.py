from .config import *
class Card:
    def __init__(self,rank,suit):
        try:
            self.rank = rank
            self.value = card_name_to_value[rank]
            self.suit = suit
            self.validate()
        except:
            raise Exception("Card Initialization Error!")

    def validate(self):
        assert self.rank in card_ranks
        assert self.suit in card_suits

    def __str__(self):
        suit_string = card_suits_to_string[self.suit]
        if suit_string == '♥':
            color_suit_string = f"\033[31m{suit_string}\033[0m"
        elif suit_string == '♦':
            color_suit_string = f"\033[41m{suit_string}\033[0m"
        elif suit_string == '♣':
            color_suit_string = f"\033[37m{suit_string}\033[0m"
        else:
            color_suit_string = f"\033[47m{suit_string}\033[0m"
        return f"{color_suit_string}{self.rank}"
