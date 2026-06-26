from Pokemon import Pokemon
from battle import apply_end_turn_status

def test_poison_damages_pokemon():
    p = Pokemon("bulbasaur", 45, 49, 49, 65)
    p.set_status("poisoned")
    hp_before = p.hp

    apply_end_turn_status(p)

    assert p.hp < hp_before