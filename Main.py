from pokeapi import get_pokemon, get_pokemon_names
from battle import battle
from ai_helper import fuzzy_guess, guess_pokemon_with_ai

def load_pokemon(name, valid_names):
    pokemon = get_pokemon(name)

    if pokemon:
        return pokemon
    
    guessed_name = fuzzy_guess(name, valid_names)

    if not guessed_name and valid_names:
        guessed_name = guess_pokemon_with_ai(name, valid_names)

        if guessed_name:
            print(f"Using closest match: {guessed_name.title()}")
        return get_pokemon(guessed_name)

    return None

def main():
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
              "name: " + pokemon1.name,
                "hp: " + str(pokemon1.hp),
                "attack: " + str(pokemon1.attack),
                "defense: " + str(pokemon1.defense),
                "speed: " + str(pokemon1.speed)
            )

            print(
                "name: " + pokemon2.name,
                "hp: " + str(pokemon2.hp),
                "attack: " + str(pokemon2.attack),
                "defense: " + str(pokemon2.defense),
                "speed: " + str(pokemon2.speed)
            )

            battle(pokemon1, pokemon2)


if __name__ == "__main__":
    main()

