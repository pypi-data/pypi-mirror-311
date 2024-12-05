# Nomad Media CLI Tool

Command line interface for managing Nomad Media media assets.

## Installation

```bash
pip install nomad-media-cli
```

## Commands

### init
Initialize or update CLI configuration

Options:
- `--username`: Login username (required)
- `--password`: Login password (required)
- `--service-api-url`: API endpoint URL (required)
- `--api-type`: API type [admin|portal]
- `--debug-mode`: Enable debug logging
- `--singleton`: Enable singleton mode

### list-assets
List assets by ID or path

Options:
- `--id`: Asset UUID, collection ID, or saved search ID
- `--path`: Object key path (format: bucket::path)