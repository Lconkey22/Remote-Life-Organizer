"""Unit tests for the Time Tracker pure-Python renderer."""

from __future__ import annotations

from frontend.timetracker_ui import (
    TimeBlock,
    TimeTrackerSection,
    build_time_axis_labels,
    render_week_timeline_html,
)


def test_build_time_axis_labels_8_to_15() -> None:
    """Axis labels should use 12-hour formatting and include the end tick."""
    assert build_time_axis_labels(8, 15) == ["8", "9", "10", "11", "12", "1", "2", "3"]


def test_render_week_timeline_contains_day_labels() -> None:
    """Rendered HTML should include all day labels."""
    section = TimeTrackerSection(title="Work/School", blocks=())
    html = render_week_timeline_html(section)
    for day in ("Sun.", "Mon.", "Tue.", "Wed.", "Th.", "Fri.", "Sat."):
        assert day in html


def test_render_week_timeline_contains_section_title() -> None:
    """Rendered HTML should include the section title."""
    section = TimeTrackerSection(title="Homework", blocks=())
    html = render_week_timeline_html(section)
    assert "Homework" in html


def test_render_week_timeline_renders_bars() -> None:
    """Rendered HTML should include bar elements when blocks are provided."""
    section = TimeTrackerSection(
        title="Self Care",
        blocks=(TimeBlock(day_index=1, start_min=60, end_min=120, label="Demo"),),
    )
    html = render_week_timeline_html(section)
    assert "tt-bar" in html
