"""HTML export."""

from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from html.parser import HTMLParser
from os import PathLike
from typing import IO, Any
from xml.etree.ElementTree import Comment, Element, ElementTree

from gorps.exporters.templating.exporter import TemplateExporterBase
from gorps.exporters.xml import Source, process_xml_tree_template
from gorps.model import Recipe


class Exporter(TemplateExporterBase):
    """HTML exporter."""

    name = "html"
    ext = "html"

    def export_stream(self, recipes: Iterable[Recipe], stream: IO[str]) -> None:
        process_template(self.template, self.build_environment(recipes), stream)


def process_template(template: str, environment: dict[str, Any], dest: Source) -> None:
    parser = HTMLTemplateParser()
    parser.feed(template)
    (html,) = parser.document
    processed_html = process_xml_tree_template(html, environment, {})
    with generalized_open(dest) as f:
        if parser.decl is not None:
            f.write(f"<!{parser.decl}>\n")
        ElementTree(processed_html).write(
            f,
            encoding="unicode",
            xml_declaration=False,
            method="html",
            short_empty_elements=True,
        )


VOID_ELEMENTS = frozenset(
    (
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    )
)


class HTMLTemplateParser(HTMLParser):
    """Parser for HTML templates."""

    def __init__(self) -> None:
        super().__init__()
        self.document = Element("document")
        self._current_path = [self.document]
        self._last_closed: Element | None = None
        self.decl: str | None = None

    def _append(self, node: Element) -> Element:
        parent = self._current_path[-1]
        parent.append(node)
        self._current_path.append(node)
        self._last_closed = None
        return node

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._append(Element(tag, {key: val or "" for key, val in attrs}))
        if tag in VOID_ELEMENTS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        self._last_closed = self._current_path.pop()
        if tag != self._last_closed.tag:
            msg = f"HTML parser error: {self.getpos()}: Closing tag </{tag}> does not match <{self._last_closed.tag}>"
            raise RuntimeError(msg)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_data(self, data: str) -> None:
        if self._last_closed is not None:
            if self._last_closed.tail is not None:
                msg = f"HTML parser error: {self.getpos()}: Got 2 consecutive data parts for element <{self._last_closed.tag}>"
                raise RuntimeError(msg)
            self._last_closed.tail = data
        else:
            if self._current_path[-1].tail is not None:
                msg = f"HTML parser error: {self.getpos()}: Got 2 consecutive data parts for element <{self._current_path[-1].tag}>"
                raise RuntimeError(msg)
            self._current_path[-1].text = data

    def handle_entityref(self, _name: str) -> None:
        """E.g. `&name;`."""
        msg = f"HTML parser error: {self.getpos()}: Entity refs are not allowed"
        raise RuntimeError(msg)

    def handle_charref(self, _name: str) -> None:
        """E.g. `&#NNN;`."""
        msg = f"HTML parser error: {self.getpos()}: Char refs are not allowed"
        raise RuntimeError(msg)

    def handle_comment(self, data: str) -> None:
        """`<!-- comment -->`."""
        self._append(Comment(data))

    def handle_decl(self, decl: str) -> None:
        """`<!DOCTYPE html>`."""
        if self.decl is not None:
            msg = f"HTML parser error: {self.getpos()}: duplicate decl"
            raise RuntimeError(msg)
        self.decl = decl

    def error(self, message: str) -> None:
        msg = f"HTML parser error: {self.getpos()}: {message}"
        raise RuntimeError(msg)


@contextmanager
def generalized_open(source: Source) -> Iterator[IO[Any]]:
    if isinstance(source, int | str | bytes | PathLike):
        with open(source, "w", encoding="utf-8") as f:
            yield f
    else:
        yield source


def make_paragraphs(text: str) -> str | list[Element]:
    paragraphs = text.split("\n\n")
    if len(paragraphs) == 1:
        return text
    return [make_paragraph(paragraph) for paragraph in paragraphs]


def make_paragraph(text: str) -> Element:
    e = Element("p")
    e.text = text
    return e
