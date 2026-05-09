import cv2
import threading
import os
from dotenv import load_dotenv

load_dotenv()

# Relative imports that work when run from root or within core
try:
    from core.detection import ObjectDetector
    from core.alerts import Notifier
except ImportError:
    from detection import ObjectDetector
    from alerts import Notifier

class CameraStream:
    def __init__(self, camera_id: int, url: str, detector: ObjectDetector = None, notifier: Notifier = None):
        self.stream = cv2.VideoCapture(url)
        if not self.stream.isOpened():
            print(f"Error: Could not open stream for Cam {camera_id}")

        self.url = url
        self.id = camera_id
        self.frame = None
        self.stopped = False
        self.detector = detector
        self.notifier = notifier
        self.lock = threading.Lock()

        self.thread = threading.Thread(target=self.update, args=(), daemon=True)
        self.thread.start()

    def update(self):
        i = 0
        while not self.stopped:
            ret, frame = self.stream.read()
            if not ret:
                print(f"No frames from Cam {self.id}")
                self.stop()
                return

            with self.lock:
                self.frame = frame

            # Run detection every ~100 frames
            if i % 100 == 0 and self.detector:
                detections = self.detector.detect(frame)
                for label, confidence in detections:
                    if confidence > 0.65:
                        print(f"Detected: {label} ({confidence:.2f}) in Cam {self.id}")
                        # Alert for specific objects
                        if self.notifier:
                            if label == "person":
                                self.notifier.notify("Person detected", f"A person has been detected on Camera {self.id}")
                            elif label == "car":
                                self.notifier.notify("Car detected", f"A car has been detected on Camera {self.id}")
            i += 1 

    def get_frame(self):
        with self.lock:
            return self.frame.copy() if self.frame is not None else None

    def stop(self):
        self.stopped = True
        if hasattr(self, 'thread') and self.thread.is_alive():
            self.thread.join(timeout=1.0)
            
        if self.stream.isOpened():
            self.stream.release()

class CameraStreamManager:
    def __init__(self, camera_ids: list[int], use_low_res=True, notifier: Notifier = None):
        self.camera_ids = camera_ids
        self.streams: dict[int, CameraStream] = {}
        self.is_low_res = use_low_res
        self.detector = ObjectDetector()
        self.notifier = notifier

        # Pull from .env
        self.ip = os.getenv("DVR_IP")
        self.port = os.getenv("RTSP_PORT", "554")
        self.user = os.getenv("USERNAME")
        self.pwd = os.getenv("PASSWORD")

    def _get_url(self, stream_id: int) -> str:
        return f"rtsp://{self.user}:{self.pwd}@{self.ip}:{self.port}/Streaming/Channels/{stream_id}"

    def start_streams(self):
        for cid in self.camera_ids:
            stream_id = cid * 100 + (2 if self.is_low_res else 1)
            url = self._get_url(stream_id)
            self.streams[cid] = CameraStream(cid, url, self.detector, self.notifier)

    def get_frame(self, camera_id: int):
        if camera_id in self.streams:
            return self.streams[camera_id].get_frame()
        return None

    def stop(self):
        for stream in self.streams.values():
            stream.stop()
        
        cv2.destroyAllWindows()
        for _ in range(10):
            cv2.waitKey(1)

if __name__ == "__main__":
    # Test block
    stream_manager = CameraStreamManager([4])
    stream_manager.start_streams()
    try:
        while True:
            frame = stream_manager.get_frame(4)
            if frame is not None:
                cv2.imshow('Camera 4', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        stream_manager.stop()