import os
import pandas as pd
import duckdb
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template_string, redirect, send_file
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)
CORS(app)

# ================= RUTA PRINCIPAL - LA QUE VIO EN LIVE =================
@app.route('/')
def home():
    return jsonify({
        "SAAS": "AUDIT INTELLIGENCE USA v7.0 - BHD 08694150021 - Pedro Baldera",
        "status": "24/7_ACTIVO_RENDER_CERTIFIED",
        "email": "licpedrobaldera@gmail.com",
        "whatsapp": "18297717390",
        "web": "https://audit-intelligence-usa.com",
        "ruta_prueba_3_dias": "/trial",
        "salud_servidor": "/healthz",
        "planes": "/api/planes"
    })

@app.route('/healthz')
def health():
    return jsonify({"status": "OK", "timestamp": datetime.now().isoformat()})

# ================= TRIAL 7 DIAS - PARA EL PUBLICO =================
@app.route('/trial')
def trial_page():
    html = """
    <html><head><meta name='viewport' content='width=device-width,initial-scale=1'>
    <title>BASA V7 - Trial 7 Dias Gratis</title>
    <style>
    body{font-family:Arial;background:#0a192f;color:white;text-align:center;padding:20px;margin:0}
    .card{background:white;color:#0a192f;padding:25px;border-radius:15px;max-width:420px;margin:20px auto;box-shadow:0 4px 20px rgba(0,0,0,0.3)}
    .btn{display:block;background:#00d084;color:white;padding:16px;border-radius:10px;text-decoration:none;font-weight:bold;margin:15px 0;font-size:18px}
    .btn-bhd{background:#003366} h1{color:#00d084;margin:10px 0} .price{font-size:22px;font-weight:bold;color:#003366}
    </style></head><body>
    <h1>🔍 BASA V7</h1><h2>Prueba 7 Dias Gratis</h2>
    <div class='card'>
    <p><b>Sin tarjeta. Sin compromiso.</b></p>
    <p>✅ Auditoria forense completa<br>✅ Deteccion anomalias<br>✅ Reporte DGII automatico</p>
    <a class='btn' href='/'>🚀 ACTIVAR MI TRIAL GRATIS</a>
    <hr>
    <p><b>¿Listo para pagar?</b></p>
    <p class='price'>RD$7,500 / 30,000 / 75,000</p>
    <a class='btn btn-bhd' href='https://bhd.com.do' target='_blank'>💳 BHD 08694150021<br><small>Pedro Baldera</small></a>
    <p><small>Contacto: licpedrobaldera@gmail.com<br>WhatsApp: +1 829 771 7390<br>Trial valido 7 dias</small></p>
    </div></body></html>
    """
    return render_template_string(html)

@app.route('/api/planes')
def planes():
    return jsonify({
        "basico": {"precio": "RD$7,500", "auditorias": 10, "usuarios": 1},
        "profesional": {"precio": "RD$30,000", "auditorias": 50, "usuarios": 5},
        "empresarial": {"precio": "RD$75,000", "auditorias": "ilimitadas", "usuarios": "ilimitados"},
        "bhd_cuenta": "08694150021",
        "titular": "Pedro Baldera",
        "trial": "7 dias gratis sin tarjeta"
    })

@app.route('/api/trial/activar', methods=['GET','POST'])
def activar_trial():
    expira = datetime.now() + timedelta(days=7)
    email = request.args.get('email', 'cliente@prueba.com')
    return jsonify({
        "status": "ok",
        "plan": "TRIAL_7_DIAS",
        "email": email,
        "expira": expira.strftime("%Y-%m-%d"),
        "mensaje": "Trial activado - BASA V7",
        "bhd_cuenta": "08694150021"
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
