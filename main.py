from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from starlette.status import HTTP_401_UNAUTHORIZED
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

API_TOKEN = os.getenv("API_TOKEN")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")
COMPOSE_PROJECT_PATH = os.getenv("COMPOSE_PROJECT_PATH")
LOG_FILE = os.path.join(os.path.dirname(__file__), "last_update.log")

def verify_token(request: Request):
    token = request.headers.get("Authorization")
    if not token or token != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized")

@app.post("/{prefix}/update")
async def update_container(prefix: str, request: Request):
    verify_token(request)
    if prefix != CONTAINER_NAME:
        raise HTTPException(status_code=404, detail="Container not found")

    try:
        with open(LOG_FILE, "w") as log:
            subprocess.run(["docker", "compose", "pull"], cwd=COMPOSE_PROJECT_PATH, stdout=log, stderr=log, check=True)
            subprocess.run(["docker", "compose", "up", "-d"], cwd=COMPOSE_PROJECT_PATH, stdout=log, stderr=log, check=True)
            subprocess.run(["docker", "image", "prune", "-f"], stdout=log, stderr=log, check=True)
        return {"status": "success", "message": f"{CONTAINER_NAME} updated successfully."}
    except subprocess.CalledProcessError:
        raise HTTPException(status_code=500, detail="Update failed. Check logs.")

@app.get("/{prefix}/logs")
async def get_logs(prefix: str, request: Request):
    verify_token(request)
    if prefix != CONTAINER_NAME:
        raise HTTPException(status_code=404, detail="Container not found")
    if not os.path.exists(LOG_FILE):
        raise HTTPException(status_code=404, detail="Log file not found")
    return FileResponse(LOG_FILE)
