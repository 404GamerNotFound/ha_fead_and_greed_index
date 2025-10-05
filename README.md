# Fear and Greed Index for Home Assistant

A Home Assistant custom integration that exposes the Alternative.me Fear and Greed Index as rich sensor entities. The project is compatible with [HACS](https://hacs.xyz/) and includes automated tests to ensure ongoing quality.

## Features

- ✅ Numeric sensor with the latest Fear & Greed value and attribution metadata
- ✅ Sentiment sensor showing the textual classification (e.g. "Extreme Greed")
- ✅ Historical comparison attributes for the previous value, absolute and percentage change
- ✅ Config flow with UI-based setup and configurable polling interval
- ✅ Manual refresh service (`fear_and_greed.refresh`) for dashboards and automations
- ✅ Diagnostics-ready architecture using Home Assistant's DataUpdateCoordinator
- ✅ Fully typed code base with translations for English and German

## Installation via HACS

1. Open HACS in Home Assistant and choose **Integrations**.
2. Use the menu to add a **Custom repository** and enter `https://github.com/ha_fead_and_greed_index` with category **Integration**.
3. Search for **Fear and Greed Index** and install it.
4. Restart Home Assistant.
5. Add the integration via **Settings → Devices & Services → Add Integration** and search for "Fear and Greed Index".

## Manual Installation

1. Copy the `custom_components/fear_and_greed` directory into your Home Assistant `custom_components` folder.
2. Restart Home Assistant.
3. Add the integration through the UI.

## Services

- `fear_and_greed.refresh`: Triggers an immediate data refresh.

## Development

### Requirements

Install the test dependencies inside your development environment:

```bash
pip install -r requirements_test.txt
```

### Running the Tests

```bash
pytest
```

### Releasing

1. Update the version number inside `custom_components/fear_and_greed/manifest.json`.
2. Create a new release in GitHub so HACS users receive the update.

## License

This project is licensed under the terms of the [MIT License](LICENSE).
