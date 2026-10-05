import os, io, zipfile, datetime, json
from flask import Flask, jsonify, request, session, send_file
from flask_cors import CORS
app = Flask(__name__)
app.secret_key = "BASA_V9_INTERNACIONAL_250USD"
CORS(app)

BHD_CUENTA = "08694150021 - USD Y DOP"
USD_POR_MODULO = 250

PAISES_LEYES = {
    "DO": {"nombre":"Rep. Dominicana","moneda":"USD/DOP","impuesto":0.18,"leyes":["Ley 340-06","Reg 416-23","NOBACI","Ley 10-07 Control Interno","Ley 155-17 Lavado","Ley 126-02 Firma Digital"],"idiomas":["es"]},
    "US": {"nombre":"Estados Unidos","moneda":"USD","impuesto":0.0,"leyes":["FAR","2 CFR 200","SOX","GAAP"],"idiomas":["en","es"]},
    "MX": {"nombre":"Mexico","moneda":"USD/MXN","impuesto":0.16,"leyes":["Ley Adquisiciones","LAASSP","Ley Anticorrupcion"],"idiomas":["es"]},
    "PA": {"nombre":"Panama","moneda":"USD","impuesto":0.07,"leyes":["Ley 22 Contrataciones","NOBACI PA"],"idiomas":["es"]},
    "CO": {"nombre":"Colombia","moneda":"USD/COP","impuesto":0.19,"leyes":["Ley 80","Estatuto Anticorrupcion"],"idiomas":["es"]},
    "ES": {"nombre":"Espana","moneda":"EUR","impuesto":0.21,"leyes":["LCSP","Ley Transparencia"],"idiomas":["es","en"]},
}

MODULOS_V9 = {
    "B4_BASE": {"nombre":"B4 Base - Informe Pericial IA","precio_usd":250,"cat":"Informes","desc":"Informe base IA multi-idioma + contrato + demo + NOBACI"},
    "M1_SCRAPER": {"nombre":"M1 - Scraper Compras 10 anos IA","precio_usd":250,"cat":"Auditoria","desc":"Scraping automatico portal compras segun pais + IA"},
    "M2_FRACC": {"nombre":"M2 - Fraccionamiento + Libramientos","precio_usd":250,"cat":"Auditoria","desc":"Fraccionamiento + Analisis libramientos contraloria + IA"},
    "M3_DUENO": {"nombre":"M3 - Mismo Dueno + Beneficiario Final","precio_usd":250,"cat":"Forense","desc":"Multi-RNC testaferros + beneficiario final global"},
    "M4_ACC": {"nombre":"M4 - Accionistas + Activos Ocultos","precio_usd":250,"cat":"Forense","desc":"Red accionistas + Analisis activos y patrimonio IA"},
    "M5_CONF": {"nombre":"M5 - Consanguinidad + Conflicto Interes","precio_usd":250,"cat":"Legal","desc":"Parentesco + conflicto + PEPs mundial"},
    "M6_NOM": {"nombre":"M6 - Nomina Fantasma + Pagos + TSS","precio_usd":250,"cat":"Nomina","desc":"Nomina, doble cargo, pagos, TSS, MAP, IRS segun pais"},
    "M7_FIN": {"nombre":"M7 - Estados Financieros + Pagos Trucados","precio_usd":250,"cat":"Financiero","desc":"DGII/IRS/SAT vs contrataciones + pagos"},
    "M8_FULL": {"nombre":"M8 - Forense V8 Full + IA Predictiva","precio_usd":250,"cat":"IA","desc":"TODO + IA predictiva + auto-actualizacion leyes pais"},
    "M9_NOBACI": {"nombre":"M9 - NOBACI + Evaluaciones Internas","precio_usd":250,"cat":"Control Interno","desc":"Evaluacion NOBACI RD + COSO + Control Interno + Matriz Riesgo IA"},
    "M10_INV": {"nombre":"M10 - Inventarios + Activos Fijos IA","precio_usd":250,"cat":"Inventarios","desc":"Inventario, activos fijos, depreciacion, toma fisica + IA"},
    "M11_PAGOS": {"nombre":"M11 - Pagos + Libramientos + Tesoreria","precio_usd":250,"cat":"Tesoreria","desc":"Analisis libramientos, pagos, cheques, transferencias + IA forense"},
    "M12_INF": {"nombre":"M12 - Informes IA Multi-Pais + Multi-Moneda","precio_usd":250,"cat":"Informes","desc":"Informes periciales automaticos IA en idioma y moneda seleccionada"},
}

