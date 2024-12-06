"""Deserialize dicts only containing primitives."""

from collections.abc import Callable, Sequence
from datetime import timedelta
from fractions import Fraction
from typing import Any

from gorps.content_types import CONTENT_TYPES
from gorps.model import (
    AmountRange,
    ContentType,
    Image,
    Ingredient,
    IngredientGroup,
    Recipe,
    Value,
)


def deserialize_recipe(dct: dict[str, Any]) -> Recipe:
    """Deserialize a Recipe instance from a dict only containing primitive types."""
    return Recipe(**deserialize_recipe_args(dct))


def deserialize_recipe_args(dct: dict[str, Any]) -> dict[str, Any]:
    def deserialize_ingredient_groups(
        ingredients: Sequence[dict[str, Any]],
    ) -> Sequence[Ingredient | IngredientGroup]:
        return [parse_ingredient_group(ingredient) for ingredient in ingredients]

    def deserialize_nutrition_labels(
        nutrition_labels: dict[str, Any],
    ) -> dict[str, Value]:
        return {name: deserialize_value(val) for name, val in nutrition_labels.items()}

    try:
        return deserialize_optionals(
            dct,
            ingredients=deserialize_ingredient_groups,
            nutrition_labels=deserialize_nutrition_labels,
            image=lambda data: Image(**data),
            amount=Fraction,
            preparation_time=parse_timedelta,
            cooking_time=parse_timedelta,
            instruction_content_type=deserialize_content_type,
        )
    except AttributeError:
        raise ValueError(dct["title"]) from None


def deserialize_content_type(content_type: str) -> ContentType:
    try:
        return CONTENT_TYPES[content_type]
    except KeyError:
        msg = f"Invalid content type: {content_type}"
        raise ValueError(msg) from None


def deserialize_items(
    data: dict[str, Any], **items: Callable[[Any], Any]
) -> dict[str, Any]:
    return {**data, **{key: type_(data[key]) for key, type_ in items.items()}}


def deserialize_optionals(
    data: dict[str, Any], **items: Callable[[Any], Any]
) -> dict[str, Any]:
    return {
        **data,
        **{key: type_(data[key]) for key, type_ in items.items() if key in data},
    }


def parse_ingredient_group(obj: dict[str, Any]) -> Ingredient | IngredientGroup:
    if "ingredients" in obj:
        return IngredientGroup(
            **deserialize_items(
                obj, ingredients=lambda igts: [deserialize_ingredient(i) for i in igts]
            )
        )
    return deserialize_ingredient(obj)


def deserialize_ingredient(dct: dict[str, Any]) -> Ingredient:
    def deserialize_amount(amount: str | dict[str, Any]) -> Fraction | AmountRange:
        if isinstance(amount, dict):
            return deserialize_amount_range(amount)
        return Fraction(amount)

    return Ingredient(**deserialize_optionals(dct, amount=deserialize_amount))


def deserialize_amount_range(dct: dict[str, Any]) -> AmountRange:
    return AmountRange(**{key: Fraction(val) for key, val in dct.items()})


def deserialize_value(dct: dict[str, Any]) -> Value:
    return Value(**deserialize_items(dct, value=Fraction))


def parse_timedelta(s: str) -> timedelta:
    unit_args_by_suffix = {
        "sec": ("seconds",),
        "min": ("minutes", "seconds"),
        "h": ("hours", "minutes", "seconds"),
    }
    if " " in s:
        s, suffix = s.split(" ", 1)
        try:
            unit_args = unit_args_by_suffix[suffix]
        except KeyError:
            raise ValueError("Invalid timedelta unit: {suffix}") from None
    else:
        unit_args = None
    parts = s.split(":")
    if unit_args is None:
        if len(parts) != 3:  # noqa: PLR2004
            msg = f"Invalid timedelta: {s}. Either specify unit or use format ##:##:##"
            raise ValueError(msg)
        unit_args = unit_args_by_suffix["h"]
    if len(parts) > len(unit_args):
        msg = f"Invalid timedelta: {s}. Too many `:` for unit {suffix}"
        raise ValueError(msg)

    return timedelta(**dict(zip(unit_args, map(int, parts), strict=False)))
