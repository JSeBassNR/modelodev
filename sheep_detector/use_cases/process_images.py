import os
from typing import List
import csv
import cv2
from pathlib import Path

from sheep_detector.adapters.yolo_detector import YOLODetector
from sheep_detector.adapters.color_classifier import classify_color_by_hsv, map_color_to_health
from sheep_detector.infrastructure.db import init_engine, get_session, save_results
from sheep_detector.infrastructure.api_clients import send_image_summary, send_alert


def annotate_image(img_bgr, detections: List[dict]):
    for d in detections:
        x1, y1, x2, y2 = d['x1'], d['y1'], d['x2'], d['y2']
        label = f"{d.get('class_name','obj')}:{d.get('color','')}:{d.get('health_status','')}"
        cv2.rectangle(img_bgr, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img_bgr, label, (x1, max(15, y1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    return img_bgr


def process_folder(input_dir: str, output_dir: str, model_path: str = 'yolov8n.pt', conf: float = 0.25, device: str = 'cpu'):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    detector = YOLODetector(model_path=model_path, conf=conf, device=device)

    engine = init_engine()
    session = get_session(engine)

    csv_path = output_dir / 'results.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['image', 'x1', 'y1', 'x2', 'y2', 'score', 'class', 'color', 'health_status'])

        for img_path in sorted(input_dir.glob('*')):
            if not img_path.is_file():
                continue
            try:
                boxes = detector.detect(str(img_path))
            except Exception as e:
                print(f"Failed to run detector on {img_path}: {e}")
                continue

            img_bgr = cv2.imread(str(img_path))
            processed_boxes = []
            for b in boxes:
                x1, y1, x2, y2 = b['x1'], b['y1'], b['x2'], b['y2']
                crop = img_bgr[y1:y2, x1:x2]
                color = classify_color_by_hsv(crop)
                health = map_color_to_health(color)
                b['color'] = color
                b['health_status'] = health
                processed_boxes.append(b)
                writer.writerow([str(img_path.name), x1, y1, x2, y2, b['score'], b['class_name'], color, health])

            # annotate and save
            annotated = annotate_image(img_bgr, processed_boxes)
            out_img_path = output_dir / img_path.name
            cv2.imwrite(str(out_img_path), annotated)

            # save to DB if available
            if session is not None:
                try:
                    save_results(session, str(img_path), processed_boxes)
                except Exception as e:
                    print(f"DB save failed for {img_path}: {e}")

            # call external APIs: summary per image
            try:
                payload = {
                    'image': str(img_path.name),
                    'detections': [{'class': d['class_name'], 'score': d['score'], 'color': d['color'], 'health_status': d['health_status']} for d in processed_boxes]
                }
                send_image_summary(payload)
                # alerts for grave
                for d in processed_boxes:
                    if d.get('health_status') == 'grave':
                        send_alert({'image': str(img_path.name), 'detection': d})
            except Exception:
                pass
