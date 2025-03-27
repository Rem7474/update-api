from fastapi import FastAPI, Header, HTTPException
import subprocess
import os

app = FastAPI()
subapi = FastAPI()

API_KEY = os.environ.get("API_KEY", "my-secret-token")

@subapi.post("/update")
def update(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API token")

    try:
        result = subprocess.run(
            ["/usr/local/bin/update.sh"],
            capture_output=True,
            text=True,
            check=True
        )
        return {"status": "success", "output": result.stdout}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=e.stderr)

# Important: adapter à la route reverse proxy
app.mount("/immich", subapi)
