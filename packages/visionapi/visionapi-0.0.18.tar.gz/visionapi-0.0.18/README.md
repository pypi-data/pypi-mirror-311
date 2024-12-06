# VisionAPI

A comprehensive Python library providing utilities and tools for computer vision tasks, focusing on camera handling, video processing, and integration with popular ML frameworks.

## Features

- Multi-camera support with simultaneous streaming and recording
- Video editing utilities (concatenation, trimming, etc.)
- Easy integration with Ultralytics YOLO models
- Real-time visualization tools
- Configurable camera settings and display options

## Installation

```bash
pip install visionapi
```

## Quick Start

### Multi-Camera Handling

Easily manage multiple camera streams with the `CameraApp` class:

```python
from visionapi.camera_loader import CameraApp, CameraConfig
import cv2

# Configure camera settings
config = CameraConfig(
    width=1280,
    height=720,
    fps=60,
    show_window=True
)

# Initialize and use cameras
with CameraApp(config) as app:
    # Detect and load cameras
    available_cameras = app.detect_cameras()
    num_loaded = app.load_cameras(available_cameras)
    
    # Start recording with custom camera names
    output_folder = app.start_recording(["Front", "Back"])
    
    # Main capture loop
    while True:
        frames = app.capture_frame()
        # Process frames here
        
        # Exit on 'q' press (requires show_window=True)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Clean up
    app.stop_recording()
```

### Video Editing

Combine multiple video streams:

```python
from visiontools.video_editing import concat_videos

# Concatenate videos horizontally
concat_videos(
    input_videos=['cam0.mp4', 'cam1.mp4', 'cam2.mp4'],
    output_path='concatenated_video.mp4',
    direction='horizontal'
)
```

### YOLO Integration

VisionAPI provides convenient utilities for working with Ultralytics YOLO models:

#### Single Image Analysis
```python
from ultralytics import YOLO
from visionapi import quick_display

model = YOLO("yolov8n.pt")
results = model("cats.jpg", verbose=False)
quick_display(results, ultralytics_results=True)
```

#### Single Video Analysis
```python
from ultralytics import YOLO
from visionapi import quick_display

model = YOLO("yolov8n.pt")
results = model("videos/cam0.mp4", verbose=False)
quick_display(results, ultralytics_results=True)
```

#### Multi-Camera Analysis
```python
from ultralytics import YOLO
from visionapi import quick_display

# Process multiple video streams
videos_list = ["videos/cam0.mp4", "videos/cam1.mp4", "videos/cam2.mp4"]
model = YOLO("yolov8n.pt")

results = {
    f"camera{i}": model(video, verbose=False)
    for i, video in enumerate(videos_list)
}

quick_display(results, ultralytics_results=True, multicam=True)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.