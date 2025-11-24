from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sheep_detector.use_cases.process_oveja_from_sheep import process_oveja_from_sheep

app = FastAPI()

class OvejaProcessRequest(BaseModel):
    oveja_id: int

@app.post("/procesar-oveja")
def procesar_oveja_endpoint(req: OvejaProcessRequest):
    resultado = process_oveja_from_sheep(
        oveja_id=req.oveja_id,
        sheep_base_url="http://localhost:9191"
    )
    if resultado is None:
        raise HTTPException(status_code=400, detail="No se pudo procesar la oveja")
    return {"resultadoML": resultado}
