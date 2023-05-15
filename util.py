from simulator import *
from collections import Counter
from itertools import combinations



def validate_card(card):
    assert isinstance(card,Card)
    assert card.validate()

def check_all_equal(lst):
    if not lst:  # If the list is empty, return True
        return True
    first_element = lst[0]
    for element in lst:
        if element != first_element:
            return False
    return True

def pretty_bool(bool):
    if bool:
        return '🟩'
    else:
        return '🟥'

def are_consecutive(lst):
    sorted_lst = sorted(lst)  # Sort the list in ascending order
    return all(sorted_lst[i] + 1 == sorted_lst[i + 1] for i in range(len(sorted_lst) - 1))

def flatten(lst):
    flattened_list = []
    for item in lst:
        if isinstance(item, list):
            flattened_list.extend(flatten(item))
        else:
            flattened_list.append(item)
    return flattened_list



def extract_hand(hand):
    hand_id = {name: 0 for name in hand_names}
    hand_values = sorted([card.value for card in hand.cards])
    hand_suits = [card.suit for card in hand.cards]
    hand_value_counter = Counter(hand_values)
    hand_suit_counter = Counter(hand_suits)

    repeated_cards_values = {}
    for card_value, count in hand_value_counter.items():
        if count not in repeated_cards_values:
            repeated_cards_values[count] = [card_value]
        else:
            repeated_cards_values[count].append(card_value)
            repeated_cards_values[count] = sorted(repeated_cards_values[count], reverse=True)

    flush_hand = any(count >= 5 for count in hand_suit_counter.values())
    straight_hand = are_consecutive(hand_values)

    hand_id['High Card'] = max(hand_values)
    if 2 in repeated_cards_values:
        hand_id['One Pair'] = repeated_cards_values[2]
        if len(repeated_cards_values[2]) >= 2:
            hand_id['Two Pair'] = repeated_cards_values[2][:2]
    if 3 in repeated_cards_values:
        hand_id['Three of a Kind'] = repeated_cards_values[3][0]
    if straight_hand:
        hand_id['Straight'] = max(hand_values)
    if flush_hand:
        hand_id['Flush'] = 1
    if hand_id['One Pair'] and hand_id['Three of a Kind']:
        hand_id['Full House'] = [hand_id['Three of a Kind'], hand_id['One Pair'][0]]
    if 4 in repeated_cards_values:
        hand_id['Four of a Kind'] = repeated_cards_values[4][0]
    if straight_hand and flush_hand:
        if hand_values[0] == 10 and hand_values[-1] == 14:
            hand_id['Royal Flush'] = 1
        else:
            hand_id['Straight Flush'] = max(hand_values)

    return hand_id

def compare_hands(hand1, hand2):
    def compare_nested_lists(list1, list2):
        for i in range(min(len(list1), len(list2))):
            if list1[i] != list2[i]:
                return list1[i] > list2[i]
        return len(list1) > len(list2)

    for hand_name in hand_names:
        if hand1[hand_name] != hand2[hand_name]:
            if isinstance(hand1[hand_name], list) and isinstance(hand2[hand_name], list):
                return compare_nested_lists(hand1[hand_name], hand2[hand_name])
            elif isinstance(hand1[hand_name], list):
                return 1
            elif isinstance(hand2[hand_name], list):
                return -1
            else:
                return hand1[hand_name] > hand2[hand_name]
    return 0

def extract_best_hand(seven_card_hand):
    best_hand = None
    best_hand_id = None
    best_hand_name = None

    for hand in combinations(seven_card_hand.cards, 5):
        hand_object = Hand(list(hand))  # Assuming Hand is your defined class for a poker hand
        hand_id = extract_hand(hand_object)

        if best_hand_id is None or compare_hands(hand_id, best_hand_id) > 0:
            best_hand = hand_object
            best_hand_id = hand_id
            # Now, find the best hand name
            for hand_name in hand_names:
                if hand_id[hand_name] != 0:
                    best_hand_name = hand_name
                    break

    return best_hand,best_hand_id,best_hand_name



if __name__ == "__main__":
    hand = Hand(
        [Card('10', 'Hearts'), Card('J', 'Hearts'), Card('Q', 'Hearts'), Card('K', 'Hearts'), Card('A', 'Hearts'),
         Card('2', 'Clubs'), Card('3', 'Clubs')])
    print(extract_best_hand(hand)[1])

    hand = Hand(
        [Card('9', 'Hearts'), Card('10', 'Hearts'), Card('J', 'Hearts'), Card('Q', 'Hearts'), Card('K', 'Hearts'),
         Card('2', 'Clubs'), Card('3', 'Clubs')])
    print(extract_best_hand(hand)[1])

    hand = Hand([Card('9','Hearts'), Card('9','Clubs'), Card('9','Spades'), Card('9','Diamonds'), Card('K','Hearts'), Card('2','Clubs'), Card('3','Clubs')])
    print(extract_best_hand(hand)[1])

    hand = Hand(
        [Card('9', 'Hearts'), Card('9', 'Clubs'), Card('K', 'Spades'), Card('K', 'Diamonds'), Card('K', 'Hearts'),
         Card('2', 'Clubs'), Card('3', 'Clubs')])
    print(extract_best_hand(hand)[1])

    hand = Hand(
        [Card('2', 'Hearts'), Card('5', 'Hearts'), Card('9', 'Hearts'), Card('K', 'Hearts'), Card('Q', 'Hearts'),
         Card('2', 'Clubs'), Card('3', 'Clubs')])
    print(extract_best_hand(hand)[1])

    hand = Hand(
        [Card('9', 'Hearts'), Card('10', 'Clubs'), Card('J', 'Spades'), Card('Q', 'Diamonds'), Card('K', 'Hearts'),
         Card('2', 'Clubs'), Card('3', 'Clubs')])
    print(extract_best_hand(hand)[1])

    hand = Hand([Card('9','Hearts'), Card('9','Clubs'), Card('9','Spades'), Card('K','Diamonds'), Card('Q','Hearts'), Card('2','Clubs'), Card('3','Clubs')])
    print(extract_best_hand(hand)[1])

    hand = Hand(
        [Card('9', 'Hearts'), Card('9', 'Clubs'), Card('K', 'Spades'), Card('K', 'Diamonds'), Card('Q', 'Hearts'),
         Card('2', 'Clubs'), Card('3', 'Clubs')])
    print(extract_best_hand(hand)[1])

    hand = Hand(
        [Card('9', 'Hearts'), Card('9', 'Clubs'), Card('10', 'Spades'), Card('K', 'Diamonds'), Card('Q', 'Hearts'),
         Card('2', 'Clubs'), Card('3', 'Clubs')])
    print(extract_best_hand(hand)[1])

















