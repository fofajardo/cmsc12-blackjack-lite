import utils
import os

FILENAME_SCORES = "scores.txt"

is_running = True

def _sortByScore(value):
    return int(value[1])

def get_default():
    scores = []
    for i in range(10, 0, -1):
        scores.append(["Juan de la Cruz", str(15 * i)])
    return scores

RESET_REASON_INVALID = "Your high scores file is invalid and was reset to default."

def reset(reason):
    print(reason)
    scores = get_default()
    save(scores)
    return scores

def get():
    scores = []

    exists = os.path.exists(FILENAME_SCORES)
    if exists:
        file_scores = open(FILENAME_SCORES, "r")
        lines = file_scores.read().splitlines()
        # Check: do we have exactly 10 entries?
        if len(lines) == 10:
            for line in lines:
                entry = line.split(",")
                # Check: do we have a name-score pair and is the
                # score a "digit" or a valid number?
                if len(entry) != 2 or not entry[1].isdigit():
                    scores = reset(RESET_REASON_INVALID)
                    break
                scores.append(entry)
        else:
            scores = reset(RESET_REASON_INVALID)
        file_scores.close()

    if len(scores) == 0:
        scores = get_default()

    scores.sort(key=_sortByScore, reverse=True)

    return scores

def save(scores):
    file_scores = open(FILENAME_SCORES, "w")
    for i in scores:
        file_scores.write(",".join(i) + "\n")

def add(entry):
    scores = get()

    score_player = int(entry[1])
    insertion_index = 0
    for i in range(len(scores)):
        score_current = int(scores[i][1])
        if score_current < score_player:
            insertion_index = i

    scores.insert(insertion_index, entry)
    scores.pop()
    save(scores)

def do_clear():
    reset("The high scores list was cleared.")

def do_return(state = None):
    global is_running
    is_running = False

# The available menu items.
MENU_ITEMS = {
    # Switches to the high score scene.
    "1": {
        "label": "Clear High Scores",
        "action": do_clear
    },
    # Exits the game.
    "0": {
        "label": "Return to Main Menu",
        "action": do_return
    }
}

def run():
    global is_running
    is_running = True

    for i in utils.strings["intro_hs"]:
        print(i.center(80))
    print()

    scores = get()

    divider = "━" * 80

    print(divider)

    headers = [
        ["Rank", 14],
        ["Name", 50],
        ["Score", 14]
    ]
    header_count = len(headers)
    for cell_i in range(header_count):
        header = headers[cell_i][0]
        width = headers[cell_i][1]
        suffix = "┃"
        if cell_i == (header_count - 1):
            suffix = "\n"
        print(header.center(width), end=suffix)

    print(divider)

    row_count = len(scores)
    for row_i in range(row_count):
        row = scores[row_i]
        cells = [
            str(row_i + 1).center(headers[0][1]),
            row[0].center(headers[1][1]),
            "  " + row[1].ljust(headers[2][1] - 2)
        ]
        for cell_i in range(header_count):
            suffix = "│"
            if cell_i == (header_count - 1):
                suffix = "\n"
            print(cells[cell_i], end=suffix)

    print()

    while is_running:
        utils.process_menu(MENU_ITEMS)

def do_add(state):
    while True:
        print("Please enter your name (max. 50 characters):")
        name = input()

        if len(name) > 50:
            print("Your name should not be greater than 50 characters.")
        else:
            break

    add([name, str(state)])
    print("Thanks! Your score has been added to the list.")
    do_return()

MENU_ITEMS_ADD_HS = {
    # Switches to the high score scene.
    "1": {
        "label": "Save my score",
        "action": do_add
    },
    # Exits the game.
    "0": {
        "label": "Return to Main Menu",
        "action": do_return
    }
}

def run_save_score(score):
    global is_running
    is_running = True

    # Print the player's score (Reached only during game over).
    print(f"Your score: {score}")

    while is_running:
        utils.process_menu(MENU_ITEMS_ADD_HS, score)
