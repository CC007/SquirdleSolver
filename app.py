import statistics

from guess import ValueResult, TypeResult
from information import expected_information, get_histogram
from pokedex import get_pokemon, Pokemon
from utils import sort_dict_by_val


def get_stats(pokedex, attr_mapper):
    data = list(map(attr_mapper, pokedex))
    print(statistics.mean(data))
    print(statistics.median(data))
    print(statistics.quantiles(data, n=3, method="inclusive"))


def calculate_expected_information(pokedex, reduced_pokedex=None):
    if reduced_pokedex == None:
        reduced_pokedex = pokedex

    expected_info: dict[Pokemon, float] = {}
    for pokemon in pokedex:
        expected_info[pokemon] = expected_information(pokemon, reduced_pokedex)
    sorted_expected_info = sort_dict_by_val(expected_info, desc=False)
    for pokemon, info in sorted_expected_info.items():
        print(pokemon.name + " (" + pokemon.type1 + ", " + pokemon.type2 + "): " + str(info) + " bits")


def take_a_guess(guess_name, guess_result, pokedex, options_after_previous_guess=None):
    if options_after_previous_guess == None:
        options_after_previous_guess = pokedex

    guess = get_pokemon(guess_name)
    print()
    print(guess)
    print()
    histogram_after_guess = get_histogram(guess, options_after_previous_guess)
    options_after_guess = histogram_after_guess[
        guess_result]
    calculate_expected_information(pokedex, options_after_guess)
    print()
    calculate_expected_information(options_after_guess)
    return options_after_guess


def get_result(gen: int, type1: bool, type2: bool, height: int, weight: int) -> tuple[ValueResult, TypeResult, TypeResult, ValueResult, ValueResult]:
    """Get the tuple of a result based on the enum values"""
    return ValueResult(gen), TypeResult(type1), TypeResult(type2), ValueResult(height), ValueResult(weight)


def main():
    pokedex = get_pokemon()
    # histogram(pokedex, "gen")
    # histogram(pokedex, "type", sort_dict_by_val, desc=True, plot_width=20)
    # histogram(pokedex, "height")
    # histogram(pokedex, "weight")
    # get_stats(pokedex, lambda elem: elem.height)
    # get_stats(pokedex, lambda elem: elem.weight)
    # calculate_expected_information(pokedex)
    options_after_guess1 = take_a_guess(
        "Simipour",
        get_result(0, False, False, -1, -1),
        pokedex
    )
    options_after_guess2 = take_a_guess(
        "Rufflet",
        get_result(0, False, False, 1, 1),
        pokedex, options_after_guess1
    )
    options_after_guess3 = take_a_guess(
        "Galarian Zapdos",
        get_result(0, False, False, 1, 1),
        pokedex, options_after_guess2
    )
    options_after_guess4 = take_a_guess(
        "Runerigus",
        get_result(0, False, False, 1, 1),
        pokedex, options_after_guess3
    )
    options_after_guess5 = take_a_guess(
        "Runerigus",
        get_result(0, False, False, 1, 1),
        pokedex, options_after_guess4
    )
    options_after_guess6 = take_a_guess(
        "Runerigus",
        get_result(0, False, False, 1, 1),
        pokedex, options_after_guess5
    )


if __name__ == '__main__':
    main()
