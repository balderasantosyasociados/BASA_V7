import os, io, zipfile, datetime, json, calendar
from flask import Flask, jsonify, request, session, send_file, Response, render_template_string
from flask_cors import CORS
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = "BASA_V13_FIX_404_TRIAL_NETLIFY"
CORS(app, origins="*")

BHD_CUENTA = "08694150021 - USD Y DOP"
STRIPE_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
BASE_URL = "https://basa-v7-1.onrender.com"
FRONT_URL = "https://audit-intelligence-usa.com"

PAISES = {
    "DO": {"nombre":"Rep. Dominicana","moneda":"DOP","impuesto":0.18,"leyes":["Ley 340-06","NOBACI","Ley 10-07"],"portal":"comprasdominicana.gob.do"},
    "US": {"nombre":"Estados Unidos","moneda":"USD","impuesto":0.0,"leyes":["FAR","SOX","GAAP"],"portal":"sam.gov"},
    "MX": {"nombre":"Mexico","moneda":"MXN","impuesto":0.16,"leyes":["LAASSP"],"portal":"compranet.hacienda.gob.mx"},
    "PA": {"nombre":"Panama","moneda":"USD","impuesto":0.07,"leyes":["Ley 22"],"portal":"panamacompra.gob.pa"},
    "CO": {"nombre":"Colombia","moneda":"COP","impuesto":0.19,"leyes":["Ley 80"],"portal":"colombiacompra.gov.co"},
    "ES": {"nombre":"Espana","moneda":"EUR","impuesto":0.21,"leyes":["LCSP","eIDAS"],"portal":"contrataciondelestado.es"},
}
MODULOS = {
    "B4_BASE": {"nombre":"B4 Base - Informe Pericial IA","precio":250,"cat":"Informes","desc":"Informe base IA + NOBACI"},
    "M1_SCRAPER": {"nombre":"M1 - Scraper 10 anos IA","precio":250,"cat":"Auditoria","desc":"Scraping portal + IA"},
    "M2_FRACC": {"nombre":"M2 - Fraccionamiento + Libramientos","precio":250,"cat":"Auditoria","desc":"Fracc + SIGEF"},
    "M3_DUENO": {"nombre":"M3 - Mismo Dueno","precio":250,"cat":"Forense","desc":"Multi-RNC"},
    "M4_ACC": {"nombre":"M4 - Accionistas + Activos","precio":250,"cat":"Forense","desc":"Activos ocultos"},
    "M5_CONF": {"nombre":"M5 - Consanguinidad + PEPs","precio":250,"cat":"Legal","desc":"PEPs"},
    "M6_NOM": {"nombre":"M6 - Nomina + TSS","precio":250,"cat":"Nomina","desc":"Nomina fantasma"},
    "M7_FIN": {"nombre":"M7 - Financieros","precio":250,"cat":"Financiero","desc":"DGII"},
    "M8_FULL": {"nombre":"M8 - Forense Full + IA","precio":250,"cat":"IA","desc":"TODO + IA"},
    "M9_NOBACI": {"nombre":"M9 - NOBACI","precio":250,"cat":"Control","desc":"NOBACI + COSO"},
    "M10_INV": {"nombre":"M10 - Inventarios","precio":250,"cat":"Inventarios","desc":"Toma fisica IA"},
    "M11_PAGOS": {"nombre":"M11 - Pagos + Libramientos","precio":250,"cat":"Tesoreria","desc":"SIGEF + cheques"},
    "M12_INF": {"nombre":"M12 - Informes IA","precio":250,"cat":"Informes","desc":"Informes IA"},
}

HISTORIAL_FILE = "/tmp/historial_replicas.json"
UPLOAD_FOLDER = "/tmp/replicas"

def get_historial():
    if os.path.exists(HISTORIAL_FILE):
        try:
            with open(HISTORIAL_FILE,'r',encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_historial(data):
    try:
        with open(HISTORIAL_FILE,'w',encoding='utf-8') as f:
            json.dump(data,f,ensure_ascii=False,indent=2)
    except:
        pass

def add_event(tipo, descripcion, archivo, accion):
    hist=get_historial()
    ev={"fecha":datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),"tipo":tipo.upper(),"descripcion":descripcion,"archivo":archivo,"accion":accion,"empresa":session.get('empresa','DEMO'),"contrato":session.get('contrato','CTR-DEMO')}
    hist.insert(0,ev)
    save_historial(hist)
    return ev

