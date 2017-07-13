import statistics

# This essentally maps two discards to a possible score for each discard, and
# calculates stats based on those scores.
# Pulled it into a separate object rather than a complicated dictionary as I may do more with this later.
class Discard:
    def __init__(self, card1, card2):
        self.cards = [card1, card2]
        # Keeping track of the actual flip card associated with each score for future use
        self.possible_scores = {} # hash of potential flip cards to their score

    def __str__(self):
        return "{}, {}".format(str(self.cards[0]), str(self.cards[1]))

    def add(self, flip_card, score):
        if flip_card in self.possible_scores:
            raise RuntimeError("Cannot overwrite a previously calculated score for a given flip_card")
        self.possible_scores[flip_card] = score

    def scores(self):
      return list(self.possible_scores.values())

    def mean(self):
        return statistics.mean(self.scores())

    def median(self):
        return statistics.median(self.scores())

    def mode(self):
        return statistics.mode(self.scores())

    def min(self):
        return min(self.scores())

    def max(self):
        return max(self.scores())
