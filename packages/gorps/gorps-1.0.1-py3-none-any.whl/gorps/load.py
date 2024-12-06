"""Loading of recipes by extension."""

import glob
import os
from collections.abc import Iterable, Sequence

from .importers import cooklang, yml
from .model import Recipe

HOME = os.path.expanduser("~")
RECIPE_DIR = os.path.join(HOME, ".local", "var", "recipes")
INPUT_FORMATS = {
    "yml": yml.load_recipe,
    "yaml": yml.load_recipe,
    "cook": cooklang.load_recipe,
}


def load_recipes(
    sources: Iterable[str] = (),
) -> Iterable[Recipe]:
    """Load recipes from specified sources (files / directories / symlinks), filtered by titles (if not None)."""
    if not sources:
        if not os.path.isdir(RECIPE_DIR):
            return []
        sources = (RECIPE_DIR,)
    files = sorted(collect_files(sources))
    recipes = (load_recipe(f) for f in files)
    return (r for r in recipes if r is not None)


def load_recipe(path: str) -> Recipe:
    """Load a single recipe by extension."""
    fmt = INPUT_FORMATS.get(path_ext(path))
    if fmt is None:
        msg = f"Unsupported format: {path}"
        raise ValueError(msg)
    return fmt(path)


def path_ext(path: str) -> str:
    return path.rsplit(".", 1)[-1]


def collect_files(sources: Iterable[str]) -> Sequence[str]:
    """From an iterable of files / directories / links, form a list of files either directly listed or contained (recursively) in a listed directory."""
    sources = set(sources)
    files = {src for src in sources if os.path.isfile(src)}
    directories = sources - files
    invalid_dirs = [src_dir for src_dir in directories if not os.path.isdir(src_dir)]
    if invalid_dirs:
        msg = f"Input paths {', '.join(invalid_dirs)} are neither files nor directories nor links to thereof."
        raise ValueError(msg)
    return list(files) + [
        path
        for src_dir in directories
        for path in glob.glob(os.path.join(src_dir, "**", "*.*"), recursive=True)
        if path_ext(path) in INPUT_FORMATS
    ]