def generar_contrato_txt(empresa, rnc, email, mods, pais, total, cid):
    info=PAISES.get(pais,PAISES["DO"])
    lista=""
    for m in mods:
        if m in MODULOS:
            lista=lista+"- "+MODULOS[m]["nombre"]+" USD250\n"
    txt="CONTRATO SAAS BASA V13 FIX 404 - "+cid+"\nFECHA: "+datetime.datetime.now().strftime("%d/%m/%Y")+"\nEMPRESA: "+empresa+"\nRNC: "+rnc+"\nEMAIL: "+email+"\nPAIS: "+info["nombre"]+" - "+",".join(info["leyes"])+"\nMODULOS:\n"+lista+"\nTOTAL: USD$"+str(total)+"\nBHD: "+BHD_CUENTA+"\nFRONT: "+FRONT_URL+"/trial - BACK: "+BASE_URL+"\nFIRMA DIGITAL Ley 126-02 + ESIGN + eIDAS\n"
    return txt

def generar_informe_txt(tipo, empresa, rnc):
    fecha=datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    if tipo=="acta_lectura":
        return "ACTA DE LECTURAS - BASA V13\nEmpresa: "+empresa+"\nRNC: "+rnc+"\nFecha: "+fecha+"\nContrato: "+session.get('contrato','CTR')+"\nHallazgos lectura NOBACI Ley 10-07...\n"
    elif tipo=="preliminar":
        return "INFORME PRELIMINAR V13\nEmpresa: "+empresa+"\nRNC: "+rnc+"\nFecha: "+fecha+"\nHallazgos: Fraccionamiento, SIGEF sin soporte, NOBACI debil, Inventarios...\nPlazo 10 dias replica Reg 416-23.\n"
    else:
        return "INFORME FINAL V13\nEmpresa: "+empresa+"\nRNC: "+rnc+"\nFecha: "+fecha+"\nInforme final definitivo TSA, analisis replicas, NOBACI final, libramientos, inventarios, matriz riesgo.\n"

INDEX_HTML = """
<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>BASA V13 - Audit Intelligence USA</title><link rel='manifest' href='/manifest.json'><style>
body{font-family:system-ui,Arial;background:#0f172a;color:white;margin:0;padding:0}.hero{background:linear-gradient(135deg,#003366 0%,#00d084 100%);padding:40px 20px;text-align:center}.card{background:white;color:#0f172a;padding:20px;border-radius:16px;max-width:1100px;margin:20px auto}.btn{padding:12px 18px;border-radius:8px;font-weight:bold;border:none;margin:5px;cursor:pointer;text-decoration:none;display:inline-block}.verde{background:#00d084;color:white}.azul{background:#003366;color:white}
</style></head><body>
<div class='hero'><h1>BASA V13 - AUDIT INTELLIGENCE USA - FIX 404</h1><p>USD250 x modulo | BHD 08694150021 | PWA Android iPhone | Contrato Funcional + Informes + Replicas + Historial</p><p style='background:rgba(0,0,0,0.2);padding:8px;border-radius:8px;display:inline-block'>Dominio: audit-intelligence-usa.com/trial - Backend: basa-v7-1.onrender.com</p></div>
<div class='card'>
<h2 id='ruta'>Cargando...</h2>
<div id='contenido'></div>
<div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-top:15px'>
<a href='/trial' class='btn azul'>/trial (FIX 404)</a><a href='/contrato' class='btn azul'>Contrato Funcional</a><a href='/gestion-informes' class='btn verde'>Gestion Informes + Replicas + Historial</a>
<a href='/b4' class='btn azul'>B4 FULL</a><a href='/v8' class='btn azul'>V8 FULL NOBACI</a><a href='/demo' class='btn azul' style='background:#6b7280'>ZIP REAL</a>
</div>
<div style='margin-top:15px;background:#fef3c7;padding:12px;border-radius:8px;color:#92400e'><b>FIX NETLIFY 404:</b> Si ve este index en audit-intelligence-usa.com/trial significa que el fix _redirects funciono. Este archivo maneja todas las rutas.</div>
</div>
<script>
var path=window.location.pathname;
document.getElementById('ruta').innerText='Ruta actual: '+path+' - OK FIX 200';
var html='';
if(path.includes('trial')){
 html='<h3>TRIAL - Audit Intelligence USA - Activacion Demo</h3><p>Prueba gratis 7 dias BASA V13</p><form id="auditSaaSForm" onsubmit="return activar(event)"><label>Empresa:</label><input id="empresa" required style="width:100%;padding:8px;margin:4px 0"><label>RNC:</label><input id="rnc" required style="width:100%;padding:8px"><label>Email:</label><input id="email" type="email" required style="width:100%;padding:8px"><label><input type="checkbox" id="acepta" required> Acepto Contrato BASA</label><br><button type="submit" class="btn verde">Activar Trial + Generar Contrato</button></form><div id="res"></div>';
} else if(path.includes('contrato')){
 html='<iframe src="https://basa-v7-1.onrender.com/contrato" style="width:100%;height:800px;border:none;border-radius:12px"></iframe>';
} else if(path.includes('gestion')){
 html='<iframe src="https://basa-v7-1.onrender.com/gestion-informes" style="width:100%;height:900px;border:none;border-radius:12px"></iframe>';
} else {
 html='<h3>Sistema BASA V13 FULL</h3><p>Use /trial para registro SaaS</p>';
}
document.getElementById('contenido').innerHTML=html;
function activar(e){
 e.preventDefault();
 var empresa=document.getElementById('empresa').value;
 var rnc=document.getElementById('rnc').value;
 var email=document.getElementById('email').value;
 fetch('https://basa-v7-1.onrender.com/api/activar-saas',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({empresa:empresa,rnc:rnc,email:email,pais:'DO',mods:['B4_BASE','M9_NOBACI','M11_PAGOS','M10_INV']})}).then(function(r){return r.json();}).then(function(d){
  document.getElementById('res').innerHTML='<p style="color:#00a86b">Contrato '+d.contrato+' generado Total USD$'+d.total+'</p><a href="https://basa-v7-1.onrender.com/api/contrato/'+d.contrato+'" target="_blank" class="btn verde">Descargar Contrato PDF Real</a><a href="https://basa-v7-1.onrender.com/gestion-informes" class="btn azul">Ir a Gestion Informes y Replicas</a>';
 });
 return false;
}
if('serviceWorker' in navigator){navigator.serviceWorker.register('/sw.js');}
</script></body></html>
"""

