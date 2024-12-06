"""Export to a cooklang file."""

import os
import warnings
from collections.abc import Iterable, Sequence
from dataclasses import replace
from typing import IO, Any

from gorps.content_types import COOKLANG
from gorps.exporters.base import TextExporterBaseAtomic
from gorps.exporters.serialize import fmt_time
from gorps.model import Ingredient, IngredientGroup, Recipe, Value


class Exporter(TextExporterBaseAtomic):
    """Cooklang exporter."""

    name = "cooklang"
    ext = "cook"

    def export(self, recipes: Iterable[Recipe], out: str) -> None:
        self.export_single(self._unpack_recipe(recipes), out)

    def export_single(self, recipe: Recipe, out: str) -> None:
        if not out.endswith(recipe.title + "." + self.ext):
            warnings.warn(
                "Exporting a cooklang file to a file name different from the recipes title. This will change the title of the recipe",
                stacklevel=0,
            )
        with open(out, "w", encoding="utf-8") as f:
            self.export_stream_single(recipe, f)
        if recipe.image is not None:
            ext = recipe.image.fmt.removeprefix("image/")
            pic_path = out.removesuffix("." + self.ext) + "." + ext
            with open(pic_path, "wb") as stream:
                stream.write(recipe.image.data)

    def export_multifile(self, recipes: Iterable[Recipe], out_dir: str) -> None:
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir, exist_ok=True)
        used_paths: set[str] = set()
        for rcp in recipes:
            path = os.path.join(out_dir, f"{rcp.title}.{self.ext}")
            if path in used_paths:
                warnings.warn(
                    f"Multiple recipes with title `{rcp.title}`. Only last one will be exported.",
                    stacklevel=0,
                )
            used_paths.add(path)
            self.export_single(rcp, path)

    def export_stream_single(self, recipe: Recipe, stream: IO[str]) -> None:
        if recipe.instruction_content_type is not COOKLANG:
            (
                instruction,
                remaining_ingredients,
                remaining_cookware,
            ) = markup_instructions(
                recipe.instruction,
                flatten_ingredients(recipe.ingredients),
                recipe.cookware,
            )
            stream.write(instruction + "\n")
            stream.write("\nIngredients:\n\n")
            for ingredient in remaining_ingredients:
                stream.write("- " + format_ingredient(ingredient) + "\n")
            if remaining_cookware:
                stream.write("\nCookware:\n\n")
                for ware in remaining_cookware:
                    stream.write(f"- #{ware}{{}}\n")
        else:
            stream.write(recipe.instruction + "\n")

        metadata = [
            (key, val)
            for key, val in [
                ("description", recipe.description),
                ("amount", recipe.amount),
                ("amount_unit", recipe.amount_unit),
                (
                    "preparation_time",
                    (
                        fmt_time(recipe.preparation_time)
                        if recipe.preparation_time is not None
                        else None
                    ),
                ),
                (
                    "cooking_time",
                    (
                        fmt_time(recipe.cooking_time)
                        if recipe.cooking_time is not None
                        else None
                    ),
                ),
                ("source", recipe.source),
                ("link", recipe.link),
                ("notes", recipe.notes),
                *prepare_tags(recipe.tags),
                *prepare_nutrition_labels(recipe.nutrition_labels),
            ]
            if val is not None
        ]
        if not metadata:
            return
        stream.write("\n")
        for key, val in metadata:
            stream.write(f">> {key}: {val}\n")


def markup_instructions(
    instruction: str, ingredients: Iterable[Ingredient], cookware: Iterable[str]
) -> tuple[str, list[Ingredient], list[str]]:
    instruction_lower = instruction.lower()
    replacements = []
    remaining_ingredients = []
    remaining_cookware = []
    for ingredient in ingredients:
        region = find_word(instruction_lower, ingredient.name.lower())
        if region is None:
            remaining_ingredients.append(ingredient)
            continue
        formatted = format_ingredient(replace(ingredient, name=instruction[region]))
        replacements.append((region, formatted))
        instruction_lower = clear_region(instruction_lower, region)
    for ware in cookware:
        region = find_word(instruction_lower, ware.lower())
        if region is None:
            remaining_cookware.append(ware)
            continue
        replacements.append((region, "#" + instruction[region] + "{}"))
        instruction_lower = clear_region(instruction_lower, region)
    return (
        replace_regions(instruction, replacements),
        remaining_ingredients,
        remaining_cookware,
    )


def find_word(text: str, word: str) -> slice | None:
    pos = text.find(word)
    stop = pos + len(word)
    if (
        pos == -1
        or (pos > 0 and not is_word_boundary(text[pos - 1]))
        or (stop < len(text) and not is_word_boundary(text[stop]))
    ):
        return None
    return slice(pos, stop)


def clear_region(text: str, region: slice) -> str:
    out: str = (
        text[: region.start] + " " * (region.stop - region.start) + text[region.stop :]
    )
    return out


def replace_regions(text: str, replacements: Iterable[tuple[slice, str]]) -> str:
    for region, substitution in sorted(replacements, reverse=True):
        text = text[: region.start] + substitution + text[region.stop :]
    return text


def is_word_boundary(s: str) -> bool:
    return not s.isalnum() and s not in {"_", "-"}


def prepare_tags(tags: dict[str, Any]) -> Iterable[tuple[str, str]]:
    for key, val in tags.items():
        if isinstance(val, str):
            yield (key, val)
        elif isinstance(val, Sequence):
            for subval in val:
                if not isinstance(subval, str):
                    warnings.warn(
                        f"Skipping unsupported type {type(subval)} in tags.{key}",
                        stacklevel=0,
                    )
                    continue
                yield (f"{key}[]", subval)
        else:
            warnings.warn(
                f"Skipping tags.{key}: unsupported type {type(subval)}", stacklevel=0
            )
            continue


def prepare_nutrition_labels(labels: dict[str, Value]) -> Iterable[tuple[str, str]]:
    for key, val in labels.items():
        yield (f"nutrition_labels.{key}", f"{val.value} {val.unit}")


def flatten_ingredients(
    ingredients: Iterable[Ingredient | IngredientGroup],
) -> Iterable[Ingredient]:
    for obj in ingredients:
        if isinstance(obj, IngredientGroup):
            yield from obj.ingredients
        else:
            yield obj


def format_ingredient(ingredient: Ingredient) -> str:
    if ingredient.amount is not None:
        amount = format(ingredient.amount)
        if ingredient.unit is not None:
            amount += "%" + ingredient.unit
    else:
        amount = ""
    return f"@{ingredient.name}{{{amount}}}"
