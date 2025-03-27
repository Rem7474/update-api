# 🔄 Update API – Déploiement et mise à jour centralisée de containers Docker via API

Ce projet permet d'exposer une API HTTP pour déclencher la mise à jour d'applications Docker (via `docker compose pull && up -d`), même si elles sont réparties sur plusieurs LXC.  
Il est conçu pour être intégré avec un reverse proxy (comme **NGINX Proxy Manager**) pour centraliser tous les appels.

---

## ⚙️ Fonctionnalités

- Déclenchement sécurisé via une API POST
- Configuration par `.env` pour chaque conteneur
- Compatible avec NGINX Proxy Manager
- 100% Dockerisé

---

## 🚀 Utilisation

### 1. 🧱 Pré-requis

- Docker + Docker Compose
- Docker socket monté dans le conteneur (`/var/run/docker.sock`)
- Ton application Docker (Immich, Vaultwarden, etc.) déjà en place avec `docker-compose.yml`

---

### 2. 📁 Cloner ce dépôt sur le LXC cible

```bash
git clone https://github.com/Rem7474/update-api.git
cd update-api
```

---

### 3. 📝 Configurer le fichier `.env`

```env
HOST_COMPOSE_PATH=/root/docker/immich      # Chemin sur le LXC vers le docker-compose de ton app
API_KEY=my-secret-token                    # Token d'authentification
ROUTE_PREFIX=immich                        # Suffixe de l'URL (ex: /immich/update)
```

---

### 4. 🐳 Lancer le conteneur

```bash
docker compose up -d --build
```

---

### 5. 📡 Appeler l’API

```bash
curl -X POST http://<IP_LXC>:8000/immich/update \
     -H "x-api-key: my-secret-token"
```

---

## 🌐 Intégration avec NGINX Proxy Manager

Tu peux exposer cette API depuis chaque LXC via un sous-domaine ou une sous-route, par exemple :

- `update.remcorp.fr/immich/update` → redirige vers le LXC Immich sur `8000`
- `update.remcorp.fr/vaultwarden/update` → vers le LXC Vaultwarden

Assure-toi que **NPM** est configuré pour gérer les sous-routes correctement avec un préfixe (`/immich`, `/vaultwarden`, etc.).

---

## 🗂 Structure du projet

```
.
├── .env
├── docker-compose.yml
├── Dockerfile
├── main.py
├── requirements.txt
└── update.sh         # (facultatif)
```

---

## 🛡 Sécurité

- Authentification par clé API (`x-api-key` dans les headers)
- Token configurable via `.env`

---

## 🧩 Exemple pour un autre projet (Vaultwarden)

```env
HOST_COMPOSE_PATH=/root/docker/vaultwarden
API_KEY=vault-token
ROUTE_PREFIX=vaultwarden
```

---

## 🙌 Contributions

PR et suggestions bienvenues !

---

## 🧑‍💻 Auteur

Projet créé par **Rem7474**

---

## 🔁 Mettre à jour depuis GitHub

Si tu as déjà cloné ce dépôt sur ton LXC et que le conteneur tourne, voici comment mettre à jour facilement :

### 1. 📂 Aller dans le dossier du projet

```bash
cd /chemin/vers/update-api
```

### 2. 📥 Récupérer les dernières modifications

```bash
git pull origin main
```

> 🔁 Si ta branche est `master` :
```bash
git pull origin master
```

### 3. 🔧 Rebuild l'image avec le nouveau Dockerfile

```bash
docker compose build
```

### 4. 🔄 Redémarrer le conteneur

```bash
docker compose up -d
```

### 5. 🧹 (Facultatif) Nettoyer les anciennes images

```bash
docker image prune -f
```

---

