"""Config flow for Putzplan."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .const import CONF_SEED, DOMAIN


class PutzplanConfigFlow(ConfigFlow, domain=DOMAIN):
    """Single-instance setup flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        if user_input is not None:
            return self.async_create_entry(
                title="Putzplan", data={CONF_SEED: user_input[CONF_SEED]}
            )
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_SEED, default=True): bool}),
        )
