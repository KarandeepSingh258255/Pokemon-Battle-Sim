from dotenv import load_dotenv
from google import genai
import os
from rapidfuzz import process


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None


def ask_gemini(prompt):
    if not client:
        return "Gemini API key is missing. Add GEMINI_API_KEY to your .env file."

    try:
        interaction = client.interactions.create(
            model="gemini-3.5-flash",
            input=prompt,
            timeout=8,
        )
        return interaction.output_text
    except Exception as error:
        return f"Gemini request failed: {error}"


def fuzzy_guess(name, valid_names):
    match = process.extractOne(name.lower(), valid_names)

    if match and match[1] >= 80:
        return match[0]

    return None



def guess_pokemon_with_ai(user_input, possible_names):
    prompt = f"""
The user typed this Pokemon name or description: {user_input}

Choose the most likely intended Pokemon from this list:
{possible_names[:50]}

Return only the Pokemon name. No explanation.
"""
    return ask_gemini(prompt).strip().lower()


def get_strategy(battle_state):
    local_advice = get_local_strategy(battle_state)
    prompt = f"""
You are helping a player in a simple Pokemon battle simulator.

Battle state:
{battle_state}

Give strategy for the next turn only.
Keep it short.
Mention:
1. who is winning
2. which move the user should choose
3. why
"""
    gemini_advice = ask_gemini(prompt)

    if gemini_advice.startswith("Gemini "):
        return local_advice

    return gemini_advice


def get_local_strategy(battle_state):
    player = battle_state["your_pokemon"]
    opponent = battle_state["opponent"]
    player_hp_ratio = player["hp"] / player["max_hp"]
    opponent_hp_ratio = opponent["hp"] / opponent["max_hp"]
    best_move = max(player["moves"], key=lambda move: move["power"])

    if player_hp_ratio >= opponent_hp_ratio:
        status = "You are currently ahead."
    else:
        status = "You are currently behind."

    return (
        f"{status} Use {best_move['name']} because it has the highest "
        f"power available ({best_move['power']})."
    )


