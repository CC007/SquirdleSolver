from typing import Any

import matplotlib.pyplot as plt

from pokedex import Pokemon
from utils import sort_dict_by_key


def histogram(
        pokemon: list[Pokemon],
        attr: str,
        sorting_func=sort_dict_by_key,
        desc=False,
        plot_width=10
):
    hist: dict[Any, int] = {}
    if attr == "type":
        _populate_histogram("type1", hist, pokemon)
        _populate_histogram("type2", hist, pokemon)
    else:
        _populate_histogram(attr, hist, pokemon)

    hist = sorting_func(hist, desc)
    # Dataset generation
    keys = list(map(lambda key: "Single-typed" if key == "" else key, hist.keys()))
    values = list(hist.values())
    plt.figure(figsize=(plot_width, 5))
    #  Bar plot
    plt.bar(keys, values, color='green',
            width=0.5)
    plt.xlabel(attr)
    plt.ylabel("No. of pokemon")
    plt.title("Histogram of pokemon per " + attr)
    plt.show()


def _populate_histogram(attr, hist, pokemon):
    for p in pokemon:
        attr_value: str = getattr(p, attr)
        count: int = hist.get(attr_value) or 0
        hist[attr_value] = count + 1
