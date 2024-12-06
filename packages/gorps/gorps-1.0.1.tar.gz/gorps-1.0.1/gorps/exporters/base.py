"""Base classes for recipe exporters."""

import os
from abc import ABC
from collections.abc import Iterable
from typing import IO

from gorps.model import Recipe


class ExporterBase:
    """Exporter Interface."""

    name: str
    ext: str

    def export(self, recipes: Iterable[Recipe], out: str) -> None:
        raise NotImplementedError("Must be implemented by a derived class")

    def export_multifile(self, recipes: Iterable[Recipe], out_dir: str) -> None:
        raise NotImplementedError("Must be implemented by a derived class")


class TextExporterBase(ExporterBase):
    """Text exporter specialization."""

    def export(self, recipes: Iterable[Recipe], out: str) -> None:
        with open(out, "w", encoding="utf-8") as f:
            self.export_stream(recipes, f)

    def export_multifile(self, recipes: Iterable[Recipe], out_dir: str) -> None:
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir, exist_ok=True)
        used_paths: dict[str, int] = {}
        for rcp in recipes:
            slug = slugify(rcp.title)
            counter = used_paths.get(slug, 0) + 1
            counter_suffix = "" if counter == 1 else f"-{counter}"
            path = os.path.join(out_dir, f"{slug}{counter_suffix}.{self.ext}")
            used_paths[slug] = counter

            with open(path, "w", encoding="utf-8") as f:
                self.export_stream([rcp], f)

    def export_stream(self, recipes: Iterable[Recipe], stream: IO[str]) -> None:
        raise NotImplementedError("Not implemented")


class TextExporterBaseAtomic(TextExporterBase, ABC):
    """Only one recipe per file allowed."""

    def export_stream_single(self, recipe: Recipe, stream: IO[str]) -> None:
        raise NotImplementedError("Not implemented")

    @classmethod
    def _unpack_recipe(cls, recipes: Iterable[Recipe]) -> Recipe:
        try:
            (recipe,) = recipes
        except ValueError:
            msg = f"Eporting multiple recipes to a single file is not supported by {cls.name}"
            raise RuntimeError(msg) from None
        return recipe

    def export_stream(self, recipes: Iterable[Recipe], stream: IO[str]) -> None:
        self.export_stream_single(self._unpack_recipe(recipes), stream)


def slugify(name: str) -> str:
    return name.lower().replace(" ", "-")
