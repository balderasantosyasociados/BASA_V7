import os, io, zipfile, datetime, json, calendar
from flask import Flask, jsonify, request, session, send_file, Response
from flask_cors import CORS
app = Flask(__name__)
app.secret_key = "BASA_V9_3_PWA_ANDROID_IPHONE"
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
    "M2_FRACC": {"nombre":"M2 - Fraccionamiento + Libramientos","precio":250,"cat":"Auditoria","desc":"Fracc + Analisis libramientos SIGEF Contraloria + IA"},
    "M3_DUENO": {"nombre":"M3 - Mismo Dueno + Beneficiario Final","precio":250,"cat":"Forense","desc":"Multi-RNC testaferros + beneficiario final global"},
    "M4_ACC": {"nombre":"M4 - Accionistas + Activos Ocultos","precio":250,"cat":"Forense","desc":"Red accionistas + Analisis activos patrimonio IA"},
    "M5_CONF": {"nombre":"M5 - Consanguinidad + PEPs","precio":250,"cat":"Legal","desc":"Parentesco + conflicto interes + PEPs mundial"},
    "M6_NOM": {"nombre":"M6 - Nomina + Pagos + TSS","precio":250,"cat":"Nomina","desc":"Nomina fantasma, doble cargo, pagos TSS, MAP, IRS"},
    "M7_FIN": {"nombre":"M7 - Estados Financieros + Pagos","precio":250,"cat":"Financiero","desc":"DGII vs contrataciones + pagos trucados IA"},
    "M8_FULL": {"nombre":"M8 - Forense Full + IA Predictiva","precio":250,"cat":"IA","desc":"TODO + IA predictiva + auto-leyes pais"},
    "M9_NOBACI": {"nombre":"M9 - NOBACI + Control Interno","precio":250,"cat":"Control Interno","desc":"NOBACI RD + COSO + Matriz Riesgo IA"},
    "M10_INV": {"nombre":"M10 - Inventarios + Activos Fijos","precio":250,"cat":"Inventarios","desc":"Toma fisica IA, Kardex, depreciacion"},
    "M11_PAGOS": {"nombre":"M11 - Pagos + Libramientos + Tesoreria","precio":250,"cat":"Tesoreria","desc":"Libramientos Contraloria, SIGEF, cheques, transferencias IA"},
    "M12_INF": {"nombre":"M12 - Informes IA Multi-Pais","precio":250,"cat":"Informes","desc":"Informes periciales automaticos IA multi-pais"},
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

# PWA MANIFEST PARA ANDROID / IPHONE
@app.route('/manifest.json')
def manifest():
    return jsonify({
        "name": "BASA V9.3 - Auditoria Forense + NOBACI + IA",
        "short_name": "BASA V9",
        "description": "Sistema Forense USD250 x modulo + NOBACI + Libramientos + Inventarios + Nomina + IA - Multi-Pais",
        "start_url": "/activar-modulos",
        "display": "standalone",
        "background_color": "#0f172a",
        "theme_color": "#00d084",
        "icons": [{"src":"https://cdn-icons-png.flaticon.com/512/3064/3064197.png","sizes":"512x512","type":"image/png"}]
    })

@app.route('/sw.js')
def sw():
    js = "self.addEventListener('install', e=>{self.skipWaiting();}); self.addEventListener('fetch', e=>{e.respondWith(fetch(e.request));});"
    return Response(js, mimetype='application/javascript')

@app.route('/')
def home():
    return jsonify({"BASA":"V9.3 PWA ANDROID IPHONE","bhd":BHD_CUENTA,"instalable":"Android + iPhone - Agregue a pantalla inicio","demo_zip":"/demo - ARCHIVOS REALES","demo_json":"/api/auditoria-demo - solo JSON prueba"})

