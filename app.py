import os, io, zipfile, datetime, json, calendar
from flask import Flask, jsonify, request, session, send_file, Response
from flask_cors import CORS
app = Flask(__name__)
app.secret_key = "BASA_V9_4_FULL_PWA_FIX"
CORS(app)

BHD_CUENTA = "08694150021 - USD Y DOP"
USD_POR_MODULO = 250
STRIPE_KEY = os.environ.get("STRIPE_SECRET_KEY", "")

PAISES_LEYES = {
    "DO": {"nombre":"Rep. Dominicana","moneda":"USD/DOP","impuesto":0.18,"leyes":["Ley 340-06","Reg 416-23","NOBACI","Ley 10-07","Ley 155-17","Ley 126-02"],"portal":"comprasdominicana.gob.do"},
    "US": {"nombre":"Estados Unidos","moneda":"USD","impuesto":0.0,"leyes":["FAR","2 CFR 200","SOX","GAAP","ESIGN"],"portal":"sam.gov"},
    "MX": {"nombre":"Mexico","moneda":"USD/MXN","impuesto":0.16,"leyes":["LAASSP","Anticorrupcion"],"portal":"compranet.hacienda.gob.mx"},
    "PA": {"nombre":"Panama","moneda":"USD","impuesto":0.07,"leyes":["Ley 22 Contrataciones"],"portal":"panamacompra.gob.pa"},
    "CO": {"nombre":"Colombia","moneda":"USD/COP","impuesto":0.19,"leyes":["Ley 80"],"portal":"colombiacompra.gov.co"},
    "ES": {"nombre":"Espana","moneda":"EUR","impuesto":0.21,"leyes":["LCSP","eIDAS"],"portal":"contrataciondelestado.es"},
}

MODULOS_V9 = {
    "B4_BASE": {"nombre":"B4 Base - Informe Pericial IA","precio":250,"cat":"Informes","desc":"Informe base IA multi-idioma + NOBACI"},
    "M1_SCRAPER": {"nombre":"M1 - Scraper 10 anos IA","precio":250,"cat":"Auditoria","desc":"Scraping portal compras segun pais + IA"},
    "M2_FRACC": {"nombre":"M2 - Fraccionamiento + Libramientos","precio":250,"cat":"Auditoria","desc":"Fracc + Libramientos SIGEF Contraloria + IA"},
    "M3_DUENO": {"nombre":"M3 - Mismo Dueno + Benef Final","precio":250,"cat":"Forense","desc":"Multi-RNC testaferros + beneficiario final"},
    "M4_ACC": {"nombre":"M4 - Accionistas + Activos Ocultos","precio":250,"cat":"Forense","desc":"Red accionistas + patrimonio oculto IA"},
    "M5_CONF": {"nombre":"M5 - Consanguinidad + PEPs","precio":250,"cat":"Legal","desc":"Parentesco + conflicto + PEPs mundial"},
    "M6_NOM": {"nombre":"M6 - Nomina + Pagos + TSS","precio":250,"cat":"Nomina","desc":"Nomina fantasma, doble cargo, TSS, MAP, IRS"},
    "M7_FIN": {"nombre":"M7 - Estados Financieros + Pagos","precio":250,"cat":"Financiero","desc":"DGII vs contrataciones + pagos trucados"},
    "M8_FULL": {"nombre":"M8 - Forense Full + IA Predictiva","precio":250,"cat":"IA","desc":"TODO + IA predictiva + auto-leyes"},
    "M9_NOBACI": {"nombre":"M9 - NOBACI + Control Interno","precio":250,"cat":"Control Interno","desc":"NOBACI RD + COSO + Matriz Riesgo"},
    "M10_INV": {"nombre":"M10 - Inventarios + Activos Fijos","precio":250,"cat":"Inventarios","desc":"Toma fisica IA, Kardex, depreciacion"},
    "M11_PAGOS": {"nombre":"M11 - Pagos + Libramientos","precio":250,"cat":"Tesoreria","desc":"Libramientos Contraloria SIGEF + cheques"},
    "M12_INF": {"nombre":"M12 - Informes IA Multi-Pais","precio":250,"cat":"Informes","desc":"Informes periciales automaticos IA"},
}

