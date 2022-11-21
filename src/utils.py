# ANSI escape codes.
AEC = {
    # Common
    "@": "\033[H\033[2J",
    "_": "\033[0m",
    "UE": "\033[4m",
    "UD": "\033[24m",
    "BE": "\033[1m",
    "BD": "\033[21m",
    # Regular text
    "BLK": "\033[0;30m",
    "RED": "\033[0;31m",
    "GRN": "\033[0;32m",
    "YEL": "\033[0;33m",
    "BLU": "\033[0;34m",
    "MAG": "\033[0;35m",
    "CYN": "\033[0;36m",
    "WHT": "\033[0;37m",
    # Regular bold text
    "BBLK": "\033[1;30m",
    "BRED": "\033[1;31m",
    "BGRN": "\033[1;32m",
    "BYEL": "\033[1;33m",
    "BBLU": "\033[1;34m",
    "BMAG": "\033[1;35m",
    "BCYN": "\033[1;36m",
    "BWHT": "\033[1;37m",
    # Regular underline text
    "UBLK": "\033[4;30m",
    "URED": "\033[4;31m",
    "UGRN": "\033[4;32m",
    "UYEL": "\033[4;33m",
    "UBLU": "\033[4;34m",
    "UMAG": "\033[4;35m",
    "UCYN": "\033[4;36m",
    "UWHT": "\033[4;37m",
    # Regular background
    "BLKB": "\033[40m",
    "REDB": "\033[41m",
    "GRNB": "\033[42m",
    "YELB": "\033[43m",
    "BLUB": "\033[44m",
    "MAGB": "\033[45m",
    "CYNB": "\033[46m",
    "WHTB": "\033[47m",
    # High intensity background
    "BLKHB": "\033[0;100m",
    "REDHB": "\033[0;101m",
    "GRNHB": "\033[0;102m",
    "YELHB": "\033[0;103m",
    "BLUHB": "\033[0;104m",
    "MAGHB": "\033[0;105m",
    "CYNHB": "\033[0;106m",
    "WHTHB": "\033[0;107m",
    # High intensity text
    "HBLK": "\033[0;90m",
    "HRED": "\033[0;91m",
    "HGRN": "\033[0;92m",
    "HYEL": "\033[0;93m",
    "HBLU": "\033[0;94m",
    "HMAG": "\033[0;95m",
    "HCYN": "\033[0;96m",
    "HWHT": "\033[0;97m",
    # Bold high intensity text
    "BHBLK": "\033[1;90m",
    "BHRED": "\033[1;91m",
    "BHGRN": "\033[1;92m",
    "BHYEL": "\033[1;93m",
    "BHBLU": "\033[1;94m",
    "BHMAG": "\033[1;95m",
    "BHCYN": "\033[1;96m",
    "BHWHT": "\033[1;97m"
}

# Print an ANSI escape code given a key.
def ansi(keys):
    if isinstance(keys, list):
        for i in keys:
            print(AEC[i], end="")
    else:
        print(AEC[keys], end="")

# Processes all menu items, executes their associated action based
# on user input, and provides a prompt.
KEY_CACHE = "_cache"

_message = None
_message_is_error = True

def set_message(text, is_error = True):
    global _message, _message_is_error
    _message = text
    _message_is_error = is_error

def clear_message():
    global _message
    _message = None

def process_menu(menu, state = None):
    global _message
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
        cache["separator_top"] = f" ╔{menu_separator}╗ ".center(80)
        cache["separator_bottom"] = f" ╚{menu_separator}╝ ".center(80)
        # Append the cached items to the menu dictionary.
        menu[KEY_CACHE] = cache
    # Print the top separator.
    print(menu[KEY_CACHE]["separator_top"])
    # Print all menu items.
    for i in menu:
        menuitem = menu[i]
        # Ignore the cache entry.
        if i == KEY_CACHE:
            continue
        # Skip disabled menu items.
        if "disabled" in menuitem:
            continue
        # Try to cache the center and enclosed label if it hasn't been
        # done already.
        label = menuitem["label_cached"]
        if not "final" in menuitem:
            # Determine the padding between the inner text
            # and the end separator.
            padding = " " * (menu[KEY_CACHE]["width"] - len(label))
            menu[i]["label_cached"] = f" ║ {label}{padding} ║ ".center(80)
            # Mark the menu item as "final" and update the value of
            # the label variable. Otherwise, the separators will
            # not be included.
            menu[i]["final"] = True
            label = menuitem["label_cached"]
        # Finally, print the centered and enclosed label.
        print(label)
    # Print the bottom separator.
    print(menu[KEY_CACHE]["separator_bottom"])

    if _message != None:
        if _message_is_error:
            ansi("BRED")
        else:
            ansi("BGRN")
        print(_message)
        ansi("_")

    # Handle user choice selection.
    choice = input("Enter choice: ").strip()

    # Check if the choice is in the menu.
    # NOTE: KEY_CACHE is reserved and should NOT
    # be used as a choice key.
    if choice in menu and choice != KEY_CACHE:
        menuitem = menu[choice]
        # Ignore actions for disabled menu items.
        if not "disabled" in menuitem:
            clear_message()
            if state != None:
                menuitem["action"](state)
            else:
                menuitem["action"]()
            return

    set_message("Invalid option!")

# Set the disabled state of a menu item.
def menuitem_setdisabled(menu, index, state):
    if state == True:
        menu[index]["disabled"] = True
    elif state == False:
        # This menu item is not disabled. Ignore.
        if not "disabled" in menu[index]:
            return

        del menu[index]["disabled"]
    else:
        raise ValueError("'state' argument must be boolean.")

# String constants.
FILE_STRINGS = "strings.txt"

SECTION_STRING_MULTILINE = "string_ml"
SECTION_STRING_GROUP = "string"
SECTION_END = "end"

strings = None

# Load and parse the strings file.
def load_strings(force_reload = False):
    global strings
    # Don't load the strings file again unless we're forcing it.
    if strings and not force_reload:
        return
    # Initialize strings dictionary.
    strings = {}
    # Keep track of current section details.
    section_type = None
    section_name = None
    # Open up the strings file and read it line-by-line.
    strings_file = open(FILE_STRINGS, "r")
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
                strings[section_name].append(i)
            # Section: string group
            elif section_type == SECTION_STRING_GROUP:
                separator_index = line.index("=")
                key = line[0:separator_index]
                value = line[separator_index + 1:len(line)]
                strings[section_name][key] = value
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
                raise ValueError(f"Stray '{line}' on strings file.")

            # Create a new list or dictionary if the section name does
            # not yet exist. Otherwise, merge their contents.
            if not section_name in strings:
                if header[0] == SECTION_STRING_MULTILINE:
                    strings[section_name] = []
                elif header[0] == SECTION_STRING_GROUP:
                    strings[section_name] = {}
    # Close the strings file for good measure.
    strings_file.close()

load_strings()