def calcular_usd(mods, pais="DO"):
    info_pais = PAISES_LEYES.get(pais, PAISES_LEYES["DO"])
    imp = info_pais["impuesto"]
    subtotal = sum(MODULOS_V9[m]["precio_usd"] for m in mods if m in MODULOS_V9)
    impuesto = round(subtotal * imp, 2)
    total = subtotal + impuesto
    import calendar
    hoy = datetime.datetime.now()
    ultimo = calendar.monthrange(hoy.year, hoy.month)[1]
    dias = ultimo - hoy.day + 1
    primer = round((total/30)*dias,2)
    return {"mods":mods,"subtotal":subtotal,"impuesto":impuesto,"total":total,"primer":primer,"dias":dias,"pais":pais,"info":info_pais,"tasa":imp,"bhd":BHD_CUENTA}

@app.route('/')
def home():
    return jsonify({"BASA":"V9 INTERNACIONAL USD250","bhd":BHD_CUENTA,"modulos":len(MODULOS_V9),"precio":"USD250 x modulo + impuestos","paises":list(PAISES_LEYES.keys())})

@app.route('/healthz')
def health():
    return jsonify({"status":"OK V9 USD250"})

@app.route('/activar-modulos')
def activar_mod():
    mods_html = ""
    cats = {}
    for k,v in MODULOS_V9.items():
        c = v["cat"]
        if c not in cats: cats[c]=[]
        cats[c].append((k,v))
    for cat, lista in cats.items():
        mods_html += "<h3 style='color:#003366;margin-top:15px;border-bottom:2px solid #00d084'>"+cat+"</h3>"
        for k,v in lista:
            chk = "checked disabled" if k=="B4_BASE" else ""
            mods_html += "<div style='border:2px solid #e2e8f0;padding:12px;margin:8px 0;border-radius:12px;display:flex;justify-content:space-between;background:#f8fafc'><div><b>"+v["nombre"]+"</b><br><small>"+v["desc"]+"</small><br><span style='color:#00a86b;font-weight:bold'>USD$"+str(v["precio_usd"])+"/mes + imp</span></div><div><input type='checkbox' value='"+k+"' "+chk+" class='chk' onchange='calcUSD()' style='width:22px;height:22px'></div></div>"

    pais_opts = ""
    for code,info in PAISES_LEYES.items():
        pais_opts += "<option value='"+code+"'>"+info["nombre"]+" - "+",".join(info["leyes"][:2])+"</option>"

    html = """<html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>body{font-family:Arial;background:#0f172a;color:white;padding:10px}.card{background:white;color:black;padding:18px;border-radius:16px;max-width:1000px;margin:auto}.btn{padding:10px;border-radius:8px;font-weight:bold;border:none;margin:5px;cursor:pointer;text-decoration:none;display:inline-block}.verde{background:#00d084;color:white;width:100%;font-size:15px}.azul{background:#003366;color:white}.fact{background:#f0f7ff;padding:14px;border-radius:12px;border-left:5px solid #003366}.amarillo{background:#fef3c7;border:2px solid #f59e0b;padding:12px;border-radius:10px;margin:10px 0;color:#92400e}select,input{width:100%;padding:9px;border:2px solid #cbd5e1;border-radius:8px;margin:4px 0}</style></head><body>
    <h1 style='text-align:center;color:#00d084'>BASA V9 INTERNACIONAL<br><small style='font-size:13px;color:#94a3b8'>USD$250 x Modulo + Impuestos | NOBACI | Multi-Pais | Multi-Idioma | IA</small></h1>
    <div class='card'>
    <div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px'>
    <div>Pais/Leyes: <select id='pais' onchange='calcUSD()'>"""+pais_opts+"""</select></div>
    <div>Idioma: <select id='idioma' onchange='calcUSD()'><option value='es'>Espanol</option><option value='en'>English</option><option value='fr'>Francais</option><option value='pt'>Portugues</option></select></div>
    <div>Moneda: <select id='moneda' onchange='calcUSD()'><option value='USD'>USD Dolar</option><option value='DOP'>DOP Peso Dom</option><option value='EUR'>EUR Euro</option><option value='MXN'>MXN Peso Mex</option></select></div>
    </div>
    """+mods_html+"""
    <div class='fact'><h3>Facturacion Automatica USD BHD """+BHD_CUENTA+"""</h3>
    Empresa: <input id='emp' placeholder='Empresa'><br>RNC/TAX ID: <input id='rnc' placeholder='RNC'><br>
    <div id='factUSD'>Calculando USD...</div></div>
    <div class='amarillo'><input type='checkbox' id='ok'> <b>ACEPTO CONTRATO V9 INTERNACIONAL USD250</b><br><small>USD250 por modulo + impuestos pais. NOBACI + Libramientos + Inventarios + Nomina + Activos + IA incluidos segun modulos. Firma digital Ley 126-02 + ESIGN US + eIDAS EU.</small><br><a href='/api/contrato' target='_blank' class='btn azul'>Ver Contrato V9</a> <a href='/api/nobaci' target='_blank' class='btn azul'>Ver NOBACI + Libramientos</a></div>
    <button class='btn verde' onclick='activarV9()'>ACEPTO Y ACTIVAR V9 USD + DESCARGAR TODO</button><div id='res' style='display:none;background:#ecfdf5;padding:14px;border-radius:12px;margin-top:10px;border:2px solid #00d084'></div>
    <div style='text-align:center;margin-top:10px'><a href='/b4' class='btn azul'>B4 Informe IA</a> <a href='/v8' class='btn azul'>V8 Auditoria + NOBACI</a> <a href='/api/auditoria-demo' class='btn azul'>Demo JSON V9</a></div>
    </div><script>
    function calcUSD(){var activos=['B4_BASE'];document.querySelectorAll('.chk:checked').forEach(function(c){if(c.value!='B4_BASE' && activos.indexOf(c.value)==-1) activos.push(c.value);});var total=activos.length*250;var pais=document.getElementById('pais').value;var imp=0.18;if(pais=='DO') imp=0.18; if(pais=='MX') imp=0.16; if(pais=='PA') imp=0.07; if(pais=='CO') imp=0.19; if(pais=='ES') imp=0.21; if(pais=='US') imp=0;var impuesto=Math.round(total*imp*100)/100;var grand=total+impuesto;var hoy=new Date();var ultimo=new Date(hoy.getFullYear(),hoy.getMonth()+1,0).getDate();var dias=ultimo-hoy.getDate()+1;var primer=Math.round((grand/30)*dias*100)/100;var moneda=document.getElementById('moneda').value;document.getElementById('factUSD').innerHTML='Pais: '+pais+' | Modulos: '+activos.length+'<br>Subtotal: USD$'+total+' (USD$250 x '+activos.length+')<br>Impuesto '+Math.round(imp*100)+'%: USD$'+impuesto+'<br><b>Total Mensual: USD$'+grand+' '+moneda+'</b><br>Primer pago ('+dias+' dias): <b>USD$'+primer+'</b><br>BHD: """+BHD_CUENTA+""" - Multi-moneda';window._act=activos;window._grand=grand;window._pri=primer;window._pais=pais;}
    function activarV9(){if(!document.getElementById('ok').checked){alert('Acepte contrato');return;}var emp=document.getElementById('emp').value;var rnc=document.getElementById('rnc').value;if(!emp||!rnc){alert('Empresa y RNC');return;}fetch('/api/activar-v9',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({mods:window._act,pais:window._pais,empresa:emp,rnc:rnc,idioma:document.getElementById('idioma').value,moneda:document.getElementById('moneda').value})}).then(function(r){return r.json();}).then(function(d){var res=document.getElementById('res');res.style.display='block';res.innerHTML='<h3>ACTIVADO V9 '+d.contrato+'</h3><p>USD$'+window._grand+' Total - Primer USD$'+window._pri+'</p><a href="/api/contrato/'+d.contrato+'" class="btn azul">Contrato V9 USD</a> <a href="/demo" class="btn verde" style="width:auto">Descargar V9 FULL</a> <a href="/b4" class="btn azul">B4</a> <a href="/v8" class="btn azul">V8+NOBACI</a>';});}
    calcUSD();
    </script></body></html>"""
    return html

