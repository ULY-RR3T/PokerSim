import random
from util import *

card_ranks = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
card_values = [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
card_suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

card_name_to_value = {'A':14,'K':13,'Q':12,'J':11,'10':10,'9':9,'8':8,'7':7,'6':6,'5':5,'4':4,'3':3,'2':2}
card_value_to_name = {14:'A',13:'K',12:'Q',11:'J',10:'10',9:'9',8:'8',7:'7',6:'6',5:'5',4:'4',3:'3',2:'2'}

card_suits_to_string = {'Hearts':'♥','Diamonds':'♦','Clubs':'♣','Spades':'♠'}

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
        return f"{card_suits_to_string[self.suit]}{self.rank}"

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

class Hand:
    def __init__(self, cards):
        self.cards = cards
        self.size = len(cards)
        self.validate()

    def add_card(self, card):
        card.validate()
        if self.size + 1 > 7:  # Assuming 7 cards is the max
            raise Exception(f"Can't add more card to hand of size {self.size}")
        self.cards.append(card)

    def validate(self):
        for card in self.cards:
            card.validate()

    def __str__(self):
        return ",".join([str(card) for card in self.cards])

    def __lt__(self, other):
        if self.size != 7 or other.size != 7:
            raise Exception("Hands can only be compared if they both contain exactly 7 cards.")
        return compare_hands(extract_best_hand(self)[1], extract_best_hand(other)[1]) < 0

    def __eq__(self, other):
        if self.size != 7 or other.size != 7:
            raise Exception("Hands can only be compared if they both contain exactly 7 cards.")
        return compare_hands(extract_best_hand(self)[1], extract_best_hand(other)[1]) == 0



class Round:
    def __init__(self,players):
        self.players = players
        self.pot = 0
        self.total_players = len(self.players)
        self.players_bets = [0 for i in range(self.total_players)]
        self.players_playing = [True for i in range(self.total_players)]
        self.players_actionable = [True for i in range(self.total_players)]
        self.players_all_in = [False for i in range(self.total_players)]
        self.players_split_pot = [True for i in range(self.total_players)]
        self.players_name_to_id = {player.name:i for i,player in enumerate(players)}
        self.curr_stage = "Initialization"
        self.history = []
        self.flop = Hand([])
        self.init_deck()

    def init_deck(self):
        self.deck = Deck()
        self.deck.shuffle()

    def play(self):
        ## Initial Hand
        self.bb = self.players[-1]
        self.sb = self.players[-2]
        for i,player in enumerate(self.players):
            self.history.append(f"{i}:{player.name}")

        self.prebet()
        self.draw_preflop()
        self.curr_stage = "Preflop"
        self.print_state()
        self.action()

        self.draw_flop(3)
        self.curr_stage = "Flop"
        self.print_state()
        self.action()


        self.draw_flop(1)
        self.curr_stage = "Turn"
        self.print_state()
        self.action()

        self.draw_flop(1)
        self.curr_stage = "River"
        self.print_state()
        self.action()

        self.distribute_pot()
        self.clean_round()

    def draw_preflop(self):
        for i in range(2):
            for player in self.players:
                player.receive_card(self.deck.draw())

    def draw_flop(self,num_cards):
        for i in range(num_cards):
            self.flop.add_card(self.deck.draw())

    def prebet(self):
        self.bet(self.bb,bb_cost)
        self.history.append(f"BB bets {bb_cost}")
        self.bet(self.sb,sb_cost)
        self.history.append(f"SB bets {sb_cost}")

    def bet(self,player,amount):
        if amount > player.chips:
            return False
        player.decrement_chips(amount)
        self.pot += amount
        player_id = self.players_name_to_id[player.name]
        self.players_bets[player_id] += amount
        return True

    def round_ended(self):
        ended = sum(self.players_playing) <= 1
        if ended:
            print("Round Ended!")
        return ended

    def action(self):
        action_id = 0
        while (not self.round_ended()) and (sum(self.players_actionable) != 0):
            if self.players_actionable[action_id]:
                self.move(action_id)
                self.print_state()
            action_id = (action_id + 1) % self.total_players
        self.renew_action_for_all_playing()
        self.reset_bets()

    def move(self,id):
        player = self.players[id]
        player_current_bet = self.players_bets[id]
        current_max_bet = max(self.players_bets)
        to_call = current_max_bet - player_current_bet
        valid_input = False
        while not valid_input:
            valid_input = True
            action = input(f"Player {self.players[id].name} (Fold 'F' / Check {to_call} 'C' / Raise x 'R' x / All-in 'A'): ")
            if action.upper() == 'F':
                self.players_playing[id] = False
            elif action.upper() == 'C':
                if to_call != 0:
                    valid_bet = self.bet(player,to_call)
                    if valid_bet:
                        self.history.append(f"{player.name} calls {to_call}")
                    else:
                        valid_input = False
                        print("Invalid move. Not enough chips.")
            elif action[0].upper() == 'R':
                try:
                    raise_amount = int(action[1:])
                    if raise_amount <= to_call or not self.bet(player, raise_amount):
                        valid_input = False
                        print("Invalid move. Raise must be more than the call amount and within your chip amount.")
                    else:
                        self.history.append(f"{player.name} raises {raise_amount}")
                        self.renew_action_for_insufficient_bet()
                except:
                    valid_input = False
                    print("Invalid input. Please try again.")
            elif action.upper() == 'A':
                if self.bet(player, player.chips):
                    self.history.append(f"{player.name} goes all in with {player.chips}")
                    self.players_all_in[id] = True
                    self.renew_action_for_insufficient_bet()
                else:
                    valid_input = False
                    print("Invalid move. You don't have any chips left.")
        self.players_actionable[id] = False

    def renew_action_for_insufficient_bet(self):
        max_bet = max(self.players_bets)
        for i in range(self.total_players):
            to_call = max_bet - self.players_bets[i]
            if self.players_bets[i] < max_bet and self.players_playing[i] and self.players[i].chips >= to_call and (not self.players_all_in[i]):
                self.players_actionable[i] = True

    def renew_action_for_all_playing(self):
        for i in range(self.total_players):
            if self.players_playing[i] and (not self.players_all_in[i]):
                self.players_actionable[i] = True

    def reset_bets(self):
        for i in range(self.total_players):
            self.players_bets[i] = 0

    def distribute_pot(self):
        # Find the best hand among the remaining players
        best_hand = None
        winners = []

        for i, player in enumerate(self.players):
            if self.players_playing[i]:
                hand = Hand(player.hand.cards + self.flop.cards)
                if best_hand is None or hand > best_hand:
                    best_hand = hand
                    winners = [player]
                elif hand == best_hand:
                    winners.append(player)

        # Distribute the pot among the winners
        for winner in winners:
            chips_won = round(self.pot / len(winners),2)
            print(f"Winner is {winner.name}! Winner hand is {best_hand}! Won chips {chips_won}!")
            winner.increment_chips(chips_won)

    def clean_round(self):
        # Reset the round-specific variables
        self.pot = 0
        self.deck = Deck()
        self.deck.shuffle()
        self.players_bets = [0 for _ in range(self.total_players)]
        self.players_playing = [True for _ in range(self.total_players)]
        self.players_actionable = [True for _ in range(self.total_players)]
        self.players_split_pot = [True for _ in range(self.total_players)]
        self.curr_stage = "Initialization"
        self.history = []
        self.flop = Hand([])
        self.init_deck()

        # Return the cards to the deck and shuffle
        for player in self.players:
            player.hand = Hand([])

    def print_state(self):
        print("-----------------------")
        print(f"Current Round Stage: {self.curr_stage}")
        print(f"Current pot: {self.pot}")
        print(f"Current flop: {self.flop}")
        for i,player in enumerate(self.players):
            print(f"{player.name} {player.hand} Bets:{self.players_bets[i]} Balance:{player.chips} "
                  f"Actionable:{pretty_bool(self.players_actionable[i])}. Playing:{pretty_bool(self.players_playing[i])}")
        print("-----------------------")


class Game:
    def __init__(self):
        self.init_players()
        self.round_number = 0

    def init_players(self):
        self.num_players = num_players
        self.players = []
        for i in range(self.num_players):
            new_player = Player(f"Player {i+1}", Hand([]), buyin_size)
            self.players.append(new_player)

    def play_round(self):
        print(f"\nRound {self.round_number}")
        round = Round(self.players)
        round.play()
        self.round_number += 1

    def play_game(self):
        while len(self.players) > 1:
            self.play_round()
            self.check_players()
        print(f"\nGame Over! Player {self.players[0].name} wins!")

    def check_players(self):
        self.players = [p for p in self.players if p.chips > 0]

if __name__ == "__main__":
    game = Game()
    game.play_game()