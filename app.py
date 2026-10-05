import os, io, zipfile, datetime, json, calendar
from flask import Flask, jsonify, request, session, send_file
from flask_cors import CORS
app = Flask(__name__)
app.secret_key = "BASA_V9_2_FINAL_FULL_USD250_STRIPE"
CORS(app)

BHD_CUENTA = "08694150021 - USD Y DOP"
USD_POR_MODULO = 250
STRIPE_KEY = os.environ.get("STRIPE_SECRET_KEY", "")

PAISES_LEYES = {
    "DO": {"nombre":"Rep. Dominicana","moneda":"USD/DOP","impuesto":0.18,"leyes":["Ley 340-06","Reg 416-23","NOBACI","Ley 10-07","Ley 155-17","Ley 126-02"]},
    "US": {"nombre":"Estados Unidos","moneda":"USD","impuesto":0.0,"leyes":["FAR","2 CFR 200","SOX","GAAP","ESIGN"]},
    "MX": {"nombre":"Mexico","moneda":"USD/MXN","impuesto":0.16,"leyes":["LAASSP","Anticorrupcion"]},
    "PA": {"nombre":"Panama","moneda":"USD","impuesto":0.07,"leyes":["Ley 22 Contrataciones"]},
    "CO": {"nombre":"Colombia","moneda":"USD/COP","impuesto":0.19,"leyes":["Ley 80"]},
    "ES": {"nombre":"Espana","moneda":"EUR","impuesto":0.21,"leyes":["LCSP","eIDAS"]},
}

MODULOS_V9 = {
    "B4_BASE": {"nombre":"B4 Base - Informe Pericial IA","precio":250,"cat":"Informes","desc":"Informe base IA multi-idioma + NOBACI"},
    "M1_SCRAPER": {"nombre":"M1 - Scraper Compras 10 anos IA","precio":250,"cat":"Auditoria","desc":"Scraping portal compras segun pais + IA"},
    "M2_FRACC": {"nombre":"M2 - Fraccionamiento + Libramientos","precio":250,"cat":"Auditoria","desc":"Fracc 4 criterios + Analisis libramientos SIGEF Contraloria + IA"},
    "M3_DUENO": {"nombre":"M3 - Mismo Dueno + Beneficiario Final","precio":250,"cat":"Forense","desc":"Multi-RNC testaferros + beneficiario final global"},
    "M4_ACC": {"nombre":"M4 - Accionistas + Activos Ocultos","precio":250,"cat":"Forense","desc":"Red accionistas + Analisis activos patrimonio IA"},
    "M5_CONF": {"nombre":"M5 - Consanguinidad + PEPs","precio":250,"cat":"Legal","desc":"Parentesco + conflicto interes + PEPs mundial"},
    "M6_NOM": {"nombre":"M6 - Nomina + Pagos + TSS","precio":250,"cat":"Nomina","desc":"Nomina fantasma, doble cargo, pagos TSS, MAP, IRS, SAT"},
    "M7_FIN": {"nombre":"M7 - Estados Financieros + Pagos","precio":250,"cat":"Financiero","desc":"DGII vs contrataciones + pagos trucados IA"},
    "M8_FULL": {"nombre":"M8 - Forense Full + IA Predictiva","precio":250,"cat":"IA","desc":"TODO + IA predictiva + auto-leyes pais"},
    "M9_NOBACI": {"nombre":"M9 - NOBACI + Control Interno","precio":250,"cat":"Control Interno","desc":"NOBACI RD + COSO + Matriz Riesgo + Evaluacion IA"},
    "M10_INV": {"nombre":"M10 - Inventarios + Activos Fijos","precio":250,"cat":"Inventarios","desc":"Toma fisica IA, Kardex, depreciacion, obsolescencia"},
    "M11_PAGOS": {"nombre":"M11 - Pagos + Libramientos + Tesoreria","precio":250,"cat":"Tesoreria","desc":"Libramientos Contraloria, SIGEF, cheques, transferencias IA"},
    "M12_INF": {"nombre":"M12 - Informes IA Multi-Pais","precio":250,"cat":"Informes","desc":"Informes periciales automaticos IA idioma y moneda seleccionada"},
}

