FROM python:3.11-slim

WORKDIR /app

# Installer dépendances système + docker CLI
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    lsb-release

# Ajouter dépôt officiel Docker + installer docker CLI
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" \
    > /etc/apt/sources.list.d/docker.list && \
    apt-get update && apt-get install -y docker-ce-cli

# Nettoyage
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

COPY main.py .
COPY update.sh .
RUN chmod +x update.sh
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
