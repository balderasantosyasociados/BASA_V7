import os, io, zipfile, datetime
from flask import Flask, jsonify, render_template_string, send_file, request
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)
CORS(app)

B4_DATA = {"caso_id":"B4-2026-001","empresa":"Demo","periodo":"2026","fecha":""}

@app.route('/')
def home(): return jsonify({"BASA":"V7 B4 ACTIVO","b4":"/b4","trial":"/trial","demo":"/demo","bhd":"08694150021"})
@app.route('/healthz')
def health(): return jsonify({"status":"OK"})

@app.route('/trial')
def trial():
    return render_template_string("""
<html><head><meta name='viewport' content='width=device-width,initial-scale=1'>
<style>body{font-family:Arial;background:#0a192f;color:white;text-align:center;padding:15px}
.card{background:white;color:#0a192f;padding:20px;border-radius:15px;max-width:900px;margin:auto}
.planes{display:flex;gap:12px;flex-wrap:wrap;justify-content:center}
.plan{border:2px solid #ddd;border-radius:12px;padding:18px;width:250px;cursor:pointer}
.plan.activo{border-color:#00d084;background:#f0fff7;transform:scale(1.05)}
.btn{padding:14px 22px;border-radius:10px;text-decoration:none;font-weight:bold;display:inline-block;margin:8px;border:none;cursor:pointer}
.btn-verde{background:#00d084;color:white} .btn-naranja{background:#ff8c00;color:white} .btn-azul{background:#003366;color:white}
</style>
<script>function sel(id,p){document.querySelectorAll('.plan').forEach(x=>x.classList.remove('activo'));document.getElementById(id).classList.add('activo');document.getElementById('res').innerHTML='Plan: '+id.toUpperCase()+' '+p+'<br>BHD 08694150021';document.getElementById('res').style.display='block'}</script>
</head><body><h1 style='color:#00d084'>BASA V7</h1>
<div class='card'><h2>Seleccione Plan</h2>
<div class='planes'>
<div class='plan' id='basico' onclick="sel('basico','RD$7,500')"><h3>BASICO</h3><h2>RD$7,500</h2><button class='btn btn-verde'>Seleccionar</button></div>
<div class='plan' id='pro' onclick="sel('pro','RD$30,000')"><h3>PRO</h3><h2>RD$30,000</h2><button class='btn btn-verde'>Seleccionar</button></div>
<div class='plan' id='emp' onclick="sel('emp','RD$75,000')"><h3>EMPRESARIAL</h3><h2>RD$75,000</h2><button class='btn btn-verde'>Seleccionar</button></div>
</div>
<div id='res' style='display:none;background:#e8f5e9;padding:15px;border-radius:10px;margin:15px 0;border-left:5px solid #00d084'></div>
<a href='/b4' class='btn btn-azul'>🔍 B4 - GENERAR INFORME PERICIAL</a><br>
<a href='/demo' class='btn btn-naranja'>🎮 DESCARGAR BASA V7 DEMO 7 DIAS</a><br>
<a href='/descarga-pagada' class='btn btn-verde'>📥 DESCARGA PAGADA BHD 08694150021</a>
</div></body></html>
""")

@app.route('/b4')
def b4_page():
    return render_template_string("""
<html><head><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>B4 BASA V7</title>
<style>body{font-family:Arial;background:#0f172a;color:white;padding:15px}.card{background:white;color:#0f172a;padding:22px;border-radius:15px;max-width:950px;margin:auto}input,textarea{width:100%;padding:12px;margin:6px 0;border:1px solid #ddd;border-radius:8px}.btn{padding:14px 20px;border-radius:10px;border:none;font-weight:bold;cursor:pointer;margin:6px}.btn-gen{background:#003366;color:white;width:100%;font-size:18px}.btn-excel{background:#217346;color:white}.btn-pdf{background:#d32f2f;color:white}.btn-zip{background:#00d084;color:white}.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}</style>
</head><body><h1 style='text-align:center;color:#00d084'>B4 - INFORME PERICIAL + EXCEL + DICTAMEN</h1>
<div class='card'><h3>Datos del Caso</h3>
<div class='grid'><input id='empresa' placeholder='Empresa'><input id='periodo' placeholder='Periodo'><input id='monto' placeholder='Monto'><input id='tipo' placeholder='Tipo Fraude'></div>
<textarea id='hallazgos' rows='4' placeholder='Hallazgos'></textarea>
<button class='btn btn-gen' onclick='generar()'>⚙️ GENERAR B4</button>
<div id='resultado' style='display:none;margin-top:20px;padding:15px;background:#f0fff7;border-radius:10px;border-left:5px solid #00d084'><h3>✅ B4 Listo - Descargue</h3><p id='res'></p>
<a href='/b4/descargar/excel' class='btn btn-excel'>📊 Excel Auditado</a>
<a href='/b4/descargar/pdf' class='btn btn-pdf'>📄 Informe PDF</a>
<a href='/b4/descargar/dictamen' class='btn btn-pdf'>📑 Dictamen</a>
<a href='/b4/descargar/todo' class='btn btn-zip'>📦 TODO ZIP</a></div></div>
<script>function generar(){let d={empresa:empresa.value,periodo:periodo.value,monto:monto.value,tipo:tipo.value,hallazgos:hallazgos.value};fetch('/api/b4/generar',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)}).then(r=>r.json()).then(x=>{resultado.style.display='block';res.innerHTML='Caso: '+x.caso_id+'<br>BHD 08694150021';})}</script></body></html>
""")