@app.route('/')
def root():
    return render_template_string(INDEX_HTML)

@app.route('/trial')
def trial():
    return render_template_string(INDEX_HTML)

@app.route('/index.html')
def index_html():
    return render_template_string(INDEX_HTML)

@app.route('/manifest.json')
def manifest():
    return jsonify({"name":"BASA V13 Audit Intelligence","short_name":"BASA V13","start_url":"/trial","display":"standalone","theme_color":"#00d084"})

@app.route('/sw.js')
def sw():
    return Response("self.addEventListener('install',function(e){self.skipWaiting();});", mimetype='application/javascript')

@app.route('/healthz')
def health():
    return jsonify({"status":"OK V13 FIX 404","front":FRONT_URL+"/trial","back":BASE_URL})

@app.route('/contrato')
def contrato_page():
    pais_opts=""
    for code in PAISES:
        pais_opts=pais_opts+"<option value='"+code+"'>"+PAISES[code]["nombre"]+"</option>"
    mods_opts=""
    for k in MODULOS:
        sel="selected" if k in ["B4_BASE","M9_NOBACI"] else ""
        mods_opts=mods_opts+"<option value='"+k+"' "+sel+">"+MODULOS[k]["nombre"]+"</option>"
    html="<html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Contrato V13</title><style>body{font-family:Arial;background:#0f172a;color:white;padding:10px}.card{background:white;color:black;padding:18px;border-radius:16px;max-width:950px;margin:auto}.btn{padding:10px;border-radius:8px;font-weight:bold;border:none;margin:4px;text-decoration:none;display:inline-block}.verde{background:#00d084;color:white;width:100%}input,select{width:100%;padding:8px;border:2px solid #cbd5e1;border-radius:8px;margin:4px 0}</style></head><body>"
    html=html+"<h2 style='color:#00d084;text-align:center'>CONTRATO FUNCIONAL V13 + TRIAL FIX</h2><div class='card'><form id='auditSaaSForm' onsubmit='return integrar(event)'><label>Empresa:</label><input id='empresa' required><label>RNC:</label><input id='rnc' required><label>Email:</label><input id='email' type='email' required><label>Pais:</label><select id='pais'>"+pais_opts+"</select><label>Modulos:</label><select id='modulos' multiple size='6'>"+mods_opts+"</select><label><input type='checkbox' id='aceptaContrato' required style='width:20px;height:20px'> Acepto Contrato SaaS BASA</label><div id='resumen' style='background:#ecfdf5;padding:8px;border-radius:8px;margin:8px 0'></div><button type='submit' class='btn verde'>Activar Cuenta y Acceder</button></form><div id='res' style='display:none'></div><a href='/gestion-informes' class='btn' style='background:#003366;color:white;width:100%;text-align:center;margin-top:10px'>GESTION INFORMES Y REPLICAS + HISTORIAL</a></div>"
    html=html+"<script>function integrar(e){e.preventDefault();var emp=document.getElementById('empresa').value;var rnc=document.getElementById('rnc').value;var email=document.getElementById('email').value;var pais=document.getElementById('pais').value;var sel=document.getElementById('modulos');var mods=[];for(var i=0;i<sel.options.length;i++){if(sel.options[i].selected) mods.push(sel.options[i].value);}if(mods.indexOf('B4_BASE')==-1) mods.unshift('B4_BASE');fetch('/api/activar-saas',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({empresa:emp,rnc:rnc,email:email,pais:pais,mods:mods})}).then(function(r){return r.json();}).then(function(d){var res=document.getElementById('res');res.style.display='block';res.innerHTML='<h3>Contrato '+d.contrato+' OK</h3><a href=\"/api/contrato/'+d.contrato+'\" target=\"_blank\" class=\"btn verde\">Descargar PDF Real</a><a href=\"/gestion-informes\" class=\"btn\" style=\"background:#003366;color:white\">Ir a Informes y Replicas</a>';});return false;}</script></body></html>"
    return html

