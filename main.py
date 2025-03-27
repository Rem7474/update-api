import os
import subprocess
from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import PlainTextResponse

app = FastAPI()

API_KEY = os.environ.get("API_KEY")
ROUTE_PREFIX = os.environ.get("ROUTE_PREFIX")
LOG_PATH = "/app/update.log"

@app.post("/{prefix}/update")
async def update(prefix: str, request: Request, x_api_key: str = Header(...)):
    if x_api_key != API_KEY or prefix != ROUTE_PREFIX:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        with open(LOG_PATH, "w") as log_file:
            subprocess.Popen(
                ["bash", "/app/update.sh"],
                stdout=log_file,
                stderr=log_file
            )
        return {"status": "Update started in background."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/{prefix}/logs")
async def get_logs(prefix: str, x_api_key: str = Header(...)):
    if x_api_key != API_KEY or prefix != ROUTE_PREFIX:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not os.path.exists(LOG_PATH):
        raise HTTPException(status_code=404, detail="Log file not found")

    with open(LOG_PATH, "r") as f:
        content = f.read()
    return PlainTextResponse(content)
