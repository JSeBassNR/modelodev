Sheep Detector (batch) — prototipo

Este repositorio contiene un prototipo de detección por lotes para identificar ovejas en imágenes y clasificar el color del pelaje (blanco, negro, gris, café). Según el color se asigna un estado de salud:
- blanco -> sana
- café -> enfermedad leve
- gris -> enfermedad media
- negro -> enfermedad grave

Características:
- Arquitectura limpia (capas domain/use_cases/adapters/infrastructure)
- Detector: Ultralytics YOLOv8 (preentrenado COCO)
- Clasificador de color: reglas HSV sobre el recorte del bounding box (prototipo)
- Persistencia: PostgreSQL (SQLAlchemy)
- Integración: adaptadores HTTP para llamar a APIs externas (placeholders)

Requisitos
- Python 3.9+
- GPU NVIDIA opcional (se requiere instalar PyTorch con la versión CUDA adecuada)

Instalación (PowerShell en Windows)

1. Crear y activar un entorno virtual (ejemplo PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instalar dependencias (primero instala PyTorch desde https://pytorch.org/ siguiendo el comando recomendado para Windows y tu versión de CUDA). Luego:

```powershell
pip install -r requirements.txt
```

3. Configurar variables de entorno (ejemplo PowerShell):

```powershell
$env:POSTGRES_URL = "postgresql://user:password@localhost:5432/sheepdb"
$env:API1_URL = "http://localhost:8080/api/summary"
$env:API2_URL = "http://localhost:8080/api/alerts"
```

Uso rápido

```powershell
python scripts\detect_batch.py --input images\ --output outputs\ --conf 0.25
```

Esto procesará todas las imágenes de la carpeta `images\`, guardará imágenes anotadas en `outputs/` y exportará `results.csv`. También intentará persistir resultados en PostgreSQL si `POSTGRES_URL` está configurada y llamará a las APIs si `API1_URL`/`API2_URL` están definidas.

Notas
- El clasificador de color es una heurística (HSV) pensada como prototipo. Para alta precisión considera entrenar un clasificador supervisado o usar segmentación para aislar mejor el pelaje.
- Ajusta `--conf` para cambiar el umbral de confianza de detección.
