"""Putzplan – a cleaning schedule for Home Assistant."""

from __future__ import annotations

from datetime import date
import logging
from pathlib import Path
from typing import Any

import voluptuous as vol

from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall, callback
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.event import async_track_time_change
from homeassistant.util import dt as dt_util

from .const import (
    CONF_SEED,
    DOMAIN,
    FRONTEND_CARD_FILE,
    FRONTEND_URL_BASE,
    VERSION,
)
from .manager import PutzplanManager

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]

SERVICES = ("mark_done", "undo_done", "add_task", "update_task", "remove_task")

ENTITY_IDS = vol.Required("entity_id")
INTERVAL = vol.All(vol.Coerce(int), vol.Range(min=0, max=3650))

SCHEMA_MARK_DONE = vol.Schema(
    {ENTITY_IDS: cv.entity_ids, vol.Optional("date"): cv.date}
)
SCHEMA_ENTITIES = vol.Schema({ENTITY_IDS: cv.entity_ids})
SCHEMA_ADD = vol.Schema(
    {
        vol.Required("name"): cv.string,
        vol.Required("room"): cv.string,
        vol.Optional("icon"): cv.icon,
        vol.Optional("interval_days"): INTERVAL,
        vol.Optional("last_done"): cv.date,
    }
)
SCHEMA_UPDATE = vol.Schema(
    {
        ENTITY_IDS: cv.entity_ids,
        vol.Optional("name"): cv.string,
        vol.Optional("room"): cv.string,
        vol.Optional("icon"): cv.icon,
        vol.Optional("interval_days"): INTERVAL,
        vol.Optional("last_done"): cv.date,
    }
)


def _manager(hass: HomeAssistant) -> PutzplanManager:
    manager = hass.data.get(DOMAIN, {}).get("manager")
    if manager is None:
        raise ServiceValidationError("Putzplan is not set up")
    return manager


def _task_ids(hass: HomeAssistant, entity_ids: list[str]) -> list[str]:
    """Map entity ids to task ids via the entity registry."""
    registry = er.async_get(hass)
    manager = _manager(hass)
    result: list[str] = []
    for entity_id in entity_ids:
        entry = registry.async_get(entity_id)
        if entry is None or entry.platform != DOMAIN or not entry.unique_id:
            raise ServiceValidationError(f"{entity_id} is not a Putzplan task")
        task_id = entry.unique_id.removeprefix(f"{DOMAIN}_")
        if task_id not in manager.tasks:
            raise ServiceValidationError(f"{entity_id} is not a Putzplan task")
        result.append(task_id)
    return result


def _register_services(hass: HomeAssistant) -> None:
    async def mark_done(call: ServiceCall) -> None:
        day: date = call.data.get("date") or dt_util.now().date()
        manager = _manager(hass)
        for task_id in _task_ids(hass, call.data["entity_id"]):
            manager.mark_done(task_id, day)

    async def undo_done(call: ServiceCall) -> None:
        manager = _manager(hass)
        for task_id in _task_ids(hass, call.data["entity_id"]):
            manager.undo_done(task_id)

    async def add_task(call: ServiceCall) -> None:
        _manager(hass).add_task(
            name=call.data["name"],
            room=call.data["room"],
            icon=call.data.get("icon"),
            interval_days=call.data.get("interval_days"),
            last_done=call.data.get("last_done"),
        )

    async def update_task(call: ServiceCall) -> None:
        manager = _manager(hass)
        fields: dict[str, Any] = {
            key: call.data[key]
            for key in ("name", "room", "icon", "interval_days", "last_done")
            if key in call.data
        }
        for task_id in _task_ids(hass, call.data["entity_id"]):
            manager.update_task(task_id, **fields)

    async def remove_task(call: ServiceCall) -> None:
        manager = _manager(hass)
        for task_id in _task_ids(hass, call.data["entity_id"]):
            manager.remove_task(task_id)

    hass.services.async_register(DOMAIN, "mark_done", mark_done, SCHEMA_MARK_DONE)
    hass.services.async_register(DOMAIN, "undo_done", undo_done, SCHEMA_ENTITIES)
    hass.services.async_register(DOMAIN, "add_task", add_task, SCHEMA_ADD)
    hass.services.async_register(DOMAIN, "update_task", update_task, SCHEMA_UPDATE)
    hass.services.async_register(DOMAIN, "remove_task", remove_task, SCHEMA_ENTITIES)


async def _register_frontend(hass: HomeAssistant) -> None:
    """Serve the card and load it on every dashboard."""
    domain_data = hass.data.setdefault(DOMAIN, {})
    if domain_data.get("frontend"):
        return
    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                FRONTEND_URL_BASE,
                str(Path(__file__).parent / "frontend"),
                False,
            )
        ]
    )
    add_extra_js_url(hass, f"{FRONTEND_URL_BASE}/{FRONTEND_CARD_FILE}?v={VERSION}")
    domain_data["frontend"] = True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Putzplan from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    manager = PutzplanManager(hass)
    await manager.async_load()
    if not manager.seeded and entry.data.get(CONF_SEED, True):
        manager.seed_defaults(german=hass.config.language.startswith("de"))
    hass.data[DOMAIN]["manager"] = manager
    hass.data[DOMAIN][entry.entry_id] = manager

    await _register_frontend(hass)
    _register_services(hass)

    # Day changes at midnight: refresh "days ago" and overdue states.
    @callback
    def _midnight(_now: Any) -> None:
        manager.notify()

    entry.async_on_unload(
        async_track_time_change(hass, _midnight, hour=0, minute=0, second=10)
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id, None)
        hass.data[DOMAIN].pop("manager", None)
        for service in SERVICES:
            hass.services.async_remove(DOMAIN, service)
    return unloaded
