import json

def load_game(game_file_name):
    """
    Loads the game data from a JSON file.

    Arguments:
    - game_file_name (str): The name of the JSON file containing game data.

    Returns:
    - dict or None: The game data if loaded successfully
    """
    game = None
    try:
        with open(game_file_name) as game_file:
            game_data = game_file.read()
            game = json.loads(game_data)
    except FileNotFoundError:
        print('That file does not exist.')
    return game


def build_world(locations, people, clues):
    """
    Initializes the game world by setting up locations, people, and clues.

    Arguments:
    - locations (dict): Dictionary containing location
    - people (dict): Dictionary containing people
    - clues (dict): Dictionary containing clue
    """
    for loc_name, loc_data in locations.items():
        loc_data['locked'] = loc_data.get('starts-locked', False)
    for person_name, person_data in people.items():
        person_data['hidden'] = person_data.get('starts-hidden', False)
    for clue_name, clue_data in clues.items():
        clue_data['hidden'] = True


def can_go(start, end, locations, visited=None):
    """
    Checks if you can move from one place to another

    Arguments:
    - start (str): The starting location.
    - end (str): The destination location.
    - locations (dict): Dictionary containing location data.
    - visited (list): List of visited locations

    Returns:
    - bool: True if movement is possible or else it is false
    """
    if visited is None:
        visited = []
    visited.append(start)
    if start == end:
        return True
    if end in locations[start]['connections'] and not locations[end]['starts-locked']:
        return True
    for neighbor in locations[start]['connections']:
        if neighbor not in visited and not locations[neighbor]['starts-locked']:
            if can_go(neighbor, end, locations, visited):
                return True
    return False


def talk_to_person(person_name, current_location, locations, people, clues):
    """
    Handles interactions with characters in the game.

    Arguments:
    - person_name (str): The name of the person to talk to.
    - current_location (str): The current location of the player.
    - locations (dict): Dictionary containing location data.
    - people (dict): Dictionary containing people data.
    - clues (dict): Dictionary containing clue data.
    """
    person_data = people.get(person_name.capitalize())

    # Check if the person exists, is in the current location, and is not hidden
    if person_data and person_data['location'] == current_location and not person_data['hidden']:
        print(person_data['conversation'])

        # Unlock locations
        unlock_locations = person_data.get('unlock-locations', [])
        for loc_name in unlock_locations:
            if loc_name in locations:
                locations[loc_name]['starts-locked'] = False

        # Unhide people
        unlock_people = person_data.get('unlock-people', [])
        for unlock_person_name in unlock_people:
            if unlock_person_name.capitalize() in people:
                people[unlock_person_name.capitalize()]['hidden'] = False

        # Unhide clues
        unlock_clues = person_data.get('unlock-clues', [])
        for unlock_clue_name in unlock_clues:
            if unlock_clue_name.capitalize() in clues:
                clues[unlock_clue_name.capitalize()]['hidden'] = False
    else:
        print("There's no one named {} here to talk to.".format(person_name))


def investigate_location(clue_name, current_location, locations, people, clues):
    """
    Allows the player to investigate a location for clues.

    Arguments:
    - clue_name (str): The name of the clue to investigate.
    - current_location (str): The current location of the player.
    - locations (dict): Dictionary containing location data.
    - people (dict): Dictionary containing people data.
    - clues (dict): Dictionary containing clue data.
    """
    # Remove "investigate" from the clue_name and capitalize the rest of the words
    clue_name = " ".join([word.capitalize() for word in clue_name.split()])

    # Check if the clue exists, is not hidden, and is unlocked at the current location
    if clue_name in clues and not clues[clue_name]['hidden'] and current_location in clues[clue_name].get(
            'unlock-locations', []):
        print(clues[clue_name]['clue-text'])

        # Unlock locations
        unlock_locations = clues[clue_name].get('unlock-locations', [])
        for loc_name in unlock_locations:
            if loc_name in locations:
                locations[loc_name]['starts-locked'] = False

        # Unhide people
        unlock_people = clues[clue_name].get('unlock-people', [])
        for person_name in unlock_people:
            if person_name.capitalize() in people:
                people[person_name.capitalize()]['hidden'] = False

        # Unhide other clues
        unlock_clues = clues[clue_name].get('unlock-clues', [])
        for other_clue_name in unlock_clues:
            if other_clue_name.capitalize() in clues:
                clues[other_clue_name.capitalize()]['hidden'] = False
    else:
        print("There's no clue named '{}' here.".format(clue_name))


def display_locations(locations):
    """
    Displays the available locations.

    Arguments:
    - locations (dict): Dictionary containing location data.
    """
    print("Locations:")
    for loc_name in locations:
        loc_data = locations[loc_name]
        print(f"{loc_name} {'(locked)' if loc_data['starts-locked'] else ''}")


def display_clues(current_location, clues):
    """
    Displays the clues available at the current location.

    Arguments:
    - current_location (str): The current location of the player.
    - clues (dict): Dictionary containing clue data.
    """
    print("Clues at {}: ".format(current_location))
    for clue_name in clues:
        clue_data = clues[clue_name]
        if not clue_data['hidden'] and current_location in clue_data.get('unlock-locations', []):
            print(clue_name, ":", clue_data['clue-text'])


