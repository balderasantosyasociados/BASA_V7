import os, io, zipfile, datetime, json
from flask import Flask, jsonify, render_template_string, send_file, request, session
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "BASA_V8_LITE_08694150021"
CORS(app)

BHD_CUENTA = "08694150021"
MODULOS = {
    "B4_BASE": {"nombre":"B4 Base - Informe Pericial","precio":7500,"incluido":True},
    "M1_SCRAPER": {"nombre":"M1 - Scraper Compras 10 años","precio":2500},
    "M2_FRACC": {"nombre":"M2 - Fraccionamiento Ley 340","precio":3500},
    "M3_DUENO": {"nombre":"M3 - Mismo Dueño","precio":3000},
    "M4_ACC": {"nombre":"M4 - Accionistas","precio":4000},
    "M5_CONF": {"nombre":"M5 - Consanguinidad","precio":4500},
    "M6_NOM": {"nombre":"M6 - Nomina Fantasma","precio":3500},
    "M7_FIN": {"nombre":"M7 - Estados Financieros","precio":3000},
    "M8_FULL": {"nombre":"M8 - Forense V8 Full","precio":5000},
}

def calc_fact(mods):
    hoy=datetime.datetime.now(); dias=30-hoy.day+1
    total=sum(MODULOS[m]["precio"] for m in mods if m in MODULOS)
    return {"mods":mods,"total":total,"primer":round((total/30)*dias,2),"dias":dias,"proximo":(hoy+datetime.timedelta(days=dias)).strftime("%d/%m/%Y")}

@app.route('/')
def home(): return jsonify({"BASA":"V8 LITE LIVE","bhd":BHD_CUENTA,"activar":"/activar-modulos","b4":"/b4","v8":"/v8"})

@app.route('/healthz')
def health(): return jsonify({"status":"OK V8 LITE"})

@app.route('/activar-modulos')
def activar():
    mods_html="".join([f"<div style='border:2px solid #ddd;padding:12px;margin:8px;border-radius:10px;display:flex;justify-content:space-between'><div><b>{v['nombre']}</b><br>RD${v['precio']}/mes</div><div><input type='checkbox' value='{k}' {'checked disabled' if v.get('incluido') else ''} class='chk' style='width:22px;height:22px' onchange='calc()'></div></div>" for k,v in MODULOS.items()])
    return render_template_string(f"""
<html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>body{{font-family:Arial;background:#0f172a;color:white;padding:12px}}.card{{background:white;color:black;padding:20px;border-radius:15px;max-width:900px;margin:auto}}.btn{{padding:12px;border-radius:8px;font-weight:bold;cursor:pointer;border:none;margin:5px}}.verde{{background:#00d084;color:white}}.azul{{background:#003366;color:white}}</style></head>
<body><h1 style='text-align:center;color:#00d084'>⚙️ BASA V8 - ACTIVAR MODULOS</h1><div class='card'>
{mods_html}<div style='background:#f0f7ff;padding:12px;border-radius:10px'><h3>Facturacion</h3>Empresa: <input id='emp' style='width:100%;padding:8px'><br>RNC: <input id='rnc' style='width:100%;padding:8px'><div id='fact'></div></div>
<div style='background:#fff3cd;padding:12px;border-radius:10px;margin:10px 0'><input type='checkbox' id='ok'> <b>Estoy de acuerdo con contrato virtual BASA V8 - BHD {BHD_CUENTA}</b><br><a href='/api/contrato' target='_blank'>Ver Contrato</a></div>
<button class='btn verde' style='width:100%' onclick='activar()'>✅ ACEPTO Y ACTIVAR + DESCARGAR DEMO</button><div id='res' style='display:none;background:#e8f5e9;padding:12px;border-radius:10px;margin-top:10px'></div>
</div><script>
let mods=['B4_BASE'];function calc(){{mods=['B4_BASE'];document.querySelectorAll('.chk:checked').forEach(c=>{{if(c.value!='B4_BASE') mods.push(c.value)}});fetch('/api/fact',{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{mods}})}).then(r=>r.json()).then(d=>{{document.getElementById('fact').innerHTML=`Total: RD$${{d.total}}<br>Primer pago (${{d.dias}} dias): RD$${{d.primer}}<br>Proximo: ${{d.proximo}}<br>BHD: {BHD_CUENTA}`}})}};
function activar(){{if(!document.getElementById('ok').checked){{alert('Acepte contrato');return}}fetch('/api/activar',{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{mods,empresa:document.getElementById('emp').value,rnc:document.getElementById('rnc').value}})}).then(r=>r.json()).then(d=>{{document.getElementById('res').style.display='block';document.getElementById('res').innerHTML=`Contrato: ${{d.contrato}}<br><a href='/api/contrato/${{d.contrato}}' class='btn azul'>📄 Descargar Contrato</a> <a href='/demo' class='btn verde'>📦 Descargar DEMO V8</a>`}})}};calc();
</script></body></html>""")

