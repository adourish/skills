# Python Torrent Downloader

A simple command-line torrent downloader using libtorrent.

## Installation

```bash
pip install -r requirements.txt
```

**Note:** On Windows, you may need to install libtorrent via conda:
```bash
conda install -c conda-forge libtorrent
```

Or use pre-built wheels from: https://github.com/arvidn/libtorrent/releases

## Usage

### Download from .torrent file:
```bash
python torrent_downloader.py path/to/file.torrent
```

### Download from magnet link:
```bash
python torrent_downloader.py "magnet:?xt=urn:btih:HASH&dn=NAME&tr=TRACKER"
```

### Specify custom download directory:
```bash
python torrent_downloader.py file.torrent ./my_downloads
```

## Features

- ✓ Supports both .torrent files and magnet links
- ✓ DHT, PEX, and Local Service Discovery enabled
- ✓ Real-time progress display
- ✓ Shows download/upload speeds and peer count
- ✓ Automatic timeout handling
- ✓ Seeds for 30 seconds after completion

## Alternative: Using transmission-cli

If you prefer a command-line client without Python:

```bash
# Install transmission-cli
# Windows: Download from https://transmissionbt.com/
# Linux: sudo apt install transmission-cli
# macOS: brew install transmission-cli

# Download torrent
transmission-cli file.torrent -w ./downloads
```

## Alternative: Using aria2

```bash
# Install aria2
# Windows: choco install aria2
# Linux: sudo apt install aria2
# macOS: brew install aria2

# Download torrent
aria2c --seed-time=0 file.torrent
aria2c --seed-time=0 "magnet:?xt=urn:btih:..."
```

## Legal Notice

Only download content that you have the legal right to access. This tool is for educational purposes and legitimate use cases only.
