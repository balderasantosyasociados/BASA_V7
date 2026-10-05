import os, io, zipfile, datetime, json
from flask import Flask, jsonify, request, session, send_file
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "BASA_V7_V8_FUSION_FULL_08694150021"
CORS(app)

BHD_CUENTA = "08694150021"
MODULOS = {
    "B4_BASE": {"nombre":"B4 Base - Informe Pericial","precio":7500,"incluido":True,"desc":"Informe base + contrato + demo"},
    "M1_SCRAPER": {"nombre":"M1 - Scraper Compras 10 anos","precio":2500,"desc":"Scraping DGCP 2014-2024"},
    "M2_FRACC": {"nombre":"M2 - Fraccionamiento Ley 340-06 Art5 + Reg 416-23","precio":3500,"desc":"4 criterios: temporal, objeto, proveedor, monto"},
    "M3_DUENO": {"nombre":"M3 - Mismo Dueno Multi-RNC","precio":3000,"desc":"Detecta testaferros"},
    "M4_ACC": {"nombre":"M4 - Accionistas Cruzados","precio":4000,"desc":"Red empresas vinculadas"},
    "M5_CONF": {"nombre":"M5 - Consanguinidad y Afinidad","precio":4500,"desc":"3er grado Art14"},
    "M6_NOM": {"nombre":"M6 - Nomina Fantasma","precio":3500,"desc":"TSS MAP doble cargo"},
    "M7_FIN": {"nombre":"M7 - Estados Financieros","precio":3000,"desc":"DGII capital vs contratos"},
    "M8_FULL": {"nombre":"M8 - Forense V8 Full + Actualizacion Leyes","precio":5000,"desc":"TODO + IA + auto-leyes"},
}

def calc_fact(mods):
    import calendar
    hoy = datetime.datetime.now()
    ultimo = calendar.monthrange(hoy.year, hoy.month)[1]
    dias = ultimo - hoy.day + 1
    total = sum(MODULOS[m]["precio"] for m in mods if m in MODULOS)
    primer = round((total/30)*dias,2)
    proximo = (hoy + datetime.timedelta(days=dias)).strftime("%d/%m/%Y")
    return {"mods":mods,"total":total,"primer":primer,"dias":dias,"proximo":proximo,"bhd":BHD_CUENTA}

@app.route('/')
def home():
    return jsonify({"BASA":"V7+V8 FUSION FULL","status":"LIVE","bhd":BHD_CUENTA,"rutas":["/activar-modulos","/b4","/v8","/api/auditoria-demo"]})

@app.route('/healthz')
def health():
    return jsonify({"status":"OK FULL"})