def calc(mods, pais="DO"):
    info=PAISES_LEYES.get(pais,PAISES_LEYES["DO"])
    imp=info["impuesto"]; sub=sum(MODULOS_V9[m]["precio"] for m in mods if m in MODULOS_V9)
    impuesto=round(sub*imp,2); total=sub+impuesto; hoy=datetime.datetime.now()
    ultimo=calendar.monthrange(hoy.year,hoy.month)[1]; dias=ultimo-hoy.day+1; primer=round((total/30)*dias,2)
    return {"mods":mods,"subtotal":sub,"impuesto":impuesto,"total":total,"primer":primer,"dias":dias,"pais":pais,"info":info,"bhd":BHD_CUENTA}

@app.route('/manifest.json')
def manifest():
    return jsonify({"name":"BASA V9.4 Forense NOBACI IA","short_name":"BASA V9","description":"USD250 x modulo + NOBACI + Libramientos + Inventarios + Android iPhone","start_url":"/activar-modulos","display":"standalone","background_color":"#0f172a","theme_color":"#00d084","icons":[{"src":"https://cdn-icons-png.flaticon.com/512/3064/3064197.png","sizes":"512x512","type":"image/png"}]})

@app.route('/sw.js')
def sw():
    return Response("self.addEventListener('install',e=>self.skipWaiting());self.addEventListener('fetch',e=>e.respondWith(fetch(e.request)));", mimetype='application/javascript')

@app.route('/')
def home():
    return jsonify({"BASA":"V9.4 FULL PWA FIX","bhd":BHD_CUENTA,"b4":"/b4 - FULL RESTAURADO","v8":"/v8 - FULL NOBACI","zip_real":"/demo","json_prueba":"/api/auditoria-demo"})

@app.route('/healthz')
def h(): return jsonify({"status":"OK V9.4"})

