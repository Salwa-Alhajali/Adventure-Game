import random
import time
import turtle


game_weapon = {  # *
    "w1": {"name": "Stun Gun", "price": 30, "effect": "Temporarily incapacitates a monster (one use)"},
    "w2": {"name": "Sword", "price": 100, "effect": "Kills the monster permanently (one use)"},
    "w3": {"name": "Invisibility Cloak", "price": 40, "effect": "Avoid the monster completely (two uses)"}
}

my_weapon = [0, 0, 0]

rooms = {  # *
    "Basement": [["Giant Crawler", "Old Key", "Chemical", "Saw"], [0, 15, 25, 25], True],
    "car": [["Snake", "Map", "Phone", "Gas Bottle"], [0, 20, 15, 20], True],
    "Swamp": [["Crocodile", "Fishing Net", "Fish", "Emergency Kit"], [0, 12, 8, 10], True],
    "Haunted House": [["Mad Man", "Screwdriver", "Knife", "Handcuffs"], [0, 15, 31, 20], True]
}

basement = (  # *
    "\n  (     )\n(       )\n(        )\n  |   |\n  |   |\n___________\n"
    "/ __________ \\\n/ __________ \\\n\\  _________  /\n-------------\n"
    "You find yourself in a dark, damp basement.\nThe walls are covered in moss, "
    "and a foul smell fills the air.\nShadows move strangely across the walls.\nYou have found!"
)

car = (  # *
    "\n    ______\n  /|_||_\\`.__\n ( _    _ _\\\n =`-(_)--(_)-'\n"
    "You approach a broken-down car, rusted and abandoned.\nThe engine is cold and the windows are shattered.\n"
    "The interior smells musty and the tires are flat.\nYou have found!"
)

swamp = (  # *
    "\n  ~~~~~~~~~~~~~~\n ~~~~~~~~~~~~~~~~\n  ~~~~~~~~~~~~~~\n   ~~~~~~~~~~~~\n"
    "    ~~~~~~~~~~\nYou step into a murky swamp.\nThe water is thick with mud and plants, "
    "and the air is humid.\nStrange noises echo across the water.\nYou have found!"
)

haunted_house = (  # *
    "\n  /\\\n /  \\\n/----\\\n| [] |\n|    |\n|____|\nYou enter a creepy, abandoned house.\n"
    "The wooden floors creak under your weight, and dust covers every surface.\n"
    "A chill runs down your spine as you move inside.\nYou have found!"
)


def Monster(only_One_Time):  # *
    """Draw monster with turtle if monster is Mad Man."""
    if only_One_Time[0] == 0:
        monsters = turtle.Turtle()
        monsters.pendown()
        monsters.speed(0)
        for _ in range(360):
            monsters.forward(2)
            monsters.left(1)
        monsters.penup()
        monsters.left(90)
        monsters.forward(130)
        monsters.left(-90)
        monsters.forward(20)
        monsters.pendown()
        monsters.width(20)
        monsters.forward(0.1)
        monsters.penup()
        monsters.backward(80)
        monsters.pendown()
        monsters.forward(0.1)
        monsters.penup()
        monsters.backward(10)
        monsters.left(-90)
        monsters.forward(40)
        monsters.pendown()
        monsters.width(10)
        for _ in range(180):
            monsters.color("red")
            monsters.forward(1.3)
            monsters.left(1)
        turtle.done()


def print_delay(message, delay=2):
    print(message)
    time.sleep(delay)


def room_not_empty(room, room_massage, money, hasTreasure, isAlive, only_One_Time, attempts):  # *
    if not rooms[room][0]:
        print_delay("* You cannot enter this room anymore! *")
        return False
    attempts[0] += 1
    check_monster(room, room_massage, money, hasTreasure, isAlive, only_One_Time)
    if hasTreasure[0]:
        return True


def print_use_weapon(my_weapon, num, monster, room):  # *
    if num == 1:
        my_weapon[1] -= 1
        print_delay(f"You used your weapon and successfully killed the {monster}!\n")
        del rooms[room][0][0]
        del rooms[room][1][0]
        rooms[room][2] = False
    else:
        my_weapon[num] -= 1
        print_delay(f"( -_•)╦̵̵̿╤─\nYou used your weapon and managed to stop the {monster}!")


def ihave_weapon(monster, room, my_weapon):
    print_weapons(my_weapon[0], my_weapon[1], my_weapon[2])
    while True:
        weapon = input("Enter your weapon choice:\n")
        if weapon == "1" and my_weapon[0] != 0:
            print_use_weapon(my_weapon, 0, monster, room)
            return
        elif weapon == "2" and my_weapon[1] != 0:
            print_use_weapon(my_weapon, 1, monster, room)
            return
        elif weapon == "3" and my_weapon[2] != 0:
            print_use_weapon(my_weapon, 2, monster, room)
            return
        else:
            print_delay("You don't have this weapon. Try another one...")


def random_choose(lst):
    return random.choice(lst)


def print_weapons(w1, w2, w3):
    print("-----------------------------------------------------------------------")
    print_delay(f"1-Stun Gun: {w1}\n2-Sword: {w2}\n3-Invisibility Cloak: {w3}\n")
    print("-----------------------------------------------------------------------")


def decrease_money(money, key, my_weapon):
    money[0] -= game_weapon[key]["price"]
    my_weapon[0] += 1
    return


