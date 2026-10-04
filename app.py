import os
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template_string, send_file
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
import io

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        "SAAS": "AUDIT INTELLIGENCE USA v7.0 - BHD 08694150021",
        "status": "24/7_ACTIVO",
        "trial": "/trial"
    })

@app.route('/healthz')
def health():
    return jsonify({"status": "OK"})

@app.route('/trial')
def trial_page():
    html = """
    <html><head><meta name='viewport' content='width=device-width,initial-scale=1'>
    <title>BASA V7 - Planes y Descargas</title>
    <style>
    body{font-family:Arial;background:#0a192f;color:white;text-align:center;padding:15px;margin:0}
    .card{background:white;color:#0a192f;padding:20px;border-radius:15px;max-width:900px;margin:15px auto}
    .planes{display:flex;gap:12px;flex-wrap:wrap;justify-content:center;margin:20px 0}
    .plan{border:2px solid #ddd;border-radius:12px;padding:18px;width:250px;cursor:pointer;transition:0.3s}
    .plan.activo{border-color:#00d084;transform:scale(1.05);box-shadow:0 5px 20px rgba(0,208,132,0.4);background:#f0fff7}
    .plan h3{margin:5px 0;color:#003366} .precio{font-size:24px;font-weight:bold;color:#003366;margin:10px 0}
    .btn{padding:14px 20px;border-radius:10px;text-decoration:none;font-weight:bold;display:inline-block;margin:8px;border:none;cursor:pointer;font-size:16px}
    .btn-verde{background:#00d084;color:white;width:90%} .btn-azul{background:#003366;color:white;width:90%}
    .btn-demo{background:#ff8c00;color:white} .btn-pago{background:#00d084;color:white}
    .seleccionado{background:#e8f5e9;padding:15px;border-radius:10px;margin:15px 0;border-left:5px solid #00d084;text-align:left}
    </style>
    <script>
    let planSel = '';
    let precioSel = '';
    function seleccionar(plan, precio){
        document.querySelectorAll('.plan').forEach(p=>p.classList.remove('activo'));
        document.getElementById(plan).classList.add('activo');
        planSel = plan; precioSel = precio;
        document.getElementById('resumen').innerHTML = '<b>Plan seleccionado:</b> '+plan.toUpperCase()+' - <b>'+precio+'</b><br><b>BHD:</b> 08694150021 - Pedro Baldera<br><b>Titular:</b> Pedro Baldera - <b>WhatsApp:</b> +1 829 771 7390';
        document.getElementById('resumen').style.display='block';
        document.getElementById('btnPagar').innerHTML = '💳 PAGAR '+precio+' - BHD 08694150021';
    }
    </script>
    </head><body>
    <h1 style='color:#00d084'>🔍 BASA V7</h1>
    <h2>Prueba 7 Días Gratis + Planes BHD</h2>
    
    <div class='card'>
    <h3>👇 SELECCIONE SU PLAN (click para activar)</h3>
    <div class='planes'>
        <div class='plan' id='basico' onclick="seleccionar('basico','RD$7,500')">
            <h3>BÁSICO</h3><div class='precio'>RD$7,500</div>
            <p>10 auditorías<br>1 usuario<br>Reporte DGII</p>
            <button class='btn btn-verde'>Seleccionar Básico</button>
        </div>
        <div class='plan' id='profesional' onclick="seleccionar('profesional','RD$30,000')">
            <h3>PROFESIONAL ⭐</h3><div class='precio'>RD$30,000</div>
            <p>50 auditorías<br>5 usuarios<br>Forense completo</p>
            <button class='btn btn-verde'>Seleccionar Pro</button>
        </div>
        <div class='plan' id='empresarial' onclick="seleccionar('empresarial','RD$75,000')">
            <h3>EMPRESARIAL</h3><div class='precio'>RD$75,000</div>
            <p>Ilimitadas<br>Usuarios ilimitados<br>Soporte 24/7</p>
            <button class='btn btn-verde'>Seleccionar Empresarial</button>
        </div>
    </div>
    
    <div id='resumen' class='seleccionado' style='display:none'></div>
    
    <hr>
    <h3>🚀 DESCARGAS</h3>
    <a href='/demo' class='btn btn-demo'>🎮 DEMO GRATIS - Descargar Prueba 7 Días</a>
    <a id='btnPagar' href='/api/planes' class='btn btn-azul'>💳 VER DATOS BHD PARA PAGAR</a>
    
    <div style='margin-top:20px;background:#003366;color:white;padding:15px;border-radius:10px'>
    <b>Después de pagar:</b><br>
    BHD 08694150021 - Pedro Baldera<br>
    Enviar comprobante a: licpedrobaldera@gmail.com<br>
    WhatsApp: +1 829 771 7390<br>
    <a href='/descarga-pagada' class='btn btn-pago' style='margin-top:10px'>📥 DESCARGA PAGADA - Versión Completa</a>
    </div>
    
    <p><small>Contacto: licpedrobaldera@gmail.com | Trial valido 7 dias sin tarjeta</small></p>
    </div>
    </body></html>
    """
    return render_template_string(html)

@app.route('/demo')
def demo():
    # Crea un Excel de prueba
    content = "BASA V7 DEMO - 7 DIAS GRATIS\nInstrucciones de uso\n1. Instale\n2. Pruebe auditoria\nContacto: licpedrobaldera@gmail.com\nBHD 08694150021"
    return send_file(
        io.BytesIO(content.encode()),
        mimetype="text/plain",
        as_attachment=True,
        download_name="BASA_V7_DEMO_7_DIAS.txt"
    )

@app.route('/descarga-pagada')
def descarga_pagada():
    html = """
    <html><body style='font-family:Arial;text-align:center;padding:30px;background:#0a192f;color:white'>
    <h1>🔒 Descarga Pagada BASA V7</h1>
    <div style='background:white;color:#0a192f;padding:25px;border-radius:15px;max-width:500px;margin:auto'>
    <h3>Para descargar la versión completa:</h3>
    <p><b>1.</b> Pague a BHD <b>08694150021</b><br>
    Titular: Pedro Baldera<br>
    Monto: RD$7,500 / 30,000 / 75,000</p>
    <p><b>2.</b> Envíe comprobante a:<br>
    licpedrobaldera@gmail.com<br>
    WhatsApp: +1 829 771 7390</p>
    <p><b>3.</b> Recibirá link de descarga completa + licencia</p>
    <a href='https://wa.me/18297717390?text=Hola%20LIC%20Baldera,%20pague%20BASA%20V7%20BHD%2008694150021' 
    style='background:#25D366;color:white;padding:15px 25px;border-radius:10px;text-decoration:none;display:inline-block;font-weight:bold;margin-top:15px'>
    📲 Enviar comprobante por WhatsApp</a>
    <br><a href='/trial' style='color:#003366'>← Volver a planes</a>
    </div></body></html>
    """
    return render_template_string(html)

@app.route('/api/planes')
def planes():
    return jsonify({
        "basico": {"precio": "RD$7,500", "boton": "ACTIVO", "descarga": "/demo"},
        "profesional": {"precio": "RD$30,000", "boton": "ACTIVO"},
        "empresarial": {"precio": "RD$75,000", "boton": "ACTIVO"},
        "bhd_cuenta": "08694150021",
        "titular": "Pedro Baldera",
        "demo_gratis": "/demo",
        "descarga_pagada": "/descarga-pagada"
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    """
    return render_template_string(html)
