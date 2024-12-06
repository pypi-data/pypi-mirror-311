"""svg export."""

import os
import warnings
from collections.abc import Iterable
from dataclasses import replace
from typing import IO, Any, TypeVar, cast

from gorps.exporters.templating import FallbackValue, fill_template, find_placeholders
from gorps.exporters.templating.exporter import TemplateExporterBase
from gorps.model import Recipe


class Exporter(TemplateExporterBase):
    """Svg exporter."""

    name = "svg"
    ext = "svg"

    def export(self, recipes: Iterable[Recipe], out: str) -> None:
        for file_number, rendered_template in enumerate(
            fill_template_multi_slot(self.template, recipes, variables=self.variables)
        ):
            base, ext = os.path.splitext(out)
            with open(f"{base}-{file_number:02}{ext}", "w", encoding="utf-8") as f:
                f.write(rendered_template)

    def export_stream(self, recipes: Iterable[Recipe], stream: IO[str]) -> None:
        (recipe,) = recipes
        rendered_template = fill_template(
            self.template, env={"recipe": recipe, **self.variables}
        )
        stream.write(rendered_template)


def fill_template_multi_slot(
    template: str, recipes: Iterable[Recipe], variables: dict[str, Any]
) -> Iterable[str]:
    slot_numbers = scan_slot_numbers(template, root="recipes")
    if max(slot_numbers) + 1 != len(slot_numbers):
        warnings.warn(
            f"The slot numbers {','.join(str(n) for n in slot_numbers)} have gaps!",
            stacklevel=0,
        )
    recipes = [
        replace(
            recipe,
            instruction=recipe.instruction_content_type.to_plain_text(
                recipe.instruction
            ),
        )
        for recipe in recipes
    ]
    for chunk in chunked(recipes, max(slot_numbers) + 1):
        extended_chunk = chunk
        if len(extended_chunk) < len(slot_numbers):
            extended_chunk += [cast(Recipe, FallbackValue[str](""))] * (
                len(slot_numbers) - len(extended_chunk)
            )
        yield fill_template(template, env={"recipes": extended_chunk, **variables})


T = TypeVar("T")


def chunked(items: Iterable[T], size: int) -> Iterable[list[T]]:
    items = iter(items)
    while True:
        chunk = [item for _, item in zip(range(size), items, strict=False)]
        if not chunk:
            return
        yield chunk


def scan_slot_numbers(template: str, root: str) -> list[int]:
    def scan_placeholder(marker: str) -> int | None:
        if not marker.startswith("["):
            return None
        try:
            return int(marker.lstrip("[").split("]")[0])
        except ValueError:
            return None

    placeholders = [
        placeholder.strip()[len(root) :]
        for placeholder in find_placeholders(template)
        if placeholder.strip().startswith(root)
    ]
    slot_numbers = (scan_placeholder(placeholder) for placeholder in placeholders)
    return sorted({n for n in slot_numbers if n is not None})
