from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .coordinator import SolarEdge2MQTTForecastCoordinator

type SolarEdge2MQTTForecastConfigEntry = ConfigEntry[SolarEdge2MQTTForecastCoordinator]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SolarEdge2MQTTForecastConfigEntry,
) -> bool:
    coordinator = SolarEdge2MQTTForecastCoordinator(hass, entry)
    await coordinator.async_setup()
    entry.runtime_data = coordinator
    entry.async_on_unload(coordinator.async_unload)
    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: SolarEdge2MQTTForecastConfigEntry,
) -> bool:
    return True
