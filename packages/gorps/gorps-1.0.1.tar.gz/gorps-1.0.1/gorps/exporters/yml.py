"""Export to yml (main format)."""

from collections import OrderedDict
from dataclasses import asdict
from fractions import Fraction
from typing import IO, Any

import yaml

from gorps.exporters.base import TextExporterBaseAtomic
from gorps.exporters.serialize import fmt_time
from gorps.model import Recipe


def _represent_dictorder(self: yaml.Dumper, data: dict[str, Any]) -> yaml.MappingNode:
    return self.represent_mapping(
        "tag:yaml.org,2002:map",
        filter(lambda t: t[1] is not None and t != ("optional", False), data.items()),
    )


yaml.add_representer(OrderedDict, _represent_dictorder)


class Exporter(TextExporterBaseAtomic):
    """Yml exporter."""

    name = "yml"
    ext = "yml"

    def export_stream_single(self, recipe: Recipe, stream: IO[str]) -> None:
        serialized: dict[str, Any] = asdict(recipe, dict_factory=OrderedDict)
        serialized["instruction_content_type"] = (
            recipe.instruction_content_type.mime_type
        )
        for key in ("cooking_time", "preparation_time"):
            if serialized[key] is not None:
                serialized[key] = fmt_time(serialized[key])

        def represent_fraction(dumper: yaml.Dumper, data: Fraction) -> yaml.ScalarNode:
            if data.denominator == 1:
                return dumper.represent_scalar(
                    "tag:yaml.org,2002:int", str(data.numerator)
                )
            return dumper.represent_scalar("tag:yaml.org,2002:str", str(data))

        yaml.add_representer(
            Fraction,
            represent_fraction,
        )
        yaml.dump(
            serialized,
            stream,
            encoding="utf-8",
            allow_unicode=True,
            explicit_start=True,
        )
