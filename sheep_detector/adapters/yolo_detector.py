import os
from typing import List

# Import ultralytics lazily (only when used) to avoid hard dependency at import-time in environments
def _import_yolo():
    try:
        from ultralytics import YOLO
        return YOLO
    except Exception as e:
        raise ImportError("ultralytics.YOLO is required for YOLO detector. Install ultralytics and torch. Error: %s" % e)


class YOLODetector:
    def __init__(self, model_path: str = 'yolov8n.pt', conf: float = 0.25, device: str = 'cpu'):
        YOLO = _import_yolo()
        self.model = YOLO(model_path)
        self.conf = conf
        self.device = device

    def detect(self, image_path: str) -> List[dict]:
        """Run detection on a single image and return list of boxes as dicts: x1,y1,x2,y2,score,class_id,class_name"""
        # Use predict API
        results = self.model.predict(source=image_path, conf=self.conf, device=self.device, verbose=False)
        if len(results) == 0:
            return []
        r = results[0]
        boxes = []
        # results boxes -> r.boxes
        if hasattr(r, 'boxes') and r.boxes is not None:
            for box in r.boxes:
                xyxy = box.xyxy.tolist()[0] if hasattr(box.xyxy, 'tolist') else box.xyxy
                conf = float(box.conf.tolist()[0]) if hasattr(box.conf, 'tolist') else float(box.conf)
                cls = int(box.cls.tolist()[0]) if hasattr(box.cls, 'tolist') else int(box.cls)
                # class name resolution via model.names if available
                class_name = self.model.names[cls] if hasattr(self.model, 'names') and cls in self.model.names else str(cls)
                boxes.append({
                    'x1': int(xyxy[0]), 'y1': int(xyxy[1]), 'x2': int(xyxy[2]), 'y2': int(xyxy[3]),
                    'score': conf, 'class_id': cls, 'class_name': class_name
                })
        return boxes
