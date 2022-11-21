import random
import scores
import utils

# The total a hand must have to hit blackjack.
TOTAL_BLACKJACK = 21
POINTS_BLACKJACK = TOTAL_BLACKJACK
POINTS_STAND = 10

# Define the cards that will be generated in the deck.
SUITS = ["c", "d", "h", "s"]
CARDS_COURT = ["J", "Q", "K"]
CARD_ACE = "A"

is_running = True

# Card: stores the suit and type (court) or value (pip).
# XXX: If we're not allowed to use OOP classes, this should probably
# be converted to a function that is equivalent to what init does
# but instead stores the data into either a list or dictionary.
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

# 0 = text only
# 1 = ascii large
# 2 = ascii small
CARD_DISPLAY = 2

# 0 = letters
# 1 = symbols and colors
SUIT_DISPLAY = 1

# Prints all cards to console.
def print_cards(hand, target):
    utils.ansiprint(f"{target} cards are:", "BE", utils.STYLE_TERMINATE)

    # 0: Plain text-only cards.
    if CARD_DISPLAY == 0:
        for card in hand:
            print(f"{card.type}{card.suit}", end=" ")
    # 1/2: ASCII art-based cards.
    elif CARD_DISPLAY == 1 or CARD_DISPLAY == 2:
        # Get our target card graphic.
        lines = []
        # Large vs. small card display.
        if CARD_DISPLAY == 2:
            lines = utils.strings["card"]
        else:
            lines = utils.strings["card_sm"]
        lines_count = len(lines)
        # Initialize the list which will hold the merged cards.
        lines_merged = [""] * lines_count
        # Process all cards in hand.
        for card in hand:
            suit_ascii = card.suit
            color = ""
            if SUIT_DISPLAY == 1:
                if card.suit == "c":
                    suit_ascii = "♣"
                    color = ["WHTB", "BBLK"]
                elif card.suit == "d":
                    suit_ascii = "♦"
                    color = ["WHTB", "BRED"]
                elif card.suit == "h":
                    suit_ascii = "♥"
                    color = ["WHTB", "BRED"]
                elif card.suit == "s":
                    suit_ascii = "♠"
                    color = ["WHTB", "BBLK"]

            suit_line = ((lines_count - 1) / 2)
            for i in range(lines_count):
                lines_merged[i] += utils.ansicode(color) + " "
                # Substitute the suit and card value/type.
                line = lines[i]
                if i == suit_line:
                    lines_merged[i] += line.format(suit_ascii)
                else:
                    type_padded = card.type
                    # Add space before type if it's only a single character.
                    if len(card.type) == 1:
                        type_padded = " " + card.type
                    lines_merged[i] += line.format(type_padded)

                lines_merged[i] += " " + utils.ansicode(utils.STYLE_TERMINATE) + " "
        # Print all merged cards.
        for i in lines_merged:
            print(i)
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

# Stand: don't draw an additional card and compare the
# player total with the dealer total.
def _do_stand(state):
    utils.ansi("@")
    # Print the player's and dealer's cards.
    print_cards(state["player"], "Your")
    print_cards(state["dealer"], "Dealer's")
    # Determine whether the player should win or lose points.
    result = ""
    style = "BGRN"
    if state["player_total"] > state["dealer_total"]:
        result = "win"
        state["score"] += POINTS_STAND
    else:
        result = "lose"
        state["score"] -= POINTS_STAND
        style = "BRED"
    utils.ansiprint(f"You {result} {POINTS_STAND} points!".center(80), style, utils.STYLE_TERMINATE)
    utils.prompt_enter()
    state["new_round"] = True

# Hit: draw a random card from the deck.
def _do_hit(state):
    card = random.choice(state["deck"])
    state["player"].append(card)
    state["deck"].remove(card)

# Surrender: stop playing and settle with your current score.
def _do_surrender(state):
    global is_running
    is_running = False

def _do_cheatwin(state):
    state["score"] += POINTS_STAND
    utils.set_message(f"+{POINTS_STAND}", False)
    state["new_round"] = True

def _do_cheatlose(state):
    state["score"] -= POINTS_STAND
    utils.set_message(f"-{POINTS_STAND}")
    state["new_round"] = True

MENU_ITEMS = {
    "1": {
        "label": "Stand",
        "action": _do_stand
    },
    "2": {
        "label": "Hit",
        "action": _do_hit
    },
    "3": {
        "label": "Surrender",
        "action": _do_surrender
    },
    "klapaucius": {
        "label": "Instant win",
        "action": _do_cheatwin,
        "hidden": True
    },
    "wannacry": {
        "label": "Instant lose",
        "action": _do_cheatlose,
        "hidden": True
    }
}

# The main game function.
def run():
    global is_running
    is_running = True

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

    while is_running:
        utils.ansi("@")
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
            state["game_over"] = f"You exceeded {TOTAL_BLACKJACK}. Game over!"
            break

        # Blackjack. A total of 21 in the player's hand results
        # in winning the current round.
        if state["player_total"] == TOTAL_BLACKJACK:
            utils.ansiprint(
                f"\nYou hit blackjack! ({POINTS_BLACKJACK} points)",
                "BGRN", utils.STYLE_TERMINATE)
            state["score"] += POINTS_BLACKJACK
            utils.prompt_enter()
            state["new_round"] = True
            continue

        # Process player choices.
        utils.process_menu(MENU_ITEMS, state)

    scores.run_save(state)
