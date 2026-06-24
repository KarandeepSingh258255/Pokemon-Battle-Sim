def calculate_damage(attacker, defender):
    damage = attacker.attack - (defender.defense // 2)

    return max(1, damage)

def battle(p1, p2):

    if p1.speed >= p2.speed:
        first = p1
        second = p2
    else:
        first = p2
        second = p1

    print(f"\n{p1.name} VS {p2.name}\n")

    turn = 1

    while p1.is_alive() and p2.is_alive():

        print(f"Turn {turn}")

        damage = calculate_damage(first, second)
        second.take_damage(damage)

        print(
            f"{first.name} attacks "
            f"{second.name} for {damage}"
        )

        if not second.is_alive():
            break

        damage = calculate_damage(second, first)
        first.take_damage(damage)

        print(
            f"{second.name} attacks "
            f"{first.name} for {damage}"
        )

        print(
            f"{first.name}: {first.hp} HP | "
            f"{second.name}: {second.hp} HP\n"
        )

        turn += 1

    winner = p1 if p1.is_alive() else p2

    print(f"\nWinner: {winner.name}")