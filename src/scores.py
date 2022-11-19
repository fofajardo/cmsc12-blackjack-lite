import utils
import os

FILENAME_SCORES = "scores.txt"

is_running = True

def add_high_score(score):
    print("TODO: unimplemented")
    pass

def _sortByScore(value):
    return int(value[1])

def get():
    scores = []

    exists = os.path.exists(FILENAME_SCORES)
    if exists:
        file_scores = open(FILENAME_SCORES, "r")
        lines = file_scores.read().splitlines()
        for line in lines:
            scores.append(line.split(","))
        file_scores.close()

    if len(scores) == 0:
        for i in range(10):
            scores.append(["Juan de la Cruz", str(15 * i)])

    scores.sort(key=_sortByScore, reverse=True)

    return scores

def do_clear():
    print("TODO: unimplemented")

def do_return():
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
    # Prints the intro text, which is retrieved from a text file.
    intro_file = open("intro_scores.txt", "r")
    for i in intro_file.read().splitlines():
        print(i.center(80))
    intro_file.close()
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
