import random

# Define the cards that will be generated in the deck.
SUITS = ["c", "d", "h", "s"]
CARDS_COURT = ["J", "Q", "K"]
CARD_ACE = "A"

# Card: stores the suit and type (court) or value (pip).
class Card:
    # Initialize a new card.
    def __init__(self, suit, type):
        self.suit = suit
        self.type = str(type)
        # Card with one (1) pip: ace
        if type == 1:
            self.type = CARD_ACE
        # Court cards: their value is 10 by default.
        elif type in CARDS_COURT:
            self.type = type
            self.value = 10
            return
        # If we're a pip card with a value other than 1, just
        # set the value.
        self.value = type
    # Get a string representation of the card.
    def to_text(self):
        return self.type + self.suit

# Generates a deck of cards, including all pips and court cards.
def generate_deck():
    deck = []
    for suit in SUITS:
        for pip in range(1, 11):
            deck.append(Card(suit, pip))
        for court in CARDS_COURT:
            deck.append(Card(suit, court))
    return deck

# Retrieves the value of all the cards in a hand.
def get_hand_value(hand):
    value = 0
    for i in hand:
        value += i.value
    return value

# Prints all cards to console.
def print_cards(hand, target):
    print(f"{target} cards are:")
    for card in hand:
        print(card.to_text(), end=" ")
    print()

# The main game function.
def run():
    deck = generate_deck()
    # Hands: cards held by the player and dealer.
    player = []
    dealer = []
    # Player score
    score = 0
    # Determines if we're in a new round, which triggers checks on whether
    # a new deck should be generated and if a blackjack is hit through
    # an ace and 10-value card combination.
    new_round = True

    while True:
        has_ace = False
        has_ten = False

        # We're in a new round.
        if new_round:
            # There are fewer than 10 cards left in the deck.
            # Generate a new deck.
            if len(deck) < 10:
                deck = generate_deck()

            # Reset player hand and draw two additional cards.
            player.clear()
            for i in range(2):
                card = random.choice(deck)
                player.append(card)
                deck.remove(card)

                # Check if our first two cards match a combination for
                # hitting a blackjack early.
                if card.type == CARD_ACE:
                    has_ace = True
                if card.value == 10:
                    has_ten = True

            # Reset dealer hand and draw two additional cards.
            dealer.clear()
            for i in range(2):
                card = random.choice(deck)
                dealer.append(card)
                deck.remove(card)

            # We're done and prevent these checks from occurring in the
            # next iteration unless we're in a new round again.
            new_round = False

        # Print the player's cards.
        print_cards(player, "Your")
        # Get the value of the player and dealer hands.
        player_value = get_hand_value(player)
        dealer_value = get_hand_value(dealer)

        # Bust. Getting a total of 21 in the player's hand
        # results in a game over.
        # TODO: 21 should probably be a constant.
        if player_value > 21:
            print("You exceeded 21. Game over!")
            break

        # Check if we've hit blackjack by looking at whether the player
        # has an ace and a 10-value card combination OR if the value of
        # all the player's cards is 21.
        # XXX: we should probably change the value of ace instead
        #      based on the spec; it's also probably cleaner that way.
        if (has_ace and has_ten) or player_value == 21:
            print("You hit blackjack! (21 points)")
            score += 21
            # Mark next round.
            new_round = True
            continue

        # Process player choices.
        while True:
            print("[1] Stand")
            print("[2] Hit")
            choice = input("Enter choice: ")
            if choice.isdigit():
                choice = int(choice)
                # Stand: don't draw an additional card and compare the
                # player total with the dealer total.
                if choice == 1:
                    # Print the dealer's cards.
                    print_cards(dealer, "Dealer's")
                    # Determine whether the player should win or lose points.
                    result = ""
                    if player_value > dealer_value:
                        result = "win 10"
                        score += 10
                    else:
                        result = "lose 10"
                        score -= 10
                    print(f"You {result} points!")
                    # Mark next round.
                    new_round = True
                    break
                # Hit: draw a random card from the deck.
                elif choice == 2:
                    card = random.choice(deck)
                    player.append(card)
                    deck.remove(card)
                    break
            # The player chose an option outside 1-2.
            print("Invalid option.")

        print("\n")

    # Print the player's score. (Reached only during game over.) 
    print(f"Your score: {score}")

# Run the game by calling the main game function.
run()
