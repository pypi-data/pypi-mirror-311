"""Markdown export."""

from collections.abc import Iterable
from typing import IO

from gorps.exporters.base import TextExporterBase
from gorps.exporters.templating import format_ingredient
from gorps.model import Ingredient, IngredientGroup, Recipe


class Exporter(TextExporterBase):
    """Markdown exporter."""

    name = "markdown"
    ext = "md"

    def export_stream(self, recipes: Iterable[Recipe], stream: IO[str]) -> None:
        for recipe in recipes:
            stream.write(f"# {recipe.title}\n\n")
            for ingredient in recipe.ingredients:
                if isinstance(ingredient, Ingredient):
                    write_ingredient(ingredient, stream)
                elif isinstance(ingredient, IngredientGroup):
                    stream.write(f"\n### {ingredient.name}\n\n")
                    for sub_ingredient in ingredient.ingredients:
                        write_ingredient(sub_ingredient, stream)
            stream.write(
                f"\n{recipe.instruction_content_type.to_plain_text(recipe.instruction)}\n"
            )


def write_ingredient(ingredient: Ingredient, stream: IO[str]) -> None:
    stream.write(f"* {format_ingredient(ingredient)}\n")
