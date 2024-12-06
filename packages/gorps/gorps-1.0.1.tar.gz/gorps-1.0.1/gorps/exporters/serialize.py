"""Serializing utilities."""

from datetime import timedelta


def fmt_time(t: timedelta) -> str:
    secs = int(t.total_seconds())
    h = secs // 3600
    secs %= 3600
    m = secs // 60
    secs %= 60
    if h > 0:
        if secs > 0:
            return f"{h}:{m:02}:{secs:02} h"
        if m > 0:
            return f"{h}:{m:02} h"
        return f"{h} h"
    if m > 0:
        if secs > 0:
            return f"{m}:{secs:02} min"
        return f"{m} min"
    return f"{secs} sec"
