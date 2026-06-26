import Main


def test_invalid_pokemon_returns_none(monkeypatch):
    monkeypatch.setattr(Main, "get_pokemon", lambda name: None)
    monkeypatch.setattr(Main, "fuzzy_guess", lambda name, valid_names: None)
    monkeypatch.setattr(Main, "guess_pokemon_with_ai", lambda name, valid_names: None)

    result = Main.load_pokemon("notapokemon", ["pikachu"])

    assert result is None