@app.route('/api/b4/generar', methods=['POST'])
def b4_generar():
    data=request.get_json() or {}; B4_DATA.update(data)
    B4_DATA["caso_id"]=f"B4-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"
    B4_DATA["fecha"]=datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    return jsonify({"caso_id":B4_DATA["caso_id"]})

def crear_excel():
    out=io.BytesIO()
    try:
        import openpyxl; wb=openpyxl.Workbook(); ws=wb.active; ws.title="B4"
        ws.append(["BASA V7 B4","CASO",B4_DATA.get("caso_id")]); ws.append(["Empresa",B4_DATA.get("empresa")]); ws.append(["Periodo",B4_DATA.get("periodo")]); ws.append([])
        ws.append(["TIPO","HALLAZGO","MONTO"]); ws.append([B4_DATA.get("tipo"),B4_DATA.get("hallazgos"),B4_DATA.get("monto")]); wb.save(out)
    except: out.write(b"B4 Excel")
    out.seek(0); return out

@app.route('/b4/descargar/<tipo>')
def descargar(tipo):
    if tipo=='excel': return send_file(crear_excel(),mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",as_attachment=True,download_name=f"B4_{B4_DATA['caso_id']}_Excel.xlsx")
    if tipo=='pdf': return send_file(io.BytesIO(f"INFORME PERICIAL B4 CASO {B4_DATA['caso_id']} EMPRESA {B4_DATA['empresa']} HALLAZGOS {B4_DATA['hallazgos']} BHD 08694150021".encode()),mimetype="application/pdf",as_attachment=True,download_name=f"B4_{B4_DATA['caso_id']}_Informe.pdf")
    if tipo=='dictamen': return send_file(io.BytesIO(f"DICTAMEN FORENSE B4 {B4_DATA['caso_id']} {B4_DATA['empresa']} BHD 08694150021".encode()),mimetype="application/pdf",as_attachment=True,download_name=f"B4_{B4_DATA['caso_id']}_DICTAMEN.pdf")
    if tipo=='todo':
        m=io.BytesIO()
        with zipfile.ZipFile(m,mode="w",compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(f"{B4_DATA['caso_id']}/Excel.xlsx",crear_excel().getvalue())
            zf.writestr(f"{B4_DATA['caso_id']}/LEAME.txt","BHD 08694150021 Pedro Baldera licpedrobaldera@gmail.com")
        m.seek(0); return send_file(m,mimetype="application/zip",as_attachment=True,download_name=f"B4_{B4_DATA['caso_id']}_COMPLETO.zip")

@app.route('/demo')
def demo():
    m=io.BytesIO()
    with zipfile.ZipFile(m,mode="w",compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("BASA_V7_DEMO/LEAME.txt","BASA V7 DEMO 7 DIAS BHD 08694150021 licpedrobaldera@gmail.com")
        zf.writestr("BASA_V7_DEMO/CODIGO.txt","TRIAL-7-DIAS-GRATIS")
    m.seek(0); return send_file(m,mimetype="application/zip",as_attachment=True,download_name="BASA_V7_DEMO_7_DIAS.zip")

@app.route('/descarga-pagada')
def pagada(): return render_template_string("<h1>BHD 08694150021 - Envie comprobante a licpedrobaldera@gmail.com</h1><a href='/b4'>Probar B4</a>")

@app.route('/api/planes')
def planes(): return jsonify({"bhd":"08694150021","b4":"/b4","demo":"/demo"})

if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.environ.get("PORT",10000)))
