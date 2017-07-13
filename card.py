from collections import OrderedDict

class Card:
    RANK_MAPPINGS = OrderedDict([
        ('A', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7),
        ('8', 8), ('9', 9), ('10', 10), ('J', 10), ('Q', 10), ('K', 10)
    ])
    VALID_SUITS = ['S', 'C', 'D', 'H']

    def __init__(self, rank, suit):
        """
        value: String
            Describes the card number/value. One of A, 1, ... , 9, J, Q, K
        suit: String
            Describes the card suit. One of S, C, D, H
        """
        Card.validate_card_input(rank, suit)
        self.rank = rank
        self.suit = suit
        self.value = Card.RANK_MAPPINGS[self.rank]
        self.numerical_order = Card.RANK_MAPPINGS.keys().index(self.rank)

    def __hash__(self):
        return hash((self.rank, self.suit))

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __str__(self):
        return self.rank + self.suit

    @staticmethod
    def validate_card_input(rank, suit):
        """
        Check that given value is one of A, 1, ... , 9, J, Q, K.
        Check that suit is one of S, C, D, H
        """
        if rank not in Card.RANK_MAPPINGS:
            raise ValueError("Invalid card value")
        if suit not in Card.VALID_SUITS:
            raise ValueError("Invalid card suit")

    def next_rank(self):
        """
        Returns the rank that comes directly after this card's rank
        """
        if self.rank == 'K':
            return None
        return self.RANK_MAPPINGS.keys()[self.RANK_MAPPINGS.keys().index(self.rank) + 1]
