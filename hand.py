from itertools import combinations
from collections import Counter
from card import Card

class Hand:
    def __init__(self, cards, flip_card):
        Hand.validate_hand_input(cards, flip_card)
        self.cards = cards
        self.flip_card = flip_card
        self.all_sorted_cards = self.sort_all_cards() # sorted cards + flip_card

    @staticmethod
    def validate_hand_input(cards, flip_card):
        if len(cards) != 4:
            raise ValueError("Hand must contain 4 cards")
        if not isinstance(flip_card, Card):
            raise TypeError("The given flip card must be of type Card")

    def sort_all_cards(self):
        """
        Sorts the four main cards and the flip card in order of rank (as defined
        by Card.RANK_MAPPINGS) from lowest rank to highest rank
        """
        all_cards = self.cards + [self.flip_card]
        return sorted(all_cards, key=lambda x: Card.RANK_MAPPINGS.keys().index(x.rank))

    def calculate_score(self):
        """ Sums up all the points to calculate the total score of the hand """
        score = 0
        score += self.calculate_pairs()
        score += self.calculate_runs()
        score += self.calculate_15s()
        score += self.calculate_suit()
        score += self.calculate_nobs()
        return score

    def calculate_pairs(self):
        """ Calculates the total score of all pairs """
        all_combinations = combinations(self.all_sorted_cards, 2)
        score = 0
        for c in all_combinations:
            if c[0].rank == c[1].rank:
                score += 2
        return score

    def calculate_runs(self):
        """ Calculates the total score of all runs/run combinations """
        run = [self.all_sorted_cards[0]]

        index = 1
        while index < len(self.all_sorted_cards):
            current_card = self.all_sorted_cards[index]
            previous_run_card = run[-1]

            if previous_run_card.next_rank() == current_card.rank:
                run.append(current_card)
            elif previous_run_card.rank != current_card.rank:
                if len(run) < 3: # We don't already have a run, so safe to reset & start over
                    run = [current_card]
                else:
                    break
            index += 1

        # Count number of duplicates
        if len(run) >= 3:
            multiplier = 0
            for card in run:
                count = map(lambda x: x.rank, self.all_sorted_cards).count(card.rank)
                if count > 1:
                  multiplier += count

            if multiplier > 0:
              return len(run) * multiplier

            return len(run)
        else:
            return 0

    def calculate_15s(self):
        """ Calculates the total score of all cards adding up to 15 (2 points each) """
        score = 0
        for i in range(2, len(self.all_sorted_cards)+1):
            for subset in combinations(self.all_sorted_cards, i):
                if sum(c.value for c in subset) == 15:
                    score += 2
        return score

    def calculate_suit(self):
        """ Calculates the points allotted to having cards of the same suit """
        if self.cards[0].suit == self.cards[1].suit == self.cards[2].suit == self.cards[3].suit:
            if self.cards[0].suit == self.flip_card.suit:
                return 5
            return 4
        return 0

    def calculate_nobs(self):
        """
        Returns 1 point if the card has the potential to have nobs
        (a Jack that has the same suit as the flip card)
        """
        for card in self.cards:
            if card.rank == 'J' and card.suit == self.flip_card.suit:
                return 1
        return 0
