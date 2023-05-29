from enum import Enum

card_ranks = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
card_values = [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
card_suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
card_name_to_value = {'A':14,'K':13,'Q':12,'J':11,'10':10,'9':9,'8':8,'7':7,'6':6,'5':5,'4':4,'3':3,'2':2}
card_value_to_name = {14:'A',13:'K',12:'Q',11:'J',10:'10',9:'9',8:'8',7:'7',6:'6',5:'5',4:'4',3:'3',2:'2'}
card_suits_to_string = {'Hearts':'♥','Diamonds':'♦','Clubs':'♣','Spades':'♠'}

class HandType(Enum):
    ROYAL_FLUSH = 0
    STRAIGHT_FLUSH = 1
    FOUR_OF_A_KIND = 2
    FULL_HOUSE = 3
    FLUSH = 4
    STRAIGHT = 5
    THREE_OF_A_KIND = 6
    TWO_PAIR = 7
    ONE_PAIR = 8
    HIGH_CARD = 9


hand_names = [
    'Royal Flush',
    'Straight Flush',
    'Four of a Kind',
    'Full House',
    'Flush',
    'Straight',
    'Three of a Kind',
    'Two Pair',
    'One Pair',
    'High Card'
]

max_hand_size = 7
num_players = 8
bb_cost = 2
sb_cost = 1
buyin_size = 100