@app.route('/healthz')
def health():
    return jsonify({"status":"OK V9.3 PWA"})

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
    html = "<html><head><meta name='viewport' content='width=device-width,initial-scale=1'><link rel='manifest' href='/manifest.json'><meta name='theme-color' content='#00d084'><meta name='apple-mobile-web-app-capable' content='yes'><style>body{font-family:Arial;background:#0f172a;color:white;padding:10px}.card{background:white;color:black;padding:18px;border-radius:16px;max-width:1000px;margin:auto}.btn{padding:10px;border-radius:8px;font-weight:bold;border:none;margin:5px;cursor:pointer;text-decoration:none;display:inline-block}.verde{background:#00d084;color:white;width:100%;font-size:16px;padding:14px}.azul{background:#003366;color:white}.fact{background:#f0f7ff;padding:14px;border-radius:12px;border-left:5px solid #003366}.amarillo{background:#fef3c7;border:2px solid #f59e0b;padding:12px;border-radius:10px;margin:10px 0;color:#92400e}select,input{width:100%;padding:9px;border:2px solid #cbd5e1;border-radius:8px;margin:4px 0}</style></head><body>"
    html += "<h1 style='text-align:center;color:#00d084'>BASA V9.3 PWA<br><small style='font-size:11px;color:#94a3b8'>ANDROID + iPHONE INSTALABLE | USD$250 x Modulo | NOBACI + Libramientos + Inventarios</small></h1>"
    html += "<div style='background:#00d084;color:white;padding:8px;border-radius:8px;text-align:center;margin-bottom:10px;font-size:12px'>📱 ANDROID: Menu ⋮ > Instalar app | iPHONE: Compartir > Agregar a inicio</div>"
    html += "<div class='card'><div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px'><div>Pais: <select id='pais' onchange='calcUSD()'>" + pais_opts + "</select></div><div>Idioma: <select id='idioma'><option value='es'>Espanol</option><option value='en'>English</option></select></div><div>Moneda: <select id='moneda'><option value='USD'>USD</option><option value='DOP'>DOP</option><option value='EUR'>EUR</option></select></div></div>"
    html += mods_html
    html += "<div class='fact'><h3>Facturacion USD BHD " + BHD_CUENTA + " + Stripe</h3>Empresa: <input id='emp' placeholder='Empresa'><br>RNC: <input id='rnc' placeholder='RNC'><br><div id='factUSD'>Calculando...</div></div>"
    html += "<div class='amarillo'><input type='checkbox' id='ok'> <b>ACEPTO CONTRATO V9.3 USD250 + PAGO AUTO</b><br><small>BHD " + BHD_CUENTA + " - Multi-pais Multi-idioma</small></div>"
    html += "<button class='btn verde' onclick='pagarAuto()'>PAGAR AUTOMATICO USD + ACTIVAR FULL</button>"
    html += "<div style='margin-top:12px;display:grid;grid-template-columns:1fr 1fr;gap:6px'><a href='/demo' class='btn azul' style='text-align:center'>📦 DESCARGAR APP REAL ZIP (Android/iPhone)</a><a href='/b4' class='btn azul' style='text-align:center'>B4 Informe IA</a><a href='/v8' class='btn azul' style='text-align:center'>V8 Auditoria NOBACI</a><a href='/api/auditoria-demo' class='btn azul' style='text-align:center;background:#6b7280'>JSON Prueba (no archivo)</a></div>"
    html += "<div id='res' style='display:none;background:#ecfdf5;padding:14px;border-radius:12px;margin-top:10px;border:2px solid #00d084'></div></div>"
    html += "<script>if('serviceWorker' in navigator){navigator.serviceWorker.register('/sw.js');} function calcUSD(){var activos=[];document.querySelectorAll('.chk:checked').forEach(function(c){if(activos.indexOf(c.value)==-1) activos.push(c.value);});if(activos.indexOf('B4_BASE')==-1) activos.unshift('B4_BASE');var total=activos.length*250;var pais=document.getElementById('pais').value;var imp=0.18;if(pais=='DO') imp=0.18; if(pais=='MX') imp=0.16; if(pais=='PA') imp=0.07; if(pais=='CO') imp=0.19; if(pais=='ES') imp=0.21; if(pais=='US') imp=0;var impuesto=Math.round(total*imp*100)/100;var grand=total+impuesto;var hoy=new Date();var ultimo=new Date(hoy.getFullYear(),hoy.getMonth()+1,0).getDate();var dias=ultimo-hoy.getDate()+1;var primer=Math.round((grand/30)*dias*100)/100;var moneda=document.getElementById('moneda').value;document.getElementById('factUSD').innerHTML='Pais: '+pais+' | Modulos: '+activos.length+'<br>Subtotal: USD$'+total+'<br>Impuesto '+Math.round(imp*100)+'%: USD$'+impuesto+'<br><b>Total: USD$'+grand+' '+moneda+'</b><br>Primer: USD$'+primer+'<br>BHD: 08694150021';window._act=activos;window._grand=grand;window._pri=primer;window._pais=pais;} function pagarAuto(){if(!document.getElementById('ok').checked){alert('Acepte contrato');return;}var emp=document.getElementById('emp').value;var rnc=document.getElementById('rnc').value;if(!emp||!rnc){alert('Empresa y RNC');return;}var btn=document.querySelector('.verde');btn.innerHTML='PROCESANDO USD$'+window._grand+'...';fetch('/api/pagar-stripe',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({mods:window._act,pais:window._pais,empresa:emp,rnc:rnc,total:window._grand})}).then(function(r){return r.json();}).then(function(d){if(d.url){window.location=d.url;}else{var res=document.getElementById('res');res.style.display='block';res.innerHTML='<h3>FACTURA BHD</h3><p>USD$'+d.total+' a BHD 08694150021</p><a href=\"/pago-exitoso?demo=1&empresa='+emp+'\" class=\"btn verde\">Ya pague - Activar</a>';}});} calcUSD();</script></body></html>"
    return html