@app.route('/api/activar-saas', methods=['POST'])
def activar_saas():
    data=request.get_json() or {}
    empresa=data.get('empresa','Empresa Demo')
    rnc=data.get('rnc','001')
    email=data.get('email','demo@demo.com')
    pais=data.get('pais','DO')
    mods=data.get('mods',['B4_BASE'])
    if 'B4_BASE' not in mods:
        mods=['B4_BASE']+mods
    sub=len(mods)*250
    imp=PAISES.get(pais,PAISES["DO"])["impuesto"]
    total=round(sub*(1+imp),2)
    cid="CTR-V13-"+datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    texto=generar_contrato_txt(empresa,rnc,email,mods,pais,total,cid)
    session['activado']=True
    session['contrato']=cid
    session['empresa']=empresa
    session['rnc']=rnc
    session['email']=email
    session['mods']=mods
    session['pais']=pais
    session['total']=total
    session['texto_contrato']=texto
    path="/tmp/"+cid+".txt"
    try:
        with open(path,'w',encoding='utf-8') as f:
            f.write(texto)
    except:
        pass
    add_event("CONTRATO","Contrato "+cid+" "+empresa, cid+".pdf","GENERACION")
    return jsonify({"contrato":cid,"total":total,"bhd":BHD_CUENTA,"trial_url":FRONT_URL+"/trial"})

@app.route('/api/contrato/<cid>')
def get_contrato(cid):
    path="/tmp/"+cid+".txt"
    texto=""
    if os.path.exists(path):
        with open(path,'r',encoding='utf-8') as f:
            texto=f.read()
    else:
        texto=session.get('texto_contrato', "CONTRATO "+cid)
    return send_file(io.BytesIO(texto.encode('utf-8')), mimetype="application/pdf", as_attachment=True, download_name=cid+".pdf")

@app.route('/api/contrato')
def contrato_base():
    txt=generar_contrato_txt("DEMO","001","demo@demo.com",list(MODULOS.keys())[:3],"DO",750,"CTR-DEMO")
    return send_file(io.BytesIO(txt.encode('utf-8')), mimetype="application/pdf", as_attachment=False, download_name="CONTRATO_BASE.pdf")

