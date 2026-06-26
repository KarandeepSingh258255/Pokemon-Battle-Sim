import math
import random
from ai_helper import get_strategy
from pokeapi import get_type_multiplier

POTION_HEAL = 20
STARTING_POTIONS = 3
STATUS_NAMES = {
    "burn": "burned",
    "poison": "poisoned",
    "paralysis": "paralyzed",
    "sleep": "asleep",
    "freeze": "frozen",
}

def calculate_damage(attacker, defender, move):
    level = 50
    level_calc = (2 * level) / 5 + 2
    attack = attacker.attack
    if attacker.status == "burned" and move.get("damage_class") == "physical":
        attack = math.floor(attack / 2)

    ratio = attack / defender.defense
    base = ((level_calc * move["power"] * ratio) / 50) + 2

    variance = random.uniform(0.85, 1.0)
    crit = random.randint(1, 24) == 1
    crit_damage = 1.5 if crit else 1.0
    type_multiplier = get_type_multiplier(move["type"], defender.types)

    total_damage = math.floor(base * variance * crit_damage * type_multiplier)

    return max(1, total_damage), crit, type_multiplier

def player_turn_menu(pokemon, potions):
    print(f"\nwhat will {pokemon.name} do?")
    for i, move in enumerate(pokemon.moves):
        print(f"{i + 1}. {move['name']} (Power: {move['power']})")
    potion_choice = len(pokemon.moves) + 1
    print(f"{potion_choice}. Use potion ({potions} left)")

    while True: 
        choice = input(">")
        if choice.isdigit() and 1 <= int(choice) <= len(pokemon.moves):
            return "move", pokemon.moves[int(choice) - 1]
        if choice.isdigit() and int(choice) == potion_choice:
            if potions > 0:
                return "potion", None
            print("You do not have any potions left.")
            continue

        print("Invalid choice. Choose a valid option.")

def use_potion(pokemon):
    old_hp = pokemon.hp
    pokemon.heal(POTION_HEAL)
    healed = pokemon.hp - old_hp
    print(f"\n{pokemon.name} used a potion and healed {healed} HP.")

def status_label(pokemon):
    if pokemon.status:
        return f" [{pokemon.status}]"

    return ""

def effective_speed(pokemon):
    if pokemon.status == "paralyzed":
        return math.floor(pokemon.speed / 2)

    return pokemon.speed

def can_move(pokemon):
    if pokemon.status == "asleep":
        if pokemon.sleep_turns > 0:
            pokemon.sleep_turns -= 1
            print(f"\n{pokemon.name} is asleep and cannot move.")
            return False

        pokemon.status = None
        print(f"\n{pokemon.name} woke up.")

    if pokemon.status == "frozen":
        if random.randint(1, 5) == 1:
            pokemon.status = None
            print(f"\n{pokemon.name} thawed out.")
        else:
            print(f"\n{pokemon.name} is frozen and cannot move.")
            return False

    if pokemon.status == "paralyzed" and random.randint(1, 4) == 1:
        print(f"\n{pokemon.name} is paralyzed and cannot move.")
        return False

    return True

def try_apply_status(move, defender):
    status = STATUS_NAMES.get(move.get("status"))
    status_chance = move.get("status_chance", 0)

    if not status or defender.status or status_chance <= 0:
        return

    if random.randint(1, 100) <= status_chance and defender.set_status(status):
        print(f"{defender.name} is now {status}.")

def use_move(attacker, defender, move):
    if not can_move(attacker):
        return

    damage, crit, type_multiplier = calculate_damage(attacker, defender, move)
    defender.take_damage(damage)

    print(f"\n{attacker.name} used {move['name']} on {defender.name}.")
    if crit:
        print("Critical hit!")
    print(f"It dealt {damage} damage.")

    if defender.is_alive():
        try_apply_status(move, defender)