def buy_weapon(money, my_weapon):  # *
    print("-----------------------------------------------------------------------")
    print_delay("Buy a weapon to defend yourself ︻╦╤─ :\n")
    print("-----------------------------------------------------------------------")
    for i, key in enumerate(game_weapon, 1):
        weapon = game_weapon[key]
        print_delay(f"{i}-{weapon['name']}: ${weapon['price']} - {weapon['effect']}")
    print("-----------------------------------------------------------------------")
    while True:
        choice = input("\nYou have to pay for a weapon:\n")
        if choice == "1" and game_weapon["w1"]["price"] <= money[0]:
            decrease_money(money, "w1", my_weapon)
            break
        elif choice == "2" and game_weapon["w2"]["price"] <= money[0]:
            decrease_money(money, "w2", my_weapon)
            break
        elif choice == "3" and game_weapon["w3"]["price"] <= money[0]:
            decrease_money(money, "w3", my_weapon)
            break
        else:
            print_delay("Try to buy another item. You cannot buy this one.\n")
            continue


def fight(monster, room, money, my_weapon, isAlive):
    if any(my_weapon):
        ihave_weapon(monster, room, my_weapon)
        return
    elif money[0] >= 30 and not any(my_weapon):
        buy_weapon(money, my_weapon)
        ihave_weapon(monster, room, my_weapon)
    else:
        print_delay("Game over! You don't have any weapon or money...\n")
        isAlive[0] = False
        return


def check_monster(room, room_massage, money, hasTreasure, isAlive, only_One_Time):  # *
    randomChoose = random_choose(rooms[room][0])
    print_delay(f"{room_massage} {randomChoose}\n")
    print("-" * 40)
    if randomChoose == rooms[room][0][0] and rooms[room][2]:
        print_delay(f"You encounter the {randomChoose}! Prepare to fight for your life!\n")
        Monster(only_One_Time)
        only_One_Time[0] = 1
        fight(randomChoose, room, money, my_weapon, isAlive)
    elif randomChoose == "treasure":
        print("    \\ | /    \n  --  *  --  \n    / | \\    \n     '      ")
        hasTreasure[0] = True
        return hasTreasure[0]
    else:
        index = rooms[room][0].index(randomChoose)
        money[0] += rooms[room][1][index]
        print(f"You found {randomChoose} worth ${rooms[room][1][index]}! Total money: ${money[0]}")
        del rooms[room][0][index]
        del rooms[room][1][index]
        return


def choose_room(money, hasTreasure, attempts, isAlive, only_One_Time):  # *
    while True:
        if not isAlive[0]:
            print_delay("GAME OVER! ☠︎︎")
            return
        if attempts[0] == 3:
            random_list = random.choice(["car", "Basement", "Haunted House", "Swamp"])
            rooms[random_list][0].append("treasure")
        elif attempts[0] == 4:
            random_list = random.choice(["car", "Basement", "Haunted House", "Swamp"])
            rooms[random_list][0].clear()
            for _ in range(4):
                rooms[random_list][0].append("treasure")
            rooms[random_list][2] = False
        elif attempts[0] == 6:
            print_delay("Game over, you lost your power !✘_ ✘\nYou have 5 chances to explore the rooms ")
            isAlive[0] = False
            return True
        print_delay("-" * 40)
        print_delay(f"\nYou are outside. Attempt number: {attempts[0]}  and your money: {money[0]}$")  # *
        print_delay("-" * 40)
        choose = input("Enter your choice \n1- Haunted House\n2- Swamp\n3- car\n4- Basement\n")
        if choose == "1":
            if room_not_empty("Haunted House", haunted_house, money, hasTreasure, isAlive, only_One_Time, attempts):
                return
            else:
                continue
        elif choose == "2":
            if room_not_empty("Swamp", swamp, money, hasTreasure, isAlive, only_One_Time, attempts):
                return
            else:
                continue
        elif choose == "3":
            if room_not_empty("car", car, money, hasTreasure, isAlive, only_One_Time, attempts):
                return
            else:
                continue
        elif choose == "4":
            if room_not_empty("Basement", basement, money, hasTreasure, isAlive, only_One_Time, attempts):
                return
            else:
                continue
        else:
            print_delay("\nInvalid choice. Please enter a valid room number.\n")


Again = "yes"
only_One_Time = [0]
while Again == "yes":
    attempts = [1]
    money = [100]
    isAlive = [True]
    hasTreasure = [False]
    choose = 1
    print_delay("You wake up in a dense jungle, kidnapped and trapped by electric wires!")
    print_delay("You have some money with you. If you lose it all, you will perish...")
    print_delay("You have 5 chances to explore the rooms and locate the hidden treasure...")
    print_delay("In front of you are 4 mysterious rooms. Choose wisely!")
    print_delay("The game has started... Good luck!\n")
    while isAlive[0] and not hasTreasure[0]:
        end_game = choose_room(money, hasTreasure, attempts, isAlive, only_One_Time)
        if hasTreasure[0] or end_game:
            while True:
                Again = input("if you want play again? enter yes or no ").lower()
                if Again == "yes":
                    hasTreasure[0] = True
                    break
                elif Again == "no":
                    choose = 0
                    print_delay("GOOD BYE..")
                    break
                else:
                    print_delay("Not a choice!")