@app.route('/api/fact', methods=['POST'])
def fact():
    data=request.get_json() or {}; return jsonify(calc_fact(data.get('mods',['B4_BASE'])))

@app.route('/api/activar', methods=['POST'])
def api_activar():
    data=request.get_json() or {}; cid=f"CTR-V8-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"; session['pagado']=True; return jsonify({"contrato":cid,"bhd":BHD_CUENTA})

@app.route('/api/contrato')
def cont_prev(): return send_file(io.BytesIO(f"CONTRATO VIRTUAL BASA V8 - BHD {BHD_CUENTA} - Acepta marcando Estoy de acuerdo".encode()),mimetype="application/pdf",as_attachment=True,download_name="CONTRATO_V8_PREVIEW.pdf")
@app.route('/api/contrato/<cid>')
def cont_down(cid): return send_file(io.BytesIO(f"CONTRATO FIRMADO {cid} - BHD {BHD_CUENTA} - MODULOS ACTIVOS".encode()),mimetype="application/pdf",as_attachment=True,download_name=f"{cid}.pdf")

@app.route('/b4')
def b4():
    banner="" if session.get('pagado') else f"<div style='background:#ff8c00;color:white;padding:10px;border-radius:8px'>DEMO - <a href='/activar-modulos' style='color:white;font-weight:bold'>Activar modulos</a> - Novedad Ley 340-06 2026</div>"
    return render_template_string(f"<body style='font-family:Arial;background:#0f172a;color:white;padding:15px'><h1>B4 V8</h1>{banner}<div style='background:white;color:black;padding:15px;border-radius:12px;max-width:800px;margin:auto'><a href='/activar-modulos' style='background:#00d084;color:white;padding:10px;border-radius:8px;text-decoration:none'>Activar Modulos</a> <a href='/v8' style='background:#003366;color:white;padding:10px;border-radius:8px;text-decoration:none'>V8 Scraper 10 años</a></div></body>")

@app.route('/v8')
def v8(): return render_template_string("<body style='font-family:Arial;background:#0a192f;color:white;padding:15px'><h1 style='color:#00d084'>V8 Auditoria 10 años</h1><div style='background:white;color:black;padding:15px;border-radius:12px;max-width:800px;margin:auto'><p>Entidad: Ministerio Educacion<br>Scraper, Fraccionamiento, Mismo Dueño, Accionistas, Consanguinidad, Nomina, Financiero</p><a href='/activar-modulos' style='background:#00d084;color:white;padding:10px;border-radius:8px;text-decoration:none'>Activar M1-M8</a></div></body>")

@app.route('/demo')
def demo():
    m=io.BytesIO()
    with zipfile.ZipFile(m,mode="w",compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("BASA_V8_DEMO/README.txt",f"BASA V8 LITE - BHD {BHD_CUENTA}")
        zf.writestr("BASA_V8_DEMO/CONTRATO.txt","Aceptado via web")
    m.seek(0); return send_file(m,mimetype="application/zip",as_attachment=True,download_name="BASA_V8_LITE_DEMO.zip")

if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.environ.get("PORT",10000)))