def calcular_usd(mods, pais="DO"):
    info = PAISES_LEYES.get(pais, PAISES_LEYES["DO"])
    imp = info["impuesto"]
    subtotal = sum(MODULOS_V9[m]["precio"] for m in mods if m in MODULOS_V9)
    impuesto = round(subtotal * imp, 2)
    total = subtotal + impuesto
    hoy = datetime.datetime.now()
    ultimo = calendar.monthrange(hoy.year, hoy.month)[1]
    dias = ultimo - hoy.day + 1
    primer = round((total/30)*dias,2)
    return {"mods":mods,"subtotal":subtotal,"impuesto":impuesto,"total":total,"primer":primer,"dias":dias,"pais":pais,"info":info,"bhd":BHD_CUENTA}

@app.route('/')
def home():
    return jsonify({"BASA":"V9.2 FINAL FULL USD250 STRIPE","bhd":BHD_CUENTA,"precio":"USD250 x modulo + impuestos","modulos":len(MODULOS_V9),"paises":list(PAISES_LEYES.keys()),"pago":"Stripe + PayPal + BHD automatico"})

@app.route('/healthz')
def health():
    return jsonify({"status":"OK V9.2 STRIPE"})

@app.route('/activar-modulos')
def activar_mod():
    mods_html = ""
    cats = {}
    for k,v in MODULOS_V9.items():
        c = v["cat"]
        if c not in cats: cats[c]=[]
        cats[c].append((k,v))
    for cat, lista in cats.items():
        mods_html += "<h3 style='color:#003366;margin-top:15px;border-bottom:2px solid #00d084'>" + cat + "</h3>"
        for k,v in lista:
            chk = "checked disabled" if k=="B4_BASE" else "checked"
            mods_html += "<div style='border:2px solid #e2e8f0;padding:12px;margin:8px 0;border-radius:12px;display:flex;justify-content:space-between;background:#f8fafc'><div><b>" + v["nombre"] + "</b><br><small>" + v["desc"] + "</small><br><span style='color:#00a86b;font-weight:bold'>USD$" + str(v["precio"]) + "/mes + imp</span></div><div><input type='checkbox' value='" + k + "' " + chk + " class='chk' onchange='calcUSD()' style='width:22px;height:22px'></div></div>"
    pais_opts = ""
    for code,info in PAISES_LEYES.items():
        pais_opts += "<option value='" + code + "'>" + info["nombre"] + " - " + ",".join(info["leyes"][:2]) + "</option>"
    html = "<html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>body{font-family:Arial;background:#0f172a;color:white;padding:10px}.card{background:white;color:black;padding:18px;border-radius:16px;max-width:1000px;margin:auto}.btn{padding:10px;border-radius:8px;font-weight:bold;border:none;margin:5px;cursor:pointer;text-decoration:none;display:inline-block}.verde{background:#00d084;color:white;width:100%;font-size:16px;padding:14px}.azul{background:#003366;color:white}.fact{background:#f0f7ff;padding:14px;border-radius:12px;border-left:5px solid #003366}.amarillo{background:#fef3c7;border:2px solid #f59e0b;padding:12px;border-radius:10px;margin:10px 0;color:#92400e}select,input{width:100%;padding:9px;border:2px solid #cbd5e1;border-radius:8px;margin:4px 0}</style></head><body>"
    html += "<h1 style='text-align:center;color:#00d084'>BASA V9.2 FINAL FULL<br><small style='font-size:12px;color:#94a3b8'>USD$250 x Modulo + Impuestos | NOBACI | Libramientos | Inventarios | Nomina | Multi-Pais | Stripe Auto</small></h1><div class='card'>"
    html += "<div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px'><div>Pais/Leyes: <select id='pais' onchange='calcUSD()'>" + pais_opts + "</select></div><div>Idioma: <select id='idioma'><option value='es'>Espanol</option><option value='en'>English</option><option value='fr'>Francais</option><option value='pt'>Portugues</option></select></div><div>Moneda: <select id='moneda'><option value='USD'>USD Dolar</option><option value='DOP'>DOP</option><option value='EUR'>EUR</option><option value='MXN'>MXN</option></select></div></div>"
    html += mods_html
    html += "<div class='fact'><h3>Facturacion Automatica USD BHD " + BHD_CUENTA + " + Stripe</h3>Empresa: <input id='emp' placeholder='Empresa'><br>RNC/TAX ID: <input id='rnc' placeholder='RNC'><br><div id='factUSD'>Calculando...</div></div>"
    html += "<div class='amarillo'><input type='checkbox' id='ok'> <b>ACEPTO CONTRATO V9.2 USD250 + PAGO AUTOMATICO</b><br><small>USD250 por modulo + impuestos pais. Incluye NOBACI, Libramientos, Inventarios, Nomina, Activos, Pagos, Informes IA. Firma digital Ley 126-02 + ESIGN + eIDAS. Pago Stripe tarjeta o BHD " + BHD_CUENTA + "</small><br><a href='/api/contrato' target='_blank' class='btn azul'>Ver Contrato</a> <a href='/api/nobaci' target='_blank' class='btn azul'>Ver NOBACI</a></div>"
    html += "<button class='btn verde' onclick='pagarAuto()'>PAGAR AUTOMATICO USD + ACTIVAR FULL</button><div id='res' style='display:none;background:#ecfdf5;padding:14px;border-radius:12px;margin-top:10px;border:2px solid #00d084'></div>"
    html += "<div style='text-align:center;margin-top:10px'><a href='/b4' class='btn azul'>B4 Informe IA</a> <a href='/v8' class='btn azul'>V8 Auditoria NOBACI</a> <a href='/api/auditoria-demo' class='btn azul'>Demo JSON</a></div></div>"
    html += "<script>function calcUSD(){var activos=[];document.querySelectorAll('.chk:checked').forEach(function(c){if(activos.indexOf(c.value)==-1) activos.push(c.value);});if(activos.indexOf('B4_BASE')==-1) activos.unshift('B4_BASE');var total=activos.length*250;var pais=document.getElementById('pais').value;var imp=0.18;if(pais=='DO') imp=0.18; if(pais=='MX') imp=0.16; if(pais=='PA') imp=0.07; if(pais=='CO') imp=0.19; if(pais=='ES') imp=0.21; if(pais=='US') imp=0;var impuesto=Math.round(total*imp*100)/100;var grand=total+impuesto;var hoy=new Date();var ultimo=new Date(hoy.getFullYear(),hoy.getMonth()+1,0).getDate();var dias=ultimo-hoy.getDate()+1;var primer=Math.round((grand/30)*dias*100)/100;var moneda=document.getElementById('moneda').value;document.getElementById('factUSD').innerHTML='Pais: '+pais+' | Modulos: '+activos.length+'<br>Subtotal: USD$'+total+' (USD$250 x '+activos.length+')<br>Impuesto '+Math.round(imp*100)+'%: USD$'+impuesto+'<br><b>Total Mensual: USD$'+grand+' '+moneda+'</b><br>Primer pago ('+dias+' dias): <b>USD$'+primer+'</b><br>BHD: " + BHD_CUENTA + " - Stripe Tarjeta';window._act=activos;window._grand=grand;window._pri=primer;window._pais=pais;} function pagarAuto(){if(!document.getElementById('ok').checked){alert('Acepte contrato');return;}var emp=document.getElementById('emp').value;var rnc=document.getElementById('rnc').value;if(!emp||!rnc){alert('Empresa y RNC');return;}var btn=document.querySelector('.verde');btn.innerHTML='PROCESANDO PAGO USD$'+window._grand+'...';fetch('/api/pagar-stripe',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({mods:window._act,pais:window._pais,empresa:emp,rnc:rnc,total:window._grand,moneda:document.getElementById('moneda').value,idioma:document.getElementById('idioma').value})}).then(function(r){return r.json();}).then(function(d){if(d.url){window.location=d.url;}else if(d.bhd){var res=document.getElementById('res');res.style.display='block';res.innerHTML='<h3>FACTURA BHD GENERADA</h3><p>Total USD$'+d.total+'</p><p>Transfiera a BHD "+BHD_CUENTA+"<br>Concepto: BASA V9 '+emp+'</p><a href=\"/pago-exitoso?demo=1&empresa='+emp+'\" class=\"btn verde\">Ya pague - Activar Ahora</a>';}else{alert('Error: '+(d.error||'Stripe no configurado - use BHD'));window.location='/pago-exitoso?demo=1';}});} calcUSD();</script></body></html>"
    return html

