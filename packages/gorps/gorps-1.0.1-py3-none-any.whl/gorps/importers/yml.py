"""yml import."""

from typing import IO

import yaml

from gorps.importers.deserialize.primitive_dict import deserialize_recipe
from gorps.model import Recipe


def load_recipe(path: str) -> Recipe:
    """Load a single recipe."""
    with open(path, encoding="utf-8") as f:
        return load_recipe_from_stream(f)


def load_recipe_from_stream(stream: IO[str]) -> Recipe:
    raw = yaml.safe_load(stream)
    return deserialize_recipe(raw)