@app.route('/gestion-informes')
def gestion_informes():
    empresa=session.get('empresa','Empresa DEMO - Active en /contrato o /trial')
    rnc=session.get('rnc','001')
    contrato=session.get('contrato','CTR-DEMO')
    historial=get_historial()
    filas=""
    if len(historial)==0:
        filas="<tr><td colspan='5' class='text-center text-muted'>No hay replicas registradas en esta auditoria.</td></tr>"
    else:
        for ev in historial[:50]:
            filas=filas+"<tr><td>"+ev["fecha"]+"</td><td><span style='background:#003366;color:white;padding:2px 6px;border-radius:4px'>"+ev["tipo"]+"</span></td><td>"+ev["descripcion"]+"<br><small>"+ev["archivo"]+"</small></td><td>"+ev["accion"]+"</td><td><a href='/api/descargar-replica/"+ev["archivo"]+"' target='_blank'>Ver</a></td></tr>"
    html="<html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'><title>Gestion Informes V13</title><style>body{background:#0f172a;color:white}</style></head><body>"
    html=html+"<div class='container mt-3'><h2 style='color:#00d084;text-align:center'>BASA V13 - GESTION INFORMES Y REPLICAS + HISTORIAL - FIX 404</h2><div class='card shadow mb-4' style='color:#0f172a'><div class='card-header py-3 bg-primary text-white' style='background:#003366!important'><h5 class='m-0'>Empresa: "+empresa+" - Contrato: "+contrato+" - RNC: "+rnc+"</h5></div><div class='card-body'>"
    html=html+"<div class='row mb-4'><div class='col-md-4'><div class='border p-3 rounded bg-light'><h6>1. Acta de Lecturas</h6><button class='btn btn-sm btn-info w-100 mb-2' onclick='generarInforme(\"acta_lectura\")'>Generar Acta</button><hr><label class='small fw-bold'>Cargar Replica multiple:</label><input type='file' class='form-control form-control-sm mb-2' id='file_acta' multiple><button class='btn btn-sm btn-secondary w-100' onclick='subirReplica(\"acta_lectura\")'>Subir Replica</button></div></div>"
    html=html+"<div class='col-md-4'><div class='border p-3 rounded bg-light'><h6>2. Informe Preliminar</h6><button class='btn btn-sm btn-info w-100 mb-2' onclick='generarInforme(\"preliminar\")'>Generar Preliminar</button><hr><label class='small fw-bold'>Cargar Replica multiple:</label><input type='file' class='form-control form-control-sm mb-2' id='file_preliminar' multiple><button class='btn btn-sm btn-secondary w-100' onclick='subirReplica(\"preliminar\")'>Subir Replica</button></div></div>"
    html=html+"<div class='col-md-4'><div class='border p-3 rounded bg-light'><h6>3. Informe Final</h6><button class='btn btn-sm btn-info w-100 mb-2' onclick='generarInforme(\"final\")'>Generar Final</button><hr><label class='small fw-bold'>Cargar Recurso multiple:</label><input type='file' class='form-control form-control-sm mb-2' id='file_final' multiple><button class='btn btn-sm btn-secondary w-100' onclick='subirReplica(\"final\")'>Subir Recurso</button></div></div></div>"
    html=html+"<hr><h6 class='fw-bold'>Historial Intervenciones y Replicas</h6><div class='table-responsive'><table class='table table-striped table-sm' id='tablaHistorial'><thead style='background:#003366;color:white'><tr><th>Fecha/Hora</th><th>Tipo</th><th>Descripcion/Archivo</th><th>Accion</th><th>Ver</th></tr></thead><tbody>"+filas+"</tbody></table></div>"
    html=html+"<div style='text-align:center'><a href='/contrato' class='btn btn-sm' style='background:#003366;color:white'>Contrato</a><a href='/trial' class='btn btn-sm' style='background:#00d084;color:white'>Trial FIX</a><a href='/api/exportar-historial' class='btn btn-sm btn-dark'>Exportar Historial</a></div></div></div></div>"
    html=html+"<script>function generarInforme(tipo){if(confirm('Generar '+tipo.toUpperCase()+'?')){window.location.href='/api/generar-informe/'+tipo;}}function subirReplica(etapa){var input=document.getElementById('file_'+etapa);if(input.files.length==0){alert('Seleccione archivo(s)');return;}var fd=new FormData();for(var i=0;i<input.files.length;i++){fd.append('files',input.files[i]);}fd.append('etapa',etapa);fetch('/api/subir-replica',{method:'POST',body:fd}).then(function(r){return r.json();}).then(function(d){if(d.ok){alert('Replica(s) cargada(s) '+etapa.toUpperCase());location.reload();}});}</script></body></html>"
    return html

