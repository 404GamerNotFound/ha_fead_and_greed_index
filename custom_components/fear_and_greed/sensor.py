"""Sensor platform for the Fear and Greed integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTR_CLASSIFICATION, DEFAULT_NAME, DOMAIN


@dataclass
class FearAndGreedEntityDescription:
    """Describe Fear and Greed sensors."""

    key: str
    name: str
    device_class: SensorDeviceClass | None = None
    native_unit_of_measurement: str | None = None


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up Fear and Greed sensors."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]

    sensors: list[SensorEntity] = [
        FearAndGreedIndexSensor(coordinator),
        FearAndGreedSentimentSensor(coordinator),
    ]

    async_add_entities(sensors)


class FearAndGreedBaseSensor(CoordinatorEntity, SensorEntity):
    """Base sensor for Fear and Greed data."""

    _attr_has_entity_name = True
    _attr_attribution = "Data provided by Alternative.me"

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_{self.entity_description.key}"

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, DOMAIN)},
            "name": DEFAULT_NAME,
            "manufacturer": "Alternative.me",
            "entry_type": "service",
        }


class FearAndGreedIndexSensor(FearAndGreedBaseSensor):
    """Sensor for the numeric index value."""

    entity_description = FearAndGreedEntityDescription(
        key="index",
        name="Index",
        device_class=SensorDeviceClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
    )

    @property
    def native_value(self) -> int | None:
        index = self.coordinator.data
        return index.value if index else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        index = self.coordinator.data
        if not index:
            return {}
        return {
            **index.as_sensor_attributes,
            ATTR_CLASSIFICATION: index.classification,
        }


class FearAndGreedSentimentSensor(FearAndGreedBaseSensor):
    """Sensor for the textual sentiment classification."""

    entity_description = FearAndGreedEntityDescription(
        key="sentiment",
        name="Sentiment",
    )

    @property
    def native_value(self) -> str | None:
        index = self.coordinator.data
        return index.classification if index else None

    @property
    def icon(self) -> str:
        index = self.coordinator.data
        if not index:
            return "mdi:help-circle"
        classification = index.classification.lower()
        if "extreme" in classification and "fear" in classification:
            return "mdi:emoticon-dead-outline"
        if "fear" in classification:
            return "mdi:emoticon-sad-outline"
        if "greed" in classification and "extreme" in classification:
            return "mdi:emoticon-devil-outline"
        if "greed" in classification:
            return "mdi:emoticon-excited-outline"
        return "mdi:emoticon-neutral-outline"
