from unittest import TestCase, main
from hand import Hand
from card import Card

class TestHand(TestCase):
    def create_hand(self, card_strings, flip_card):
        cards = map(lambda c: Card(c[:-1], c[-1]), card_strings)
        return Hand(cards, Card(flip_card[:-1], flip_card[-1]))

    def test_validate_hand_input(self):
        card0 = Card('A', 'S')
        card1 = Card('3', 'D')
        card2 = Card('5', 'D')
        card3 = Card('K', 'H')
        card5 = Card('5', 'H')
        self.assertIsNone(Hand.validate_hand_input([card0, card1, card1, card3], card5))

        self.assertRaises(ValueError, Hand.validate_hand_input, [card0, card1, card2], card5)
        self.assertRaises(ValueError, Hand.validate_hand_input, [card0, card1, card2, card3, card5], card5)
        self.assertRaises(TypeError, Hand.validate_hand_input, [card0, card1, card2, card3], '5C')

    def test_sort_all_cards_in_order(self):
        """ Cards in hand are already in order (lowest to highest) """
        card0 = Card('A', 'D')
        card1 = Card('2', 'C')
        card2 = Card('5', 'H')
        card3 = Card('J', 'S')
        flip_card = Card('Q', 'H')
        hand = Hand([card0, card1, card2, card3], flip_card)
        self.assertEqual(hand.sort_all_cards(), [card0, card1, card2, card3, flip_card])

    def test_sort_all_cards_in_reversed_order(self):
        """ Cards in hand are sorted in opposite order (highest to lowest) """
        card0 = Card('Q', 'D')
        card1 = Card('J', 'C')
        card2 = Card('5', 'H')
        card3 = Card('2', 'S')
        flip_card = Card('A', 'H')
        hand = Hand([card0, card1, card2, card3], flip_card)
        self.assertEqual(hand.sort_all_cards(), [flip_card, card3, card2, card1, card0])

    def test_sort_all_cards_random_order(self):
        """ Cards in in a random, non-sorted order """
        card0 = Card('10', 'C')
        card1 = Card('7', 'H')
        card2 = Card('A', 'D')
        card3 = Card('Q', 'D')
        flip_card = Card('2', 'C')
        hand = Hand([card0, card1, card2, card3], flip_card)
        self.assertEqual(hand.sort_all_cards(), [card2, flip_card, card1, card0, card3])

    def test_sort_all_cards_one_duplicate(self):
        """ 1 pair of cards with the same rank """
        card0 = Card('8', 'S')
        card1 = Card('2', 'S')
        card2 = Card('Q', 'C')
        card3 = Card('9', 'S')
        flip_card = Card('8', 'H')
        hand = Hand([card0, card1, card2, card3], flip_card)
        self.assertEqual(hand.sort_all_cards(), [card1, card0, flip_card, card3, card2])

    def test_sorted_two_duplicates(self):
        """ 2 pairs of cards with the same rank """
        card0 = Card('8', 'S')
        card1 = Card('2', 'S')
        card2 = Card('2', 'C')
        card3 = Card('9', 'S')
        flip_card = Card('8', 'H')
        hand = Hand([card0, card1, card2, card3], flip_card)
        self.assertEqual(hand.sort_all_cards(), [card1, card2, card0, flip_card, card3])

    def test_sorted_multiple_duplicates(self):
        """ Four cards with the same rank """
        card0 = Card('4', 'C')
        card1 = Card('4', 'D')
        card2 = Card('K', 'C')
        card3 = Card('4', 'S')
        flip_card = Card('4', 'H')
        hand = Hand([card0, card1, card2, card3], flip_card)
        self.assertEqual(hand.sort_all_cards(), [card0, card1, card3, flip_card, card2])

    def test_calculate_pairs_no_pairs(self):
        """ There are no paris in the hand """
        hand = self.create_hand(['AC', 'JD', '2C', '6S'], 'KH')
        self.assertEqual(hand.calculate_pairs(), 0)

    def test_calculate_pairs_one_pair(self):
        """ One pair exists in the hand """
        hand = self.create_hand(['AC', 'JD', '2C', 'AS'], 'KH')
        self.assertEqual(hand.calculate_pairs(), 2)

    def test_calculate_pairs_one_pair_with_flip_card(self):
        """ The hand has one pair made up of a normal card and the flip card """
        hand = self.create_hand(['AC', 'JD', '2C', '6S'], 'JH')
        self.assertEqual(hand.calculate_pairs(), 2)

    def test_calculate_pairs_one_set_three_cards(self):
        """ The hand has three cards with the same rank """
        hand = self.create_hand(['AC', 'JD', '2C', '2S'], '2H')
        self.assertEqual(hand.calculate_pairs(), 6)

    def test_calculate_pair_one_set_four_cards(self):
        """ The hand has four cards with the same rank """
        hand = self.create_hand(['AC', '6D', '6C', '6S'], '6H')
        self.assertEqual(hand.calculate_pairs(), 12)

    def test_calculate_pairs_two_pairs(self):
        """ Two separate (non-overlapping) pairs exist in the hand """
        hand = self.create_hand(['AC', 'AD', '2C', '6S'], '6H')
        self.assertEqual(hand.calculate_pairs(), 4)

    def test_calculate_pairs_one_pair_one_set_three(self):
        """ The hand has one pair and one set of three cards with the same rank """
        hand = self.create_hand(['KC', 'JD', 'JC', 'JS'], 'KH')
        self.assertEqual(hand.calculate_pairs(), 8)

    def test_calculate_runs_no_run(self):
        """ The hand doesn't have any runs """
        hand = self.create_hand(['AC', '7D', '6C', 'KS'], '9H')
        self.assertEqual(hand.calculate_runs(), 0)

    def test_calculate_runs_three_cards_numerical(self):
        """ The hand contains one run of three cards """
        hand = self.create_hand(['3C', 'JD', '2C', '4S'], 'KH')
        self.assertEqual(hand.calculate_runs(), 3)

    def test_calculate_runs_three_cards_face_cards(self):
        """ The hand contains one run of three cards including face cards """
        hand = self.create_hand(['10C', '9D', '2C', 'JS'], 'KH')
        self.assertEqual(hand.calculate_runs(), 3)

    def test_calculate_runs_no_wraparound(self):
        """ The hand contains 0 runs because K - A does not wrap around """
        hand = self.create_hand(['QC', 'KC', 'AC', '2C'], '4C')
        self.assertEqual(hand.calculate_runs(), 0)

    def test_calculate_runs_three_cards_flip_card(self):
        """ The hand contains one run of three cards that also uses the flip card """
        hand = self.create_hand(['QC', 'JD', '2C', '6S'], 'KH')
        self.assertEqual(hand.calculate_runs(), 3)

    def test_calculate_runs_four_cards(self):
        """ The hand contains one run of four cards """
        hand = self.create_hand(['AC', '3D', '2C', '6S'], '4H')
        self.assertEqual(hand.calculate_runs(), 4)

    def test_calculate_runs_five_cards(self):
        """ The hand contains one run of five cards """
        hand = self.create_hand(['8C', 'JD', '9C', '10S'], 'QH')
        self.assertEqual(hand.calculate_runs(), 5)

    def test_calculate_runs_three_double_run_end(self):
        """
        The hand contains a double run of three, with the double card occurring
        at the end of the run
        """
        hand = self.create_hand(['AC', '5D', '4C', '6S'], '6H')
        self.assertEqual(hand.calculate_runs(), 6)

    def test_calculate_runs_three_double_run_middle(self):
        """
        The hand contains a double run of three, with the double card occurring
        at the middle of the run
        """
        hand = self.create_hand(['AC', '5D', '4C', '5S'], '6H')
        self.assertEqual(hand.calculate_runs(), 6)

    def test_calculate_runs_four_double_run(self):
        """ The hand contains a double run of four """
        hand = self.create_hand(['JC', 'QD', '9C', 'JS'], '10H')
        self.assertEqual(hand.calculate_runs(), 8)

    def test_calculate_runs_triple_run(self):
        """ The hand contains a triple run """
        hand = self.create_hand(['4C', '3D', '2C', '3S'], '2H')
        self.assertEqual(hand.calculate_runs(), 12)

    def test_calculate_15s_no_15(self):
        """ No cards add up to 15 """
        hand = self.create_hand(['AC', 'JD', '2C', '6S'], 'KH')
        self.assertEqual(hand.calculate_15s(), 0)

    def test_calculate_15s_one_15(self):
        """ Some cards add up to one 15 """
        hand = self.create_hand(['QC', 'JD', '7C', 'KS'], '8H')
        self.assertEqual(hand.calculate_15s(), 2)

    def test_calculate_15_all_cards_one_15(self):
        """ All the cards add up to one 15 """
        hand = self.create_hand(['AC', '4D', '2C', '6S'], '2H')
        self.assertEqual(hand.calculate_15s(), 2)

    def test_calculate_15s_two_15s(self):
        """ Two sets of 15 in the hand """
        hand = self.create_hand(['JC', 'KD', '2C', '5S'], '6H')
        self.assertEqual(hand.calculate_15s(), 4)

    def test_calculate_15s_many_15s(self):
        """ Many 15s formed in the hand """
        hand = self.create_hand(['5C', '4D', '6C', '5S'], '6H')
        self.assertEqual(hand.calculate_15s(), 8)

    def test_calculate_15s_maximum(self):
        """ The maximum number of 15s achieved in a hand """
        hand = self.create_hand(['5C', 'JD', '5D', '5S'], '5H')
        self.assertEqual(hand.calculate_15s(), 16)

    def test_calculate_suit_cards_match(self):
        """ Four cards of same suit in hand """
        hand = self.create_hand(['JC', '3C', '5C', 'KC'], '5D')
        self.assertEqual(hand.calculate_suit(), 4)

    def test_calculate_suit_flip_card_matches(self):
        """ Four cards and flip card all have the same suit """
        hand = self.create_hand(['JC', '3C', '5C', 'KC'], '5C')
        self.assertEqual(hand.calculate_suit(), 5)

    def test_calculate_suit_no_match(self):
        """ Three cards of the same suit and flip card of the same suit """
        hand = self.create_hand(['JD', '3S', '5S', 'KS'], '5S')
        self.assertEqual(hand.calculate_suit(), 0)

    def test_calculate_suit_all_different(self):
        """ All four cards in hand have a different suit """
        hand = self.create_hand(['JD', '3H', '5C', 'KS'], '5H')
        self.assertEqual(hand.calculate_suit(), 0)

    def test_calculate_nobs_single_jack_match(self):
        """ One jack in list of cards that matches suit of flip card) """
        hand = self.create_hand(['JD', '3C', '5H', 'KS'], '5D')
        self.assertEqual(hand.calculate_nobs(), 1)

    def test_calculate_nobs_single_jack_no_match(self):
        """ One jack in list of cards that doesn't match suit of flip card) """
        hand = self.create_hand(['JD', '3C', '5H', 'KS'], '5H')
        self.assertEqual(hand.calculate_nobs(), 0)

    def test_calculate_nobs_no_jack(self):
        """ No jacks in hand """
        hand = self.create_hand(['AD', '3C', '5H', 'KS'], '5D')
        self.assertEqual(hand.calculate_nobs(), 0)

    def test_calculate_nobs_two_jacks_no_point(self):
        """ Two jacks that don't match the flip card """
        hand = self.create_hand(['AD', 'JD', '5H', 'JC'], '5H')
        self.assertEqual(hand.calculate_nobs(), 0)

    def test_calculate_nobs_two_jacks_one_point(self):
        """ Two jacks, with one matching the flip card """
        hand = self.create_hand(['AD', 'JD', '5H', 'JC'], '5D')
        self.assertEqual(hand.calculate_nobs(), 1)

    def test_calculate_nobs_jack_flip_card(self):
        """ Jack is in the flip card """
        hand = self.create_hand(['AD', 'JD', '5H', 'JC'], 'JH')
        self.assertEqual(hand.calculate_nobs(), 0)

    def test_calculate_score(self):
        hand = self.create_hand(['4C', '4D', '5C', '6C'], '6H')
        self.assertEqual(hand.calculate_pairs(), 4)
        self.assertEqual(hand.calculate_runs(), 12)
        self.assertEqual(hand.calculate_suit(), 0)
        self.assertEqual(hand.calculate_nobs(), 0)
        self.assertEqual(hand.calculate_15s(), 8)
        self.assertEqual(hand.calculate_score(), 24)

    def test_calculate_score_one_of_everything(self):
        hand = self.create_hand(['2C', '3C', 'JC', '4C'], '3C')
        self.assertEqual(hand.calculate_pairs(), 2)
        self.assertEqual(hand.calculate_runs(), 6)
        self.assertEqual(hand.calculate_suit(), 5)
        self.assertEqual(hand.calculate_nobs(), 1)
        self.assertEqual(hand.calculate_15s(), 4)
        self.assertEqual(hand.calculate_score(), 18)


if __name__ == '__main__':
    main()
