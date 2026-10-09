# gateway_celular.py - Detecta células solas y las acumula como tejido
import os, json, glob, requests
from flask import Flask, jsonify

app = Flask(__name__)

def escanear_celulas():
    """Auto-descubre células en /celulas/"""
    celulas = []
    for manifest_path in glob.glob("celulas/*/manifest.json"):
        manifest = json.load(open(manifest_path))
        celulas.append(manifest)
    return celulas

@app.route('/api/celulas/disponibles')
def disponibles():
    return jsonify(escanear_celulas())

@app.route('/api/orquestar/tejidocompleto', methods=['POST'])
def tejer():
    celulas = escanear_celulas()
    resultados = {}
    total_facturacion = 0
    for cel in celulas:
        try:
            r = requests.get(f"http://localhost:{cel['puerto']}/api/detectar", timeout=2)
            resultados[cel['codigo']] = r.json()
            total_facturacion += cel['precio_mensual']
        except:
            resultados[cel['codigo']] = {"status":"CELULA_DORMIDA","nota":"Ejecuta su celula.py sola"}

    return jsonify({
        "organismo": "BASA ENTERPRISE TEJIDO CELULAR",
        "celulas_detectadas": len(celulas),
        "celulas": [c['codigo'] for c in celulas],
        "facturacion_acumulada": total_facturacion,
        "modo": "ACUMULADO" if len(celulas)>1 else "CELULA_SOLA",
        "resultados": resultados,
        "nota": "Cada célula vive sola, pero acumuladas forman FULL"
    })

# El gateway también corre solo
if __name__ == '__main__':
    print("🧬 Gateway Celular - Auto-detecta células en /celulas/")
    print(f"Células encontradas: {len(escanear_celulas())}")
    app.run(port=5000)