@app.route('/activar-modulos')
def act():
    mods_html=""; cats={}
    for k,v in MODULOS_V9.items():
        c=v["cat"]; cats.setdefault(c,[]).append((k,v))
    for cat, lista in cats.items():
        mods_html+="<h3 style='color:#003366;margin-top:12px;border-bottom:2px solid #00d084'>"+cat+"</h3>"
        for k,v in lista:
            chk="checked disabled" if k=="B4_BASE" else "checked"
            mods_html+="<div style='border:2px solid #e2e8f0;padding:10px;margin:6px 0;border-radius:12px;display:flex;justify-content:space-between;background:#f8fafc'><div><b>"+v["nombre"]+"</b><br><small>"+v["desc"]+"</small><br><span style='color:#00a86b;font-weight:bold'>USD$"+str(v["precio"])+"</span></div><div><input type='checkbox' value='"+k+"' "+chk+" class='chk' onchange='calcUSD()' style='width:22px;height:22px'></div></div>"
    pais_opts="".join(["<option value='"+c+"'>"+i["nombre"]+" - "+i["leyes"][0]+"</option>" for c,i in PAISES_LEYES.items()])
    html="<html><head><meta name='viewport' content='width=device-width,initial-scale=1'><link rel='manifest' href='/manifest.json'><style>body{font-family:Arial;background:#0f172a;color:white;padding:10px}.card{background:white;color:black;padding:16px;border-radius:16px;max-width:1000px;margin:auto}.btn{padding:10px;border-radius:8px;font-weight:bold;border:none;margin:4px;cursor:pointer;text-decoration:none;display:inline-block}.verde{background:#00d084;color:white;width:100%;font-size:16px;padding:14px}.azul{background:#003366;color:white}.fact{background:#f0f7ff;padding:12px;border-radius:12px;border-left:5px solid #003366}.amarillo{background:#fef3c7;border:2px solid #f59e0b;padding:10px;border-radius:10px;margin:8px 0;color:#92400e}select,input{width:100%;padding:8px;border:2px solid #cbd5e1;border-radius:8px;margin:3px 0}</style></head><body>"
    html+="<h2 style='text-align:center;color:#00d084'>BASA V9.4 FULL - USD$250 x Modulo<br><small style='color:#94a3b8'>PWA Android/iPhone + NOBACI + Libramientos + Inventarios + Stripe</small></h2><div style='background:#00d084;color:white;padding:6px;border-radius:8px;text-align:center;margin-bottom:8px;font-size:11px'>📱 ANDROID: Menu ⋮ > Instalar app | iPHONE: Compartir > Agregar a inicio</div><div class='card'>"
    html+="<div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px'><div>Pais:<select id='pais' onchange='calcUSD()'>"+pais_opts+"</select></div><div>Idioma:<select id='idioma'><option value='es'>ES</option><option value='en'>EN</option></select></div><div>Moneda:<select id='moneda'><option>USD</option><option>DOP</option><option>EUR</option></select></div></div>"
    html+=mods_html+"<div class='fact'><h3>Facturacion USD BHD "+BHD_CUENTA+"</h3>Empresa:<input id='emp' placeholder='Empresa'><br>RNC:<input id='rnc' placeholder='RNC'><div id='factUSD'></div></div>"
    html+="<div class='amarillo'><input type='checkbox' id='ok'> <b>ACEPTO CONTRATO V9.4 USD250</b> <a href='/api/contrato' target='_blank'>Ver</a> <a href='/api/nobaci' target='_blank'>NOBACI</a></div>"
    html+="<button class='btn verde' onclick='pagar()'>PAGAR AUTOMATICO USD + ACTIVAR FULL</button><div id='res' style='display:none;background:#ecfdf5;padding:12px;border-radius:12px;margin-top:8px'></div>"
    html+="<div style='display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:10px'><a href='/demo' class='btn azul' style='text-align:center'>📦 DESCARGAR ZIP REAL APP</a><a href='/b4' class='btn azul' style='text-align:center'>B4 FULL Informe IA</a><a href='/v8' class='btn azul' style='text-align:center'>V8 FULL NOBACI</a><a href='/api/auditoria-demo' class='btn azul' style='background:#6b7280;text-align:center'>JSON Prueba</a></div></div>"
    html+="<script>if('serviceWorker' in navigator){navigator.serviceWorker.register('/sw.js');}function calcUSD(){var a=[];document.querySelectorAll('.chk:checked').forEach(function(c){if(a.indexOf(c.value)==-1)a.push(c.value);});if(a.indexOf('B4_BASE')==-1)a.unshift('B4_BASE');var t=a.length*250;var p=document.getElementById('pais').value;var imp=0.18;if(p=='DO')imp=0.18;if(p=='MX')imp=0.16;if(p=='PA')imp=0.07;if(p=='CO')imp=0.19;if(p=='ES')imp=0.21;if(p=='US')imp=0;var impuesto=Math.round(t*imp*100)/100;var grand=t+impuesto;var hoy=new Date();var ult=new Date(hoy.getFullYear(),hoy.getMonth()+1,0).getDate();var dias=ult-hoy.getDate()+1;var primer=Math.round((grand/30)*dias*100)/100;document.getElementById('factUSD').innerHTML='Modulos:'+a.length+' Sub:USD$'+t+' Imp:'+Math.round(imp*100)+'% USD$'+impuesto+'<br><b>Total:USD$'+grand+'</b> Primer:USD$'+primer+' BHD:"+BHD_CUENTA+"';window._act=a;window._grand=grand;window._pais=p;}function pagar(){if(!document.getElementById('ok').checked){alert('Acepte');return;}var emp=document.getElementById('emp').value;var rnc=document.getElementById('rnc').value;if(!emp||!rnc){alert('Empresa RNC');return;}var b=document.querySelector('.verde');b.innerHTML='PROCESANDO USD$'+window._grand+'...';fetch('/api/pagar-stripe',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({mods:window._act,pais:window._pais,empresa:emp,total:window._grand})}).then(r=>r.json()).then(d=>{if(d.url)window.location=d.url;else{var res=document.getElementById('res');res.style.display='block';res.innerHTML='<p>Total USD$'+d.total+' BHD "+BHD_CUENTA+" Concepto BASA V9 '+emp+'</p><a href=\"/pago-exitoso?demo=1&empresa='+emp+'\" class=\"btn verde\">Ya pague Activar</a>';}});}calcUSD();</script></body></html>"
    return html

