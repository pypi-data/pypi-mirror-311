# Nomad Media CLI Tool

Command line interface for managing Nomad Media media assets.

## Installation

```bash
pip install nomad-media-cli
```

## Configuration
- Default config location: %APPDATA%\Local\nomad_media_cli\config.json
- Custom config location: Use --config-path option

## Commands

### init
Initializes CLI configuration

Options:
- `--username`: Login username (required)
- `--password`: Login password (required)
- `--service-api-url`: API endpoint URL (required)
- `--api-type`: API type [admin|portal]
- `--debug-mode`: Enable debug logging [true|false]
- `--singleton`: Enable singleton mode [true|false]

### update-config
Updates CLI configuration

Options:
- `--username`: Login username
- `--password`: Login password
- `--service-api-url`: API endpoint URL
- `--api-type`: API type [admin|portal]
- `--debug-mode`: Enable debug logging [true|false]
- `--singleton`: Enable singleton mode [true|false]

### list-assets
List assets by ID or path

Options:
- `--id`: Asset UUID, collection ID, or saved search ID
- `--path`: Object key path (format: bucket::path)