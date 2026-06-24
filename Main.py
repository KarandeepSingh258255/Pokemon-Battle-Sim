from pokeapi import get_pokemon, get_pokemon_names
from battle import battle
from ai_helper import fuzzy_guess, guess_pokemon_with_ai

def load_pokemon(name, valid_names):
    pokemon = get_pokemon(name)

    if pokemon:
        return pokemon
    
    guessed_name = fuzzy_guess(name, valid_pokemon_names)

    if not guessed_name and valid_pokemon_names:
        guessed_name = guess_pokemon_with_ai(name, valid_pokemon_names)

        if guessed_name:
            print(f"Using closest match: {guessed_name.title()}")
        return get_pokemon(guessed_name)

    return None

valid_pokemon_names = get_pokemon_names()

name1 = input("Pokemon 1: ").strip()
name2 = input("Pokemon 2: ").strip()

if not name1 or not name2:
    print("Please enter two Pokemon names.")
else:
    pokemon1 = load_pokemon(name1, valid_pokemon_names)
    pokemon2 = load_pokemon(name2, valid_pokemon_names)

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