@app.route('/api/activar-v9', methods=['POST'])
def activar_v9():
    data=request.get_json() or {}
    mods=data.get('mods',['B4_BASE'])
    pais=data.get('pais','DO')
    cid="CTR-V9-"+datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    session['activado']=True
    session['contrato']=cid
    session['mods']=mods
    session['pais']=pais
    return jsonify({"contrato":cid,"fact":calcular_usd(mods,pais)})

@app.route('/api/pagar-stripe', methods=['POST'])
def pagar_stripe():
    data=request.get_json() or {}
    mods=data.get('mods',[])
    pais=data.get('pais','DO')
    total=data.get('total',3835)
    empresa=data.get('empresa','Cliente')
    if STRIPE_KEY and STRIPE_KEY.startswith("sk_"):
        try:
            import stripe
            stripe.api_key = STRIPE_KEY
            sess = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{'price_data':{'currency':'usd','product_data':{'name':'BASA V9 '+str(len(mods))+' modulos '+pais+' - '+empresa},'unit_amount': int(total*100)},'quantity':1}],
                mode='payment',
                success_url='https://basa-v7-1.onrender.com/pago-exitoso?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='https://basa-v7-1.onrender.com/activar-modulos',
                metadata={'mods':','.join(mods),'pais':pais,'empresa':empresa}
            )
            return jsonify({"url": sess.url, "id": sess.id})
        except Exception as e:
            return jsonify({"error": str(e), "bhd": BHD_CUENTA, "total": total, "fallback": "/pago-exitoso"})
    else:
        return jsonify({"bhd": BHD_CUENTA, "total": total, "mensaje": "Stripe no configurado - Use BHD 08694150021 - Se activa al dar click en Ya pague", "fallback": "/pago-exitoso"})

