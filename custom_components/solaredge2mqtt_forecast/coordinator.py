from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback

from .const import CONF_TOPIC, DEFAULT_TOPIC

_LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class ForecastData:
    wh_period: dict[datetime, int] = field(default_factory=dict)
    power_period: dict[datetime, int] = field(default_factory=dict)


class SolarEdge2MQTTForecastCoordinator:
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self.entry = entry
        self.data = ForecastData()
        self._unsubscribe: mqtt.UnsubscribeCallback | None = None

    async def async_setup(self) -> None:
        topic = self.entry.data.get(CONF_TOPIC, DEFAULT_TOPIC)

        self._unsubscribe = await mqtt.async_subscribe(
            self.hass,
            topic,
            self._message_received,
            qos=0,
            encoding="utf-8",
        )

    @callback
    def _message_received(self, message: mqtt.ReceiveMessage) -> None:
        try:
            payload = json.loads(message.payload)
        except (TypeError, json.JSONDecodeError) as err:
            _LOGGER.warning("Invalid forecast payload JSON: %s", err)
            return

        self.data = ForecastData(
            wh_period=self._parse_period(payload.get("energy_period")),
            power_period=self._parse_period(payload.get("power_period")),
        )

    @staticmethod
    def _parse_period(value: Any) -> dict[datetime, int]:
        if not isinstance(value, dict):
            return {}

        result: dict[datetime, int] = {}

        for raw_timestamp, raw_value in value.items():
            try:
                timestamp = datetime.fromisoformat(str(raw_timestamp))
                forecast_value = int(raw_value)
            except (TypeError, ValueError):
                continue

            result[timestamp] = max(0, forecast_value)

        return dict(sorted(result.items()))

    @callback
    def async_unload(self) -> None:
        if self._unsubscribe is not None:
            self._unsubscribe()
            self._unsubscribe = None
