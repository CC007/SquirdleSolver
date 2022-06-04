from decimal import Decimal
from enum import Enum
from typing import TypeAlias

from pokedex import Pokemon, Type


class ValueResult(Enum):
    HIGHER = 1
    EQUAL = 0
    LOWER = -1

    @staticmethod
    def compare(a: int | Decimal, b: int | Decimal):
        if a == b:
            return ValueResult.EQUAL
        elif a < b:
            return ValueResult.LOWER
        elif a > b:
            return ValueResult.HIGHER


class TypeResult(Enum):
    EQUAL = True
    NOT_EQUAL = False

    @staticmethod
    def compare(a: Type, b: Type):
        if a == b:
            return TypeResult.EQUAL
        else:
            return TypeResult.NOT_EQUAL


Result: TypeAlias = tuple[ValueResult, TypeResult, TypeResult, ValueResult, ValueResult]


def get_result(gen: int, type1: bool, type2: bool, height: int, weight: int) \
        -> tuple[ValueResult, TypeResult, TypeResult, ValueResult, ValueResult]:
    """Get the tuple of a result based on the enum values"""
    return ValueResult(gen), TypeResult(type1), TypeResult(type2), ValueResult(height), ValueResult(weight)


def get_possible_results() -> list[Result]:
    results = []
    for gen in ValueResult:
        for type1 in TypeResult:
            for type2 in TypeResult:
                for height in ValueResult:
                    for weight in ValueResult:
                        results.append((gen, type1, type2, height, weight))
    return results


def guess(actual_pokemon: Pokemon, guessed_pokemon: Pokemon) -> Result:
    return (
        ValueResult.compare(actual_pokemon.gen, guessed_pokemon.gen),
        TypeResult.compare(actual_pokemon.type1, guessed_pokemon.type1),
        TypeResult.compare(actual_pokemon.type2, guessed_pokemon.type2),
        ValueResult.compare(actual_pokemon.height, guessed_pokemon.height),
        ValueResult.compare(actual_pokemon.weight, guessed_pokemon.weight),
    )