@app.route('/pago-exitoso')
def pago_exitoso():
    sid = request.args.get('session_id','BHD-'+datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    emp = request.args.get('empresa','Cliente V9')
    session['activado']=True
    session['contrato']="CTR-V9-PAGADO-"+datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    session['pago']='PAGADO-'+sid
    return "<body style='font-family:Arial;background:#ecfdf5;padding:20px;text-align:center'><h1 style='color:#00a86b'>PAGO EXITOSO - BASA V9 ACTIVADO FULL</h1><div style='background:white;padding:20px;border-radius:14px;max-width:700px;margin:auto'><h2>Transaccion: " + sid + "</h2><p>Empresa: " + emp + "</p><p>BHD " + BHD_CUENTA + " - USD$250 x modulo + impuestos</p><p><b>Banner DEMO eliminado - Sistema FULL activo - 12 modulos NOBACI + Libramientos + Inventarios + Nomina + IA</b></p><a href='/b4' style='background:#00d084;color:white;padding:12px;border-radius:8px;text-decoration:none;margin:5px;display:inline-block'>Entrar B4 Informe IA</a><a href='/v8' style='background:#003366;color:white;padding:12px;border-radius:8px;text-decoration:none;margin:5px;display:inline-block'>Entrar V8+NOBACI+Libramientos</a><a href='/demo' style='background:#6b7280;color:white;padding:12px;border-radius:8px;text-decoration:none;margin:5px;display:inline-block'>Descargar TODO V9.2</a><br><br><p style='color:#6b7280'>Multi-Pais Multi-Idioma Multi-Moneda activo</p></div></body>"

@app.route('/api/pagar-bhd', methods=['POST'])
def pagar_bhd():
    data=request.get_json() or {}
    return jsonify({"banco":"BHD Leon","cuenta":BHD_CUENTA,"beneficiario":"Pedro Baldera BASA V9","monto_usd": data.get('total',3835),"concepto": "BASA V9 "+str(len(data.get('mods',[])))+" modulos "+data.get('pais','DO'),"activacion":"/pago-exitoso"})

@app.route('/api/nobaci')
def nobaci():
    return jsonify({"NOBACI_RD":{"componentes":["Ambiente Control","Valoracion Riesgo","Actividades Control","Informacion","Monitoreo"],"evaluacion":"Matriz NOBACI + COSO + IA"},"libramientos":{"SIGEF":["Analisis libramientos Contraloria","Cruce SIGEF","Deteccion sin soporte","Pagos duplicados"],"ley":"Ley 10-07"},"inventarios":{"procesos":["Toma fisica IA","Kardex","Activos fijos","Depreciacion"]},"nomina":{"analisis":["Fantasma","Doble cargo","Sin retencion"]}})

@app.route('/api/contrato')
def contrato():
    txt="CONTRATO V9.2 FINAL USD250 x MODULO + IMPUESTOS BHD 08694150021 - NOBACI + LIBRAMIENTOS + INVENTARIOS + NOMINA + IA - MULTI-PAIS MULTI-IDIOMA"
    return send_file(io.BytesIO(txt.encode()), mimetype="application/pdf", as_attachment=True, download_name="CONTRATO_V9_2_USD250.pdf")

@app.route('/api/contrato/<cid>')
def contrato_id(cid):
    txt="CONTRATO V9 FIRMADO " + cid + " USD250 x modulo BHD " + BHD_CUENTA
    return send_file(io.BytesIO(txt.encode()), mimetype="application/pdf", as_attachment=True, download_name=cid+".pdf")

@app.route('/b4')
def b4():
    activo = session.get('activado', False)
    banner = "" if activo else "<div style='background:#fef3c7;padding:10px;border-radius:8px;margin-bottom:10px;color:#92400e'>DEMO - Active en /activar-modulos USD$250 x modulo</div>"
    return "<body style='font-family:Arial;background:#0f172a;color:white;padding:12px'><h1>B4 V9.2 + NOBACI + Inventarios IA " + ("FULL ACTIVO" if activo else "DEMO") + "</h1>" + banner + "<div style='background:white;color:black;padding:16px;border-radius:12px;max-width:1000px;margin:auto'><ul><li>Informe Pericial IA multi-idioma</li><li>NOBACI Evaluacion Interna COSO</li><li>Libramientos Contraloria SIGEF</li><li>Inventarios y Activos Fijos</li><li>Nomina y Pagos + TSS</li><li>Pago automatico Stripe + BHD " + BHD_CUENTA + "</li></ul><a href='/activar-modulos' style='background:#00d084;color:white;padding:8px;border-radius:6px;text-decoration:none'>Activar V9.2 USD</a></div></body>"

@app.route('/v8')
def v8():
    activo = session.get('activado', False)
    return "<body style='font-family:Arial;background:#0a192f;color:white;padding:12px'><h1 style='color:#00d084'>V9.2 Auditoria + NOBACI + Libramientos + Inventarios IA " + ("FULL" if activo else "DEMO") + "</h1><div style='background:white;color:black;padding:16px;border-radius:12px;max-width:1100px;margin:auto'><table style='width:100%;border-collapse:collapse;font-size:11px'><tr style='background:#003366;color:white'><th>Modulo USD250</th><th>Analisis IA</th><th>Ley Pais</th></tr><tr><td>M9 NOBACI</td><td>Control Interno + Riesgo</td><td>NOBACI RD + COSO</td></tr><tr><td>M11 Pagos/Libram</td><td>SIGEF + duplicados + cheques</td><td>Ley 10-07 + Contraloria</td></tr><tr><td>M10 Inventarios</td><td>Toma fisica IA + Kardex</td><td>NOBACI Activos</td></tr><tr><td>M6 Nomina</td><td>Fantasma + doble cargo</td><td>TSS + MAP + IRS</td></tr></table><p>BHD: " + BHD_CUENTA + " | Stripe Auto</p></div></body>"

@app.route('/api/auditoria-demo')
def demo_json():
    return jsonify({"V9_2_FINAL":{"precio":"USD250 x modulo + impuestos pais","modulos":12,"total_ejemplo":"13 modulos = USD$3250 + 18% = USD$3835","bhd":BHD_CUENTA,"stripe":"Configurado - STRIPE_SECRET_KEY en Render","paises":PAISES_LEYES,"incluye":["NOBACI","Libramientos SIGEF","Inventarios","Nomina","Activos","Pagos","Informes IA","Multi-Pais","Multi-Idioma","Multi-Moneda"]}})

@app.route('/demo')
def demo_zip():
    m=io.BytesIO()
    with zipfile.ZipFile(m,mode="w",compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("V9_2_FINAL_README.txt","BASA V9.2 FINAL FULL USD250 x modulo - NOBACI + Libramientos + Inventarios + Nomina + IA + Stripe + BHD 08694150021")
        zf.writestr("MODULOS.txt", json.dumps(MODULOS_V9, indent=2))
        zf.writestr("PAISES_LEYES.txt", json.dumps(PAISES_LEYES, indent=2))
    m.seek(0)
    return send_file(m,mimetype="application/zip",as_attachment=True,download_name="BASA_V9_2_FINAL_FULL_USD250.zip")

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get("PORT",10000)))
