
# rpg pequeno, com batalhas, dados para definir a sorte, criação de personagem (classe personagem), opcoes de ações para o jogador, etc
#vai precisar do random, talvez pygame?, inflect, sys, Image, fpdf, re, requests, etc
#historia?
#classes de personagens(mago, arqueiro), cada uma com danos diferentes vidas diferentes
#classes: arqueiro, mago, guerreiro, ogro, ladrao
from classes import Dice, Weapon, Potions, Classe, Character, Choice, print_slow, unlister
from time import sleep
import sys
import random
import re


def drink_potion(character : Character,potion : Potions):

#   Checking if the character has the refered potion, and gets the index of the potion in the inventory

    if not potion in character.inventory["Potions"]:
        raise ValueError(f"\n{character.name} does not have {potion}")
    index = character.inventory["Potions"].index(potion)
    if not type(potion) == Potions:
        return False
#   Checks the potion type, to perform the effect
    match potion._type:

        case "Healing":
            character.heal(potion.effect)
            potion_drank = "healing"

        case "Strength":
            character.stats["strength"] += potion.effect
            print(character.stats["strength"])
            potion_drank = "strength"

        case "Quickness":
            character.stats["agility"] += potion.effect
            potion_drank = "quickness"

        case "Resistance":
            character.stats["resistance"] += potion.effect
            potion_drank = "resistance"

    print_slow(f"\n{character.name} took {potion} Potion")

#   Takes the potion out of the character's inventory

    character.inventory["Potions"][index] = None
    return potion_drank


#Setting do and choice to None, so the function can be easily tested, by calling the function with the choices
def player_action(player, villain, choice=None, do = None, choice_2 = None):

    d10 = Dice(10)
#   The player has the choices of Attack, open inventory and run
#   If player opens inventory, player can drink potion, or go back

    while True:
        choice_2 = None
        if not choice:
            choice = Choice("What will you do?", "Attack", "Open Inventory", "Run")

        match choice:

#   If the player chose to attack, the attack method will be called

            case "Attack":
                player.attack(villain)
                action = "player attacked"
                break

#   If the player chose to run, the player has a 1 in 10 chance to suceed

            case "Run":

                if d10.roll() == 3 or d10.roll() == 5:
                    print_slow("\nYou ran away")
                    return True

                else:
                    action = False
                    choice = None
                    print_slow("\nYou tried to run away, but failed.")
                    break


#   If the player chose to open the inventory, the inventory will be printed

            case "Open Inventory":
                player.print_inventory()

#   Now, the player can choose between drinking a potion or going back
                if not do:
                    do = Choice("What will you do?", "Drink Potion", "Go Back")

                match do:

#   If the player chose to drink a potion, if the player has any potions, they will have to choose which potion to drink
                    case "Drink Potion":

                        action = "Player tried to drink potion"
                        if len(player.inventory["Potions"]) > 0:
                            if len(player.inventory["Potions"]) > 1:
                                if not choice_2:
                                    choice_2 = Choice("What potion do you want?",*player.inventory["Potions"], "Go Back")
                                    if choice_2 == "Go Back":
                                        choice = None
                                        do = None
                                        action = "Go Back"
                                        continue
                                index = player.inventory["Potions"].index(choice_2)
                            else:
                                index = 0

                            if drink_potion(player, player.inventory["Potions"][index]) == False:
                                print_slow("\nYou do not have any potions")
                                continue
                            break
                        else:
                            print_slow("\nYou do not have any potions\n")
                            choice = None
                            do = None
                            action = "Go Back"
                            continue

#   If player chose to go back, the player's action will not be over yet, and he will go back to initial choice
                    case "Go Back":
                        choice = None
                        do = None
                        action = "Go Back"
                        continue
    return action


def battle(player, villain, xp, first = None, action=None):

    run = False

