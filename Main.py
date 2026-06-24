from pokeapi import get_pokemon
from battle import battle

name1 = input("Pokemon 1: ").strip()
name2 = input("Pokemon 2: ").strip()

if not name1 or not name2:
    print("Please enter two Pokemon names.")
else:
    pokemon1 = get_pokemon(name1)
    pokemon2 = get_pokemon(name2)

    if not pokemon1 or not pokemon2:
        print("Pokemon not found.")
    else:
        print("\nLoaded Pokemon:")
        print(
            pokemon1.name,
            pokemon1.hp,
            pokemon1.attack,
            pokemon1.defense,
            pokemon1.speed
        )

        print(
            pokemon2.name,
            pokemon2.hp,
            pokemon2.attack,
            pokemon2.defense,
            pokemon2.speed
        )

        battle(pokemon1, pokemon2)
