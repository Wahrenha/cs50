from project import drink_potion, player_action, battle, create_character
from classes import Potions, Character, Weapon
import pytest

character = Character("David", "Male", 40, "Warrior")
villain = Character("Xandao", "Male", 55, "Archer")

healing = Potions("Healing")
strength = Potions("Strength")
quickness = Potions("Quickness")
character.take_item(healing)
character.take_item(strength)
character.take_item(quickness)


def test_healing():
    assert drink_potion(character, healing) == "healing"

def test_strength():
    assert drink_potion(character, strength) == "strength"

def test_quickness():
    assert drink_potion(character, quickness) == "quickness"

def test_error():
    resistance = Potions("Resistance")
    with pytest.raises(ValueError):
        drink_potion(character, resistance) == "resistance"

def test_resistance():
    resistance = Potions("Resistance")
    character.take_item(resistance)
    drink_potion(character, resistance) == "resistance"



def test_attack():
    assert player_action(character, villain, "Attack") == "player attacked"

def test_run():
    assert player_action(character, villain, "Run") == True or  player_action(character, villain, "Run") == False




def main():

    test_healing()
    test_strength()
    test_quickness()
    test_error()
    test_resistance()

    test_attack()
    test_run()




if __name__ == "__main__":

    main()