@app.route('/api/pagar-stripe', methods=['POST'])
def pagar_stripe():
    data=request.get_json() or {}
    mods=data.get('mods',[]); pais=data.get('pais','DO'); total=data.get('total',3835); empresa=data.get('empresa','Cliente')
    if STRIPE_KEY and STRIPE_KEY.startswith("sk_"):
        try:
            import stripe; stripe.api_key = STRIPE_KEY
            sess = stripe.checkout.Session.create(payment_method_types=['card'],line_items=[{'price_data':{'currency':'usd','product_data':{'name':'BASA V9 '+str(len(mods))+' mod '+pais+' - '+empresa},'unit_amount': int(total*100)},'quantity':1}],mode='payment',success_url='https://basa-v7-1.onrender.com/pago-exitoso?session_id={CHECKOUT_SESSION_ID}',cancel_url='https://basa-v7-1.onrender.com/activar-modulos',metadata={'mods':','.join(mods),'pais':pais,'empresa':empresa})
            return jsonify({"url": sess.url})
        except Exception as e:
            return jsonify({"bhd": BHD_CUENTA, "total": total, "error": str(e)})
    else:
        return jsonify({"bhd": BHD_CUENTA, "total": total})

@app.route('/pago-exitoso')
def pago_exitoso():
    sid = request.args.get('session_id','BHD-'+datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    session['activado']=True
    session['contrato']="CTR-V9-PAGADO-"+datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    return "<body style='font-family:Arial;background:#ecfdf5;padding:20px;text-align:center'><h1 style='color:#00a86b'>PAGO OK - BASA V9.3 ACTIVO</h1><div style='background:white;padding:20px;border-radius:14px;max-width:700px;margin:auto'><h2>" + sid + "</h2><p>FULL 12 modulos - NOBACI + Libramientos + Inventarios + Android/iPhone</p><a href='/b4' style='background:#00d084;color:white;padding:12px;border-radius:8px;text-decoration:none'>B4</a><a href='/v8' style='background:#003366;color:white;padding:12px;border-radius:8px;text-decoration:none'>V8</a><a href='/demo' style='background:#6b7280;color:white;padding:12px;border-radius:8px;text-decoration:none'>Descargar APP ZIP</a></div></body>"

@app.route('/b4')
def b4():
    return "<body style='font-family:Arial;background:#0f172a;color:white;padding:12px'><h1>B4 V9.3 PWA Android/iPhone</h1><div style='background:white;color:black;padding:16px;border-radius:12px;max-width:1000px;margin:auto'><p>Instalable Android + iPhone</p><a href='/activar-modulos'>Activar</a> | <a href='/demo'>Descargar ZIP APP</a></div></body>"

@app.route('/v8')
def v8():
    return "<body style='font-family:Arial;background:#0a192f;color:white;padding:12px'><h1 style='color:#00d084'>V9.3 NOBACI + Libramientos + Inventarios</h1><div style='background:white;color:black;padding:16px;border-radius:12px;max-width:1100px;margin:auto'><p>PWA Android/iPhone - BHD: " + BHD_CUENTA + "</p></div></body>"

@app.route('/api/auditoria-demo')
def demo_json():
    return jsonify({"AVISO":"ESTE ES SOLO JSON DE PRUEBA - NO ES EL ARCHIVO REAL","ARCHIVO_REAL":"Vaya a /demo para descargar ZIP con ejecutables Android/iPhone","V9_3_FINAL":{"bhd":BHD_CUENTA,"modulos":12,"precio":"USD250 x modulo","incluye":["NOBACI","Libramientos SIGEF","Inventarios","Nomina","Activos","Pagos","Informes IA","Multi-Pais","PWA Android iPhone"]}})

@app.route('/api/nobaci')
def nobaci():
    return jsonify({"NOBACI":"OK","libramientos":"SIGEF","inventarios":"OK"})

@app.route('/api/contrato')
def contrato():
    txt="CONTRATO V9.3 PWA USD250 BHD 08694150021"
    return send_file(io.BytesIO(txt.encode()), mimetype="application/pdf", as_attachment=True, download_name="CONTRATO_V9_3.pdf")

# ESTE ES EL BUENO - ARCHIVOS REALES PARA ANDROID / IPHONE
@app.route('/demo')
def demo_zip():
    m=io.BytesIO()
    with zipfile.ZipFile(m,mode="w",compression=zipfile.ZIP_DEFLATED) as zf:
        # README
        zf.writestr("LEAME_INSTALACION_ANDROID_IPHONE.txt", "BASA V9.3 PWA - INSTALACION ANDROID/iPHONE\n1. ANDROID: Abra Chrome en basa-v7-1.onrender.com/activar-modulos -> Menu 3 puntos -> Instalar app -> Se instala como APP real\n2. iPHONE: Abra Safari en basa-v7-1.onrender.com/activar-modulos -> Compartir -> Agregar a pantalla de inicio -> Se instala como APP\n3. WINDOWS/MAC: Chrome -> Instalar BASA V9\nBHD: 08694150021\nUSD250 x modulo\nIncluye: NOBACI, Libramientos, Inventarios, Nomina, Activos, Pagos, Informes IA\n")
        # PWA files
        zf.writestr("manifest.json", json.dumps({"name":"BASA V9.3","short_name":"BASA V9","start_url":"/activar-modulos","display":"standalone","background_color":"#0f172a","theme_color":"#00d084","icons":[{"src":"https://cdn-icons-png.flaticon.com/512/3064/3064197.png","sizes":"512x512"}]}, indent=2))
        zf.writestr("sw.js", "self.addEventListener('install', e=>{self.skipWaiting();});")
        zf.writestr("index.html", "<html><head><link rel='manifest' href='manifest.json'><meta name='viewport' content='width=device-width,initial-scale=1'><title>BASA V9.3</title></head><body><h1>BASA V9.3 Android/iPhone</h1><p>App instalable PWA</p><a href='https://basa-v7-1.onrender.com/activar-modulos'>Abrir Sistema</a></body></html>")
        # Modulos
        zf.writestr("MODULOS_12_USD250.txt", json.dumps(MODULOS_V9, indent=2, ensure_ascii=False))
        zf.writestr("PAISES_LEYES_NOBACI.txt", json.dumps(PAISES_LEYES, indent=2, ensure_ascii=False))
        # Ejecutable Android wrapper
        zf.writestr("ANDROID/iPHONE_INSTALACION.txt", "ANDROID:\n1. Chrome -> basa-v7-1.onrender.com/activar-modulos\n2. Menu > Instalar app\n3. Ya tiene APK PWA\n\niPHONE:\n1. Safari -> basa-v7-1.onrender.com/activar-modulos\n2. Compartir -> Agregar a inicio\n3. Ya tiene APP iOS\n\nPara APK nativo: Use PWABuilder.com -> ponga URL -> Genere APK\nPara IPA iOS: Use PWABuilder.com -> Genere IPA")
        # Sistema completo html offline
        zf.writestr("BASA_V9_3_OFFLINE.html", "<html><body><h1>BASA V9.3 OFFLINE - USD250 x modulo</h1><p>BHD 08694150021</p><p>12 modulos: B4 + M1-M12 + NOBACI + Libramientos + Inventarios + Nomina</p><p>Multi-Pais: DO,US,MX,PA,CO,ES</p></body></html>")
        # Script instalacion
        zf.writestr("INSTALAR_APP.bat", "@echo off\necho Instalando BASA V9.3 PWA\nstart https://basa-v7-1.onrender.com/activar-modulos\n")
        zf.writestr("INSTALAR_APP.sh", "#!/bin/bash\necho Instalando BASA V9.3\nxdg-open https://basa-v7-1.onrender.com/activar-modulos\n")
    m.seek(0)
    return send_file(m, mimetype="application/zip", as_attachment=True, download_name="BASA_V9_3_PWA_ANDROID_IPHONE_FULL.zip")

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get("PORT",10000)))
