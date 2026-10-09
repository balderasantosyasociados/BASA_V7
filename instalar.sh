#!/bin/bash
echo "🧬 BASA CELULAR FULL - Instalador"

# Verificar Python
if ! command -v python3 &> /dev/null; then
  echo "Instalando Python..."
  sudo apt update && sudo apt install -y python3 python3-pip
fi

# Dependencias
pip3 install flask pandas requests

# Licencias ejemplo
cat > licencia_FULL.json <<EOF
{"cliente":"BASA ENTERPRISE","tipo":"FULL","modulos":["M1","M2","M3","M4","M5","M6","M7","M8","M9","M10","M11","M12","M13","M14","M15","M16","M17"],"precio":185000,"vencimiento":"2027-12-31"}
EOF

cat > licencia_M3_INDEPENDIENTE.json <<EOF
{"cliente":"Ayuntamiento SDN","tipo":"INDEPENDIENTE","modulos":["M3"],"precio":15000,"vencimiento":"2026-12-31"}
EOF

echo "✓ Instalado"
echo "Uso:"
echo "  python3 basa_celular_full_17modulos.py --celula M3  # Solo M3"
echo "  python3 basa_celular_full_17modulos.py --full       # 17 modulos FULL"
echo "  ./instalar.sh && docker-compose up                  # Docker FULL"
