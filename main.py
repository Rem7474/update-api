from fastapi import FastAPI, Header, HTTPException
import subprocess
import os

app = FastAPI()
subapi = FastAPI()

API_KEY = os.environ.get("API_KEY", "my-secret-token")
ROUTE_PREFIX = os.environ.get("ROUTE_PREFIX", "immich")
DOCKER_COMPOSE_PATH = os.environ.get("DOCKER_COMPOSE_PATH", "/mnt/project")

@subapi.post("/update")
def update(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API token")

    try:
        result = subprocess.run(
            ["bash", "-c", f"cd {DOCKER_COMPOSE_PATH} && docker compose pull && docker compose up -d"],
            capture_output=True,
            text=True,
            check=True
        )
        return {"status": "success", "output": result.stdout}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=e.stderr)

app.mount(f"/{ROUTE_PREFIX}", subapi)