@app.route('/api/generar-informe/<tipo>')
def api_gen_inf(tipo):
    if tipo not in ["acta_lectura","preliminar","final"]:
        return jsonify({"error":"Tipo invalido"}),400
    empresa=session.get('empresa','DEMO')
    rnc=session.get('rnc','001')
    contenido=generar_informe_txt(tipo,empresa,rnc)
    add_event(tipo,"Generado "+tipo+" para "+empresa, tipo+"_"+session.get('contrato','CTR')+".pdf","GENERACION INFORME")
    return send_file(io.BytesIO(contenido.encode('utf-8')), mimetype="application/pdf", as_attachment=True, download_name=tipo.upper()+"_"+session.get('contrato','CTR')+".pdf")

@app.route('/api/subir-replica', methods=['POST'])
def api_subir_replica():
    etapa=request.form.get('etapa','acta_lectura')
    empresa=session.get('empresa','DEMO')
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    files=request.files.getlist('files')
    guardados=[]
    for f in files:
        if f.filename=='':
            continue
        fname=secure_filename(f.filename)
        final_name=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+"_"+etapa+"_"+fname
        path=os.path.join(UPLOAD_FOLDER, final_name)
        f.save(path)
        add_event(etapa,"Replica cargada: "+fname+" - "+empresa, final_name,"CARGA REPLICA")
        guardados.append(final_name)
    return jsonify({"ok":True,"files":guardados})

@app.route('/api/descargar-replica/<fname>')
def descargar_rep(fname):
    path=os.path.join(UPLOAD_FOLDER, secure_filename(fname))
    if os.path.exists(path):
        return send_file(path, as_attachment=True, download_name=fname)
    return jsonify({"error":"No encontrado"}),404

@app.route('/api/exportar-historial')
def exportar_hist():
    hist=get_historial()
    txt="HISTORIAL V13 - "+session.get('contrato','CTR')+"\n"
    for ev in hist:
        txt=txt+ev["fecha"]+" | "+ev["tipo"]+" | "+ev["descripcion"]+" | "+ev["archivo"]+" | "+ev["accion"]+"\n"
    return send_file(io.BytesIO(txt.encode('utf-8')), mimetype="application/pdf", as_attachment=True, download_name="HISTORIAL_"+session.get('contrato','CTR')+".pdf")

@app.route('/api/historial')
def api_hist():
    return jsonify(get_historial())

@app.route('/b4')
def b4():
    return "<body style='font-family:Arial;background:#0f172a;color:white;padding:10px'><h2 style='color:#00d084'>B4 V13 FIX 404</h2><div style='background:white;color:black;padding:16px;border-radius:12px;max-width:1100px;margin:auto'><a href='/gestion-informes' style='background:#00d084;color:white;padding:10px;border-radius:8px;text-decoration:none'>Gestion Informes</a> <a href='/trial' style='background:#003366;color:white;padding:10px;border-radius:8px;text-decoration:none'>Trial FIX</a></div></body>"

@app.route('/v8')
def v8():
    return "<body style='font-family:Arial;background:#0a192f;color:white;padding:10px'><h2 style='color:#00d084'>V8 V13 FIX</h2><div style='background:white;color:black;padding:16px;border-radius:12px;max-width:1100px;margin:auto'><a href='/gestion-informes' style='background:#00d084;color:white;padding:10px;border-radius:8px;text-decoration:none'>Gestion Informes</a></div></body>"

@app.route('/demo')
def demo_zip():
    m=io.BytesIO()
    with zipfile.ZipFile(m,mode="w",compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("FIX_404_NETLIFY.txt","FIX para audit-intelligence-usa.com/trial 404\n1. Crear netlify.toml con redirects\n2. Crear _redirects con /* /index.html 200\n3. Subir a Netlify\n4. Limpiar cache y redeploy\nBackend Render: basa-v7-1.onrender.com\nFrontend Netlify: audit-intelligence-usa.com\n")
        zf.writestr("netlify.toml","[build]\n publish = \".\"\n[[redirects]]\n from = \"/*\"\n to = \"/index.html\"\n status = 200\n")
        zf.writestr("_redirects","/* /index.html 200\n")
    m.seek(0)
    return send_file(m, mimetype="application/zip", as_attachment=True, download_name="BASA_V13_FIX_404_TRIAL.zip")

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get("PORT",10000)))
