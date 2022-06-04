import json
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class Type(Enum):
    NORMAL = "Normal"
    FIRE = "Fire"
    WATER = "Water"
    GRASS = "Grass"
    ELECTRIC = "Electric"
    ICE = "Ice"
    FIGHTING = "Fighting"
    POISON = "Poison"
    GROUND = "Ground"
    FLYING = "Flying"
    PSYCHIC = "Psychic"
    BUG = "Bug"
    ROCK = "Rock"
    GHOST = "Ghost"
    DARK = "Dark"
    DRAGON = "Dragon"
    STEEL = "Steel"
    FAIRY = "Fairy"
    NONE = ""


@dataclass(frozen=True)
class Pokemon:
    name: str
    gen: int
    type1: Type
    type2: Type
    height: Decimal
    weight: Decimal


def _get_pokemon(name: str, data: list):
    return Pokemon(name, data[0], data[1], data[2], Decimal(str(data[3])), Decimal(str(data[4])))


def get_pokemon(name=None):
    with open('pokedex.json', "r") as pokedex_file:
        pokedex: dict[str, list] = json.load(pokedex_file)
        if name is None:
            pokemon_list: list[Pokemon] = []
            for name, data in pokedex.items():
                pokemon_list.append(_get_pokemon(name, data))
            return pokemon_list
        else:
            return _get_pokemon(name, pokedex[name])
