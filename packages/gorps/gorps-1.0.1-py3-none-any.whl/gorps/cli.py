"""CLI utilities."""

import argparse
from collections.abc import Callable, Sequence
from typing import Any, cast


class Argument:
    """CLI argument."""

    def __init__(self, *args: str, **kwargs: Any):
        self.args = args
        self.kwargs = kwargs


class MutuallyExclusiveGroup:
    """Mutually exclusive group of CLI arguments."""

    def __init__(self, *args: Argument):
        self.args = args


class Action:
    """CLI subcommand."""

    args: Sequence[Argument | MutuallyExclusiveGroup]
    help: str
    description: str | None = None

    __call__: Callable[..., None]


def declarative_parser(action_type: type, **kwargs: Any) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(**kwargs)
    subparsers = parser.add_subparsers(
        title="List of actions",
        description="For an overview of action specific parameters, "
        "use %(prog)s <ACTION> --help",
        help="Action help",
        required=True,
        metavar="<ACTION>",
    )
    actions = [
        (to_kebab_case(key), val)
        for key, val in vars(action_type).items()
        if isinstance(val, type) and issubclass(val, Action)
    ]
    for action_name, action in actions:
        subparser = subparsers.add_parser(
            action_name,
            help=action.__doc__,
            description=action.description,
        )
        subparser.set_defaults(action=action())
        for argument in action.args:
            if isinstance(argument, Argument):
                subparser.add_argument(*argument.args, **argument.kwargs)
            elif isinstance(argument, MutuallyExclusiveGroup):
                group = subparser.add_mutually_exclusive_group()
                for group_argument in argument.args:
                    group.add_argument(*group_argument.args, **group_argument.kwargs)
    return parser


class StoreDictKeyPair(argparse.Action):
    """Argparse action to store a key value pair into a dict."""

    def __call__(
        self,
        _parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: str | Sequence[Any] | None,
        _option_string: str | None = None,
    ) -> None:
        if isinstance(values, str) or values is None:
            msg = f"Wrong value: {values}"
            raise ValueError(msg)
        (key, value) = cast(Sequence[str], values)
        dct = getattr(namespace, self.dest)
        dct = {**(dct or {}), key: value}
        setattr(namespace, self.dest, dct)


def to_kebab_case(name: str) -> str:
    return name[0].lower() + "".join(
        c if not c.isupper() else "-" + c.lower() for c in name[1:]
    )


def map_dict(dct: dict[str, Any], err_msg: str) -> Callable[[str], Any]:
    def mapping(key: str) -> Any:
        try:
            return dct[key]
        except KeyError:
            raise ValueError(err_msg.format(key=key)) from None

    return mapping