def display_people(current_location, people):
    """
    Displays the people available at the current location.

    Arguments:
    - current_location (str): The current location of the player.
    - people (dict): Dictionary containing people data.
    """
    print("People at {}: ".format(current_location))
    for person_name in people:
        person_data = people[person_name]
        if not person_data['hidden'] and person_data['location'] == current_location:
            print(person_name)


def carmen_sandiego(file_name):
    """
    Runs the main game loop for Where's Carmen game.

    Arguments:
    - file_name (str): The name of the game data file.
    """
    game = load_game(file_name)
    if not game:
        return

    locations = game.get('locations', {})
    people = game.get('people', {})
    clues = game.get('clues', {})
    starting_location = game.get('starting-location', '')

    current_location = starting_location

    build_world(locations, people, clues)

    # Counter for unsuccessful searches for Carmen
    unsuccessful_searches = 0

    # Game loop
    while True:
        print("\nYou are at:", current_location)
        command = input("What would you like to do? ").lower()

        if command == "display locations":
            display_locations(locations)
        elif command == "display clues":
            display_clues(current_location, clues)
        elif command == "display people":
            display_people(current_location, people)
        elif command.startswith("go to ") or command.startswith("travel to "):
            destination = command[6:].capitalize()
            if can_go(current_location, destination, locations):
                current_location = destination
                print("You have traveled to {}.".format(destination))
            else:
                print("You can't go there from here.")
        elif command.startswith("talk to "):
            person_name = command[8:].strip()
            talk_to_person(person_name, current_location, locations, people, clues)
        elif command.startswith("investigate "):
            clue_name = command[12:].strip()
            investigate_location(clue_name, current_location, locations, people, clues)
        elif command == "catch carmen":
            if locations[current_location].get('carmen', False):
                print("You have caught Carmen Sandiego! You win the game!")
            else:
                unsuccessful_searches += 1
                print("You didn't find Carmen here.")
                if unsuccessful_searches == 3:
                    print("You have searched unsuccessfully for Carmen three times. You lose the game.")
        elif command == "quit" or command == "exit":
            print("Exiting the game...")
            return
        else:
            print("Command not recognized.")

if __name__ == '__main__':
    game_file_name = input('Which game do you want to play? ')
    carmen_sandiego(game_file_name)






"""
File:    carmen.py
Author:  Hader Hamayun
Date:    5/14/24
Section: 14
E-mail:  haderh1@umbc.edu
Description:
  You play the game where's carmen
"""

import json

def load_game(game_file_name):
    """
    Loads the game data from a JSON file.

    Arguments:
    - game_file_name (str): The name of the JSON file containing game data.

    Returns:
    - dict or None: The game data if loaded successfully
    """
    game = None
    try:
        with open(game_file_name) as game_file:
            game_data = game_file.read()
            game = json.loads(game_data)
    except FileNotFoundError:
        print('That file does not exist.')
    return game


def build_world(locations, people, clues):
    """
    Initializes the game world by setting up locations, people, and clues.

    Arguments:
    - locations (dict): Dictionary containing location
    - people (dict): Dictionary containing people
    - clues (dict): Dictionary containing clue
    """
    for loc_name, loc_data in locations.items():
        loc_data['locked'] = loc_data.get('starts-locked', False)
    for person_name, person_data in people.items():
        person_data['hidden'] = person_data.get('starts-hidden', False)
    for clue_name, clue_data in clues.items():
        clue_data['hidden'] = True


def can_go(start, end, locations, visited=None):
    """
    Checks if you can move from one place to another

    Arguments:
    - start (str): The starting location.
    - end (str): The destination location.
    - locations (dict): Dictionary containing location data.
    - visited (list): List of visited locations

    Returns:
    - bool: True if movement is possible or else it is false
    """
    if visited is None:
        visited = []
    visited.append(start)
    if start == end:
        return True
    if end in locations[start]['connections'] and not locations[end]['starts-locked']:
        return True
    for neighbor in locations[start]['connections']:
        if neighbor not in visited and not locations[neighbor]['starts-locked']:
            if can_go(neighbor, end, locations, visited):
                return True
    return False


def talk_to_person(person_name, current_location, locations, people, clues):
    """
    Handles interactions with characters in the game.

    Arguments:
    - person_name (str): The name of the person to talk to.
    - current_location (str): The current location of the player.
    - locations (dict): Dictionary containing location data.
    - people (dict): Dictionary containing people data.
    - clues (dict): Dictionary containing clue data.
    """
    person_data = people.get(person_name.capitalize())

    # Check if the person exists, is in the current location, and is not hidden
    if person_data and person_data['location'] == current_location and not person_data['hidden']:
        print(person_data['conversation'])

        # Unlock locations
        unlock_locations = person_data.get('unlock-locations', [])
        for loc_name in unlock_locations:
            if loc_name in locations:
                locations[loc_name]['starts-locked'] = False

        # Unhide people
        unlock_people = person_data.get('unlock-people', [])
        for unlock_person_name in unlock_people:
            if unlock_person_name.capitalize() in people:
                people[unlock_person_name.capitalize()]['hidden'] = False

        # Unhide clues
        unlock_clues = person_data.get('unlock-clues', [])
        for unlock_clue_name in unlock_clues:
            if unlock_clue_name.capitalize() in clues:
                clues[unlock_clue_name.capitalize()]['hidden'] = False
    else:
        print("There's no one named {} here to talk to.".format(person_name))


