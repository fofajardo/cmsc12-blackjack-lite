import random

# The total a hand must have to hit blackjack.
TOTAL_BLACKJACK = 21
POINTS_BLACKJACK = TOTAL_BLACKJACK
POINTS_STAND = 10

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
def get_hand_total(hand):
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

# Performs checks on whether a new deck should be generated and if
# a blackjack is hit through an ace and 10-value card combination.
def start_new_round(state):
    if not state["new_round"]:
        return

    # There are fewer than 10 cards left in the deck.
    # Generate a new deck.
    if len(state["deck"]) < 10:
        state["deck"] = generate_deck()

    # Reset player hand and draw two additional cards.
    state["player"].clear()
    card_ace = None
    card_ten = None

    for i in range(2):
        card = random.choice(state["deck"])
        state["player"].append(card)
        state["deck"].remove(card)
        # Check if our first two cards match a combination for
        # hitting a blackjack early.
        if card.type == CARD_ACE:
            card_ace = card
        if card.value == 10:
            card_ten = card

    # Set the ace card's value to 11 if we've matched the combination.
    if card_ace and card_ten:
        card_ace.value = 11

    # Reset dealer hand and draw two additional cards.
    state["dealer"].clear()
    for i in range(2):
        card = random.choice(state["deck"])
        state["dealer"].append(card)
        state["deck"].remove(card)

    # We're done and prevent these checks from occurring in the
    # next iteration unless we're in a new round again.
    state["new_round"] = False

def process_choices(state):
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
                print_cards(state["dealer"], "Dealer's")
                # Determine whether the player should win or lose points.
                result = ""
                if state["player_total"] > state["dealer_total"]:
                    result = "win"
                    state["score"] += POINTS_STAND
                else:
                    result = "lose"
                    state["score"] -= POINTS_STAND
                print(f"You {result} {POINTS_STAND} points!")
                state["new_round"] = True
                break

            # Hit: draw a random card from the deck.
            elif choice == 2:
                card = random.choice(state["deck"])
                state["player"].append(card)
                state["deck"].remove(card)
                break
        # The player chose an option outside 1-2.
        print("Invalid option.")

# The main game function.
def run():
    state = {
        "deck": [],
        # Hands: cards held by the player and dealer.
        "player": [],
        "dealer": [],
        # The player's score.
        "score": 0,
        # Determines if we're in a new round.
        "new_round": True,
    }

    while True:
        # Start a new round (if applicable).
        start_new_round(state)

        # Print the player's cards.
        print_cards(state["player"], "Your")

        # Get the value of the player and dealer hands.
        state["player_total"] = get_hand_total(state["player"])
        state["dealer_total"] = get_hand_total(state["dealer"])

        # Bust. A total greater than 21 in the player's hand
        # results in a game over.
        if state["player_total"] > TOTAL_BLACKJACK:
            print(f"You exceeded {TOTAL_BLACKJACK}. Game over!")
            break

        # Blackjack. A total of 21 in the player's hand results
        # in winning the current round.
        if state["player_total"] == TOTAL_BLACKJACK:
            print(f"You hit blackjack! ({POINTS_BLACKJACK} points)")
            state["score"] += POINTS_BLACKJACK
            state["new_round"] = True
            continue

        # Process player choices.
        process_choices(state)

        print("\n")

    # Print the player's score (Reached only during game over).
    print(f"Your score: {state['score']}")

# Run the game by calling the main game function.
run()
