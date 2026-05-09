# WatchDog 🐕

A lightweight, multi-threaded CCTV monitoring system with real-time object detection using YOLO.

## Features
- **Multi-threaded Streaming**: Efficiently handle multiple RTSP streams simultaneously.
- **Object Detection**: Integrated with YOLO for real-time detection (e.g., people, vehicles).
- **Native Notifications**: Desktop alerts for detected events (optimized for macOS via `osascript` and other platforms via `plyer`).
- **Resource Optimized**: Shared model instances across camera streams to minimize memory usage.

## Setup

### 1. Prerequisites
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended) or `pip`

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/amith-c/watchdog.git
cd watchdog

# Install dependencies
uv sync
```

### 3. Configuration
Create a `.env` file in the root directory based on `.env.format`:
```bash
cp .env.format .env
```
Edit `.env` with your DVR/NVR credentials and IP address.

## Usage

### Running the System
The main entry point is `main.py`. This starts the monitoring for configured cameras and displays a live feed.
```bash
uv run main.py
```

## Project Structure
- `core/camera.py`: Manages RTSP connections and threading.
- `core/detection.py`: YOLO model wrapper for object detection.
- `core/alerts.py`: Cross-platform desktop notification system.
- `main.py`: Entry point for the application.

## License
MIT
