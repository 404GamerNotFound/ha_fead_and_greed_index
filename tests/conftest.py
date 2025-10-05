"""Global fixtures for the Fear and Greed tests."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Generator

import pytest

from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.core import HomeAssistant

from custom_components.fear_and_greed.const import DOMAIN


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Return a mock config entry."""
    return MockConfigEntry(domain=DOMAIN, title="Fear & Greed Index", data={}, version=2)


@pytest.fixture
def sample_api_payload() -> dict[str, Any]:
    """Provide a sample API payload resembling Alternative.me output."""
    now = int(datetime(2024, 1, 1, 12, 0, 0).timestamp())
    previous = int(datetime(2023, 12, 31, 12, 0, 0).timestamp())
    return {
        "data": [
            {
                "value": "56",
                "value_classification": "Greed",
                "timestamp": str(now),
            },
            {
                "value": "48",
                "value_classification": "Neutral",
                "timestamp": str(previous),
            },
        ]
    }
