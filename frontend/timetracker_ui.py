"""Pure-Python HTML rendering helpers for the Time Tracker page.

This module intentionally avoids NiceGUI imports to keep it unit-testable.
"""

from __future__ import annotations

from datetime import date, datetime, time, timedelta
from dataclasses import dataclass
from html import escape
from typing import Any, Iterable


DAYS_SHORT: tuple[str, ...] = ("Sun.", "Mon.", "Tue.", "Wed.", "Th.", "Fri.", "Sat.")


@dataclass(frozen=True, slots=True)
class TimeBlock:
    """A time span within a Day/Week/Month chart.

    Times are represented as minutes from the chart start (e.g. 8:00am == 0).
    """

    day_index: int
    start_min: int
    end_min: int
    label: str | None = None
    tooltip: str | None = None


@dataclass(frozen=True, slots=True)
class TimeTrackerSection:
    """A logical grouping for a rendered chart section (e.g. Work/School)."""

    title: str
    blocks: tuple[TimeBlock, ...]


def week_start_sunday(day: date) -> date:
    """Return the Sunday for the week containing `day`."""

    days_since_sunday = (day.weekday() + 1) % 7  # Mon=0..Sun=6 -> Sun=0
    return day - timedelta(days=days_since_sunday)


def _parse_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        # FastAPI returns ISO 8601 strings; these are parseable by fromisoformat.
        return datetime.fromisoformat(value)
    raise TypeError(f"Unsupported datetime value: {type(value)!r}")


