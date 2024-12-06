"""Cooklang format."""

from collections.abc import Iterable


def format_cooklang_body(body: str) -> str:
    # Markup regions:
    for char in ("#", "@"):
        regions = list(markup_regions(body, char))
        for r, name, _ in regions[::-1]:
            body = body[: r.start] + body[name] + body[r.stop :]
    # Timers:
    regions = list(markup_regions(body, "~"))
    for r, _, spec in regions[::-1]:
        body = body[: r.start] + body[spec].replace("%", " ") + body[r.stop :]
    # Comments / Block comments:
    return "\n".join(
        strip_block_comments(line)
        for line in body.splitlines()
        if not line.startswith("-- ")
    )


def strip_block_comments(line: str) -> str:
    comment_start = line.find("[-")
    if comment_start == -1:
        return line
    comment_end = line.find("-]", comment_start + 1)
    if comment_end == -1:
        return line
    return line[:comment_start] + line[comment_end + 2 :]


def markup_regions(body: str, char: str) -> Iterable[tuple[slice, slice, slice]]:
    pos = 0
    while True:
        opt_region = markup_region(body, char, start=pos)
        if opt_region is None:
            return
        yield opt_region
        pos = opt_region[0].stop


def markup_region(
    body: str, char: str, start: int = 0
) -> tuple[slice, slice, slice] | None:
    pos = body.find(char, start)
    if pos == -1:
        return None
    end_of_line = find_any_of(body, {"\n", "@", "#", "~"}, pos + 1)
    next_markup_region = body.find(char, pos + 1)
    if -1 < next_markup_region < end_of_line:
        end_of_line = next_markup_region
    end_of_markup_name = body.find("{", pos + 1, end_of_line)
    if end_of_markup_name != -1:
        end_of_region = body.find("}", end_of_markup_name + 1, end_of_line)
        if end_of_region == -1:
            msg = f"Unterminated markup region: {body[pos:end_of_markup_name+1]}"
            raise ValueError(msg)
        return (
            slice(pos, end_of_region + 1),
            slice(pos + 1, end_of_markup_name),
            slice(end_of_markup_name + 1, end_of_region),
        )
    end_of_region = find_any_of(body, {" ", "\t", "\r", "\n"}, pos + 1, end_of_line)
    return (
        slice(pos, end_of_region),
        slice(pos + 1, end_of_region),
        slice(end_of_region, end_of_region),
    )


def find_any_of(
    s: str, chars: set[str], start: int = 0, stop: int | None = None
) -> int:
    if stop is None:
        stop = len(s)
    try:
        end_char = next(c for c in s[start:stop] if c in chars)
        return s.find(end_char, start, stop)
    except StopIteration:
        return stop
