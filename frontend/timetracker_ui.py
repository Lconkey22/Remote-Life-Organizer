"""Pure-Python HTML rendering helpers for the Time Tracker page.

This module intentionally avoids NiceGUI imports to keep it unit-testable.
"""

from __future__ import annotations

from dataclasses import dataclass
from html import escape


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


@dataclass(frozen=True, slots=True)
class TimeTrackerSection:
    """A logical grouping for a rendered chart section (e.g. Work/School)."""

    title: str
    blocks: tuple[TimeBlock, ...]


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
            tooltip = escape(block.label or "")
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
