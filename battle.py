def calculate_damage(attacker, defender):
    damage = attacker.attack - (defender.defense // 2)

    if damage < 1:
        damage = 1

    return damage


def attack(attacker, defender):
    damage = calculate_damage(attacker, defender)

    defender.take_damage(damage)

    print(
        f"{attacker.name} attacks {defender.name} "
        f"for {damage} damage!"
    )

    print(f"{defender.name} HP: {defender.hp}\n")


def battle(pokemon1, pokemon2):
    print(f"\n{pokemon1.name} VS {pokemon2.name}\n")

    if pokemon1.speed >= pokemon2.speed:
        first = pokemon1
        second = pokemon2
    else:
        first = pokemon2
        second = pokemon1

    turn = 1

    while pokemon1.is_alive() and pokemon2.is_alive():

        print(f"--- Turn {turn} ---")

        attack(first, second)

        if not second.is_alive():
            break

        attack(second, first)

        turn += 1

    winner = pokemon1 if pokemon1.is_alive() else pokemon2

    print(f"{winner.name} wins!")