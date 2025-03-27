#!/bin/bash

set -e

REPO_URL="https://github.com/Rem7474/update-api.git"
INSTALL_DIR="/opt/update-api"

echo "Installation de l'API de mise à jour..."

# Installer les dépendances système
echo "🔧 Installation de Python et Git..."
apt update && apt install -y python3 python3-venv python3-pip git

# Cloner le dépôt
if [ ! -d "$INSTALL_DIR" ]; then
  echo "Clonage du dépôt dans $INSTALL_DIR"
  git clone "$REPO_URL" "$INSTALL_DIR"
else
  echo "Le dossier $INSTALL_DIR existe déjà, pull des mises à jour..."
  cd "$INSTALL_DIR"
  git pull
fi

cd "$INSTALL_DIR"

# Créer l'environnement virtuel
echo "Création de l'environnement virtuel..."
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances Python
echo "Installation des dépendances Python..."
pip install -r requirements.txt

# Créer le service systemd
echo "Création du service systemd..."

cat <<EOF > /etc/systemd/system/update-api.service
[Unit]
Description=Update API FastAPI Service
After=network.target

[Service]
User=root
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

# Activer et démarrer le service
echo "Lancement de l'API..."
systemctl daemon-reexec
systemctl daemon-reload
systemctl enable update-api
systemctl restart update-api

echo "Installation terminée ! L'API est disponible sur le port 8000."
