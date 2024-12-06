import numpy as np
from visiontools.camera_loader.detect_cameras import DetectPossibleCameras
import cv2
from datetime import datetime
import os
import logging
from typing import List, Optional, Dict
from pydantic import BaseModel, Field

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CameraConfig(BaseModel):
    width: int = Field(default=640, ge=1)
    height: int = Field(default=480, ge=1)
    fps: int = Field(default=30, ge=1)
    show_window: bool = Field(default=False)

class CameraApp:
    def __init__(self, config: Optional[CameraConfig] = None):
        self.cameras: List[cv2.VideoCapture] = []
        self.video_writers: Dict[int, cv2.VideoWriter] = {}
        self.recording: bool = False
        self.config = config or CameraConfig()

    def detect_cameras(self) -> List[int]:
        logger.info("Detecting cameras")
        d = DetectPossibleCameras()
        available_cameras = d.find_available_cameras()
        return available_cameras.cameras_found_list

    def load_cameras(self, camera_ids: List[int]) -> int:
        self.cameras = []
        for cam_id in camera_ids:
            cap = cv2.VideoCapture(int(cam_id))
            if cap.isOpened():
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.width)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.height)
                cap.set(cv2.CAP_PROP_FPS, self.config.fps)
                self.cameras.append(cap)
            else:
                logger.warning(f"Failed to open camera {cam_id}")
        return len(self.cameras)

    def start_recording(self, camera_names: Optional[List[str]] = None) -> str:
        if self.recording:
            logger.warning("Recording is already in progress")
            return ""

        logger.info(f"Starting recording for cameras: {camera_names or 'all'}")
        self.recording = True
        date_info = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder_name = f"recorded_{date_info}"
        os.makedirs(folder_name, exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        
        for i, cam in enumerate(self.cameras):
            name = camera_names[i] if camera_names and i < len(camera_names) else f'camera_{i}'
            output_path = os.path.join(folder_name, f"{name}.mp4")
            self.video_writers[i] = cv2.VideoWriter(output_path, fourcc, self.config.fps, (self.config.width, self.config.height))

        return folder_name

    def stop_recording(self) -> None:
        if not self.recording:
            logger.warning("No recording in progress")
            return

        logger.info("Stopping recording")
        self.recording = False
        for writer in self.video_writers.values():
            writer.release()
        self.video_writers.clear()

    def capture_frame(self) -> List[Optional[np.ndarray]]:
        frames = []
        for i, cam in enumerate(self.cameras):
            ret, frame = cam.read()
            if ret:
                frames.append(frame)
                if self.recording:
                    self.video_writers[i].write(frame)
            else:
                frames.append(None)
        
        if self.config.show_window and frames:
            # Stack frames horizontally
            stacked_frame = np.hstack([f for f in frames if f is not None])
            cv2.imshow("Camera Feeds", stacked_frame)
        
        return frames

    def release(self) -> None:
        for cam in self.cameras:
            cam.release()
        self.cameras.clear()
        self.stop_recording()
        if self.config.show_window:
            cv2.destroyAllWindows()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()