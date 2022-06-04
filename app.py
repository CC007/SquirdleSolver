import statistics

from guess import guess, Result
from histogram import histogram
from information import expected_information, get_histogram
from pokedex import get_pokemon, Pokemon
from utils import sort_dict_by_val


def get_histograms(pokedex):
    histogram(pokedex, "gen")
    histogram(pokedex, "type", sort_dict_by_val, desc=True, plot_width=20)
    histogram(pokedex, "height")
    histogram(pokedex, "weight")


def get_stats(pokedex, attr_mapper):
    data = list(map(attr_mapper, pokedex))
    print(statistics.mean(data))
    print(statistics.median(data))
    print(statistics.quantiles(data, n=3, method="inclusive"))


def calculate_expected_information(pokedex, reduced_pokedex=None, *, output=False) -> dict[Pokemon, float]:
    if reduced_pokedex is None:
        reduced_pokedex = pokedex

    expected_info: dict[Pokemon, float] = {}
    for pokemon in pokedex:
        expected_info[pokemon] = expected_information(pokemon, reduced_pokedex)

    if output:
        for pokemon, info in sort_dict_by_val(expected_info, desc=False).items():
            print(f"{pokemon.name} ({pokemon.type1}, {pokemon.type2}): {info} bits")
        print()

    return sort_dict_by_val(expected_info, desc=True)


def determine_options_after_guess(guess: Pokemon, guess_result: Result, options_after_previous_guess) -> list[Pokemon]:
    histogram_after_guess = get_histogram(guess, options_after_previous_guess)
    options_after_guess = histogram_after_guess[guess_result]
    return options_after_guess


def process_guess_manually(guess_name, guess_result, pokedex, options_after_previous_guess=None) -> list[Pokemon]:
    if options_after_previous_guess is None:
        options_after_previous_guess = pokedex

    guess = get_pokemon(guess_name)

    print(guess)
    print()
    options_after_guess = determine_options_after_guess(guess, guess_result, options_after_previous_guess)

    calculate_expected_information(pokedex, options_after_guess, output=True)
    calculate_expected_information(options_after_guess, output=True)
    return options_after_guess


def solver(actual_pokemon: Pokemon, pokedex: list[Pokemon],
           cached_initial_expected_information: dict[Pokemon, float] = None):
    if cached_initial_expected_information is None:
        pokemon_expected_information = calculate_expected_information(pokedex)
    else:
        pokemon_expected_information = cached_initial_expected_information
    pokemon_guess, best_expected_info = list[tuple[Pokemon, float]](pokemon_expected_information.items())[0]
    print(f"{pokemon_guess.name} ({pokemon_guess.type1}, {pokemon_guess.type2}): {best_expected_info} bits")
    result = guess(actual_pokemon, pokemon_guess)
    options_after_guess = determine_options_after_guess(pokemon_guess, result, pokedex)
    print(f"{len(options_after_guess)} options left")
    while len(options_after_guess) > 1:
        pokemon_expected_information = calculate_expected_information(pokedex, options_after_guess)
        pokemon_guess, best_expected_info = list[tuple[Pokemon, float]](pokemon_expected_information.items())[0]
        print(f"{pokemon_guess.name} ({pokemon_guess.type1}, {pokemon_guess.type2}): {best_expected_info} bits")
        if best_expected_info == 0.0:
            print(f"Pokemon left: {options_after_guess}")
            print(f"Actual pokemon: {actual_pokemon.name}")
            exit(1)
            break
        result = guess(actual_pokemon, pokemon_guess)
        options_after_guess = determine_options_after_guess(pokemon_guess, result, options_after_guess)
        print(f"{len(options_after_guess)} options left")
    print(f"Final guess: {options_after_guess[0].name}")
    print(f"Actual pokemon: {actual_pokemon.name}")


def main():
    pokedex = get_pokemon()
    # get_histograms(pokedex)
    # get_stats(pokedex, lambda elem: elem.height)
    # get_stats(pokedex, lambda elem: elem.weight)
    # calculate_expected_information(pokedex)
    # options_after_guess1 = process_guess_manually(
    #     "Simipour",
    #     get_result(0, False, False, -1, -1),
    #     pokedex
    # )
    # options_after_guess2 = process_guess_manually(
    #     "Rufflet",
    #     get_result(0, False, False, 1, 1),
    #     pokedex, options_after_guess1
    # )
    # options_after_guess3 = process_guess_manually(
    #     "Galarian Zapdos",
    #     get_result(0, False, False, 1, 1),
    #     pokedex, options_after_guess2
    # )
    # options_after_guess4 = process_guess_manually(
    #     "Runerigus",
    #     get_result(0, False, False, 1, 1),
    #     pokedex, options_after_guess3
    # )
    # options_after_guess5 = process_guess_manually(
    #     "Runerigus",
    #     get_result(0, False, False, 1, 1),
    #     pokedex, options_after_guess4
    # )
    # options_after_guess6 = process_guess_manually(
    #     "Runerigus",
    #     get_result(0, False, False, 1, 1),
    #     pokedex, options_after_guess5
    # )
    initial_expected_information = calculate_expected_information(pokedex)

    for i in range(375, 1050):
        # n = randrange(0, 1050)
        print(i)
        solver(pokedex[i], pokedex, cached_initial_expected_information=initial_expected_information)
        print()


if __name__ == '__main__':
    main()
