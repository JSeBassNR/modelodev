from typing import Tuple
import cv2
import numpy as np


def classify_color_by_hsv(crop_bgr) -> str:
    """Classify approximate color of the crop (BGR numpy array) into: blanco, negro, gris, cafe

    This is a heuristic based on mean HSV values.
    """
    if crop_bgr is None or crop_bgr.size == 0:
        return 'desconocido'

    hsv = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2HSV)
    h_mean = int(np.mean(hsv[:, :, 0]))
    s_mean = int(np.mean(hsv[:, :, 1]))
    v_mean = int(np.mean(hsv[:, :, 2]))

    # Black: very low V
    if v_mean < 50:
        return 'negro'

    # White: very low saturation and high value
    if s_mean < 40 and v_mean > 200:
        return 'blanco'

    # Gray: low saturation and mid valu
    if s_mean < 60 and 80 < v_mean <= 200:
        return 'gris'

    # Brown (café): hue approx in orange/brown range and moderate saturation
    # Hue in OpenCV is 0-179. Brown typically around 5-30
    if (5 <= h_mean <= 30) and s_mean > 50:
        return 'cafe'

    # Fallback: choose based on value and saturation
    if v_mean > 200:
        return 'blanco'
    if v_mean < 100:
        return 'negro'

    return 'gris'


def map_color_to_health(color: str) -> str:
    mapping = {
        'blanco': 'sana',
        'cafe': 'leve',
        'gris': 'media',
        'negro': 'grave'
    }
    return mapping.get(color, 'desconocido')
