import math 
import random

def calculate_damage(attacker, defender, move):
    level = 50 
    level_calc = (2 * level) / 5 + 2
    ratio = attacker.attack / defender.defense
    base = ((level_calc * move['power'] * ratio) / 50) + 2

    variance = random.uniform(0.85, 1.0)
    
    crit = random.randint(1,24) == 1
    crit_damage =  1.5 if crit else 1.0
    total_damage = math.floor(base * variance * crit_damage)

    return max(1, total_damage), crit

def move_menu(pokemon):
    print(f"\nwhat move will {pokemon.name} use?")
    for i, move in enumerate(pokemon.moves):
        print(f"{i + 1}. {move['name']} (Power: {move['power']})")
    while True: 
        choice = input(">")
        if choice.isdigit() and 1 <= int(choice) <= len(pokemon.moves):
            return pokemon.moves[int(choice) - 1]
        else:
            print("Invalid choice. Choose a valid move.")

def followup_attack(attacker, defender, move):
    print(f"\n{attacker.name} is about to use {move['name']} on {defender.name}.")
    damage, crit = calculate_damage(attacker, defender, move)
    defender.take_damage(damage)

    if crit: 
        print("Critical hit!")
    print(f"It dealt {damage} damage.")

def battle(p1, p2):
    print(f"\n {p1.name} vs {p2.name}\n")
    turn = 1 

    while p1.is_alive() and p2.is_alive():
        print(f"\n Turn: {turn}")
        print(f"{p1.name}: {p1.hp}/{p1.max_hp} HP | {p2.name}: {p2.hp}/{p2.max_hp} HP")

        p1move= move_menu(p1)
    
        p2move= random.choice(p2.moves)

        if p1.speed > p2.speed: 
            first, f_move, second, s_move = p1, p1move, p2, p2move
        elif p2.speed > p1.speed:
            first, f_move, second, s_move = p2, p2move, p1, p1move
        else: 
            contestors  = [(p1, p1move), (p2, p2move)]
            random.shuffle(contestors)
            (first, f_move), (second, s_move) = contestors

        damage, crit = calculate_damage(first, second, f_move)
        second.take_damage(damage)
        print(f"\n{first.name} used {f_move['name']} on {second.name}.")
        followup_attack(first, second, f_move)
        
        if not second.is_alive():
            break 

        damage, crit = calculate_damage(second, first, s_move)
        first.take_damage(damage)
        print(f"\n{second.name} used {s_move['name']} it hit for {damage}!.")

        turn += 1
    winner = p1 if p1.is_alive() else p2
    print(f"\n{winner.name} wins the battle!")
