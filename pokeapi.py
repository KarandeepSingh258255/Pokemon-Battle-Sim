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
        types = [type_info["type"]["name"] for type_info in data["types"]]
    except ValueError:
        return None

    hp = data["stats"][0]["base_stat"]
    attack = data["stats"][1]["base_stat"]
    defense = data["stats"][2]["base_stat"]
    speed = data["stats"][5]["base_stat"]

    moves = []
    for move_entry in data["moves"][:4]:
        move_name = move_entry["move"]["name"]
        move_url = move_entry["move"]["url"]

        try: 
            move_data = requests.get(move_url, timeout=10).json()
            power = move_data.get("power")
            accuracy = move_data.get("accuracy")
            pp = move_data.get("pp")
            priority = move_data.get("priority")
            move_type = move_data["type"]["name"]
            damage_class = move_data["damage_class"]["name"]
    
        except requests.RequestException:
            power = 10
            accuracy = 100
            pp = 10
            priority = 0
            move_type = "normal"
            damage_class = "physical"

        if power is None:
            power = 10

        if accuracy is None:
            accuracy = 100

        moves.append({
            "name": move_name,
            "power": power,
            "accuracy": accuracy,
            "pp": pp,
            "priority": priority,
            "type": move_type,
            "damage_class": damage_class
        })
    return Pokemon(
        data["name"],
        hp,
        attack,
        defense,
        speed,
        moves=moves,
        types=types
    )

    TYPE_EFFECTIVENESS = {
        "fire": {"water": 0.5, "grass": 2.0, "ice": 2.0, "bug": 2.0, "steel": 2.0, "dragon": 0.5},
        "water": {"fire": 2.0, "grass": 0.5, "ice": 2.0, "bug": 0.5, "steel": 2.0, "dragon": 0.5},
        "grass": {"fire": 0.5, "water": 2.0, "ice": 0.5, "bug": 0.5, "steel": 0.5, "dragon": 0.5},
        "ice": {"fire": 0.5, "water": 0.5, "grass": 2.0, "bug": 2.0, "steel": 1.0, "dragon": 2.0}
    }


    def get_type_multiplier(move_type, defender_types):
        mulitplier = 1

        for defender_type in defender_types:
            multiplier *= TYPE_EFFECTIVENESS.get(move_type, {}).get(defender_type, 1.0)

        return multiplier

def get_pokemon_names():
    url = "https://pokeapi.co/api/v2/pokemon?limit=2000"

    try: 
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return []
    
    data = response.json()
    return [pokemon["name"] for pokemon in data["results"]]

# fully implement the type advantages to fix the AI 