def _minutes_from_chart_start(dt: datetime, *, start_hour: int) -> int:
    start_dt = datetime.combine(dt.date(), time(hour=start_hour))
    return int((dt - start_dt).total_seconds() // 60)


def _format_12h_from_chart_minutes(minutes_from_chart_start: int, *, start_hour: int) -> str:
    """Format minutes from chart start (start_hour:00) into 12-hour time."""

    anchor = datetime(2000, 1, 1, start_hour, 0)
    t = anchor + timedelta(minutes=int(minutes_from_chart_start))
    return t.strftime("%I:%M %p").lstrip("0")


def _coerce_same_day_span(start_dt: datetime, end_dt: datetime) -> tuple[datetime, datetime]:
    """Clamp a span to the start day if it crosses midnight."""

    if start_dt.date() == end_dt.date():
        return start_dt, end_dt
    end_of_start_day = datetime.combine(start_dt.date(), time.max).replace(microsecond=0)
    return start_dt, end_of_start_day


@dataclass(frozen=True, slots=True)
class _SpanBlockContext:
    blocks_by_title: dict[str, list[TimeBlock]]
    week_start: date
    start_hour: int


def _add_span_block(
    ctx: _SpanBlockContext,
    *,
    title: str,
    start_dt: datetime,
    end_dt: datetime,
    label: str,
) -> None:
    start_dt, end_dt = _coerce_same_day_span(start_dt, end_dt)

    day_index = (start_dt.date() - ctx.week_start).days
    if not 0 <= day_index < 7:
        return

    start_min = _minutes_from_chart_start(start_dt, start_hour=ctx.start_hour)
    end_min = _minutes_from_chart_start(end_dt, start_hour=ctx.start_hour)
    start_str = _format_12h_from_chart_minutes(start_min, start_hour=ctx.start_hour)
    end_str = _format_12h_from_chart_minutes(end_min, start_hour=ctx.start_hour)

    if label:
        tooltip = f"{label} — {start_str}–{end_str}"
    else:
        tooltip = f"{start_str}–{end_str}"

    ctx.blocks_by_title.setdefault(title, []).append(
        TimeBlock(
            day_index=day_index,
            start_min=start_min,
            end_min=end_min,
            label=label,
            tooltip=tooltip,
        )
    )


def build_sections_from_api(
    *,
    events: Iterable[dict[str, Any]],
    time_entries: Iterable[dict[str, Any]],
    week_start: date,
    start_hour: int = 8,
) -> list[TimeTrackerSection]:
    """Convert API events/time-entries into timeline-renderable sections."""

    blocks_by_title: dict[str, list[TimeBlock]] = {}
    ctx = _SpanBlockContext(
        blocks_by_title=blocks_by_title, week_start=week_start, start_hour=start_hour
    )

    for event in events:
        start_dt = _parse_datetime(event["start_time"])
        end_dt = _parse_datetime(event["end_time"])
        _add_span_block(
            ctx,
            title=str(event.get("type") or "Other"),
            start_dt=start_dt,
            end_dt=end_dt,
            label=str(event.get("name") or ""),
        )

    for entry in time_entries:
        start_dt = _parse_datetime(entry["start_time"])
        end_dt = _parse_datetime(entry["end_time"])
        note = entry.get("note")
        label = str(note) if note else str(entry.get("type") or "")
        _add_span_block(
            ctx,
            title=str(entry.get("type") or "Other"),
            start_dt=start_dt,
            end_dt=end_dt,
            label=label,
        )

    sections: list[TimeTrackerSection] = []
    for title, blocks in blocks_by_title.items():
        blocks.sort(key=lambda b: (b.day_index, b.start_min, b.end_min))
        sections.append(TimeTrackerSection(title=title, blocks=tuple(blocks)))

    sections.sort(key=lambda s: s.title.lower())
    return sections


def build_time_axis_labels(start_hour: int, end_hour: int) -> list[str]:
    """Build 12-hour clock labels from start_hour..end_hour inclusive.

    Example: start_hour=8, end_hour=15 => ["8","9","10","11","12","1","2","3"]
    """

    if start_hour < 0 or end_hour < 0 or end_hour < start_hour:
        raise ValueError("Invalid hour range")

    labels: list[str] = []
    for hour in range(start_hour, end_hour + 1):
        hour_12 = hour % 12
        if hour_12 == 0:
            hour_12 = 12
        labels.append(str(hour_12))
    return labels


def _clamp_int(value: int, min_value: int, max_value: int) -> int:
    return max(min_value, min(value, max_value))


def _group_blocks_by_day(blocks: tuple[TimeBlock, ...]) -> list[list[TimeBlock]]:
    blocks_by_day: list[list[TimeBlock]] = [[] for _ in range(7)]
    for block in blocks:
        if 0 <= block.day_index < 7:
            blocks_by_day[block.day_index].append(block)
    return blocks_by_day


def _render_day_col_html() -> str:
    parts: list[str] = []
    parts.append('<div class="tt-day-col">')
    for day in DAYS_SHORT:
        parts.append(f'<div class="tt-day-label">{escape(day)}</div>')
    parts.append('<div class="tt-day-label tt-day-label-axis">&nbsp;</div>')
    parts.append("</div>")
    return "".join(parts)


def _render_rows_html(blocks_by_day: list[list[TimeBlock]], total_minutes: int) -> str:
    parts: list[str] = []
    for day_index in range(7):
        parts.append('<div class="tt-row">')
        for block in blocks_by_day[day_index]:
            start_min = _clamp_int(int(block.start_min), 0, total_minutes)
            end_min = _clamp_int(int(block.end_min), 0, total_minutes)
            if end_min <= start_min:
                continue

            left_pct = (start_min / total_minutes) * 100
            width_pct = ((end_min - start_min) / total_minutes) * 100
            tooltip = escape(block.tooltip or block.label or "")
            parts.append(
                (
                    '<div class="tt-bar" '
                    f'style="left:{left_pct:.4f}%;width:{width_pct:.4f}%;" '
                    f'title="{tooltip}"></div>'
                )
            )
        parts.append("</div>")
    return "".join(parts)


def _render_axis_html(axis_labels: list[str]) -> str:
    parts: list[str] = []
    parts.append('<div class="tt-axis">')
    for label in axis_labels:
        parts.append(f'<div class="tt-axis-label">{escape(label)}</div>')
    parts.append("</div>")
    return "".join(parts)


def render_week_timeline_html(
    section: TimeTrackerSection,
    *,
    start_hour: int = 8,
    end_hour: int = 15,
) -> str:
    """Render a weekly timeline chart as a single HTML string.

    Output expects CSS classes defined in `frontend/theme.py`.
    """

    axis_labels = build_time_axis_labels(start_hour, end_hour)
    hours = len(axis_labels)
    total_minutes = hours * 60
    blocks_by_day = _group_blocks_by_day(section.blocks)

    title = escape(section.title)

    parts: list[str] = []
    parts.append('<div class="tt-section-card">')
    parts.append(f'<div class="tt-section-title">{title}</div>')
    parts.append('<div class="tt-chart">')
    parts.append(_render_day_col_html())

    parts.append('<div class="tt-grid-scroll">')
    parts.append(f'<div class="tt-grid" style="--tt-hours:{hours};">')
    parts.append(_render_rows_html(blocks_by_day, total_minutes))
    parts.append(_render_axis_html(axis_labels))
    parts.append("</div>")  # .tt-grid
    parts.append("</div>")  # .tt-grid-scroll
    parts.append("</div>")  # .tt-chart
    parts.append("</div>")  # .tt-section-card

    return "".join(parts)


# Demo-only: remove when backend wiring is added.
def get_demo_sections() -> list[TimeTrackerSection]:
    """Return demo-only sections used for the initial UI layout."""

    def block(
        day: int,
        start_hour: int,
        start_minute: int,
        end_hour: int,
        end_minute: int,
    ) -> TimeBlock:
        """Create a demo time block relative to an 8am chart start."""

        start = ((start_hour - 8) * 60) + start_minute
        end = ((end_hour - 8) * 60) + end_minute
        return TimeBlock(day_index=day, start_min=start, end_min=end, label="Demo")

    work_school = TimeTrackerSection(
        title="Work/School",
        blocks=(
            block(1, 9, 0, 12, 0),
            block(2, 10, 0, 12, 30),
            block(3, 9, 30, 11, 30),
            block(4, 12, 0, 15, 0),
            block(5, 10, 0, 13, 0),
        ),
    )

    homework = TimeTrackerSection(
        title="Homework",
        blocks=(
            block(1, 8, 30, 10, 0),
            block(2, 9, 0, 11, 0),
            block(4, 10, 30, 12, 30),
            block(5, 9, 30, 12, 0),
        ),
    )

    self_care = TimeTrackerSection(
        title="Self Care",
        blocks=(
            block(1, 12, 0, 13, 0),
            block(2, 13, 0, 14, 0),
            block(4, 11, 0, 12, 0),
            block(6, 10, 0, 11, 0),
        ),
    )

    return [work_school, homework, self_care]
