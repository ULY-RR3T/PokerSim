from .config import *
from collections import Counter
from itertools import combinations
from collections import defaultdict
from lib.util import are_consecutive

class Hand:
    class PokerHand:
        def __init__(self):
            self.royal_flush = {'value': 0}
            self.straight_flush = {'value': 0}
            self.four_of_a_kind = {'value': 0, 'kicker': []}
            self.full_house = {'value': []}
            self.flush = {'value': 0}
            self.straight = {'value': 0}
            self.three_of_a_kind = {'value': 0, 'kicker': []}
            self.two_pair = {'value': [], 'kicker': []}
            self.one_pair = {'value': 0, 'kicker': []}
            self.high_card = {'value': 0, 'kicker': []}

        def get_hands(self):
            return [self.royal_flush, self.straight_flush, self.four_of_a_kind, self.full_house, self.flush,
                    self.straight, self.three_of_a_kind, self.two_pair, self.one_pair, self.high_card]

        def get_best_hand_rank(self):
            current_hands = self.get_hands()
            for id, hand in enumerate(current_hands):
                if hand['value'] != 0 and hand['value'] != []:
                    return id

    def __init__(self, cards):
        self.cards = cards
        self.size = len(cards)
        self.best_hand = None
        if self.size == 7:
            self.best_hand,self.best_hand_object,self.best_hand_rank = self.extract_best_hand()
            self.best_hand_name = HandType._member_names_[self.best_hand_rank]

        self.validate()

    def add_card(self, card):
        card.validate()
        if self.size + 1 > 7:  # Assuming 7 cards is the max
            raise Exception(f"Can't add more card to hand of size {self.size}")
        self.cards.append(card)
        self.best_hand = self.extract_best_hand()

    def validate(self):
        for card in self.cards:
            card.validate()

    def __str__(self):
        return ",".join([str(card) for card in self.cards])

    def __lt__(self, other):
        if self.size != 7 or other.size != 7:
            raise Exception("Hands can only be compared if they both contain exactly 7 cards.")
        return self.compare_hands(self.best_hand, other.best_hand) < 0

    def __eq__(self, other):
        if self.size != 7 or other.size != 7:
            raise Exception("Hands can only be compared if they both contain exactly 7 cards.")
        return self.compare_hands(self.best_hand, other.best_hand) == 0

    def extract_best_hand(self):
        best_hand = None
        best_hand_object = None
        best_hand_rank = -1

        for hand in combinations(self.cards, 5):
            hand_object = Hand(list(hand))
            poker_hand = self.extract_hand(hand_object)
            if self.compare_hands(poker_hand, best_hand) > 0:
                best_hand = poker_hand
                best_hand_object = hand_object
                best_hand_rank = best_hand.get_best_hand_rank()

        return best_hand,best_hand_object,best_hand_rank

    def extract_hand(self,hand):
        poker_hand = self.PokerHand()
        hand_values = sorted([card.value for card in hand.cards], reverse=True)
        hand_suits = [card.suit for card in hand.cards]
        hand_value_counter = Counter(hand_values)
        hand_suit_counter = Counter(hand_suits)

        repeated_cards_values = defaultdict(list)
        for card_value, count in hand_value_counter.items():
            repeated_cards_values[count].append(card_value)
            repeated_cards_values[count].sort(reverse=True)

        flush_hand = any(count >= 5 for count in hand_suit_counter.values())
        straight_hand = are_consecutive(hand_values)

        poker_hand.high_card['value'] = max(hand_values)
        self.process_pairs(poker_hand, repeated_cards_values, hand_values)
        self.process_three_and_four_of_a_kind(poker_hand, repeated_cards_values, hand_values)
        self.process_straight_and_flush(poker_hand, flush_hand, straight_hand, hand_values)

        return poker_hand

    def process_pairs(self,poker_hand, repeated_cards_values, hand_values):
        if 2 in repeated_cards_values:
            poker_hand.one_pair['value'] = repeated_cards_values[2][0]
            poker_hand.one_pair['kicker'] = [x for x in hand_values if x != poker_hand.one_pair['value']][:3]
            if len(repeated_cards_values[2]) >= 2:
                poker_hand.two_pair['value'] = repeated_cards_values[2][:2]
                poker_hand.two_pair['kicker'] = [x for x in hand_values if x not in poker_hand.two_pair['value']][:1]

    def process_three_and_four_of_a_kind(self,poker_hand, repeated_cards_values, hand_values):
        if 3 in repeated_cards_values:
            poker_hand.three_of_a_kind['value'] = repeated_cards_values[3][0]
            poker_hand.three_of_a_kind['kicker'] = [x for x in hand_values if x != poker_hand.three_of_a_kind['value']][
                                                   :2]
            if poker_hand.one_pair['value']:
                poker_hand.full_house['value'] = [poker_hand.three_of_a_kind['value'], poker_hand.one_pair['value']]
        if 4 in repeated_cards_values:
            poker_hand.four_of_a_kind['value'] = repeated_cards_values[4][0]
            poker_hand.four_of_a_kind['kicker'] = [x for x in hand_values if x != poker_hand.four_of_a_kind['value']][
                                                  :1]

    def process_straight_and_flush(self,poker_hand, flush_hand, straight_hand, hand_values):
        if straight_hand:
            poker_hand.straight['value'] = max(hand_values)
        if flush_hand:
            poker_hand.flush['value'] = 1
        if straight_hand and flush_hand:
            if max(hand_values) == 14 and min(hand_values) == 10:
                poker_hand.royal_flush['value'] = 1
            else:
                poker_hand.straight_flush['value'] = max(hand_values)

    def compare_hands(self,hand1, hand2) -> int:
        """ Compare two hands.

        Return 1 if hand1 is better, -1 if hand2 is better, 0 if they are equal.
        """
        if hand1 is None and hand2 is None:
            raise Exception("Can't compare two null hands")
        if hand1 is None:
            return -1
        if hand2 is None:
            return 1

        hand1_types = hand1.get_hands()
        hand2_types = hand2.get_hands()

        for hand_type in HandType:
            if (hand1_types[hand_type.value]['value'] == 0) and (hand2_types[hand_type.value]['value'] == 0):
                continue
            if (hand1_types[hand_type.value]['value'] == []) and (hand2_types[hand_type.value]['value'] == []):
                continue
            if hand1_types[hand_type.value]['value'] > hand2_types[hand_type.value]['value']:
                return 1
            elif hand1_types[hand_type.value]['value'] < hand2_types[hand_type.value]['value']:
                return -1

            elif 'kicker' in hand1_types[hand_type.value]:  # If the hand type values are equal, compare the kicker
                kicker1 = hand1_types[hand_type.value]['kicker']
                kicker2 = hand2_types[hand_type.value]['kicker']
                if kicker1 > kicker2:
                    return 1
                elif kicker1 < kicker2:
                    return -1

        return 0  # Hands are equal
