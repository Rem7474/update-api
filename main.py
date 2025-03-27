import os
import subprocess
from fastapi import FastAPI, Request, Header, HTTPException

app = FastAPI()

API_KEY = os.environ.get("API_KEY")
ROUTE_PREFIX = os.environ.get("ROUTE_PREFIX")
CONTAINER_NAME = os.environ.get("CONTAINER_NAME")

@app.post("/{prefix}/update")
async def update(prefix: str, request: Request, x_api_key: str = Header(...)):
    if x_api_key != API_KEY or prefix != ROUTE_PREFIX:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        # Lancer le script en tâche de fond (sans bloquer l'API)
        subprocess.Popen(
            ["bash", "/app/update.sh"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return {"status": "Update started in background."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
