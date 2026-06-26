from Pokemon import Pokemon

def test_heal_max_hp():
    p = Pokemon("pikachu", 35, 55, 40, 90)
    p.take_damage(10)

    p.heal(20)

    assert p.hp == p.max_hp