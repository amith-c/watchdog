from ultralytics import YOLO

class ObjectDetector:
    def __init__(self):
        self.model = YOLO("yolo26n.pt")

    def detect(self, frame):
        results = self.model(frame)
        detections = []
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                label = result.names[class_id]
                confidence = float(box.conf[0])
                detections.append((label, confidence))
        return detections