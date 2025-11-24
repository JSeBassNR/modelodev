-- Schema para almacenar imágenes y detecciones
CREATE TABLE IF NOT EXISTS images (
    id SERIAL PRIMARY KEY,
    file_path TEXT NOT NULL,
    processed_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS detections (
    id SERIAL PRIMARY KEY,
    image_id INTEGER REFERENCES images(id) ON DELETE CASCADE,
    x1 INTEGER,
    y1 INTEGER,
    x2 INTEGER,
    y2 INTEGER,
    score REAL,
    class TEXT,
    color TEXT,
    health_status TEXT
);