@app.route('/api/activar-v9', methods=['POST'])
def activar_v9():
    data=request.get_json() or {}; mods=data.get('mods',['B4_BASE']); pais=data.get('pais','DO'); cid="CTR-V9-USD-"+datetime.datetime.now().strftime("%Y%m%d-%H%M%S"); session['activado']=True; session['contrato']=cid; session['mods']=mods; session['pais']=pais; return jsonify({"contrato":cid,"fact":calcular_usd(mods,pais)})

@app.route('/api/nobaci')
def nobaci():
    return jsonify({"NOBACI_RD":{"componentes":["Ambiente Control","Valoracion Riesgo","Actividades Control","Informacion","Monitoreo"],"evaluacion":"Matriz NOBACI + COSO + IA","libramientos":["Analisis libramientos Contraloria","Cruce SIGEF","Deteccion libramientos sin soporte","Pagos duplicados"]},"inventarios":{"procesos":["Toma fisica IA","Kardex","Activos fijos","Depreciacion","Obsolescencia"]},"nomina":{"modulo":"Nomina + Pagos + TSS + MAP + IRS + SAT","analisis":["Nomina fantasma","Doble cargo","Pagos sin retencion","Horas extras excesivas"]}})

@app.route('/api/contrato')
def contrato():
    txt="CONTRATO V9 INTERNACIONAL USD250 x MODULO + IMPUESTOS\nBHD 08694150021\nMODULOS: USD250 cada uno - B4, M1-M12\nINCLUYE: NOBACI, Libramientos, Inventarios, Nomina, Activos, Pagos, Informes IA\nMulti-Pais: DO,US,MX,PA,CO,ES - Multi-Idioma ES,EN,FR,PT - Multi-Moneda USD,DOP,EUR,MXN\nFirma digital valida internacional"
    return send_file(io.BytesIO(txt.encode()), mimetype="application/pdf", as_attachment=True, download_name="CONTRATO_V9_USD250.pdf")

