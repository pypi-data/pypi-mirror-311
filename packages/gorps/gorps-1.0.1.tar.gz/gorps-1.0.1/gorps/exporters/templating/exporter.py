"""Exporter templates."""

from abc import ABC
from collections.abc import Iterable
from typing import Any

from gorps.exporters.base import TextExporterBase
from gorps.model import Recipe


class TemplateExporterBase(TextExporterBase, ABC):
    """Base class for templated exporters."""

    def __init__(self, template: str, variables: dict[str, Any] | None = None):
        self.template = template
        if variables is None:
            self.variables = {}
        else:
            self.variables = variables

    def build_environment(self, recipes: Iterable[Recipe]) -> dict[str, Any]:
        recipes = list(recipes)
        recipe_env: dict[str, Recipe | list[Recipe]] = {"recipes": recipes}
        if len(recipes) == 1:
            recipe_env["recipe"] = recipes[0]
        return {**self.variables, **recipe_env}
