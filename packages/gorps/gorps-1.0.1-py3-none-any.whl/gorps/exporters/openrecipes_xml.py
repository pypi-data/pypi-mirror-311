"""Openrecipe xml export."""

from fractions import Fraction
from typing import IO
from xml.etree.ElementTree import Element, ElementTree, SubElement

from gorps.exporters.base import TextExporterBaseAtomic
from gorps.exporters.openrecipes import encode_img
from gorps.model import AmountRange, Ingredient, Recipe


class Exporter(TextExporterBaseAtomic):
    """OpenRecipes xml exporter."""

    name = "openrecipes-xml"
    ext = "openrecipes"

    def export_stream_single(self, recipe: Recipe, stream: IO[str]) -> None:
        root = Element("recipe")
        root.attrib.update(serialize_recipe(recipe))
        for ingredient in recipe.all_ingredients():
            child = SubElement(root, "ingredient")
            child.attrib.update(serialize_ingredient(ingredient))
        ElementTree(root).write(stream, encoding="unicode", xml_declaration=True)


def serialize_recipe(recipe: Recipe) -> dict[str, str]:
    return {
        "name": recipe.title,
        "image": encode_img(recipe.image) or "",
        "portions": str(int(recipe.amount)) if recipe.amount is not None else "1",
        "instruction": recipe.instruction_content_type.to_plain_text(
            recipe.instruction
        ),
    }


def serialize_ingredient(ingredient: Ingredient) -> dict[str, str]:
    if isinstance(ingredient.amount, AmountRange):
        count = (ingredient.amount.min + ingredient.amount.max) / 2
    elif ingredient.amount is not None:
        count = ingredient.amount
    else:
        count = Fraction(1)
    return {
        "article": ingredient.name,
        "count": str(scaled_int(count)),
        "unit": ingredient.unit or "",
    }


def scaled_int(x: Fraction) -> int:
    return int(x * 1000.0)
