# Processes all menu items, executes their associated action based
# on user input, and provides a prompt.
def process_menu(menu, state = None):
    # Print all menu items.
    [print(f"[{i}] {menu[i]['label']}") for i in menu]

    # Handle user choice selection.
    choice = input("Enter choice: ").strip()
    if choice in menu:
        if state:
            menu[choice]["action"](state)
        else:
            menu[choice]["action"]()
        return

    print("Invalid option.")
