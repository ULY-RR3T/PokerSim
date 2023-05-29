from lib.core.card import Card
from lib.core.hand import Hand
import unittest

class TestPokerHandComparison(unittest.TestCase):

    def test_compare_royal_flush_straight_flush(self):
        # Test case where hand1 is a Royal Flush and hand2 is a Straight Flush
        hand1 = Hand(
            [Card('10', 'Hearts'), Card('J', 'Hearts'), Card('Q', 'Hearts'), Card('K', 'Hearts'), Card('A', 'Hearts'),
             Card('2', 'Clubs'), Card('3', 'Clubs')])
        hand2 = Hand(
            [Card('9', 'Hearts'), Card('10', 'Hearts'), Card('J', 'Hearts'), Card('Q', 'Hearts'), Card('K', 'Hearts'),
             Card('2', 'Clubs'), Card('3', 'Clubs')])

        self.assertEqual(hand1 > hand2, True)

    def test_compare_four_of_a_kind_full_house(self):
        # Test case where hand1 is a Four of a Kind and hand2 is a Full House
        hand1 = Hand(
            [Card('5', 'Hearts'), Card('5', 'Diamonds'), Card('5', 'Spades'), Card('5', 'Clubs'), Card('A', 'Hearts'),
             Card('2', 'Clubs'), Card('3', 'Clubs')])
        hand2 = Hand(
            [Card('9', 'Hearts'), Card('9', 'Diamonds'), Card('9', 'Clubs'), Card('K', 'Hearts'), Card('K', 'Diamonds'),
             Card('2', 'Clubs'), Card('3', 'Clubs')])

        self.assertEqual(hand1 > hand2, True)

    def test_compare_same_high_card(self):
        # Test case where both hands have the same High Card
        hand1 = Hand(
            [Card('2', 'Hearts'), Card('3', 'Diamonds'), Card('4', 'Spades'), Card('5', 'Clubs'), Card('A', 'Hearts'),
             Card('6', 'Clubs'), Card('7', 'Clubs')])
        hand2 = Hand(
            [Card('2', 'Hearts'), Card('3', 'Diamonds'), Card('4', 'Spades'), Card('5', 'Clubs'), Card('A', 'Diamonds'),
             Card('6', 'Clubs'), Card('7', 'Clubs')])

        self.assertEqual(hand1 == hand2, True)  # Assuming the function returns 0 for hands of equal strength

    def test_compare_flush_straight(self):
        # Test case where hand1 is a Flush and hand2 is a Straight
        hand1 = Hand(
            [Card('2', 'Hearts'), Card('4', 'Hearts'), Card('6', 'Hearts'), Card('8', 'Hearts'),
             Card('10', 'Hearts'),
             Card('3', 'Clubs'), Card('5', 'Clubs')])

        hand2 = Hand(
            [Card('5', 'Hearts'), Card('6', 'Diamonds'), Card('7', 'Spades'), Card('8', 'Clubs'),
             Card('9', 'Hearts'),
             Card('3', 'Clubs'), Card('2', 'Clubs')])

        self.assertEqual(hand1 > hand2, True)

    def test_compare_three_of_a_kind_two_pairs(self):
        # Test case where hand1 is a Three of a Kind and hand2 is Two Pairs
        hand1 = Hand(
            [Card('5', 'Hearts'), Card('5', 'Diamonds'), Card('5', 'Spades'), Card('A', 'Hearts'),
             Card('K', 'Hearts'),
             Card('2', 'Clubs'), Card('3', 'Clubs')])
        hand2 = Hand(
            [Card('9', 'Hearts'), Card('9', 'Diamonds'), Card('K', 'Hearts'), Card('K', 'Diamonds'),
             Card('A', 'Hearts'),
             Card('2', 'Clubs'), Card('3', 'Clubs')])

        self.assertEqual(hand1 > hand2, 1)

    def test_compare_two_pairs_one_pair(self):
        # Test case where hand1 has Two Pairs and hand2 has One Pair
        hand1 = Hand(
            [Card('A', 'Hearts'), Card('A', 'Diamonds'), Card('K', 'Spades'), Card('K', 'Hearts'),
             Card('2', 'Hearts'),
             Card('3', 'Clubs'), Card('4', 'Clubs')])
        hand2 = Hand(
            [Card('Q', 'Hearts'), Card('Q', 'Diamonds'), Card('3', 'Spades'), Card('5', 'Hearts'),
             Card('7', 'Hearts'),
             Card('8', 'Clubs'), Card('9', 'Clubs')])

        self.assertEqual(hand1 > hand2, 1)

    def test_compare_one_pair_high_card(self):
        # Test case where hand1 has One Pair and hand2 is a High Card
        hand1 = Hand(
            [Card('A', 'Hearts'), Card('A', 'Diamonds'), Card('2', 'Spades'), Card('3', 'Hearts'),
             Card('4', 'Hearts'),
             Card('5', 'Clubs'), Card('6', 'Clubs')])
        hand2 = Hand(
            [Card('2', 'Hearts'), Card('3', 'Diamonds'), Card('4', 'Spades'), Card('5', 'Hearts'),
             Card('K', 'Hearts'),
             Card('Q', 'Clubs'), Card('J', 'Clubs')])

        self.assertEqual(hand1 > hand2, 1)

    def test_compare_same_two_pairs(self):
        # Test case where both hands have the same Two Pairs
        hand1 = Hand(
            [Card('A', 'Hearts'), Card('A', 'Diamonds'), Card('K', 'Spades'), Card('K', 'Hearts'),
             Card('2', 'Hearts'),
             Card('3', 'Clubs'), Card('4', 'Clubs')])
        hand2 = Hand(
            [Card('A', 'Clubs'), Card('A', 'Spades'), Card('K', 'Diamonds'), Card('K', 'Clubs'),
             Card('2', 'Diamonds'),
             Card('3', 'Hearts'), Card('4', 'Hearts')])

        self.assertEqual(hand1 == hand2, True)  # Expecting 0 if the hands are equal
    def test_compare_high_card_not_in_best_hand(self):
        hand1 = Hand(
            [Card('A', 'Hearts'), Card('2', 'Diamonds'), Card('3', 'Spades'), Card('4', 'Hearts'), Card('5', 'Hearts'),
             Card('6', 'Clubs'), Card('7', 'Clubs')])
        hand2 = Hand(
            [Card('K', 'Hearts'), Card('Q', 'Diamonds'), Card('J', 'Spades'), Card('10', 'Hearts'), Card('9', 'Hearts'),
             Card('8', 'Clubs'), Card('7', 'Clubs')])

        self.assertEqual(hand1 < hand2, True)

    def test_compare_pair_not_in_best_hand(self):
        hand1 = Hand(
            [Card('A', 'Hearts'), Card('A', 'Diamonds'), Card('2', 'Spades'), Card('3', 'Hearts'), Card('4', 'Hearts'),
             Card('5', 'Clubs'), Card('6', 'Clubs')])
        hand2 = Hand(
            [Card('K', 'Hearts'), Card('K', 'Diamonds'), Card('Q', 'Spades'), Card('J', 'Hearts'), Card('10', 'Hearts'),
             Card('9', 'Clubs'), Card('8', 'Clubs')])
        self.assertEqual(hand1 < hand2, True)

    def test_compare_identical_rankings_different_kickers(self):
        hand1 = Hand(
            [Card('A', 'Hearts'), Card('A', 'Diamonds'), Card('K', 'Spades'), Card('K', 'Hearts'), Card('Q', 'Hearts'),
             Card('J', 'Clubs'), Card('2', 'Clubs')])
        hand2 = Hand(
            [Card('A', 'Clubs'), Card('A', 'Spades'), Card('K', 'Diamonds'), Card('K', 'Clubs'), Card('Q', 'Hearts'),
             Card('10', 'Diamonds'), Card('2', 'Hearts')])

        self.assertEqual(hand1 == hand2, True)

    def test_compare_same_three_of_a_kind_different_pairs(self):
        hand1 = Hand(
            [Card('A', 'Hearts'), Card('A', 'Diamonds'), Card('A', 'Spades'), Card('K', 'Hearts'), Card('K', 'Diamonds'),
             Card('2', 'Clubs'), Card('3', 'Clubs')])
        hand2 = Hand(
            [Card('A', 'Clubs'), Card('A', 'Spades'), Card('A', 'Hearts'), Card('Q', 'Diamonds'), Card('Q', 'Hearts'),
             Card('2', 'Spades'), Card('3', 'Hearts')])

        self.assertEqual(hand1 > hand2, 1)

    def test_compare_straights_with_wheel(self):
        hand1 = Hand(
            [Card('A', 'Hearts'), Card('2', 'Diamonds'), Card('3', 'Spades'), Card('4', 'Hearts'), Card('5', 'Hearts'),
             Card('6', 'Clubs'), Card('7', 'Clubs')])
        hand2 = Hand(
            [Card('2', 'Hearts'), Card('3', 'Diamonds'), Card('4', 'Spades'), Card('5', 'Hearts'), Card('6', 'Hearts'),
             Card('K', 'Clubs'), Card('Q', 'Clubs')])

        self.assertEqual(hand1 > hand2, True)

if __name__ == '__main__':
    unittest.main()

