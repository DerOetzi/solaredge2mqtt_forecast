from __future__ import annotations

from homeassistant.core import HomeAssistant

from .coordinator import SolarEdge2MQTTForecastCoordinator


async def async_get_solar_forecast(
    hass: HomeAssistant,
    config_entry_id: str,
) -> dict[str, dict[str, float | int]] | None:
    entry = hass.config_entries.async_get_entry(config_entry_id)

    if entry is None or not isinstance(
        entry.runtime_data,
        SolarEdge2MQTTForecastCoordinator,
    ):
        return None

    return {
        "wh_hours": {
            timestamp.isoformat(): value
            for timestamp, value in entry.runtime_data.data.wh_period.items()
            if value != 0
            or (timestamp.hour, timestamp.minute, timestamp.second) != (0, 0, 0)
        }
    }
