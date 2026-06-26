from Pokemon import Pokemon

def test_damage_stops_zero():
    p = Pokemon("pikachu", 35, 55, 40, 90)
    p.take_damage(999)

    assert p.hp == 0
    assert p.is_alive() == False
