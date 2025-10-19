import random

import time

import turtle


# -------------------------

# Game Data

# -------------------------

GAME_WEAPONS = {

    "w1": {"name": "Stun Gun", "price": 30, "effect": "Incapacitates a monster (one use)"},

    "w2": {"name": "Sword", "price": 100, "effect": "Kills the monster (one use)"},

    "w3": {"name": "Invisibility Cloak", "price": 40, "effect": "Avoids the monster (two uses)"}

}


ROOMS = {

    "Basement": [["Giant Crawler", "Old Key", "Chemical", "Saw"], [0, 15, 25, 25], True],

    "Car": [["Snake", "Map", "Phone", "Gas Bottle"], [0, 20, 15, 20], True],

    "Swamp": [["Crocodile", "Fishing Net", "Fish", "Emergency Kit"], [0, 12, 8, 10], True],

    "Haunted House": [["Mad Man", "Screwdriver", "Knife", "Handcuffs"], [0, 15, 31, 20], True],

}


ROOM_DESCRIPTIONS = {

    "Basement": """

  (     )

(       )

(        )

  |   |

  |   |

___________

/ __________ \\

/ __________ \\

\\  _________  /

-------------

You find yourself in a dark, damp basement.

The walls are covered in moss, and a foul smell fills the air.

Shadows move strangely across the walls.

You have found!

""",

    "Car": """


You approach a broken-down car, rusted and abandoned.

The engine is cold and the windows are shattered.

You have found!

""",

    "Swamp": """

You step into a murky swamp.

The water is thick with mud and plants, the air is humid.

Strange noises echo across the water.

You have found!

""",

    "Haunted House": """

You enter a creepy, abandoned house.

The wooden floors creak under your weight, and dust covers every surface.

A chill runs down your spine as you move inside.

You have found!

"""

}


# -------------------------

# Utility Functions

# -------------------------

def print_delay(message, delay=2):

    """Print a message with a delay."""

    print(message)

    time.sleep(delay)


def random_choice(items):

    """Return a random item from a list."""

    return random.choice(items)


def draw_monster_once(flag):

    """Draw monster using turtle if it's the first time."""

    if flag[0] == 0:

        monster = turtle.Turtle()

        monster.speed(0)

        for _ in range(360):

            monster.forward(2)

            monster.left(1)

        turtle.done()

        flag[0] = 1


def print_weapons(w1, w2, w3):

    """Display current weapons."""

    print("-" * 50)

    print_delay(f"1- Stun Gun: {w1}\n2- Sword: {w2}\n3- Invisibility Cloak: {w3}\n")

    print("-" * 50)


def buy_weapon(money, weapons):

    """Allow the player to buy a weapon."""

    print("-" * 50)

    print_delay("Choose a weapon to buy ︻╦╤─ :\n")

    print("-" * 50)

    for i, key in enumerate(GAME_WEAPONS, 1):

        weapon = GAME_WEAPONS[key]

        print_delay(f"{i}- {weapon['name']}: ${weapon['price']} - {weapon['effect']}")

    print("-" * 50)


    while True:

        choice = input("Your choice: ").strip()

        mapping = {"1": "w1", "2": "w2", "3": "w3"}

        if choice in mapping and GAME_WEAPONS[mapping[choice]]["price"] <= money[0]:

            money[0] -= GAME_WEAPONS[mapping[choice]]["price"]

            weapons[int(choice) - 1] += 1

            break

        else:

            print_delay("You can't buy that weapon. Try again.\n")


def fight(monster, room, money, weapons, alive, first_time):

    """Handle combat with monsters."""

    if any(weapons):

        use_weapon(monster, room, weapons)

    elif money[0] >= 30:

        buy_weapon(money, weapons)

        use_weapon(monster, room, weapons)

    else:

        print_delay("Game over! You don't have weapons or money...\n")

        alive[0] = False


def use_weapon(monster, room, weapons):

    """Let player pick a weapon to use."""

    print_weapons(weapons[0], weapons[1], weapons[2])

    while True:

        choice = input("Enter weapon number: ").strip()

        if choice in ("1", "2", "3"):

            idx = int(choice) - 1

            if weapons[idx] > 0:

                weapons[idx] -= 1

                print_delay(f"You used your weapon against the {monster}!\n")

                if choice == "2":  # Sword kills permanently

                    ROOMS[room][0].remove(monster)

                    ROOMS[room][1].pop(0)

                    ROOMS[room][2] = False

                return

        print_delay("Invalid choice or no weapon left. Try again.")


def explore_room(room, money, treasure, alive, first_time, attempts):

    """Explore a chosen room."""

    if not ROOMS[room][0]:

        print_delay("* This room is empty! *")

        return False


    attempts[0] += 1

    thing = random_choice(ROOMS[room][0])

    print_delay(f"{ROOM_DESCRIPTIONS[room]} {thing}\n")


    if thing == ROOMS[room][0][0] and ROOMS[room][2]:  # Monster

        print_delay(f"A {thing} attacks!\n")

        draw_monster_once(first_time)

        fight(thing, room, money, my_weapons, alive, first_time)

    elif thing == "treasure":

        

        treasure[0] = True

    else:

        idx = ROOMS[room][0].index(thing)

        money[0] += ROOMS[room][1][idx]

        print(f"You found {thing} worth ${ROOMS[room][1][idx]}! Total: ${money[0]}")

        del ROOMS[room][0][idx]

        del ROOMS[room][1][idx]

    return treasure[0]


def choose_room(money, treasure, attempts, alive, first_time):

    """Main room selection loop."""

    while alive[0] and not treasure[0]:

        if attempts[0] == 3:

            random_room = random.choice(list(ROOMS.keys()))

            ROOMS[random_room][0].append("treasure")

        elif attempts[0] == 4:

            random_room = random.choice(list(ROOMS.keys()))

            ROOMS[random_room][0] = ["treasure"] * 4

            ROOMS[random_room][2] = False

        elif attempts[0] == 6:

            print_delay("Game over! You lost your strength.")

            alive[0] = False

            return


        print_delay(f"\nAttempt: {attempts[0]} | Money: ${money[0]}")

        print("Rooms:\n 1- Haunted House \n 2- Swamp \n 3- Car \n 4- Basement")

        choice = input("Choose a room (1-4): ").strip()


        mapping = {"1": "Haunted House", "2": "Swamp", "3": "Car", "4": "Basement"}

        if choice in mapping:

            if explore_room(mapping[choice], money, treasure, alive, first_time, attempts):

                return

        else:

            print_delay("Invalid choice. Try again.\n")


# -------------------------

# Game Loop

# -------------------------

play_again = "yes"

while play_again == "yes":

    my_weapons = [0, 0, 0]

    attempts = [1]

    money = [100]

    alive = [True]

    treasure = [False]

    first_time = [0]


    print_delay("You wake up in a jungle, trapped by electric wires!")

    print_delay("You must explore 5 rooms to find the treasure.")

    print_delay("If you lose all money, you perish.\n")


    choose_room(money, treasure, attempts, alive, first_time)


    while True:

        play_again = input("Play again? (yes/no): ").lower()

        if play_again in ("yes", "no"):

            break

        print_delay("Invalid choice.")