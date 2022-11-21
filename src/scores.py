import utils
import os

FILENAME_SCORES = "scores.txt"

def _sortByScore(value):
    return int(value[1])

scores = None

def get_default():
    scores = []
    for i in range(10, 0, -1):
        scores.append(["Juan de la Cruz", str(15 * i)])
    return scores

def get():
    global scores
    # Don't read the scores file again if we have loaded it already.
    if scores:
        return scores
    # Initialize scores to an empty list.
    scores = []
    # Read the scores file if it exists.
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
                    # Remove any previously added entries. We don't
                    # need those anymore.
                    scores.clear()
                    break
                scores.append(entry)
        file_scores.close()
    # If the scores list is still empty at this point...
    if len(scores) == 0:
        # This is already generated in descending order, so there's
        # no need to sort it. Just get the default list.
        scores = get_default()
    # Otherwise, sort the loaded score list. It is possible that it is
    # unsorted and we would not want to display that to the player.
    else:
        scores.sort(key=_sortByScore, reverse=True)
    return scores

def save():
    file_scores = open(FILENAME_SCORES, "w")
    for i in scores:
        # Delimit score entries with a comma.
        file_scores.write(",".join(i) + "\n")
    file_scores.close()

def reset():
    global scores
    scores = get_default()
    save()

def add(entry):
    global scores
    score_player = int(entry[1])
    insertion_index = 0
    for i in range(len(scores)):
        score_current = int(scores[i][1])
        if score_current < score_player:
            insertion_index = i
    scores.insert(insertion_index, entry)
    scores.pop()
    save()

def _do_return(state = None):
    global is_running
    is_running = False

def _do_add(state):
    while True:
        print("Please enter your name (max. 50 characters):")
        name = input()

        if len(name) > 50:
            print("Your name should not be greater than 50 characters.")
        else:
            break

    add([name, str(state)])
    utils.set_message("Thanks! Your score has been added to the list.", False)
    _do_return()

def _do_clear():
    utils.set_message("The high scores list was cleared.", False)
    reset()

# The available menu items.

MENU_ITEMS_ADD = {
    # Switches to the high score scene.
    "1": {
        "label": "Save my score",
        "action": _do_add
    },
    # Exits the game.
    "0": {
        "label": "Return to Main Menu",
        "action": _do_return
    }
}

MENU_ITEMS_VIEW = {
    # Switches to the high score scene.
    "1": {
        "label": "Clear High Scores",
        "action": _do_clear
    },
    # Exits the game.
    "0": {
        "label": "Return to Main Menu",
        "action": _do_return
    }
}

is_running = True

def run_view():
    global is_running
    is_running = True

    while is_running:
        utils.ansi(["@", "_", "GRN"])
        for i in utils.strings["intro_hs"]:
            print(i.center(80))
        utils.ansi("_")
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

        utils.process_menu(MENU_ITEMS_VIEW)

def run_save(score):
    global is_running
    is_running = True

    # Print the player's score (Reached only during game over).
    print(f"Your score: {score}")

    # Get the high scores list.
    scores = get()
    score_min = int(scores[len(scores)-1][1])

    # If the player got a score that is lower than the lowest score
    # in the list of high scores, then don't bother storing it.
    # Remove the option to save the score.
    is_score_low = (score < score_min)
    utils.menuitem_setdisabled(MENU_ITEMS_ADD, "1", is_score_low)
    if is_score_low:
        print()
        print("Your score is too low to be counted in the high score list.")
        print("Better luck next time!")

    while is_running:
        utils.process_menu(MENU_ITEMS_ADD, score)
