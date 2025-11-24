import argparse
from sheep_detector.use_cases.process_images import process_folder


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Input folder with images')
    parser.add_argument('--output', required=True, help='Output folder for annotated images and CSV')
    parser.add_argument('--model', default='yolov8n.pt', help='YOLO model path or name')
    parser.add_argument('--conf', type=float, default=0.25, help='Confidence threshold')
    parser.add_argument('--device', default='cpu', help='Device: cpu or cuda')
    args = parser.parse_args()

    process_folder(args.input, args.output, model_path=args.model, conf=args.conf, device=args.device)


if __name__ == '__main__':
    main()
