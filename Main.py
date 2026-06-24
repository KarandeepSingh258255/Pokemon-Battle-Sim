from pokemon import Pokemon
from battle import battle

pikachu = Pokemon(
    "Pikachu",
    hp=100,
    attack=25,
    defense=10,
    speed=30
)

charizard = Pokemon(
    "Charizard",
    hp=120,
    attack=30,
    defense=15,
    speed=20
)

battle(pikachu, charizard)