@app.route('/activar-modulos')
def activar():
    mods_html = ""
    for k,v in MODULOS.items():
        chk = "checked disabled" if v.get("incluido") else ""
        mods_html += "<div style='border:2px solid #e2e8f0;padding:14px;margin:10px 0;border-radius:12px;display:flex;justify-content:space-between;background:#f8fafc'><div><b>"+v["nombre"]+"</b><br><small>"+v["desc"]+"</small><br><span style='color:#00a86b;font-weight:bold'>RD$"+str(v["precio"])+"/mes</span></div><div><input type='checkbox' value='"+k+"' "+chk+" class='chk' onchange='calc()' style='width:24px;height:24px'></div></div>"

    html = """<html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>body{font-family:Arial;background:#0f172a;color:white;padding:12px}.card{background:white;color:black;padding:20px;border-radius:16px;max-width:950px;margin:auto}.btn{padding:12px;border-radius:10px;font-weight:bold;border:none;margin:6px;cursor:pointer;text-decoration:none;display:inline-block}.verde{background:#00d084;color:white;width:100%}.azul{background:#003366;color:white}.amarillo{background:#fef3c7;border:2px solid #f59e0b;padding:12px;border-radius:10px;margin:10px 0;color:#92400e}.fact{background:#f0f7ff;padding:14px;border-radius:12px;border-left:5px solid #003366}</style></head><body>
    <h1 style='text-align:center;color:#00d084'>BASA V7+V8 FUSION FULL - ACTIVAR MODULOS</h1><div class='card'>
    """+mods_html+"""
    <div class='fact'><h3>Facturacion Automatica BHD 08694150021</h3>Empresa: <input id='emp' style='width:100%;padding:8px'><br>RNC: <input id='rnc' style='width:100%;padding:8px'><div id='fact'>Calculando...</div></div>
    <div class='amarillo'><input type='checkbox' id='ok'> <b>ACEPTO CONTRATO VIRTUAL BASA V8 - BHD 08694150021</b><br><small>Firma digital valida Ley 126-02 RD. Actualizacion automatica leyes incluida.</small><br><a href='/api/contrato' target='_blank' class='btn azul'>Ver Contrato</a> <a href='/api/analisis-legal' target='_blank' class='btn azul'>Medidas Legales</a></div>
    <button class='btn verde' onclick='activarSys()'>ACEPTO Y ACTIVAR FULL + DESCARGAR DEMO</button><div id='res' style='display:none;background:#ecfdf5;padding:14px;border-radius:12px;margin-top:10px;border:2px solid #00d084'></div>
    <div style='text-align:center;margin-top:12px'><a href='/b4' class='btn azul'>B4 Informe</a> <a href='/v8' class='btn azul'>V8 Auditoria 10 anos</a> <a href='/api/auditoria-demo' class='btn azul'>Ver Auditoria JSON</a></div>
    </div><script>
    function calc(){var activos=['B4_BASE'];document.querySelectorAll('.chk:checked').forEach(function(c){if(c.value!='B4_BASE' && activos.indexOf(c.value)==-1) activos.push(c.value);});var precios={'B4_BASE':7500,'M1_SCRAPER':2500,'M2_FRACC':3500,'M3_DUENO':3000,'M4_ACC':4000,'M5_CONF':4500,'M6_NOM':3500,'M7_FIN':3000,'M8_FULL':5000};var total=0;activos.forEach(function(k){if(precios[k]) total+=precios[k];});var hoy=new Date();var ultimo=new Date(hoy.getFullYear(),hoy.getMonth()+1,0).getDate();var dias=ultimo-hoy.getDate()+1;var primer=Math.round((total/30)*dias);document.getElementById('fact').innerHTML='Modulos: '+activos.join(', ')+'<br>Total: RD$'+total+'<br>Primer pago ('+dias+' dias): RD$'+primer+'<br>BHD: 08694150021';window._act=activos;window._tot=total;window._pri=primer;}
    function activarSys(){if(!document.getElementById('ok').checked){alert('Acepte contrato');return;}var emp=document.getElementById('emp').value;var rnc=document.getElementById('rnc').value;if(!emp||!rnc){alert('Empresa y RNC');return;}fetch('/api/activar',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({mods:window._act,empresa:emp,rnc:rnc})}).then(function(r){return r.json();}).then(function(d){var res=document.getElementById('res');res.style.display='block';res.innerHTML='<h3>ACTIVADO '+d.contrato+'</h3><p>Total RD$'+window._tot+' Primer RD$'+window._pri+'</p><a href="/api/contrato/'+d.contrato+'" class="btn azul">Contrato Firmado</a> <a href="/demo" class="btn verde" style="width:auto">Descargar DEMO FULL</a> <a href="/b4" class="btn azul">B4</a> <a href="/v8" class="btn azul">V8</a>';});}
    calc();
    </script></body></html>"""
    return html

@app.route('/api/activar', methods=['POST'])
def api_act():
    data=request.get_json() or {}; mods=data.get('mods',['B4_BASE']); cid="CTR-V8-FULL-"+datetime.datetime.now().strftime("%Y%m%d-%H%M%S"); session['activado']=True; session['contrato']=cid; session['mods']=mods; session['empresa']=data.get('empresa',''); return jsonify({"contrato":cid,"fact":calc_fact(mods)})

@app.route('/api/contrato')
def cont_prev():
    txt="CONTRATO VIRTUAL BASA V8 ENTERPRISE FUSION V7+V8 FULL\nBHD 08694150021 Pedro Baldera\nFACTURACION: Prorrateado dias restantes, luego mensual\nACTUALIZACION AUTOMATICA LEYES RD 340-06, 416-23, 155-17, 126-02\nFIRMA VALIDA CHECKBOX\nMEDIDAS: Fraccionamiento Art5, Consanguinidad Art14"
    return send_file(io.BytesIO(txt.encode()), mimetype="application/pdf", as_attachment=True, download_name="CONTRATO_PREVIEW.pdf")

@app.route('/api/contrato/<cid>')
def cont_firm(cid):
    txt="CONTRATO FIRMADO "+cid+"\nBHD 08694150021\nMODULOS: "+",".join(session.get('mods',['B4_BASE']))+"\nEmpresa: "+session.get('empresa','')+"\nValido digital"
    return send_file(io.BytesIO(txt.encode()), mimetype="application/pdf", as_attachment=True, download_name=cid+".pdf")

@app.route('/api/analisis-legal')
def legal():
    return jsonify({"fraccionamiento":"Ley 340 Art5 - 4 compras mismo objeto <30 dias = CRITICO","consanguinidad":"Art14 - 3er grado","reg416":"2026 umbrales nuevos","medidas":["Scraper 10 anos","4 criterios","Multi-RNC","Accionistas","TSS/MAP","DGII","Auto-leyes"]})