def apply_end_turn_status(pokemon):
    if not pokemon.is_alive():
        return

    if pokemon.status == "poisoned":
        damage = max(1, math.floor(pokemon.max_hp / 8))
        pokemon.take_damage(damage)
        print(f"{pokemon.name} took {damage} poison damage.")
    elif pokemon.status == "burned":
        damage = max(1, math.floor(pokemon.max_hp / 16))
        pokemon.take_damage(damage)
        print(f"{pokemon.name} took {damage} burn damage.")

def followup_attack(attacker, defender, move):
    print(f"\n{attacker.name} is about to use {move['name']} on {defender.name}.")
    damage, crit, type_multiplier = calculate_damage(attacker, defender, move)    
    defender.take_damage(damage)

    if crit: 
        print("Critical hit!")
    print(f"It dealt {damage} damage.")


def show_strategy(turn, player, opponent):
    battle_state = {
        "turn": turn,
        "your_pokemon": {
            "name": player.name,
            "hp": player.hp,
            "max_hp": player.max_hp,
            "attack": player.attack,
            "defense": player.defense,
            "speed": player.speed,
            "moves": player.moves,
            "types": player.types,
            "status": player.status,
        },
        "opponent": {
            "name": opponent.name,
            "hp": opponent.hp,
            "max_hp": opponent.max_hp,
            "attack": opponent.attack,
            "defense": opponent.defense,
            "speed": opponent.speed,
            "moves": opponent.moves,
            "types": opponent.types,
            "status": opponent.status,
        },
    }

    try:
        print("\nStrategy:")
        print(get_strategy(battle_state))
    except Exception as error:
        print(f"\nStrategy unavailable: {error}")

def battle(p1, p2):
    print(f"\n {p1.name} vs {p2.name}\n")
    turn = 1 
    p1_potions = STARTING_POTIONS
    p2_potions = STARTING_POTIONS

    while p1.is_alive() and p2.is_alive():
        print(f"\n Turn: {turn}")
        print(
            f"{p1.name}: {p1.hp}/{p1.max_hp} HP{status_label(p1)} | "
            f"{p2.name}: {p2.hp}/{p2.max_hp} HP{status_label(p2)}"
        )
        print(f"Potions: {p1.name} {p1_potions} | {p2.name} {p2_potions}")

        show_strategy(turn, p1, p2)

        p1_action, p1move = player_turn_menu(p1, p1_potions)

        if p2_potions > 0 and p2.hp <= p2.max_hp / 2:
            p2_action = "potion"
            p2move = None
        else:
            p2_action = "move"
            p2move = random.choice(p2.moves)

        if p1_action == "potion":
            use_potion(p1)
            p1_potions -= 1

        if p2_action == "potion":
            use_potion(p2)
            p2_potions -= 1

        if p1_action == "potion" and p2_action == "potion":
            apply_end_turn_status(p1)
            apply_end_turn_status(p2)
            turn += 1
            continue

        if p1_action == "potion":
            use_move(p2, p1, p2move)
            apply_end_turn_status(p1)
            apply_end_turn_status(p2)
            turn += 1
            continue

        if p2_action == "potion":
            use_move(p1, p2, p1move)
            apply_end_turn_status(p1)
            apply_end_turn_status(p2)
            turn += 1
            continue

        if effective_speed(p1) > effective_speed(p2): 
            first, f_move, second, s_move = p1, p1move, p2, p2move
        elif effective_speed(p2) > effective_speed(p1):
            first, f_move, second, s_move = p2, p2move, p1, p1move
        else: 
            contestors  = [(p1, p1move), (p2, p2move)]
            random.shuffle(contestors)
            (first, f_move), (second, s_move) = contestors

        use_move(first, second, f_move)
        
        if not second.is_alive():
            break 
        
        use_move(second, first, s_move)

        apply_end_turn_status(p1)
        apply_end_turn_status(p2)

        turn += 1
    winner = p1 if p1.is_alive() else p2
    print(f"\n{winner.name} wins the battle!")