#   The battle lasts while the player and oponnent are alive,
#   and first it is set who attacks first, according to agility

    while player.hp > 0 and villain.hp > 0 and not run:
        if not first:
            if player.stats["agility"] < villain.stats["agility"]:
                first = "villain"
            elif player.stats["agility"] >= villain.stats["agility"]:
                first = "player"

        if first == "villain":
            villain.attack(player)
            if player.hp <= 0:
                break
            elif not action:
                if player_action(player, villain) == True:
                    run = True
            else:
                action

        elif first == "player":
            if not action:
                if player.hp <= 0:
                    break
                elif player_action(player, villain) == True:
                    run = True
            else:
                action
            villain.attack(player)

    if player.hp <= 0:
        sys.exit()
    elif villain.hp < 0:
        player.get_xp(xp)
        return "Villain Died"
    else:
        return "Ran away"


def create_character(name = None, gender = None, age = None, classe = None):

    #print_slow("Hello traveler, it is quite uncommon to see someone wandering around here...\n\n\n")

    while True:
        try:

#   Getting the name of the character, the name must have only letters, and it is optional to have two names
#   Those conditions are secured by the re.search use
            if not name:
                print("\n")
                print("\n")
                name = input("Hello prisioner, what's your name? ").strip().title()
                print("\n")
                _name  = re.search(r"([A-Z]{1}[a-z]+(?: [A-Z]{1}[a-z]+)?)", name)
                if not name == _name.group(1):
                    raise ValueError
                break

            else:
                break
        except (ValueError, AttributeError):
            print_slow("That does not seem to be a name \n\n")
            name = ""
            continue



    while True:
        try:

#   Then, the function gets the gender, which must be chosen by typing the number according to the option:
#   Type 1 for Male, and 2 for Female
            if not gender:
                #sleep(0.5)
                 #print_slow(f"It is certainly a pleasure to meet you, {name}. To proceed, we will need some more information... So,\n")
                #sleep(0.5)
                gender = int(input("\nWhat's your gender?\n[1] Male\n[2] Female\n"))
                sleep(0.5)
                if gender > 2 or gender < 1:
                    raise ValueError
                match gender:
                    case 1:
                        _gender = "Male"
                    case 2:
                        _gender = "Female"
                break
            else:
                _gender = gender
                break
        except (ValueError, TypeError):
            print("\n\nThat does not seem to be a valid gender (Type the number equivalent to your gender)")

    while True:
        try:

#   Now setting the age, only ages between 10 and 80 are accepted
          if not age:
                sleep(0.5)
                age = int(input("\nWhat's your age? "))
                sleep(0.5)
                print("\n")
                if age < 10 or age > 80:
                    raise ValueError
                break
          else:
              break

        except:
            print("I'm sorry, but that does not seem to be your age")
            continue

    while True:


#   Finally setting the class of the character, the player must choose between the existant classes
        if not classe:
            sleep(0.5)
            classe = Choice("To what class do you belong prisioner?", "Archer", "Wizard", "Warrior", "Ogre", "Thief")
            sleep(0.5)
            classe_chosen = Classe(classe)
            print(f"\n{classe_chosen.properties(classe)}")
            sleep(1)
            take = Choice("\nAre you sure?", "Yes", "No")
            if take == "Yes":
                _classe = classe
                break
            else:
                continue
        else:
            _classe = classe
            break

# Setting the player according to the info collected, and returning it

    player = Character(name, _gender, age, _classe)
    return player

def chest(player):
    items = [Weapon("Sword"), Weapon("Fireball Scroll"), Weapon("Mace"), Weapon("Knife"), Weapon("Bow"), Potions("Resistance"), Potions("Strength"), Potions("Quickness"), Potions("Healing")]
    itens = items
    content = []
    for i in range(3):
        number = random.randint(1,len(itens))
        number -= 1
        content.append(itens[number])
        num = itens.index(itens[number])
        itens.pop(num)
    a = unlister(content).strip("[],")

    l = 0
    item_show = Choice("CHEST CONTENT:", content[0], content[1], content[2],  "leave chest")
    while True:


        if item_show == "leave chest":
            break

        sleep(0.5)
        print("\n", item_show.properties())
        sleep(1)

        take = Choice("\nWill you take it?", "Yes", "No")
        if take == "Yes":
            player.take_item(item_show)
            i = content.index(item_show)
            content.pop(i)
            l += 1

            if l == 1:
                item_show = Choice("CHEST CONTENT:", content[0], content[1], "leave chest")
            if l == 2:
                item_show = Choice("CHEST CONTENT:", content[0], "leave chest")
            if l == 3:
                break

        else:
            continue

    coins = random.randint(10,100)
    coins = str(coins)
    player.take_item(f"{coins} coins")

