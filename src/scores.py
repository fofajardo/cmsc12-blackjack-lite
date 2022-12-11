import utils
import os

FILENAME_SCORES = "scores.txt"

def _sortByScore(value):
    """Internal function to sort the scores by value."""
    return int(value[1])

scores = None

def get_default():
    """Retrieve the default set of high scores and return a list."""
    scores = []
    for i in range(10, 0, -1):
        scores.append(["Juan de la Cruz", str(15 * i)])
    return scores

def get():
    """Retrieve high scores from file and return a list."""
    global scores
    # Don't read the scores file again if we have loaded it already.
    if scores:
        return scores
    # Initialize scores to an empty list.
    scores = []
    # Read the scores file if it exists.
    exists = os.path.exists(FILENAME_SCORES)
    if exists:
        file_scores = open(FILENAME_SCORES, "r", encoding="utf-8")
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
    """Save high scores to file."""
    file_scores = open(FILENAME_SCORES, "w", encoding="utf-8")
    for i in scores:
        # Delimit score entries with a comma.
        file_scores.write(",".join(i) + "\n")
    file_scores.close()

def reset():
    """Reset all high scores and save to file."""
    global scores
    scores = get_default()
    save()

def add(entry):
    """Add a new entry to the high scores list."""
    global scores
    score_player = int(entry[1])
    insertion_index = 0
    for i in range(len(scores)):
        score_current = int(scores[i][1])
        if score_player > score_current:
            insertion_index = i
            break
    scores.insert(insertion_index, entry)
    scores.pop()
    save()

def _do_return(state = None):
    """Return: exits the current scene."""
    global is_running
    is_running = False

def _do_add(state):
    """Add: prompts the user to enter their name and save their score."""
    while True:
        print("Please enter your name (max. 50 characters):")
        name = input().strip()

        if len(name) == 0 or len(name) > 50:
            print("Your name must be between 1-50 characters.")
        else:
            break

    add([name, str(state)])
    utils.set_message("Thanks! Your score has been added to the list.", False)
    _do_return()

def _do_clear():
    """Clear: reset the high scores list and inform the user."""
    utils.set_message("The high scores list was cleared.", False)
    reset()

# The available menu items (add high score).
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

# The available menu items (view all high scores).
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
    """Run the view all high scores scene."""
    global is_running
    is_running = True

    while is_running:
        # Clear the screen and set the color.
        utils.ansi(["@", "_", "GRN"])
        # Print the intro high scores text.
        for i in utils.strings["intro_hs"]:
            print(i.center(80))
        utils.ansi("_")
        # Get the high scores list.
        scores = get()
        # Create a divider string which will be used later.
        divider = "━" * 80
        # Print the header row.
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
        # Print the contents of the high scores list.
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

def run_save(state):
    """Run the save player's high score scene."""
    global is_running
    is_running = True

    score = state["score"]

    while is_running:
        # Clear the screen and set the color.
        utils.ansi(["@", "GRN"])
        for i in utils.strings["game_over"]:
            print(i.center(80))
        utils.ansi(utils.STYLE_TERMINATE)
        # Print game over header if necessary.
        if "game_over" in state:
            reason = state["game_over"]
            print(reason.center(80))
        # Print the player's score (Reached only during game over).
        utils.ansiprint("<YOUR SCORE>".center(80), "BE")
        for i in utils.get_big_number(score):
            print(i.center(80))
        # Get the high scores list.
        scores = get()
        score_min = int(scores[len(scores)-1][1])
        # If the player got a score that is lower than the lowest score
        # in the list of high scores, then don't bother storing it.
        # Remove the option to save the score.
        is_score_low = (score < score_min)
        utils.menuitem_setdisabled(MENU_ITEMS_ADD, "1", is_score_low)
        if is_score_low:
            for i in utils.strings["score_low"]:
                print(i.center(80))
        utils.process_menu(MENU_ITEMS_ADD, score)
