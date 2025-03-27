# update-api

> API REST simple pour mettre à jour des containers Docker via un appel HTTP sécurisé.

---

## 🔧 Installation via script

```bash
chmod +x install-update-api.sh
./install-update-api.sh
```

---

## ⚙️ Configuration

Copie le fichier `.env.example` en `.env` :

```bash
cp .env.example .env
```

Puis modifie les valeurs selon ton setup :

- `CONTAINER_NAME` : nom utilisé dans l’URL (`/immich/update`)
- `API_TOKEN` : token requis dans les appels API
- `COMPOSE_PROJECT_PATH` : chemin vers le dossier `docker-compose.yml`

---

## 🔐 Requête API

### Lancer une mise à jour

```bash
curl -X POST http://IP:8000/immich/update \
  -H "Authorization: Bearer mon_token_secret"
```

### Voir les logs

```bash
curl http://IP:8000/immich/logs \
  -H "Authorization: Bearer mon_token_secret"
```

---

## ✍️ Auteur

Rem7474
