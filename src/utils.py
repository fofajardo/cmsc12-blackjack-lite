# Processes all menu items, executes their associated action based
# on user input, and provides a prompt.
def process_menu(menu, state = None):
    # Print all menu items.
    [print(f"[{i}] {menu[i]['label']}") for i in menu]
    # Handle user choice selection.
    choice = input("Enter choice: ").strip()
    if choice in menu:
        if state != None:
            menu[choice]["action"](state)
        else:
            menu[choice]["action"]()
        return
    print("Invalid option.")

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
    print("LOADED")
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
