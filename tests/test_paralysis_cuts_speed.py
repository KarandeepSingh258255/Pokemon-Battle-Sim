from Pokemon import Pokemon
from battle import effective_speed

def test_paralysis_cuts_speed():
    p = Pokemon("pikachu", 35, 55, 40, 90)
    original_speed = p.speed

    p.set_status("paralyzed")

    assert effective_speed(p) == original_speed // 2
