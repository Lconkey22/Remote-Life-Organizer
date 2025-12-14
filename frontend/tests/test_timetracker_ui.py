"""Unit tests for the Time Tracker pure-Python renderer."""

from __future__ import annotations

from datetime import date

from frontend.timetracker_ui import (
    TimeBlock,
    TimeTrackerSection,
    build_sections_from_api,
    build_time_axis_labels,
    render_week_timeline_html,
    week_start_sunday,
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


def test_week_start_sunday_returns_same_day_for_sunday() -> None:
    """A Sunday should map to itself."""
    assert week_start_sunday(date(2025, 12, 14)) == date(2025, 12, 14)


def test_week_start_sunday_rolls_back_for_monday() -> None:
    """A Monday should map back to the previous Sunday."""
    assert week_start_sunday(date(2025, 12, 15)) == date(2025, 12, 14)


def test_build_sections_from_api_groups_events_and_time_entries() -> None:
    """Events and time entries should merge into the same section by type."""
    week_start = date(2025, 12, 14)  # Sunday

    events = [
        {
            "id": 1,
            "name": "Office Hours",
            "type": "Work",
            "start_time": "2025-12-16T10:00:00",
            "end_time": "2025-12-16T12:00:00",
        }
    ]
    time_entries = [
        {
            "id": 1,
            "type": "Work",
            "start_time": "2025-12-16T09:00:00",
            "end_time": "2025-12-16T09:30:00",
            "note": "Deep work",
        }
    ]

    sections = build_sections_from_api(
        events=events, time_entries=time_entries, week_start=week_start
    )
    sections_by_title = {s.title: s for s in sections}

    assert set(sections_by_title.keys()) == {"Work"}
    work = sections_by_title["Work"]
    assert len(work.blocks) == 2

    # Tuesday == day_index 2 when week_start is Sunday.
    assert all(b.day_index == 2 for b in work.blocks)
    # 9am -> 60 mins from 8am chart start; 10am -> 120 mins.
    assert any(
        b.start_min == 60 and b.end_min == 90 and b.label == "Deep work"
        for b in work.blocks
    )
    assert any(
        b.start_min == 120 and b.end_min == 240 and b.label == "Office Hours"
        for b in work.blocks
    )


def test_render_week_timeline_renders_tooltip_with_label_and_time() -> None:
    """Rendered HTML should use tooltip text for hover details."""

    week_start = date(2025, 12, 14)  # Sunday
    time_entries = [
        {
            "id": 1,
            "type": "Work",
            "start_time": "2025-12-16T09:00:00",
            "end_time": "2025-12-16T09:30:00",
            "note": "Deep work",
        }
    ]

    sections = build_sections_from_api(events=[], time_entries=time_entries, week_start=week_start)
    html = render_week_timeline_html(sections[0])
    assert 'title="Deep work — 9:00 AM–9:30 AM"' in html
