from dotenv import load_dotenv
from google import genai
import os
from rapidfuzz import process
from pokeapi import get_type_multiplier


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = (
    genai.Client(api_key=api_key, http_options={"timeout": 8_000})
    if api_key
    else None
)


def ask_gemini(prompt):
    if not client:
        return "Gemini API key is missing. Add GEMINI_API_KEY to your .env file."

    if not api_key.startswith("AIza"):
        return "Gemini API key does not look valid. Create a Gemini API key in Google AI Studio."

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
Do not keep suggesting a status move if the opponent already has a status.
If multiple moves are similarly useful, vary the suggestion based on the turn.
"types": opponent.types
"""
    gemini_advice = ask_gemini(prompt)

    if gemini_advice.startswith("Gemini "):
        return local_advice

    return gemini_advice


def get_local_strategy(battle_state):
    player = battle_state["your_pokemon"]
    opponent = battle_state["opponent"]
    turn = battle_state.get("turn", 1)
    player_hp_ratio = player["hp"] / player["max_hp"]
    opponent_hp_ratio = opponent["hp"] / opponent["max_hp"]
   
    def score_move(move):
        power = move.get("power", 10)
        accuracy = move.get("accuracy", 100)
        priority = move.get("priority", 0)
        type_multiplier = get_type_multiplier(move.get("type"), opponent["types"])
        status_bonus = 0
        expected_damage = power * type_multiplier * (accuracy / 100)

        if not opponent.get("status") and opponent_hp_ratio > 0.5 and move.get("status") not in (None, "none"):
            status_bonus = min(25, move.get("status_chance", 0) * 0.25)

        if opponent_hp_ratio <= 0.3:
            status_bonus = 0

        return expected_damage + (priority * 10) + status_bonus

    def move_reason(move):
        type_multiplier = get_type_multiplier(move.get("type"), opponent["types"])

        if opponent_hp_ratio <= 0.3:
            return "the opponent is low, so damage matters most right now"

        if not opponent.get("status") and move.get("status") not in (None, "none"):
            return (
                f"it can cause {move['status']} and still does useful damage"
            )

        if type_multiplier > 1:
            return "it is strong against the opponent's type"

        return (
            f"it has {move['power']} power, {move['accuracy']} accuracy, "
            f"and {move['priority']} priority"
        )
    
    scored_moves = sorted(
        ((score_move(move), move) for move in player["moves"]),
        key=lambda item: item[0],
        reverse=True
    )
    best_score = scored_moves[0][0]
    close_moves = [
        move for score, move in scored_moves
        if best_score - score <= max(5, best_score * 0.15)
    ]
    best_move = close_moves[(turn - 1) % len(close_moves)]

    if player_hp_ratio >= opponent_hp_ratio:
        status = "You are currently ahead."
    else:
        status = "You are currently behind."

    status_note = ""
    if player.get("status"):
        status_note = f" Your Pokemon is {player['status']}, so be careful."
    elif opponent.get("status"):
        status_note = f" The opponent is {opponent['status']}, which helps you."

    move_status_note = ""
    if best_move.get("status") not in (None, "none") and move_reason(best_move).startswith("it can"):
        move_status_note = (
            f" It has a {best_move.get('status_chance', 0)}% chance "
            f"to cause {best_move['status']}."
        )

    return (
        f"{status}{status_note} Use {best_move['name']} because "
        f"{move_reason(best_move)}.{move_status_note}"
    )    
