"""Întegration test."""

import difflib
import logging
import os
import re
import shlex
import sqlite3
import unittest
from collections.abc import Callable, Iterable, Iterator, Mapping
from contextlib import contextmanager
from io import BytesIO, StringIO
from typing import IO, Any, ClassVar
from unittest import mock
from xml.etree.ElementTree import canonicalize as etree_canonicalize

from gorps.__main__ import main
from gorps.exporters.openrecipes import unique_in_order
from gorps.exporters.templating import load_text_file

from . import BASE_DIR
from . import outputs as out

README = load_text_file(os.path.join(BASE_DIR, "README.md"))

# ruff: noqa: S108


class IntegrationTest:
    """Base class for integration tests."""

    cmd: str
    check_readme: bool = True
    expected_outputs: ClassVar[Mapping[str, str | bytes]]

    def test_readme(self) -> None:
        if not self.check_readme:
            return
        code_block = f"""
```sh
{self.cmd}
```
"""
        if code_block not in README:
            raise AssertionError("Code block not found in README.md")

    @staticmethod
    def setUp() -> None:
        os.chdir(os.path.join(os.path.dirname(__file__), ".."))

    def run_cmd(self, cmd: str | None = None) -> None:
        if cmd is None:
            cmd = self.cmd
        main(
            shlex.split(cmd.replace(" \\\n", ""))[1:],
            log_level=logging.WARNING,
        )


class TestSVG(unittest.TestCase, IntegrationTest):
    """Svg integration test."""

    cmd = "gorps export --template=examples/svg/template.svg -o /tmp/out.svg examples/recipes/yml/"

    expected_outputs: ClassVar[Mapping[str, str | bytes]] = {"/tmp/out-00.svg": out.svg}

    def test_command(self) -> None:
        with intercept_outputs() as outputs:
            self.run_cmd()
        assert_text_collection_equal(outputs, self.expected_outputs)


class TestXml(unittest.TestCase, IntegrationTest):
    """Xml integration test."""

    cmd = """gorps export \\
  --template examples/menu-card/xml-fo/template.fo.xml \\
  --group-by 'tags["category"]' \\
  --group Starters \\
  --group "Main courses" \\
  --group Dessert \\
  --variable-file examples/menu-card/xml-fo/variables.json \\
  --title "Beans with Bacon a la Bud Spencer" \\
  --title "More Beans" \\
  -o /tmp/menucard.fo.xml \\
  examples/recipes/yml/"""

    expected_outputs: ClassVar[Mapping[str, str | bytes]] = {
        "/tmp/menucard.fo.xml": out.fo_xml
    }

    def test_command(self) -> None:
        with intercept_outputs() as outputs:
            self.run_cmd()
        assert_text_collection_equal(
            outputs, self.expected_outputs, canonicalize=xml_canonicalize
        )


class TestHtml(unittest.TestCase, IntegrationTest):
    """Html integration test."""

    cmd = """gorps export \\
  --template examples/html/template.html \\
  -o /tmp/beans.html \\
  examples/recipes/yml/beans.yml"""

    expected_outputs: ClassVar[Mapping[str, str | bytes]] = {
        "/tmp/beans.html": out.html_beans
    }

    def test_command(self) -> None:
        with intercept_outputs() as outputs:
            self.run_cmd()
        assert_text_collection_equal(outputs, self.expected_outputs)


class TestHtmlFolder(unittest.TestCase, IntegrationTest):
    """Html integration test for a folder."""

    check_readme = False

    cmd = """gorps export \\
  --template examples/html/template.html \\
  -o /tmp/html/ \\
  examples/recipes/yml/"""

    expected_outputs: ClassVar[Mapping[str, str | bytes]] = {
        "/tmp/html/beans-with-bacon-a-la-bud-spencer.html": out.html_beans,
        "/tmp/html/more-beans.html": out.html_more_beans,
    }

    def test_command(self) -> None:
        with intercept_outputs() as outputs:
            self.run_cmd()
        assert_text_collection_equal(outputs, self.expected_outputs)


class TestHtmlMenucard(unittest.TestCase, IntegrationTest):
    """Html menu card integration test."""

    cmd = """gorps export \\
  --template examples/menu-card/html/menucard.template.html \\
  -V title="Beans & Beans" \\
  --filter-ingredient Salt \\
  --filter-ingredient Pepper \\
  --grouped-titles examples/menu-card/html/grouped_titles.json \\
  -o /tmp/menucard.html \\
  examples/recipes/yml/"""
    expected_outputs: ClassVar[Mapping[str, str | bytes]] = {
        "/tmp/menucard.html": out.html_menucard
    }

    def test_command(self) -> None:
        with intercept_outputs() as outputs:
            self.run_cmd()
        assert_text_collection_equal(outputs, self.expected_outputs)


class TestOpenrecipes(unittest.TestCase, IntegrationTest):
    """Openrecipes integration test."""

    cmd = """gorps export --fmt openrecipes -o /tmp/database.db examples/recipes/yml/"""

    expected_outputs: ClassVar[Mapping[str, str | bytes]] = {
        ":memory:": out.openrecipes_sql
    }

    def test_command(self) -> None:
        with dump_memory_db() as outputs:
            self.run_cmd(
                self.cmd.replace(
                    "/tmp/database.db", "file:memory?mode=memory&cache=shared"
                )
            )
        assert_text_collection_equal(outputs, self.expected_outputs)