@app.route('/api/pagar-stripe', methods=['POST'])
def ps():
    data=request.get_json() or {}; mods=data.get('mods',[]); pais=data.get('pais','DO'); total=data.get('total',3835); emp=data.get('empresa','Cliente')
    if STRIPE_KEY.startswith("sk_"):
        try:
            import stripe; stripe.api_key=STRIPE_KEY
            s=stripe.checkout.Session.create(payment_method_types=['card'],line_items=[{'price_data':{'currency':'usd','product_data':{'name':'BASA V9 '+str(len(mods))+' mod '+pais+' '+emp},'unit_amount':int(total*100)},'quantity':1}],mode='payment',success_url='https://basa-v7-1.onrender.com/pago-exitoso?session_id={CHECKOUT_SESSION_ID}',cancel_url='https://basa-v7-1.onrender.com/activar-modulos')
            return jsonify({"url":s.url})
        except Exception as e: return jsonify({"bhd":BHD_CUENTA,"total":total,"error":str(e)})
    else: return jsonify({"bhd":BHD_CUENTA,"total":total})

@app.route('/pago-exitoso')
def pe():
    sid=request.args.get('session_id','BHD-'+datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    session['activado']=True; session['contrato']="CTR-V9-PAGADO-"+datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return "<body style='font-family:Arial;background:#ecfdf5;padding:20px;text-align:center'><h1 style='color:#00a86b'>PAGO OK V9.4 ACTIVO</h1><div style='background:white;padding:20px;border-radius:14px;max-width:700px;margin:auto'><h2>"+sid+"</h2><p>12 modulos FULL + NOBACI + Libramientos + Inventarios</p><a href='/b4' style='background:#00d084;color:white;padding:10px;border-radius:8px;text-decoration:none;margin:4px;display:inline-block'>B4 FULL</a><a href='/v8' style='background:#003366;color:white;padding:10px;border-radius:8px;text-decoration:none;margin:4px;display:inline-block'>V8 FULL</a><a href='/demo' style='background:#6b7280;color:white;padding:10px;border-radius:8px;text-decoration:none;margin:4px;display:inline-block'>ZIP REAL</a></div></body>"

# B4 FULL RESTAURADO - NO MINIMAL
@app.route('/b4')
def b4():
    act=session.get('activado',False)
    banner="" if act else "<div style='background:#fef3c7;padding:10px;border-radius:8px;color:#92400e;margin-bottom:10px'>DEMO - Active en /activar-modulos USD250 x modulo</div>"
    html="<html><head><meta name='viewport' content='width=device-width,initial-scale=1'><link rel='manifest' href='/manifest.json'><style>body{font-family:Arial;background:#0f172a;color:white;padding:10px}.card{background:white;color:black;padding:16px;border-radius:12px;max-width:1100px;margin:auto}.btn{padding:8px;border-radius:6px;background:#003366;color:white;text-decoration:none;margin:3px;display:inline-block}table{width:100%;border-collapse:collapse;font-size:11px}th{background:#003366;color:white;padding:6px}td{border:1px solid #e2e8f0;padding:5px}input,select{padding:7px;border:2px solid #cbd5e1;border-radius:6px;margin:3px;width:95%}</style></head><body>"
    html+="<h2 style='color:#00d084;text-align:center'>B4 V9.4 FULL - Informe Pericial IA + NOBACI + Multi-Pais "+("FULL ACTIVO" if act else "DEMO")+"</h2><div class='card'>"+banner
    html+="<div style='display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:6px'><div>Pais:<select id='paisB4'><option value='DO'>DO</option><option value='US'>US</option><option value='MX'>MX</option><option value='PA'>
