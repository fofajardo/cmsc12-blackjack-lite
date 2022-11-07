import random

SUITS = ["c", "d", "h", "s"]
CARDS_COURT = ["J", "Q", "K"]
CARD_ACE = "A"

class Card:
    def __init__(self, suit, type):
        self.suit = suit
        self.type = str(type)
        if type == 1:
            self.type = CARD_ACE
        elif type in CARDS_COURT:
            self.type = type
            self.value = 10
            return
        self.value = type
    def to_text(self):
        return self.type + self.suit

def generate_deck():
    deck = []
    for suit in SUITS:
        for pip in range(1, 11):
            deck.append(Card(suit, pip))
        for court in CARDS_COURT:
            deck.append(Card(suit, court))
    return deck

def get_hand_value(hand):
    value = 0
    for i in hand:
        value += i.value
    return value

def print_cards(hand, target):
    print(f"{target} cards are:")
    for card in hand:
        print(card.to_text(), end=" ")
    print()

def run():
    deck = generate_deck()

    hand = []
    dealer = []
    score = 0
    new_round = True

    while True:
        has_ace = False
        has_ten = False

        if new_round:
            if len(deck) < 10:
                deck = generate_deck()

            hand.clear()
            for i in range(2):
                card = random.choice(deck)
                hand.append(card)
                deck.remove(card)

                if card.type == CARD_ACE:
                    has_ace = True
                if card.value == 10:
                    has_ten = True

            dealer.clear()
            for i in range(2):
                card = random.choice(deck)
                dealer.append(card)
                deck.remove(card)

            new_round = False

        print_cards(hand, "Your")

        hand_value = get_hand_value(hand)
        dealer_value = get_hand_value(dealer)

        if hand_value > 21:
            print("You exceeded 21. Game over!")
            break

        if (has_ace and has_ten) or hand_value == 21:
            print("You hit blackjack! (21 points)")
            score += 21
            new_round = True
            continue

        while True:
            print("[1] Stand")
            print("[2] Hit")
            print("Enter choice: ")
            choice = input()
            if choice.isdigit():
                choice = int(choice)
                if choice == 1:
                    print_cards(dealer, "Dealer's")

                    result = ""
                    if hand_value > dealer_value:
                        result = "win 10"
                        score += 10
                    else:
                        result = "lose 10"
                        score -= 10
                    print(f"You {result} points!")

                    new_round = True
                    break
                elif choice == 2:
                    card = random.choice(deck)
                    hand.append(card)
                    deck.remove(card)
                    break
            print("Invalid option.")

        print("\n")

    print(f"Your score: {score}")

run()
