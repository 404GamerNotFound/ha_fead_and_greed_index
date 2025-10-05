"""Constants for the Fear and Greed integration."""

from __future__ import annotations

DOMAIN = "fear_and_greed"
COORDINATOR_NAME = "Fear and Greed Index"
DEFAULT_NAME = "Fear & Greed Index"
PLATFORMS = ["sensor"]
UPDATE_INTERVAL = 3600  # seconds
API_ENDPOINT = "https://api.alternative.me/fng/"
SERVICE_REFRESH = "refresh"

ATTR_CLASSIFICATION = "classification"
ATTR_PREVIOUS_VALUE = "previous_value"
ATTR_CHANGE = "value_change"
ATTR_CHANGE_PERCENT = "value_change_percent"

CONF_UPDATE_INTERVAL = "update_interval"

ISSUE_URL = "https://github.com/ha_fead_and_greed_index/issues"

# The Alternative.me API exposes the following keys that we use here.
JSON_VALUE = "value"
JSON_VALUE_CLASSIFICATION = "value_classification"
JSON_TIMESTAMP = "timestamp"

# HACS metadata
INTEGRATION_TITLE = "Fear and Greed Index"
