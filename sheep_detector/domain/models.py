from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class Detection:
    x1: int
    y1: int
    x2: int
    y2: int
    score: float
    class_name: str
    color: str = None
    health_status: str = None


@dataclass
class ImageResult:
    file_path: str
    detections: List[Detection]
