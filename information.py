from numpy import log2, sum

from guess import Result, guess
from pokedex import Pokemon


def get_expected_information(pokemon: Pokemon, pokedex: list[Pokemon]) -> float:
    """The sum for all x of the probability of x times the information of x
    x is a possible result for a guess, for instance: 🔼🟩🟥🔽🔽 (we'll assume that swap is not denoted and counts as a 🟥)
    The information of x is the binary log of 1 over the probability of x
    """
    probabilities = _get_probabilities(pokemon, pokedex)
    return sum(list(map(
        calculate_expected_information,
        probabilities.values()
    )))


def calculate_expected_information(probability: float) -> float:
    return 0.0 if probability == 0.0 else probability * -log2(probability)


def _get_probabilities(pokemon: Pokemon, pokedex: list[Pokemon]) -> dict[Result, float]:
    histogram = get_histogram(pokemon, pokedex)
    return dict(map(lambda v: (v[0], float(len(v[1])) / len(pokedex)), histogram.items()))


def get_histogram(pokemon: Pokemon, pokedex: list[Pokemon]) -> dict[Result, list[Pokemon]]:
    histogram_pokemon: dict[Result, list[Pokemon]] = {}
    for actual_pokemon in pokedex:
        result = guess(actual_pokemon, pokemon)
        bucket = histogram_pokemon.get(result) or []
        bucket.append(actual_pokemon)
        histogram_pokemon[result] = bucket
    return histogram_pokemon
