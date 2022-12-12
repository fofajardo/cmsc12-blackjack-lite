# Flip this to true to disable all ANSI escape codes.
# Useful in terminals that don't support it, such as Windows'
# default command prompt.
DISABLE_AEC = False

# Common AEC combinations (styles).
STYLE_MENU = ["RED","WHTB"]
STYLE_MENU_LABEL = ["RED", "WHTB", "BE"]
STYLE_TERMINATE = ["_", "$"]
STYLE_HIDDEN = ["BLK", "BLKB"]

def ansi(keys):
    """Print an ANSI escape code given a key list."""
    # Don't print anything if AECs are disabled.
    if DISABLE_AEC:
        return
    if isinstance(keys, list):
        for i in keys:
            print(STRINGS["aec"][i], end="")
    else:
        print(STRINGS["aec"][keys], end="")

def ansicode(keys):
    """Return a string with the ANSI escape code given a key list."""
    # Don't print anything if AECs are disabled.
    if DISABLE_AEC:
        return ""
    if isinstance(keys, list):
        code = ""
        for i in keys:
            code += STRINGS["aec"][i]
        return code
    else:
        return STRINGS["aec"][keys]

def ansiprint(text, start_keys=None, end_keys=STYLE_TERMINATE, center=False):
    """Print text that is affixed with an ANSI escape code.

    Keyword arguments:
    text -- the text to be displayed
    start_keys -- list corresponding to ANSI escape codes (default None)
    end_keys -- list corresponding to ANSI escape codes (default STYLE_TERMINATE)
    center -- determines if the text should be centered
    """
    # Remove start and end keys if AECs are disabled.
    if DISABLE_AEC:
        start_keys = None
        end_keys = None
    # Holds processed text.
    code = ""
    # Add ANSI escape codes to the beginning if needed.
    len_start = 0
    if start_keys:
        start = ansicode(start_keys)
        code += start
        len_start = len(start)
    # Append the text
    code += text
    # Add ANSI escape codes to the end if needed.
    len_end = 0
    if end_keys:
        end = ansicode(end_keys)
        code += end
        len_end = len(end)
    # Print the processed text.
    if center:
        print(code.center(80 + len_start + len_end))
    else:
        print(code)

HEIGHT_BIG_NUM = 3
def get_big_number(number):
    """Return a list containing 'big' number strings."""
    # Convert the number into its string representation.
    text = str(number)
    lines_merged = [""] * HEIGHT_BIG_NUM
    # Determine what number.
    for i in text:
        lines = []
        if i == "0" or \
           i == "1" or \
           i == "2" or \
           i == "3" or \
           i == "4" or \
           i == "5" or \
           i == "6" or \
           i == "7" or \
           i == "8" or \
           i == "9":
            lines = STRINGS["num" + i]
        # Handle negative or minus sign.
        elif i == "-":
            lines = STRINGS["num_neg"]
        for i in range(HEIGHT_BIG_NUM):
            lines_merged[i] += lines[i]
    return lines_merged

# Processes all menu items, executes their associated action based
# on user input, and provides a prompt.
KEY_CACHE = "_cache"

_MESSAGE = None
_MESSAGE_IS_ERROR = True

def set_message(text, is_error = True):
    """Set the status message.

    Keyword arguments:
    text -- the text to be displayed
    is_error -- determines if the text should be colored as an error
    """
    global _MESSAGE, _MESSAGE_IS_ERROR
    if _MESSAGE:
        _MESSAGE += f"\n{text}"
    else:
        _MESSAGE = text
    _MESSAGE_IS_ERROR = is_error

def clear_message():
    """Clear the status message."""
    global _MESSAGE
    _MESSAGE = None

