"""Data structures."""

import base64
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from datetime import timedelta
from fractions import Fraction
from typing import Any


@dataclass
class AmountRange:
    """Value range for an amount."""

    min: Fraction
    max: Fraction

    def __format__(self, format_spec: str) -> str:
        return format(self.min, format_spec) + "-" + format(self.max, format_spec)


@dataclass
class Ingredient:
    """Ingredient with name amount and unit."""

    name: str
    amount: Fraction | AmountRange | None = None
    unit: str | None = None
    optional: bool = False


@dataclass
class IngredientGroup:
    """Group of ingredients."""

    name: str
    ingredients: list[Ingredient] = field(default_factory=list)


@dataclass
class Value:
    """Value with unit."""

    value: Fraction
    unit: str


@dataclass
class Image:
    """Image data with format specifier."""

    fmt: str
    data: bytes

    def as_b64(self) -> str:
        return f"data:{self.fmt};base64,{base64.b64encode(self.data).decode()}"


@dataclass(frozen=True)
class ContentType:
    """Content type attached to a loaded recipe."""

    mime_type: str
    to_plain_text: Callable[[str], str]


PLAIN_TEXT = ContentType(mime_type="text/plain", to_plain_text=lambda s: s)


@dataclass
class Recipe:
    """Recipe."""

    title: str
    instruction: str
    instruction_content_type: ContentType = PLAIN_TEXT
    description: str | None = None
    amount: Fraction | None = None
    amount_unit: str | None = None
    preparation_time: timedelta | None = None
    cooking_time: timedelta | None = None
    cookware: list[str] = field(default_factory=list)
    image: Image | None = None
    source: str | None = None
    link: str | None = None
    ingredients: Sequence[Ingredient | IngredientGroup] = field(default_factory=list)
    nutrition_labels: dict[str, Value] = field(default_factory=dict)
    notes: str | None = None
    tags: dict[str, Any] = field(default_factory=dict)

    def all_ingredients(self) -> list[Ingredient]:
        return [
            i
            for group in self.ingredients
            for i in (
                group.ingredients if isinstance(group, IngredientGroup) else [group]
            )
        ]
