import requests
from Pokemon import Pokemon

def get_pokemon(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name.strip().lower()}"

    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException:
        return None

    if response.status_code != 200:
        return None

    try:
        data = response.json()
    except ValueError:
        return None

    hp = data["stats"][0]["base_stat"]
    attack = data["stats"][1]["base_stat"]
    defense = data["stats"][2]["base_stat"]
    speed = data["stats"][5]["base_stat"]

    return Pokemon(
        data["name"],
        hp,
        attack,
        defense,
        speed
    )
