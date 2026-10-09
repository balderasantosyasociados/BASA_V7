# gateway_enterprise.py
import requests
from flask import Flask, jsonify

app = Flask(__name__)

MODULOS = {
    "M3_NOMINA": "http://localhost:5001",
    "M1_COMPRAS": "http://localhost:5002",
    "M5_PRESTAMOS": "http://localhost:5003",
    "M8_FORENSE": "http://localhost:5004",
}

@app.route('/api/orquestar/auditoria-completa', methods=['POST'])
def orquestar():
    resultados = {}
    total = 0
    for nombre, url in MODULOS.items():
        try:
            r = requests.get(f"{url}/api/detectar", timeout=3)
            data = r.json()
            resultados[nombre] = data
            total += len(data.get('hallazgos',[]))
        except Exception as e:
            # Si un módulo está caído, los demás siguen!
            resultados[nombre] = {"error": str(e), "status":"DOWN"}

    return jsonify({
        "reporte_id": f"REP-ENT-{int(datetime.now().timestamp())}",
        "arquitectura": "Enterprise Microservicios",
        "total_hallazgos": total,
        "resultados": resultados,
        "nota": "Módulos no se interrumpen - Cada uno DB propia"
    })
