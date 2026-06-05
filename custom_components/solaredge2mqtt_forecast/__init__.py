from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import SolarEdge2MQTTForecastCoordinator

SolarEdge2MQTTForecastConfigEntry = ConfigEntry[SolarEdge2MQTTForecastCoordinator]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SolarEdge2MQTTForecastConfigEntry,
) -> bool:
    coordinator = SolarEdge2MQTTForecastCoordinator(hass, entry)
    await coordinator.async_setup()

    entry.runtime_data = coordinator
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    entry.async_on_unload(coordinator.async_unload)

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: SolarEdge2MQTTForecastConfigEntry,
) -> bool:
    if isinstance(entry.runtime_data, SolarEdge2MQTTForecastCoordinator):
        entry.runtime_data.async_unload()

    domain_data = hass.data.get(DOMAIN)
    if isinstance(domain_data, dict):
        domain_data.pop(entry.entry_id, None)
        if not domain_data:
            hass.data.pop(DOMAIN, None)

    return True
