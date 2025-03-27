#!/bin/bash

cd /mnt/project || exit 1
docker compose pull
docker compose up -d
