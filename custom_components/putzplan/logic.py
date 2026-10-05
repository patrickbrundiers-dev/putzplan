"""Pure status logic for Putzplan tasks (no Home Assistant imports)."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from .const import (
    DUE_SOON_DAYS,
    STATUS_AS_NEEDED,
    STATUS_DUE_SOON,
    STATUS_OK,
    STATUS_OVERDUE,
    STATUS_UNKNOWN,
)


def parse_date(value: Any) -> date | None:
    """Parse an ISO date string (or date) to a date."""
    if value in (None, ""):
        return None
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def compute_status(task: dict[str, Any], today: date) -> dict[str, Any]:
    """Compute status and derived values for a task on a given day."""
    interval = task.get("interval_days") or None
    last = parse_date(task.get("last_done"))

    days_since = (today - last).days if last else None
    next_due = last + timedelta(days=interval) if (last and interval) else None
    days_until_due = (next_due - today).days if next_due else None
    days_overdue = max(0, -days_until_due) if days_until_due is not None else 0

    if interval is None:
        status = STATUS_AS_NEEDED
    elif last is None:
        status = STATUS_UNKNOWN
    elif days_until_due < 0:
        status = STATUS_OVERDUE
    elif days_until_due <= DUE_SOON_DAYS:
        status = STATUS_DUE_SOON
    else:
        status = STATUS_OK

    return {
        "status": status,
        "interval_days": interval,
        "last_done": last.isoformat() if last else None,
        "days_since_done": days_since,
        "next_due": next_due.isoformat() if next_due else None,
        "days_until_due": days_until_due,
        "days_overdue": days_overdue,
        "done_today": days_since == 0,
    }
