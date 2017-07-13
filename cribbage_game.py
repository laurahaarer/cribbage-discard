from itertools import combinations
from card import Card
from hand import Hand
from discard import Discard

def input_original_cards():
    """ Ask the user to input their hand """
    print("Enter 6 cards of format <rank><suit>, separated by commas")
    print(" <rank> is one of: A, 2...10, J, Q, K")
    print(" <suit> is one of: S, H, D, C")
    print("Example: 8C, AH, 10H, KC, 5D, 2S")
    card_inputs = raw_input("\nYour cards: ").upper()
    card_inputs = [c.strip() for c in card_inputs.split(',')]

    if len(card_inputs) != 6:
        raise ValueError("Must provide 6 cards")

    cards = []
    for card_string in card_inputs:
        try:
            card = Card(card_string[:-1], card_string[-1]) # will have two characters in rank when rank is 10
        except:
        ``  raise ValueError("Invalid card input")
        cards.append(card)

    return cards

def remaining_cards_in_deck(original_cards):
    ''' Determine the remaining cards in the deck besides the cards in the original hand '''
    possible_ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    possible_suits = ['S', 'C', 'D', 'H']

    all_cards = []
    for rank in possible_ranks:
        for suit in possible_suits:
            all_cards.append(Card(rank, suit))

    return [card for card in all_cards if card not in original_cards]

def calculate_scores(original_cards):
    remaining_cards = remaining_cards_in_deck(original_cards)

    discard_stats = []
    for discard_combo in combinations(original_cards, 2):
        discard = Discard(discard_combo[0], discard_combo[1])
        for flip_card in remaining_cards:
            selected_cards = [card for card in original_cards if card != discard_combo[0] and card != discard_combo[1]]
            hand = Hand(selected_cards, flip_card)
            score = hand.calculate_score()
            discard.add(flip_card, score)
        discard_stats.append(discard)

    return discard_stats

def possible_cards_in_hand(original_cards):
    assert len(original_cards) == 6
    return combinations(original_cards, 4)


original_cards = input_original_cards()
discard_stats = calculate_scores(original_cards)

# The discard with the highest average
highest_mean_discard = max(discard_stats, key=lambda s: s.mean())
print("\nDiscards with the highest average: {}".format(highest_mean_discard))
print(" (average score: {})".format(round(highest_mean_discard.mean(), 2)))

# The discard with the highest possible score
highest_max_score_discard = max(discard_stats, key=lambda s: s.max())
print("\nDiscards with the highest max score: {}".format(highest_max_score_discard))
print(" (max score: {})".format(round(highest_max_score_discard.max(), 2)))