class TestOpenrecipesXml(unittest.TestCase, IntegrationTest):
    """Openrecipes xml integration test."""

    cmd = """gorps export --fmt openrecipes-xml -o /tmp/out/ examples/recipes/yml/"""

    expected_outputs = out.openrecipes_xml

    def test_command(self) -> None:
        with intercept_outputs() as outputs:
            self.run_cmd()
        assert_text_collection_equal(
            outputs, self.expected_outputs, canonicalize=xml_canonicalize
        )


class TestMd(unittest.TestCase, IntegrationTest):
    """Md integration test."""

    cmd = "gorps export --fmt markdown -o /tmp/out/ examples/recipes/yml/"

    expected_outputs = out.md

    def test_command(self) -> None:
        with intercept_outputs() as outputs:
            self.run_cmd()
        assert_text_collection_equal(outputs, self.expected_outputs)


class TestSetImage(unittest.TestCase, IntegrationTest):
    """Integration test for set-image."""

    cmd = "gorps set-image --pic=/tmp/1x1.png examples/recipes/yml/more-beans.yml"

    expected_outputs: ClassVar[Mapping[str, str | bytes]] = {
        "examples/recipes/yml/more-beans.yml": out.yml
    }

    def test_command(self) -> None:
        with intercept_outputs(reads={"/tmp/1x1.png": out.png}) as outputs:
            self.run_cmd()
        assert_text_collection_equal(outputs, self.expected_outputs)


class TestExtractImage(unittest.TestCase, IntegrationTest):
    """Integration test for extract-image."""

    cmd = "gorps extract-image -o /tmp/1x1.png examples/recipes/yml/more-beans.yml"

    expected_outputs: ClassVar[Mapping[str, str | bytes]] = {"/tmp/1x1.png": out.png}

    def test_command(self) -> None:
        with intercept_outputs(
            reads={"examples/recipes/yml/more-beans.yml": out.yml}
        ) as outputs:
            self.run_cmd()
        assert_text_collection_equal(outputs, self.expected_outputs)


def assert_text_collection_equal(
    actual: Mapping[str, str | bytes],
    expected: Mapping[str, str | bytes],
    canonicalize: Callable[[str], str] = lambda x: x,
) -> None:
    def generic_canonicalize(val: str | bytes) -> str | bytes:
        if isinstance(val, bytes):
            return val
        return canonicalize(val)

    if {key: generic_canonicalize(val) for key, val in actual.items()} == {
        key: generic_canonicalize(val) for key, val in expected.items()
    }:
        return
    raise AssertionError("\n" + "\n".join(diff_collection(actual, expected)))


def assert_text_equal(actual: str, expected: str, caption: str = "output") -> None:
    if actual == expected:
        return
    raise AssertionError(diff(actual, expected, caption))


def diff_collection(
    actual: Mapping[str, str | bytes], expected: Mapping[str, str | bytes]
) -> Iterable[str]:
    only_actual = frozenset(actual) - frozenset(expected)
    only_expected = frozenset(expected) - frozenset(actual)
    diffs = [
        diff(actual_text, expected[caption], caption)
        for caption, actual_text in actual.items()
        if caption in expected
    ]
    if only_actual:
        yield "Only in actual: " + ", ".join(only_actual)
    if only_expected:
        yield "Only in expected: " + ", ".join(only_expected)
    yield "\n".join(diffs)


def diff(actual: str | bytes, expected: str | bytes, caption: str) -> str:
    if isinstance(actual, bytes):
        actual = actual.decode()
    if isinstance(expected, bytes):
        expected = expected.decode()
    return "\n".join(
        difflib.unified_diff(
            expected.splitlines(),
            actual.splitlines(),
            fromfile=os.path.join("expected", caption.lstrip("/")),
            tofile=os.path.join("actual", caption.lstrip("/")),
            lineterm="\n",
        )
    )


def xml_canonicalize(body: str) -> str:
    return etree_canonicalize(body, strip_text=True)


@contextmanager
def intercept_outputs(  # noqa: C901
    reads: dict[str, str | bytes] | None = None,
) -> Iterator[dict[str, str | bytes]]:
    outputs: dict[str, str | bytes] = {}

    class BytesIOBuffer(BytesIO):
        def __init__(self, path: str):
            self.path = path
            super().__init__()

        def close(self) -> None:
            outputs[self.path] = self.getvalue()

    class StringIOBuffer(StringIO):
        def __init__(self, path: str):
            self.path = path
            super().__init__()

        def close(self) -> None:
            outputs[self.path] = self.getvalue()

    original_open = open

    def mock_open(
        path: str, mode: str = "r", encoding: str | None = None, **kwargs: Any
    ) -> IO[Any]:
        if "r" in mode and reads is not None:
            contents = reads.get(path)
            if isinstance(contents, str):
                return StringIO(contents)
            if isinstance(contents, bytes):
                return BytesIO(contents)
        if mode == "w":
            return StringIOBuffer(path)
        if mode == "wb":
            return BytesIOBuffer(path)
        return original_open(path, mode, encoding=encoding, **kwargs)

    with mock.patch("builtins.open", mock_open):
        yield outputs


@contextmanager
def dump_memory_db() -> Iterator[dict[str, str]]:
    dump: dict[str, str] = {}
    connection = sqlite3.connect("file:memory?mode=memory&cache=shared")
    yield dump
    dump[":memory:"] = "\n".join(connection.iterdump())
    connection.close()


def canonicalize_sqldump(dump: str) -> str:
    expression = re.compile(r"X'[0-9A-Z]*'")
    random_ids = unique_in_order(expression.findall(dump))
    for deterministic_id, random_id in enumerate(random_ids):
        dump = dump.replace(random_id, f"X'{deterministic_id}'")
    return dump
