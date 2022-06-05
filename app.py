import statistics
from time import perf_counter

from guess import guess, Result, get_result
from histogram import histogram, show_bar_plot
from information import get_expected_information, get_histogram
from pokedex import get_pokemon, Pokemon
from utils import sort_dict_by_val, sort_dict_by_key


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
        expected_info[pokemon] = get_expected_information(pokemon, reduced_pokedex)

    if output:
        print_expected_information(sort_dict_by_val(expected_info, desc=False))

    return sort_dict_by_val(expected_info, desc=True)


def print_expected_information(expected_information: dict[Pokemon, float]):
    for pokemon, info in expected_information.items():
        print(f"{pokemon.name} ({pokemon.type1}, {pokemon.type2}): {info} bits")
    print()


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


def manual_guessing(pokedex):
    calculate_expected_information(pokedex)
    options_after_guess1 = process_guess_manually(
        "Simipour",
        get_result(0, False, False, -1, -1),
        pokedex
    )
    options_after_guess2 = process_guess_manually(
        "Rufflet",
        get_result(0, False, False, 1, 1),
        pokedex, options_after_guess1
    )
    options_after_guess3 = process_guess_manually(
        "Galarian Zapdos",
        get_result(0, False, False, 1, 1),
        pokedex, options_after_guess2
    )
    options_after_guess4 = process_guess_manually(
        "Runerigus",
        get_result(0, False, False, 1, 1),
        pokedex, options_after_guess3
    )
    options_after_guess5 = process_guess_manually(
        "Runerigus",
        get_result(0, False, False, 1, 1),
        pokedex, options_after_guess4
    )
    options_after_guess6 = process_guess_manually(
        "Runerigus",
        get_result(0, False, False, 1, 1),
        pokedex, options_after_guess5
    )


def do_guess(actual_pokemon, expected_information, options_after_guess):
    pokemon_guess, best_expected_info = list[tuple[Pokemon, float]](expected_information.items())[0]
    print(f"{pokemon_guess.name} ({pokemon_guess.type1}, {pokemon_guess.type2}): {best_expected_info} bits")
    result = guess(actual_pokemon, pokemon_guess)
    options_after_guess = determine_options_after_guess(pokemon_guess, result, options_after_guess)
    print(f"Result: {result}")
    print(f"{len(options_after_guess)} options left")
    expected_information = calculate_expected_information(options_after_guess)
    return options_after_guess, expected_information, result


def solver(actual_pokemon: Pokemon, pokedex: list[Pokemon],
           cached_initial_expected_information: dict[Pokemon, float] = None):
    if cached_initial_expected_information is None:
        expected_information = calculate_expected_information(pokedex)
    else:
        expected_information = cached_initial_expected_information
    options_after_guess = pokedex
    result = None
    i = 0
    while len(options_after_guess) > 0 and result != get_result(0, True, True, 0, 0):
        options_after_guess, expected_information, result = \
            do_guess(actual_pokemon, expected_information, options_after_guess)
        i += 1
    print(f"Final guess: {list(map(lambda x: x.name, options_after_guess))}")
    print(f"Actual pokemon: {actual_pokemon.name}")
    return i


def main():
    pokedex = get_pokemon()
    # get_histograms(pokedex)
    # get_stats(pokedex, lambda elem: elem.height)
    # get_stats(pokedex, lambda elem: elem.weight)
    # manual_guessing(pokedex)
    initial_expected_information = calculate_expected_information(pokedex)
    hist: dict[int, int] = {}

    tic = perf_counter()

    for i in range(0, 1050):
        # n = randrange(0, 1050)
        print(i)
        iterations = solver(pokedex[i], pokedex, cached_initial_expected_information=initial_expected_information)
        count = hist.get(iterations) or 0
        hist[iterations] = count + 1
        print()
    sorted_hist = dict(map(lambda item: (str(item[0]), item[1]), sort_dict_by_key(hist, desc=False).items()))
    show_bar_plot(sorted_hist, "Number of guesses", "Number of guesses", "Number of pokemon")
    print(sorted_hist)
    toc = perf_counter()
    print(f"Average time to solve: {(toc - tic)/1050.0:0.4f} seconds")


if __name__ == '__main__':
    main()
