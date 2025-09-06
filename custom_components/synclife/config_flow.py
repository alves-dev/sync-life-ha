import logging

import voluptuous as vol
from homeassistant.config_entries import (
    HANDLERS,
    ConfigFlow,
    ConfigEntry,
    ConfigSubentryFlow,
    OptionsFlow)
from homeassistant.core import callback

from .const import (
    DOMAIN, CONF_ENTRY_NAME_DEFAULT, CONF_ENTRY_NAME,
)

_LOGGER = logging.getLogger(__name__)


@HANDLERS.register(DOMAIN)
class IntegrationConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @classmethod
    @callback
    def async_get_supported_subentry_types(
            cls, config_entry: ConfigEntry
    ) -> dict[str, type[ConfigSubentryFlow]]:
        """Return subentries supported by this integration."""
        return {
        }

    async def async_step_user(self, user_input=None):
        """Handle the initial setup step for the user."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_ENTRY_NAME],
                data={
                    CONF_ENTRY_NAME: user_input[CONF_ENTRY_NAME],
                }
            )

        data_schema = vol.Schema({
            vol.Required(CONF_ENTRY_NAME, default=CONF_ENTRY_NAME_DEFAULT): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry):
        """Get the options flow for this handler."""
        return IntegrationOptionsFlowHandler()


class IntegrationOptionsFlowHandler(OptionsFlow):
    def __init__(self) -> None:
        """Initialize options flow."""

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            self.hass.config_entries.async_update_entry(
                self.config_entry,
                title=user_input[CONF_ENTRY_NAME],
                data={
                    CONF_ENTRY_NAME: user_input[CONF_ENTRY_NAME],
                },
            )

            self.hass.async_create_task(
                self.hass.config_entries.async_reload(self.config_entry.entry_id)
            )

            return self.async_create_entry(title="", data={})

        current_data = self.config_entry.data

        data_schema = self.add_suggested_values_to_schema(
            vol.Schema({
                vol.Required(CONF_ENTRY_NAME): str,
            }),
            current_data
        )

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
            description_placeholders={
                "account_name": current_data.get(CONF_ENTRY_NAME, 'Account')
            }
        )
