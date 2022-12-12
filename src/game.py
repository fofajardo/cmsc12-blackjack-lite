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

# Card index constants.
CI_SUIT = 0
CI_TYPE = 1
CI_VALUE = 2

def new_card(suit, type_or_value):
    """Create a new card and return a list.
    The list stores the assigned suit, type, and value."""
    card = [""] * 3
    card[CI_SUIT] = suit               # 0: Suit
    card[CI_TYPE] = str(type_or_value) # 1: Card type (pip/ace/court)
    card[CI_VALUE] = type_or_value     # 2: Card value
    # Card with one (1) pip: ace
    if type_or_value == 1:
        card[CI_TYPE] = CARD_ACE
    # Court cards: their value is 10 by default.
    elif type_or_value in CARDS_COURT:
        card[CI_VALUE] = 10
    # Return a list containing information about the card.
    return card

def generate_deck():
    """Return a list containing a deck of cards.
    This includes all pips and court cards."""
    deck = []
    for suit in SUITS:
        for pip in range(1, 11):
            deck.append(new_card(suit, pip))
        for court in CARDS_COURT:
            deck.append(new_card(suit, court))
    return deck

def get_hand_total(hand):
    """Return an integer representing the value of all the cards in a hand."""
    value = 0
    for i in hand:
        value += i[CI_VALUE]
    return value

# 0 = text only
# 1 = ascii large
# 2 = ascii small
CARD_DISPLAY = 2

# 0 = letters
# 1 = symbols and colors
SUIT_DISPLAY = 1

def print_cards(hand, target):
    """Prints all cards to console."""
    utils.ansiprint(f"{target} cards are:", "BE")

    # 0: Plain text-only cards.
    if CARD_DISPLAY == 0:
        for card in hand:
            print(f"{card[CI_TYPE]}{card[CI_SUIT]}", end=" ")
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
            suit_ascii = card[CI_SUIT]
            color = ""
            if SUIT_DISPLAY == 1:
                if card[CI_SUIT] == "c":
                    suit_ascii = "♣"
                    color = ["WHTB", "BBLK"]
                elif card[CI_SUIT] == "d":
                    suit_ascii = "♦"
                    color = ["WHTB", "BRED"]
                elif card[CI_SUIT] == "h":
                    suit_ascii = "♥"
                    color = ["WHTB", "BRED"]
                elif card[CI_SUIT] == "s":
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
                    type_padded = card[CI_TYPE]
                    # Add space before type if it's only a single character.
                    if len(card[CI_TYPE]) == 1:
                        type_padded = " " + card[CI_TYPE]
                    lines_merged[i] += line.format(type_padded)

                lines_merged[i] += " " + utils.ansicode(utils.STYLE_TERMINATE) + " "
        # Print all merged cards.
        for i in lines_merged:
            print(i)
    print()

def start_new_round(state):
    """Performs checks on whether a new deck should be generated and if
    a blackjack is hit through an ace and 10-value card combination."""
    if not state["new_round"]:
        return

    # There are fewer than 10 cards left in the deck.
    # Generate a new deck.
    if len(state["deck"]) < 10:
        state["deck"] = generate_deck()

    # Reset player hand and draw two additional cards.
    users = ["player", "dealer"]

    for user in users:
        state[user].clear()
        card_ace = None
        card_ten = None

        for i in range(2):
            card = random.choice(state["deck"])
            state[user].append(card)
            state["deck"].remove(card)
            # Check if our first two cards match a combination for
            # hitting a blackjack early.
            if card[CI_TYPE] == CARD_ACE:
                card_ace = card
            if card[CI_VALUE] == 10:
                card_ten = card

        # Set the ace card's value to 11 if we've matched the combination.
        if card_ace and card_ten:
            card_ace[CI_VALUE] = 11

    # We're done and prevent these checks from occurring in the
    # next iteration unless we're in a new round again.
    state["new_round"] = False

def _do_stand(state):
    """Stand: don't draw an additional card and compare the
    player total with the dealer total."""
    # Clear the screen.
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
    utils.ansiprint(f"You {result} {POINTS_STAND} points!".center(80), style)
    utils.prompt_enter()
    state["new_round"] = True

def _do_hit(state):
    """Hit: draw a random card from the deck."""
    card = random.choice(state["deck"])
    state["player"].append(card)
    state["deck"].remove(card)

def _do_surrender(state):
    """Surrender: stop playing and settle with your current score."""
    global is_running
    is_running = False

def _do_viewscore(state):
    """View score: view your current score."""
    utils.ansi("@")
    utils.ansiprint("<YOUR SCORE>".center(80), "BE")
    for i in utils.get_big_number(state["score"]):
        print(i.center(80))
    utils.prompt_enter()

def _do_cheatwin(state):
    """Cheat win: instantly gain 10 points."""
    state["score"] += POINTS_STAND
    utils.set_message(f"+{POINTS_STAND}", False)
    state["new_round"] = True

def _do_cheatlose(state):
    """Cheat lose: Instantly lose 10 points."""
    state["score"] -= POINTS_STAND
    utils.set_message(f"-{POINTS_STAND}")
    state["new_round"] = True

# The available menu items.
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
        "label": "View Score",
        "action": _do_viewscore
    },
    "4": {
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

def run():
    """The main game function."""
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
        # Clear the screen.
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
            utils.prompt_enter()
            state["game_over"] = f"You exceeded {TOTAL_BLACKJACK}. Game over!"
            break

        # Blackjack. A total of 21 in the player's hand results
        # in winning the current round.
        if state["player_total"] == TOTAL_BLACKJACK:
            utils.ansiprint(
                f"\nYou hit blackjack! ({POINTS_BLACKJACK} points)",
                "BGRN")
            state["score"] += POINTS_BLACKJACK
            utils.prompt_enter()
            state["new_round"] = True
            continue

        # Process player choices.
        utils.process_menu(MENU_ITEMS, state)

    scores.run_save(state)
