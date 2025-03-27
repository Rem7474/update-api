#!/bin/bash
cd /mnt/project || exit 1

echo "🔄 Pulling latest images..."
docker compose pull

echo "🚀 Restarting containers..."
docker compose up -d

echo "🧹 Pruning unused Docker resources..."
docker system prune -f

echo "✅ Update completed."