def story_1():
    print_slow("A long, long time ago, when the countries were not yet formed, and the nations as we know today didn't even exist, the world was composed of small villages and reigns. The Kingdom of the East was one of the most prominent in the continent, being ruled by the ruthless and brilliant mind of King Jordan, who expanded his kingdom to many lengths.")
    print_slow("\n\nAlthough King Jordan had plenty success with his plans of domination and expansion, he had a big amount of enemies, people who were seeking to overthrow him at all costs. \n\nKing Jordan started to become paranoid of such actions, and took immediate caution to arrest those involved.")
    print_slow("\n\nHowever, not all of those arrested had something to do with the threats of coups, and lots of inocent people and political enemies were inprisioned as well.")
    print_slow('\n\nAlongside some friends, you, a villager with much more knowledge of combat than the usual citizen of the kingdom, found yourself in one of those prisons, sentenced unfairly to treason, for simply trying to protect a friend who was being arrested.')
    print_slow('\n\nYou wait in what seems like an infinite line to the much awaited day of working outside, when you finally reach the guard.')
    player = create_character()
    return player

def story_2(player):
    print_slow("\n\nJust as expected, there it is. The knife you bought from the prision's dealer was outside in the hidden spot he chose.")
    knife = Weapon("Knife")
    player.take_item(knife)
    print_slow("\n\nAs you leave the building to the fenced area outside, you spot a breach. A hole in the fence, in a part which was only being watched by one single guard. And the perfect chance to take him out.")
    print_slow("\n\nYou approach the guard, with your knife at your back, pretending to look for information, and jump him.")
    guard = Character("guard", "Male", 40, "Thief")
    battle(player, guard, 50, first = "player")
    print_slow("\nAfter taking the guard out, you run without looking backwards, as fast as you can towards a forest nearby. The large amount of trees seems to hide you well and there you find a small cabin in the wild.")
    print_slow("\n\nYou try to look inside, but there is nothing to see. You turn around feeling defeated, and hear a sound in a busch by the side of the house.")
    print_slow("\n\nAn old man walks out of the trees, with what seems like a fascinated look to your face, an open mouth and a huge knife in his hands.")
    sleep(2)
    print_slow("\n\nWhat? A prisioner??\nCome in fast, don't let them see ya.")
    sleep(2)
    print_slow("\n\nYou enter the cabin, it is small but very comfortable. There is a bed with a large chest on its side and what seems to be a kitchen in the other side of the room.")
    print_slow("\n\nHave a look in the chest, there might be something to help you, and then sit down so I can give you a healing potion. You look rough.")
    chest(player)
    print_slow("\n\nHere, take the healing potion.")
    healing = Potions("Healing")
    player.take_item(healing)
    drink_potion(player, healing)
    print_slow("\n\nNow leave. You shouldn't be here, do not tell anyone about this. You should head north where you will find the headquarters of the resistance army. Good luck!")
    sleep(1)

def story_3(player):
    print_slow("\n\nYou leave the cabin and start heading north, feeling restored with the help of the old man and decided to fight the king with everything you got.")
    print_slow("\nThe forest is not an easy path and the trees hold you back along the way. \nSuddenly you hear some noise in the back.")
    bandit = Character("Bandit", "Male", 25, "Thief")
    knife = Weapon("Knife")
    bandit.take_item(knife)
    battle(player, bandit, 300)
    

def main():

    player = Character("Vi", "Female", 23, "Wizard")
    #story_1()
    story_2(player)
    story_3(player)

if __name__ == "__main__":
    main()


# / historia/ caminhos/ viloes/ quando derrotar o vilao pegar a arma dele/
# Comercio/ mostrar caracteristicas das classes e armas na hora de pegar/ armadura
