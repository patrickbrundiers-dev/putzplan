"""Task storage and manipulation for Putzplan."""

from __future__ import annotations

from datetime import date
import uuid
from typing import Any

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.storage import Store

from .const import (
    DEFAULT_ICON,
    DEFAULT_TASKS,
    SIGNAL_UPDATED,
    STORAGE_KEY,
    STORAGE_VERSION,
)


class PutzplanManager:
    """Holds all tasks and persists them."""

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass
        self._store: Store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
        self.tasks: dict[str, dict[str, Any]] = {}
        self.seeded = False

    async def async_load(self) -> None:
        data = await self._store.async_load() or {}
        self.tasks = {t["id"]: t for t in data.get("tasks", [])}
        self.seeded = bool(data.get("seeded", False))

    def _data(self) -> dict[str, Any]:
        return {"tasks": list(self.tasks.values()), "seeded": self.seeded}

    @callback
    def _changed(self) -> None:
        self._store.async_delay_save(self._data, 1)
        self.notify()

    @callback
    def notify(self) -> None:
        """Tell all entities to refresh (also called at midnight)."""
        async_dispatcher_send(self.hass, SIGNAL_UPDATED)

    @callback
    def seed_defaults(self, german: bool) -> None:
        """Create the example tasks once."""
        for room_de, room_en, name_de, name_en, icon, interval in DEFAULT_TASKS:
            self._add(
                name=name_de if german else name_en,
                room=room_de if german else room_en,
                icon=icon,
                interval_days=interval,
                last_done=None,
            )
        self.seeded = True
        self._changed()

    def _add(
        self,
        name: str,
        room: str,
        icon: str | None,
        interval_days: int | None,
        last_done: date | None,
    ) -> str:
        task_id = uuid.uuid4().hex[:8]
        self.tasks[task_id] = {
            "id": task_id,
            "name": name,
            "room": room,
            "icon": icon or DEFAULT_ICON,
            "interval_days": interval_days or None,
            "last_done": last_done.isoformat() if last_done else None,
            "previous_done": None,
        }
        return task_id

    @callback
    def add_task(
        self,
        name: str,
        room: str,
        icon: str | None = None,
        interval_days: int | None = None,
        last_done: date | None = None,
    ) -> str:
        task_id = self._add(name, room, icon, interval_days, last_done)
        self._changed()
        return task_id

    @callback
    def update_task(self, task_id: str, **fields: Any) -> None:
        task = self.tasks[task_id]
        for key in ("name", "room", "icon"):
            if fields.get(key) is not None:
                task[key] = fields[key]
        if "interval_days" in fields and fields["interval_days"] is not None:
            task["interval_days"] = fields["interval_days"] or None
        if fields.get("last_done") is not None:
            task["previous_done"] = task.get("last_done")
            task["last_done"] = fields["last_done"].isoformat()
        self._changed()

    @callback
    def remove_task(self, task_id: str) -> None:
        self.tasks.pop(task_id, None)
        self._changed()

    @callback
    def mark_done(self, task_id: str, day: date) -> None:
        task = self.tasks[task_id]
        task["previous_done"] = task.get("last_done")
        task["last_done"] = day.isoformat()
        self._changed()

    @callback
    def undo_done(self, task_id: str) -> None:
        task = self.tasks[task_id]
        task["last_done"] = task.get("previous_done")
        task["previous_done"] = None
        self._changed()