def investigate_location(clue_name, current_location, locations, people, clues):
    """
    Allows the player to investigate a location for clues.

    Arguments:
    - clue_name (str): The name of the clue to investigate.
    - current_location (str): The current location of the player.
    - locations (dict): Dictionary containing location data.
    - people (dict): Dictionary containing people data.
    - clues (dict): Dictionary containing clue data.
    """
    # Remove "investigate" from the clue_name and capitalize the rest of the words
    clue_name = " ".join([word.capitalize() for word in clue_name.split()])

    # Check if the clue exists, is not hidden, and is unlocked at the current location
    if clue_name in clues and not clues[clue_name]['hidden'] and current_location in clues[clue_name].get(
            'unlock-locations', []):
        print(clues[clue_name]['clue-text'])

        # Unlock locations
        unlock_locations = clues[clue_name].get('unlock-locations', [])
        for loc_name in unlock_locations:
            if loc_name in locations:
                locations[loc_name]['starts-locked'] = False

        # Unhide people
        unlock_people = clues[clue_name].get('unlock-people', [])
        for person_name in unlock_people:
            if person_name.capitalize() in people:
                people[person_name.capitalize()]['hidden'] = False

        # Unhide other clues
        unlock_clues = clues[clue_name].get('unlock-clues', [])
        for other_clue_name in unlock_clues:
            if other_clue_name.capitalize() in clues:
                clues[other_clue_name.capitalize()]['hidden'] = False
    else:
        print("There's no clue named '{}' here.".format(clue_name))


def display_locations(locations):
    """
    Displays the available locations.

    Arguments:
    - locations (dict): Dictionary containing location data.
    """
    print("Locations:")
    for loc_name in locations:
        loc_data = locations[loc_name]
        print(f"{loc_name} {'(locked)' if loc_data['starts-locked'] else ''}")


def display_clues(current_location, clues):
    """
    Displays the clues available at the current location.

    Arguments:
    - current_location (str): The current location of the player.
    - clues (dict): Dictionary containing clue data.
    """
    print("Clues at {}: ".format(current_location))
    for clue_name in clues:
        clue_data = clues[clue_name]
        if not clue_data['hidden'] and current_location in clue_data.get('unlock-locations', []):
            print(clue_name, ":", clue_data['clue-text'])


def display_people(current_location, people):
    """
    Displays the people available at the current location.

    Arguments:
    - current_location (str): The current location of the player.
    - people (dict): Dictionary containing people data.
    """
    print("People at {}: ".format(current_location))
    for person_name in people:
        person_data = people[person_name]
        if not person_data['hidden'] and person_data['location'] == current_location:
            print(person_name)


def carmen_sandiego(file_name):
    """
    Runs the main game loop for Where's Carmen game.

    Arguments:
    - file_name (str): The name of the game data file.
    """
    game = load_game(file_name)
    if not game:
        return

    locations = game.get('locations', {})
    people = game.get('people', {})
    clues = game.get('clues', {})
    starting_location = game.get('starting-location', '')

    current_location = starting_location

    build_world(locations, people, clues)

    # Counter for unsuccessful searches for Carmen
    unsuccessful_searches = 0

    # Game loop
    while True:
        print("\nYou are at:", current_location)
        command = input("What would you like to do? ").lower()

        if command == "display locations":
            display_locations(locations)
        elif command == "display clues":
            display_clues(current_location, clues)
        elif command == "display people":
            display_people(current_location, people)
        elif command.startswith("go to ") or command.startswith("travel to "):
            destination = command[6:].capitalize()
            if can_go(current_location, destination, locations):
                current_location = destination
                print("You have traveled to {}.".format(destination))
            else:
                print("You can't go there from here.")
        elif command.startswith("talk to "):
            person_name = command[8:].strip()
            talk_to_person(person_name, current_location, locations, people, clues)
        elif command.startswith("investigate "):
            clue_name = command[12:].strip()
            investigate_location(clue_name, current_location, locations, people, clues)
        elif command == "catch carmen":
            if locations[current_location].get('carmen', False):
                print("You have caught Carmen Sandiego! You win the game!")
            else:
                unsuccessful_searches += 1
                print("You didn't find Carmen here.")
                if unsuccessful_searches == 3:
                    print("You have searched unsuccessfully for Carmen three times. You lose the game.")
        elif command == "quit" or command == "exit":
            print("Exiting the game...")
            return
        else:
            print("Command not recognized.")

if __name__ == '__main__':
    game_file_name = input('Which game do you want to play? ')
    carmen_sandiego(game_file_name)