def process_menu(menu, state = None, center = True):
    """Process a menu list and handle its actions.

    Keyword arguments:
    menu -- a list containing menu items
    state -- a value that will be passed to the action (default None)
    center -- determines if the text should be centered (default True)
    """
    # Cache the following items, which will be stored in the given
    # menu dictionary: (a) labels with action caption, (b) width of
    # the longest label, and (c) menu separator.
    if KEY_CACHE not in menu:
        # Initialize.
        cache = {}
        cache["width"] = 0
        for i in menu:
            # Store the label with action caption.
            label = f"[{i}] {menu[i]['label']}"
            menu[i]["label_cached"] = label
            # Try to get the length of the longest label.
            label_width = len(label)
            if label_width > cache["width"]:
                cache["width"] = label_width
        # Store the separator.
        menu_separator = "═" * (cache["width"] + 2)
        cache["separator"] = menu_separator
        cache["separator_top"] = f" ╔{menu_separator}╗ "
        cache["separator_bottom"] = f" ╚{menu_separator}╝ "
        # Append the cached items to the menu dictionary.
        menu[KEY_CACHE] = cache
    # Print the top separator.
    ansiprint(menu[KEY_CACHE]["separator_top"], STYLE_MENU, center=center)
    # Print all menu items.
    for i in menu:
        menuitem = menu[i]
        # Ignore the cache entry.
        if i == KEY_CACHE:
            continue
        # Skip disabled menu items.
        if "disabled" in menuitem or \
           "hidden" in menuitem:
            continue
        # Try to cache the center and enclosed label if it hasn't been
        # done already.
        label = menuitem["label_cached"]
        if not "final" in menuitem:
            # Determine the padding between the inner text
            # and the end separator.
            padding = " " * (menu[KEY_CACHE]["width"] - len(label))
            menu[i]["label_cached"] = f" ║ {label}{padding} ║ "
            # Mark the menu item as "final" and update the value of
            # the label variable. Otherwise, the separators will
            # not be included.
            menu[i]["final"] = True
            label = menuitem["label_cached"]
        # Finally, print the centered and enclosed label.
        ansiprint(label, STYLE_MENU_LABEL, center=center)
    # Print the bottom separator.
    ansiprint(menu[KEY_CACHE]["separator_bottom"], STYLE_MENU, center=center)
    # Print the status message.
    if _MESSAGE is not None:
        style = "BGRN"
        if _MESSAGE_IS_ERROR:
            style = "BRED"
        ansiprint(_MESSAGE, style)
    # Handle user choice selection.
    ansi("RED")
    choice = input("Enter choice: " + ansicode(STYLE_TERMINATE) + ansicode("BE")).strip()
    ansi(STYLE_TERMINATE)
    # Check if the choice is in the menu.
    # NOTE: KEY_CACHE is reserved and should NOT
    # be used as a choice key.
    if choice in menu and choice != KEY_CACHE:
        menuitem = menu[choice]
        # Ignore actions for disabled menu items.
        if not "disabled" in menuitem:
            clear_message()
            if state is not None:
                menuitem["action"](state)
            else:
                menuitem["action"]()
            return

    set_message("Invalid option!")

def menuitem_setdisabled(menu, index, state):
    """Set the disabled state of a menu item.

    Keyword arguments:
    menu -- a list containing menu items
    index -- index of the menu item in the menu list
    state -- boolean that determines if the menu item is disabled
    """
    if state is True:
        menu[index]["disabled"] = True
    elif state is False:
        # This menu item is not disabled. Ignore.
        if not "disabled" in menu[index]:
            return

        del menu[index]["disabled"]
    else:
        print("'state' argument must be boolean.")

def prompt_enter():
    """Prompt the user to press Enter before proceeding."""
    while True:
        ansi("BRED")
        for i in STRINGS["enter_tc"]:
            print(i.center(80))
        ansi(STYLE_TERMINATE)

        ansi(STYLE_HIDDEN)
        input()
        ansi(STYLE_TERMINATE)
        break

# String constants.
FILE_STRINGS = "strings.txt"

SECTION_STRING_MULTILINE = "string_ml"
SECTION_STRING_GROUP = "string"
SECTION_END = "end"

STRINGS = None

def load_strings(force_reload = False):
    """Load and parse the strings file.

    Keyword arguments:
    force_reload -- bypass cache and load strings from file (default False)
    """
    global STRINGS
    # Don't load the strings file again unless we're forcing it.
    if STRINGS and not force_reload:
        return
    # Initialize strings dictionary.
    STRINGS = {}
    # Keep track of current section details.
    section_type = None
    section_name = None
    # Open up the strings file and read it line-by-line.
    strings_file = open(FILE_STRINGS, "r", encoding="utf-8")
    for i in strings_file.read().splitlines():
        # Remove whitespace from current line.
        line = i.strip()
        # We're currently in a section. Parse its contents.
        if section_type and section_name:
            # End of a section: reset section type and name
            if line == SECTION_END:
                section_type = None
                section_name = None
                continue
            # Section: string (multi-line)
            elif section_type == SECTION_STRING_MULTILINE:
                STRINGS[section_name].append(i)
            # Section: string group
            elif section_type == SECTION_STRING_GROUP:
                separator_index = line.index("=")
                key = line[0:separator_index]
                value = line[separator_index + 1:len(line)]
                # Remove extra backslash character from ANSI escape code.
                if "\\033" in value:
                    value = value.replace("\\033", "\033")
                STRINGS[section_name][key] = value
        else:
            # Set section name and type based on the header
            header = line.split(" ")

            # Check: Ignore empty lines
            if line == "":
                pass
            # Check: Is this a multi-line string or a string group?
            elif header[0] == SECTION_STRING_MULTILINE or \
                 header[0] == SECTION_STRING_GROUP:
                section_type = header[0]
                section_name = header[1]
            # Check: Throw on stray keywords.
            else:
                print(f"Stray '{line}' on strings file.")

            # Create a new list or dictionary if the section name does
            # not yet exist. Otherwise, merge their contents.
            if not section_name in STRINGS:
                if header[0] == SECTION_STRING_MULTILINE:
                    STRINGS[section_name] = []
                elif header[0] == SECTION_STRING_GROUP:
                    STRINGS[section_name] = {}
    # Close the strings file for good measure.
    strings_file.close()

load_strings()
