"""Recipe export."""

import json
import os
from collections.abc import Callable, Iterable, Sequence
from functools import wraps
from typing import Any, TypeVar

from gorps.exporters import html, md, svg, xml
from gorps.exporters.base import ExporterBase, slugify
from gorps.exporters.html import make_paragraphs
from gorps.exporters.serialize import fmt_time
from gorps.exporters.templating import (
    FallbackValue,
    class_selector,
    fmt_ingredients,
)
from gorps.exporters.templating.exporter import TemplateExporterBase
from gorps.model import Ingredient, IngredientGroup, Recipe

exporters: list[type[ExporterBase]] = [
    xml.Exporter,
    svg.Exporter,
    md.Exporter,
    html.Exporter,
]

try:
    from . import openrecipes, openrecipes_xml

    exporters += [openrecipes.Exporter, openrecipes_xml.Exporter]
except ModuleNotFoundError:
    pass

exporter_by_ext = {exporter.ext: exporter for exporter in exporters}
exporter_by_name = {exporter.name: exporter for exporter in exporters}


def export(  # noqa: PLR0913
    out: str,
    recipes: Iterable[Recipe],
    variables: dict[str, str] | None = None,
    variable_file: str | None = None,
    template: str | None = None,
    grouped_titles: list[dict[str, Any]] | None = None,
    group_selector: str | None = None,
    groups: Sequence[str] = (),
    fmt: type[ExporterBase] | None = None,
) -> None:
    exporter_class = fmt or guess_format(out)
    if exporter_class is None:
        raise ValueError("Could not infer format from output or template")
    exporter_options: dict[str, Any] = {}
    if template is not None:
        exporter_options["template"] = template
    variables = merge_dicts(
        vars_from_file(variable_file),
        variables,
        build_groups(recipes, grouped_titles, group_selector, groups),
        (
            {helper.__name__: helper for helper in HELPERS}
            if issubclass(exporter_class, TemplateExporterBase)
            else None
        ),
    )
    if variables:
        exporter_options["variables"] = variables
    exporter = exporter_class(**exporter_options)
    if os.path.isdir(out) or out.endswith(os.path.sep):
        os.makedirs(os.path.dirname(out), exist_ok=True)
        exporter.export_multifile(recipes, out_dir=out)
    else:
        exporter.export(recipes, out=out)


def is_group(obj: Ingredient | IngredientGroup) -> bool:
    return isinstance(obj, IngredientGroup)


R = TypeVar("R")
S = TypeVar("S")
T = TypeVar("T")


def accept_fallback_value(
    f: Callable[[T], R],
) -> Callable[[T | FallbackValue[S]], R | FallbackValue[S]]:
    @wraps(f)  # type: ignore[arg-type]
    def wrapped(obj: T | FallbackValue[S]) -> R | FallbackValue[S]:
        if isinstance(obj, FallbackValue):
            return obj
        return f(obj)

    return wrapped  # type: ignore[return-value]


HELPERS = [
    is_group,
    accept_fallback_value(fmt_time),
    accept_fallback_value(fmt_ingredients),
    accept_fallback_value(make_paragraphs),
    accept_fallback_value(slugify),
]


def merge_dicts(*dicts: dict[str, Any] | None) -> dict[str, Any]:
    merged = {}
    for d in dicts:
        if d is not None:
            merged.update(d)
    return merged


def vars_from_file(variable_file: str | None = None) -> dict[str, Any]:
    if variable_file is None:
        return {}
    with open(variable_file, encoding="utf-8") as f:
        variables: dict[str, Any] = json.load(f)
        return variables


def guess_format(path: str | None) -> type[ExporterBase] | None:
    if path is None:
        return None
    _, ext = os.path.splitext(path)
    try:
        return exporter_by_ext[ext.lstrip(".")]
    except KeyError:
        return None


def build_groups(
    recipes: Iterable[Recipe],
    grouped_titles: list[dict[str, Any]] | None,
    selector: str | None,
    groups: Iterable[str],
) -> dict[str, Any]:
    groups = list(groups)
    if grouped_titles is not None:
        if groups:
            grouped_titles = [
                group for group in grouped_titles if group["name"] in groups
            ]
        return {"groups": group_titles(recipes, grouped_titles)}
    if selector is None:
        return {}
    return {"groups": group_by(list(recipes), selector, groups)}


def group_by(
    recipes: Sequence[Recipe], selector: str, group_names: Sequence[str] = ()
) -> list[tuple[str, list[Recipe]]]:
    select = class_selector(selector, default=None)
    groups: dict[str, list[Recipe]] = {}
    for recipe in recipes:
        attr = select(recipe)
        if attr is None:
            continue
        if not isinstance(attr, Sequence):
            attr = [attr]
        for group_name in attr:
            if group_name in group_names or not group_names:
                groups.setdefault(group_name, []).append(recipe)
    if group_names:
        return [(group_name, groups[group_name]) for group_name in group_names]
    return sorted(groups.items(), key=lambda item: item[0])


def group_titles(
    recipes: Iterable[Recipe], grouped_titles: list[dict[str, Any]]
) -> list[tuple[str, list[Recipe]]]:
    groups_by_title: dict[str, set[str]] = {}
    for group in grouped_titles:
        for title in group["titles"]:
            groups_by_title.setdefault(title, set()).add(group["name"])
    missing_titles = set(groups_by_title)
    grouped_recipes: dict[str, list[Recipe]] = {}
    for recipe in recipes:
        groups = groups_by_title.get(recipe.title, ())
        missing_titles.discard(recipe.title)
        for group_name in groups:
            grouped_recipes.setdefault(group_name, []).append(recipe)
    if missing_titles:
        msg = f"Could not find recipes with titles: {', '.join(missing_titles)}"
        raise ValueError(msg)
    return [(group["name"], grouped_recipes[group["name"]]) for group in grouped_titles]
