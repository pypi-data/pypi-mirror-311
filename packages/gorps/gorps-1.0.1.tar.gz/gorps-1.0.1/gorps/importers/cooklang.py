"""cooklang import.

See: https://cooklang.org
"""

import os
import warnings
from collections.abc import Iterable
from dataclasses import fields
from fractions import Fraction
from typing import Any

from gorps.content_types import COOKLANG
from gorps.content_types.cooklang import markup_regions
from gorps.importers.deserialize.primitive_dict import deserialize_recipe_args
from gorps.model import Image, Ingredient, Recipe


def load_recipe(path: str) -> Recipe:
    """Load a single recipe."""
    basename = os.path.basename(path)
    title, _ = os.path.splitext(basename)
    with open(path, encoding="utf-8") as f:
        instruction = f.read()
        instruction, recipe_kwargs = extract_metadata(instruction)
        return Recipe(
            **deserialize_recipe_args(recipe_kwargs),
            ingredients=extract_ingredients(instruction),
            instruction=instruction,
            title=title,
            image=load_image(path),
            instruction_content_type=COOKLANG,
            cookware=extract_cookware(instruction),
        )


def load_image(path: str) -> Image | None:
    for ext, fmt in (
        ("jpg", "image/jpeg"),
        ("jpeg", "image/jpeg"),
        ("png", "image/png"),
    ):
        data = try_read_bytes(path.removesuffix(".cook") + "." + ext)
        if data is not None:
            return Image(data=data, fmt=fmt)
    return None


def try_read_bytes(path: str) -> bytes | None:
    try:
        with open(path, "rb") as stream:
            return stream.read()
    except FileNotFoundError:
        return None


def extract_ingredients(instruction: str) -> list[Ingredient]:
    return [
        parse_ingredient(name, spec) for name, spec in markup_items(instruction, "@")
    ]


def parse_ingredient(name: str, spec: str | None) -> Ingredient:
    if spec:
        if "%" in spec:
            amount, unit = spec.split("%")
        else:
            amount = spec
            unit = None
        return Ingredient(
            name=capitalize_first_word(name), amount=Fraction(amount), unit=unit
        )
    return Ingredient(name=name)


def extract_cookware(instruction: str) -> list[str]:
    return [capitalize_first_word(name) for name, _ in markup_items(instruction, "#")]


def capitalize_first_word(text: str) -> str:
    return text[:1].capitalize() + text[1:]


def markup_items(body: str, char: str) -> Iterable[tuple[str, str | None]]:
    for _, symbol_region, spec_region in markup_regions(body, char):
        yield (
            body[symbol_region],
            (body[spec_region] if spec_region.stop > spec_region.start else None),
        )


def extract_metadata(instruction: str) -> tuple[str, dict[str, Any]]:
    metadata_lines = (
        line for line in instruction.splitlines() if line.startswith(">> ")
    )
    metadata = (line.removeprefix(">> ").split(":", 1) for line in metadata_lines)
    recipe_fields = {
        f.name for f in fields(Recipe)
    } - {  # The following fields would be overridden. Move them into tags:
        "ingredients",
        "instruction",
        "title",
        "image",
        "instruction_content_type",
        "cookware",
        "tags",
        "nutrition_labels",
    }
    recipe_all_args = [(key.strip(), val.strip()) for key, val in metadata]
    recipe_args: dict[str, Any] = {
        key: val for key, val in recipe_all_args if key in recipe_fields
    }
    recipe_tag_entries = (
        (key, val) for key, val in recipe_all_args if key not in recipe_fields
    )
    recipe_tags: dict[str, Any] = {}
    for key, val in recipe_tag_entries:
        if key.startswith("nutrition_labels."):
            nutrition_labels = recipe_args.setdefault("nutrition_labels", {})
            nutrition_labels[key.removeprefix("nutrition_labels.")] = parse_value(val)
            continue
        if key.endswith("[]"):
            stripped_key = key.removesuffix("[]")
            recipe_tags.setdefault(stripped_key, []).append(val)
        else:
            if key in recipe_tags:
                warnings.warn(f"Duplicated metadata key '{key}'", stacklevel=0)
            recipe_tags[key] = val
    if recipe_tags:
        recipe_args["tags"] = recipe_tags
    instruction = "\n".join(
        line for line in instruction.splitlines() if not line.startswith(">> ")
    ).strip()
    return instruction, recipe_args


def parse_value(raw: str) -> dict[str, str]:
    raw_val, unit = raw.rsplit(" ", 1)
    if unit[0].isnumeric() or unit[0] in {"/", ".", ","}:
        msg = f"Invalid unit: {unit}"
        raise ValueError(msg)
    return {"value": raw_val, "unit": unit}