@app.route('/api/contrato/<cid>')
def contrato_id(cid):
    txt="CONTRATO V9 FIRMADO "+cid+" USD250 x modulo + impuestos BHD "+BHD_CUENTA
    return send_file(io.BytesIO(txt.encode()), mimetype="application/pdf", as_attachment=True, download_name=cid+".pdf")

@app.route('/b4')
def b4():
    return "<body style='font-family:Arial;background:#0f172a;color:white;padding:12px'><h1>B4 V9 + NOBACI + Inventarios IA</h1><div style='background:white;color:black;padding:16px;border-radius:12px;max-width:1000px;margin:auto'><p>USD250 x modulo + impuestos</p><ul><li>Informe Pericial IA multi-idioma</li><li>NOBACI Evaluacion Interna</li><li>Libramientos Contraloria SIGEF</li><li>Inventarios y Activos Fijos</li><li>Nomina y Pagos</li></ul><a href='/activar-modulos' style='background:#00d084;color:white;padding:8px;border-radius:6px;text-decoration:none'>Activar V9</a></div></body>"

@app.route('/v8')
def v8():
    return "<body style='font-family:Arial;background:#0a192f;color:white;padding:12px'><h1 style='color:#00d084'>V9 Auditoria + NOBACI + Libramientos + Inventarios IA</h1><div style='background:white;color:black;padding:16px;border-radius:12px;max-width:1100px;margin:auto'><p>Multi-Pais Multi-Moneda Multi-Idioma</p><table style='width:100%;border-collapse:collapse;font-size:11px'><tr style='background:#003366;color:white'><th>Modulo USD250</th><th>Analisis IA</th><th>Ley</th></tr><tr><td>M9 NOBACI</td><td>Control Interno + Riesgo</td><td>NOBACI RD + COSO</td></tr><tr><td>M11 Pagos/Libram</td><td>SIGEF + duplicados</td><td>Ley 10-07</td></tr><tr><td>M10 Inventarios</td><td>Toma fisica IA</td><td>NOBACI Activos</td></tr></table></div></body>"

@app.route('/api/auditoria-demo')
def demo_json():
    return jsonify({"V9_USD250":{"precio_por_modulo":"USD250 + impuestos","total_modulos":12,"paises":PAISES_LEYES,"modulos_nuevos":{"M9_NOBACI":"NOBACI + Evaluaciones","M10_INV":"Inventarios + Activos","M11_PAGOS":"Pagos + Libramientos","M12_INF":"Informes IA Multi-Pais"}},"bhd":BHD_CUENTA})

@app.route('/demo')
def demo_zip():
    m=io.BytesIO()
    with zipfile.ZipFile(m,mode="w",compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("V9_README.txt","BASA V9 USD250 x modulo + impuestos - NOBACI + Libramientos + Inventarios + Nomina + IA")
    m.seek(0)
    return send_file(m,mimetype="application/zip",as_attachment=True,download_name="BASA_V9_USD250_FULL.zip")

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get("PORT",10000)))
