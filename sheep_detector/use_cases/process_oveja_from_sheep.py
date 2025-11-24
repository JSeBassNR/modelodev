import requests
import cv2
import numpy as np
from sheep_detector.adapters.yolo_detector import YOLODetector
from sheep_detector.adapters.color_classifier import classify_color_by_hsv, map_color_to_health
from sheep_detector.infrastructure.api_clients import send_alert

def process_oveja_from_sheep(oveja_id, sheep_base_url, model_path='yolov8n.pt', conf=0.25, device='cpu'):
    # 1. Obtener datos de la oveja (incluye productorId)
    oveja_url = f"{sheep_base_url}/api/MachIA/ovejas/{oveja_id}"
    r_oveja = requests.get(oveja_url)
    if r_oveja.status_code != 200:
        print(f"No se pudo obtener la oveja {oveja_id}")
        return None
    oveja_data = r_oveja.json()
    productor_id = oveja_data.get('productorId')
    if not productor_id:
        print("La oveja no tiene productor asignado")
        return None

    # 2. Descargar imagen desde Sheep
    img_url = f"{sheep_base_url}/api/MachIA/ovejas/{oveja_id}/imagen"
    r = requests.get(img_url)
    if r.status_code != 200:
        print(f"No se pudo obtener la imagen de la oveja {oveja_id}")
        return None
    img_array = np.frombuffer(r.content, np.uint8)
    img_bgr = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if img_bgr is None:
        print("Error al decodificar la imagen")
        return None

    # 3. Procesar imagen (detección y clasificación)
    detector = YOLODetector(model_path=model_path, conf=conf, device=device)
    boxes = detector.detect(img_bgr)
    resultadoML = None
    for b in boxes:
        x1, y1, x2, y2 = b['x1'], b['y1'], b['x2'], b['y2']
        crop = img_bgr[y1:y2, x1:x2]
        color = classify_color_by_hsv(crop)
        health = map_color_to_health(color)
        resultadoML = health
        break  # Solo la primera oveja detectada

    if resultadoML is None:
        resultadoML = 'no_detectada'

    # 4. Notificar a ganadero-service al usuario asignado
    ganadero_notify_url = f"http://localhost:9192/api/MachIA/usuario/{productor_id}/analisis/notificar"
    payload = {
        'referencia': f"oveja-{oveja_id}",  # Puedes personalizar la referencia
        'resultado': resultadoML
    }
    resp = requests.post(ganadero_notify_url, json=payload)
    if resp.status_code in (200, 202):
        print(f"Notificación enviada correctamente: {resp.text}")
    else:
        print(f"Error al notificar: {resp.status_code} {resp.text}")
    return resultadoML
