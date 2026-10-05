"""Sensors for Putzplan: one per task plus an overdue counter."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from .const import DEFAULT_ICON, DOMAIN, SIGNAL_UPDATED, STATUS_DUE_SOON, STATUS_OVERDUE
from .logic import compute_status
from .manager import PutzplanManager

DEVICE_INFO = DeviceInfo(
    identifiers={(DOMAIN, "putzplan")},
    name="Putzplan",
    manufacturer="Putzplan",
    entry_type=DeviceEntryType.SERVICE,
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Create sensors and keep them in sync with the task list."""
    manager: PutzplanManager = hass.data[DOMAIN][entry.entry_id]
    known: set[str] = set()

    async_add_entities([PutzplanOverdueSensor(manager)])

    @callback
    def _sync() -> None:
        current = set(manager.tasks)
        new = [PutzplanTaskSensor(manager, task_id) for task_id in current - known]
        registry = er.async_get(hass)
        for task_id in known - current:
            entity_id = registry.async_get_entity_id(
                "sensor", DOMAIN, f"{DOMAIN}_{task_id}"
            )
            if entity_id:
                registry.async_remove(entity_id)
        known.clear()
        known.update(current)
        if new:
            async_add_entities(new)

    _sync()
    entry.async_on_unload(async_dispatcher_connect(hass, SIGNAL_UPDATED, _sync))


class PutzplanTaskSensor(SensorEntity):
    """State of one cleaning task: ok / due_soon / overdue / as_needed / unknown."""

    _attr_should_poll = False
    _attr_has_entity_name = True
    _attr_device_info = DEVICE_INFO

    def __init__(self, manager: PutzplanManager, task_id: str) -> None:
        self._manager = manager
        self._task_id = task_id
        self._attr_unique_id = f"{DOMAIN}_{task_id}"

    @property
    def _task(self) -> dict[str, Any] | None:
        return self._manager.tasks.get(self._task_id)

    @property
    def available(self) -> bool:
        return self._task is not None

    @property
    def name(self) -> str:
        task = self._task
        return task["name"] if task else self._task_id

    @property
    def icon(self) -> str:
        task = self._task
        return (task or {}).get("icon") or DEFAULT_ICON

    @property
    def native_value(self) -> str | None:
        task = self._task
        if task is None:
            return None
        return compute_status(task, dt_util.now().date())["status"]

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        task = self._task
        if task is None:
            return {}
        info = compute_status(task, dt_util.now().date())
        info.pop("status")
        return {
            "putzplan_task": True,
            "task_id": self._task_id,
            "task_name": task["name"],
            "room": task["room"],
            "previous_done": task.get("previous_done"),
            **info,
        }

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass, SIGNAL_UPDATED, self.async_write_ha_state
            )
        )


class PutzplanOverdueSensor(SensorEntity):
    """Number of overdue tasks – handy for notifications."""

    _attr_should_poll = False
    _attr_has_entity_name = True
    _attr_device_info = DEVICE_INFO
    _attr_name = "Overdue"
    _attr_icon = "mdi:broom"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, manager: PutzplanManager) -> None:
        self._manager = manager
        self._attr_unique_id = f"{DOMAIN}_overdue"

    def _statuses(self) -> list[tuple[dict[str, Any], dict[str, Any]]]:
        today = dt_util.now().date()
        return [(t, compute_status(t, today)) for t in self._manager.tasks.values()]

    @property
    def native_value(self) -> int:
        return sum(1 for _, s in self._statuses() if s["status"] == STATUS_OVERDUE)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        statuses = self._statuses()
        return {
            "total": len(statuses),
            "due_soon": sum(1 for _, s in statuses if s["status"] == STATUS_DUE_SOON),
            "overdue_tasks": [
                f"{t['room']}: {t['name']}"
                for t, s in statuses
                if s["status"] == STATUS_OVERDUE
            ],
        }

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass, SIGNAL_UPDATED, self.async_write_ha_state
            )
        )
