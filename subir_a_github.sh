#!/bin/bash
# ==============================================================================
# SCRIPT PARA SUBIR LOS ARCHIVOS A GITHUB Y AUTO-DESPLEGAR EN RENDER.COM:
# Repositorio: https://github.com/balderasantosyasociados/BASA_V7-system-
# Servicio Render: https://dashboard.render.com/web/srv-db0s008u01pc73bmtl90
# ==============================================================================

echo "Subiendo archivos validados para Render.com y GitHub..."

git add app.py requirements.txt render.yaml Procfile runtime.txt storage/ config.yml setup_tunnel.sh README.md
git commit -m "fix(render): Validar build para Render.com srv-db0s008u01pc73bmtl90 con gunicorn y /healthz"
git push origin main

echo "¡Listo! Render.com detectará el commit en 'main' e iniciará el Build automático."