@app.route('/b4')
def b4():
    banner="" if session.get('activado') else "<div style='background:#f59e0b;color:black;padding:10px;border-radius:8px;text-align:center'><b>DEMO</b> - <a href='/activar-modulos'>Activar FULL</a></div>"
    return "<body style='font-family:Arial;background:#0f172a;color:white;padding:15px'><h1>B4 Informe Pericial V7+V8</h1>"+banner+"<div style='background:white;color:black;padding:18px;border-radius:14px;max-width:1000px;margin:auto'><h2>Analisis Recuperados FULL</h2><ul><li>Fraccionamiento 30/60/90 dias</li><li>Mismo dueno Multi-RNC</li><li>Accionistas cruzados grafo</li><li>Consanguinidad 3er grado</li><li>Nomina fantasma TSS/MAP</li><li>Financieros DGII</li><li>Actualizacion automatica leyes 2026</li></ul><a href='/activar-modulos' style='background:#00d084;color:white;padding:10px;border-radius:8px;text-decoration:none'>Activar</a> <a href='/v8' style='background:#003366;color:white;padding:10px;border-radius:8px;text-decoration:none'>V8</a> <a href='/api/auditoria-demo' style='background:#6b7280;color:white;padding:10px;border-radius:8px;text-decoration:none'>JSON Auditoria</a></div></body>"

@app.route('/v8')
def v8():
    banner="" if session.get('activado') else "<div style='background:#f59e0b;color:black;padding:10px;border-radius:8px;text-align:center'>DEMO - <a href='/activar-modulos'>Activar V8 FULL</a></div>"
    return "<body style='font-family:Arial;background:#0a192f;color:white;padding:15px'><h1 style='color:#00d084'>V8 Auditoria 10 Anos FUSION V7</h1>"+banner+"<div style='background:white;color:black;padding:18px;border-radius:14px;max-width:1100px;margin:auto'><h2>Scraper + 7 Motores</h2><table style='width:100%;border-collapse:collapse;font-size:12px'><tr style='background:#003366;color:white'><th style='padding:8px'>Hallazgo</th><th>Proveedor</th><th>Monto</th><th>Riesgo</th></tr><tr style='border-bottom:1px solid #ddd'><td style='padding:8px'>Fraccionamiento 5 compras 22 dias</td><td>Comercial ABC</td><td>RD$4.2MM</td><td style='color:red'><b>CRITICO</b></td></tr><tr style='border-bottom:1px solid #ddd'><td style='padding:8px'>Mismo dueno 3 RNC</td><td>Juan Perez</td><td>RD$12MM</td><td style='color:red'><b>ALTO</b></td></tr><tr><td style='padding:8px'>Consanguinidad primo director</td><td>XYZ SRL</td><td>RD$2.1MM</td><td style='color:orange'><b>MEDIO</b></td></tr></table><div style='text-align:center;margin-top:12px'><a href='/activar-modulos' style='background:#00d084;color:white;padding:10px;border-radius:8px;text-decoration:none'>Activar Full</a> <a href='/b4' style='background:#003366;color:white;padding:10px;border-radius:8px;text-decoration:none'>B4</a></div></div></body>"

@app.route('/api/auditoria-demo')
def audit_demo():
    return jsonify({"sistema":"BASA V7+V8 FUSION FULL","bhd":BHD_CUENTA,"hallazgos":[{"tipo":"Fraccionamiento","monto":"RD$4.2MM","riesgo":"CRITICO"},{"tipo":"Mismo Dueno","monto":"RD$12MM","riesgo":"ALTO"},{"tipo":"Consanguinidad","monto":"RD$2.1MM","riesgo":"MEDIO"}],"medidas":["Scraper 10 anos","4 criterios","Multi-RNC","Accionistas","TSS/MAP","DGII","Auto-leyes 2026"]})

@app.route('/demo')
def demo():
    m=io.BytesIO()
    with zipfile.ZipFile(m,mode="w",compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("BASA_V7_V8_FUSION_FULL/README.txt","BASA V7+V8 FUSION FULL - BHD 08694150021 - Sistema completo recuperado")
        zf.writestr("BASA_V7_V8_FUSION_FULL/MODULOS.txt","\n".join([k+" "+v["nombre"] for k,v in MODULOS.items()]))
    m.seek(0)
    return send_file(m,mimetype="application/zip",as_attachment=True,download_name="BASA_V7_V8_FUSION_FULL.zip")

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get("PORT",10000)))
