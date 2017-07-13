from unittest import TestCase, main
from card import Card

class TestCard(TestCase):
    def setUp(self):
        self.card1 = Card('A', 'C')
        self.card2 = Card('4', 'D')
        self.card3 = Card('10', 'S')
        self.card4 = Card('Q', 'H')

    def test_init(self):
        self.assertEqual(self.card1.rank, 'A')
        self.assertEqual(self.card1.suit, 'C')
        self.assertEqual(self.card1.value, 1)
        self.assertEqual(self.card2.value, 4)
        self.assertEqual(self.card3.value, 10)
        self.assertEqual(self.card4.value, 10)

    def test_validate_card_input(self):
        self.assertIsNone(Card.validate_card_input('A', 'S'))
        self.assertIsNone(Card.validate_card_input('5', 'D'))
        self.assertIsNone(Card.validate_card_input('10', 'C'))
        self.assertIsNone(Card.validate_card_input('K', 'H'))

        self.assertRaises(ValueError, Card.validate_card_input, 3, 'S')
        self.assertRaises(ValueError, Card.validate_card_input, '11', 'S')
        self.assertRaises(ValueError, Card.validate_card_input, '3', '2')
        self.assertRaises(ValueError, Card.validate_card_input, '3', 'T')
        self.assertRaises(ValueError, Card.validate_card_input, '3', 'Spades')
        self.assertRaises(ValueError, Card.validate_card_input, 3, 'Spades')

    def test_eq(self):
        self.assertTrue(self.card2.__eq__(Card('4', 'D')))
        self.assertFalse(self.card2.__eq__(Card('4', 'C')))
        self.assertFalse(self.card2.__eq__(Card('5', 'D')))
        self.assertFalse(self.card2.__eq__(Card('3', 'H')))

    def test_next_rank(self):
        self.assertEqual(Card('A', 'C').next_rank(), '2')
        self.assertEqual(Card('2', 'H').next_rank(), '3')
        self.assertEqual(Card('9', 'D').next_rank(), '10')
        self.assertEqual(Card('10', 'C').next_rank(), 'J')
        self.assertEqual(Card('J', 'C').next_rank(), 'Q')
        self.assertEqual(Card('Q', 'C').next_rank(), 'K')
        self.assertIsNone(Card('K', 'C').next_rank())


if __name__ == '__main__':
    main()
