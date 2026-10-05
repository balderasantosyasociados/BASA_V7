import os, io, zipfile, datetime, json, calendar
from flask import Flask, jsonify, request, session, send_file, Response
from flask_cors import CORS
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = "BASA_V12_INFORMES_REPLICAS_HISTORIAL"
CORS(app)

BHD_CUENTA = "08694150021 - USD Y DOP"
STRIPE_KEY = os.environ.get("STRIPE_SECRET_KEY", "")

PAISES = {
    "DO": {"nombre":"Rep. Dominicana","moneda":"DOP","impuesto":0.18,"leyes":["Ley 340-06","Reg 416-23","NOBACI","Ley 10-07","Ley 155-17","Ley 126-02"],"portal":"comprasdominicana.gob.do"},
    "US": {"nombre":"Estados Unidos","moneda":"USD","impuesto":0.0,"leyes":["FAR","2 CFR 200","SOX"],"portal":"sam.gov"},
    "MX": {"nombre":"Mexico","moneda":"MXN","impuesto":0.16,"leyes":["LAASSP"],"portal":"compranet.hacienda.gob.mx"},
    "PA": {"nombre":"Panama","moneda":"USD","impuesto":0.07,"leyes":["Ley 22"],"portal":"panamacompra.gob.pa"},
    "CO": {"nombre":"Colombia","moneda":"COP","impuesto":0.19,"leyes":["Ley 80"],"portal":"colombiacompra.gov.co"},
    "ES": {"nombre":"Espana","moneda":"EUR","impuesto":0.21,"leyes":["LCSP","eIDAS"],"portal":"contrataciondelestado.es"},
}

MODULOS = {
    "B4_BASE": {"nombre":"B4 Base - Informe Pericial IA","precio":250,"cat":"Informes","desc":"Informe pericial IA + NOBACI"},
    "M1_SCRAPER": {"nombre":"M1 - Scraper 10 anos IA","precio":250,"cat":"Auditoria","desc":"Scraping portal + IA"},
    "M2_FRACC": {"nombre":"M2 - Fraccionamiento + Libramientos","precio":250,"cat":"Auditoria","desc":"Fracc + SIGEF"},
    "M3_DUENO": {"nombre":"M3 - Mismo Dueno","precio":250,"cat":"Forense","desc":"Multi-RNC"},
    "M4_ACC": {"nombre":"M4 - Accionistas","precio":250,"cat":"Forense","desc":"Activos ocultos"},
    "M5_CONF": {"nombre":"M5 - Consanguinidad + PEPs","precio":250,"cat":"Legal","desc":"Parentesco + PEPs"},
    "M6_NOM": {"nombre":"M6 - Nomina + TSS","precio":250,"cat":"Nomina","desc":"Nomina fantasma"},
    "M7_FIN": {"nombre":"M7 - Financieros","precio":250,"cat":"Financiero","desc":"DGII vs compras"},
    "M8_FULL": {"nombre":"M8 - Forense Full + IA","precio":250,"cat":"IA","desc":"TODO + IA"},
    "M9_NOBACI": {"nombre":"M9 - NOBACI","precio":250,"cat":"Control","desc":"NOBACI + COSO"},
    "M10_INV": {"nombre":"M10 - Inventarios","precio":250,"cat":"Inventarios","desc":"Toma fisica IA"},
    "M11_PAGOS": {"nombre":"M11 - Pagos + Libramientos","precio":250,"cat":"Tesoreria","desc":"Libramientos + cheques"},
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
    hist = get_historial()
    ev = {
        "fecha": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "tipo": tipo.upper(),
        "descripcion": descripcion,
        "archivo": archivo,
        "accion": accion,
        "empresa": session.get('empresa','DEMO'),
        "contrato": session.get('contrato','CTR-DEMO')
    }
    hist.insert(0, ev)
    save_historial(hist)
    return ev

def generar_texto_contrato(empresa, rnc, email, mods, pais, total, cid):
    info = PAISES.get(pais, PAISES["DO"])
    fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    lista = ""
    for m in mods:
        if m in MODULOS:
            lista = lista + "- " + MODULOS[m]["nombre"] + " USD$250\n"
    txt = ""
    txt = txt + "CONTRATO SAAS BASA V12 - "+cid+"\nFECHA: "+fecha+"\nEMPRESA: "+empresa+"\nRNC: "+rnc+"\nEMAIL: "+email+"\nPAIS: "+info["nombre"]+" - "+",".join(info["leyes"])+"\nMODULOS:\n"+lista+"\nTOTAL: USD$"+str(total)+"\nBHD: "+BHD_CUENTA+"\nFIRMA DIGITAL Ley 126-02 + ESIGN + eIDAS VALIDA\n"
    return txt

def generar_informe(tipo, empresa, rnc):
    fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    contenido = ""
    if tipo == "acta_lectura":
        contenido = contenido + "ACTA DE LECTURAS - BALDERA SANTOS Y ASOCIADOS\nContrato: "+session.get('contrato','CTR-DEMO')+"\nEmpresa auditada: "+empresa+"\nRNC: "+rnc+"\nFecha: "+fecha+"\n\nConforme NOBACI y Ley 10-07, se levanta Acta de Lecturas...\nHallazgos preliminares, documentacion revisada, entrevistas...\nFirma digital valida.\n"
    elif tipo == "preliminar":
        contenido = contenido + "INFORME PRELIMINAR - BASA V12\nEmpresa: "+empresa+"\nRNC: "+rnc+"\nFecha: "+fecha+"\n\nHallazgos: Fraccionamiento, Libramientos SIGEF sin soporte, NOBACI debil, Inventarios faltantes, Nomina fantasma...\nSe otorga 10 dias para replica segun Reg 416-23 Art 45.\n"
    else:
        contenido = contenido + "INFORME FINAL AUDITORIA FORENSE - BASA V12\nEmpresa: "+empresa+"\nRNC: "+rnc+"\nFecha: "+fecha+"\n\nInforme final definitivo despues de analisis replicas y recursos reconsideracion.\nIncluye: NOBACI final, libramientos, inventarios, nomina, pagos, matriz riesgo, recomendaciones, evidencias IA.\nFirma pericial valida para Tribunal Superior Administrativo.\n"
    return contenido

@app.route('/manifest.json')
def manifest():
    return jsonify({"name":"BASA V12 Informes Replicas","short_name":"BASA V12","start_url":"/gestion-informes","display":"standalone","theme_color":"#00d084"})

@app.route('/sw.js')
def sw():
    return Response("self.addEventListener('install',function(e){self.skipWaiting();});", mimetype='application/javascript')

@app.route('/')
def home():
    return jsonify({"BASA":"V12 INFORMES + REPLICAS + HISTORIAL","contrato":"/contrato","gestion":"/gestion-informes","bhd":BHD_CUENTA})

@app.route('/healthz')
def health():
    return jsonify({"status":"OK V12"})

# CONTRATO FUNCIONAL
@app.route('/contrato')
def contrato_page():
    pais_opts=""
    for code,info in PAISES.items():
        pais_opts=pais_opts+"<option value='"+code+"'>"+info["nombre"]+"</option>"
    mods_opts=""
    for k,v in MODULOS.items():
        sel="selected" if k in ["B4_BASE","M9_NOBACI","M11_PAGOS","M10_INV"] else ""
        mods_opts=mods_opts+"<option value='"+k+"' "+sel+">"+v["nombre"]+"</option>"
    html = """
<html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><link rel='manifest' href='/manifest.json'><title>Contrato V12</title><style>
body{font-family:Arial;background:#0f172a;color:white;padding:10px}.card{background:white;color:#0f172a;padding:18px;border-radius:16px;max-width:950px;margin:auto}.btn{padding:10px;border-radius:8px;font-weight:bold;border:none;margin:4px;cursor:pointer;text-decoration:none;display:inline-block}.verde{background:#00d084;color:white;width:100%;font-size:16px}.azul{background:#003366;color:white}
input,select{width:100%;padding:9px;border:2px solid #cbd5e1;border-radius:8px;margin:4px 0}
</style></head><body>
<h2 style='text-align:center;color:#00d084'>BASA V12 - CONTRATO FUNCIONAL REAL</h2>
<div class='card'>
<form id="auditSaaSForm" onsubmit="return integrarCliente(event)">
<h3>Registro Suscripcion</h3>
<label>Empresa:</label><input type="text" id="empresa" required>
<label>RNC:</label><input type="text" id="rnc" required>
<label>Email Corporativo:</label><input type="email" id="email" required>
<label>Pais:</label><select id="pais">""" + pais_opts + """</select>
<label>Modulos:</label><select id="modulos" multiple size="7">""" + mods_opts + """</select>
<label><input type="checkbox" id="aceptaContrato" required style="width:20px;height:20px"> Acepto Contrato SaaS BASA - Firma Ley 126-02 + ESIGN + eIDAS</label>
<div id='resumen' style='background:#ecfdf5;padding:10px;border-radius:8px;margin:8px 0'></div>
<button type="submit" class="btn verde">Activar Cuenta + Generar Contrato Real</button>
</form>
<div id='resultado' style='display:none;margin-top:12px'></div>
<div style='margin-top:12px'><a href='/gestion-informes' class='btn azul' style='background:#00d084;width:100%;text-align:center'>IR A GESTION INFORMES Y REPLICAS + HISTORIAL (NUEVO)</a></div>
</div>
<script>
function getMods(){var sel=document.getElementById('modulos');var m=[];for(var i=0;i<sel.options.length;i++){if(sel.options[i].selected) m.push(sel.options[i].value);}if(m.indexOf('B4_BASE')==-1) m.unshift('B4_BASE');return m;}
function integrarCliente(e){
 e.preventDefault();
 var empresa=document.getElementById('empresa').value;
 var rnc=document.getElementById('rnc').value;
 var email=document.getElementById('email').value;
 var pais=document.getElementById('pais').value;
 var mods=getMods();
 fetch('/api/activar-saas',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({empresa:empresa,rnc:rnc,email:email,pais:pais,mods:mods})}).then(function(r){return r.json();}).then(function(d){
  var res=document.getElementById('resultado');res.style.display='block';
  res.innerHTML='<h3>Contrato: '+d.contrato+' Generado</h3><p>Empresa: '+empresa+' Total USD$'+d.total+' BHD 08694150021</p><a href="/api/contrato/'+d.contrato+'" target="_blank" class="btn verde" style="width:auto">Descargar PDF Real</a><br><br><a href="/gestion-informes" class="btn azul">Ir a Gestion Informes y Replicas</a>';
 });
 return false;
}
</script></body></html>
"""
    return html

@app.route('/api/activar-saas', methods=['POST'])
def activar_saas():
    data=request.get_json() or {}
    empresa=data.get('empresa','Empresa Demo')
    rnc=data.get('rnc','001')
    email=data.get('email','demo@empresa.com')
    pais=data.get('pais','DO')
    mods=data.get('mods',['B4_BASE'])
    if 'B4_BASE' not in mods:
        mods=['B4_BASE']+mods
    sub=len(mods)*250
    imp=PAISES.get(pais,PAISES["DO"])["impuesto"]
    total=round(sub*(1+imp),2)
    cid="CTR-V12-"+datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+"-"+empresa[:3].upper().replace(" ","X")
    texto=generar_texto_contrato(empresa,rnc,email,mods,pais,total,cid)
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
    add_event("CONTRATO","Contrato "+cid+" generado para "+empresa, cid+".pdf","GENERACION")
    return jsonify({"contrato":cid,"total":total,"bhd":BHD_CUENTA})

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
    txt=generar_texto_contrato("DEMO","001","demo@demo.com",list(MODULOS.keys())[:3],"DO",750,"CTR-DEMO")
    return send_file(io.BytesIO(txt.encode('utf-8')), mimetype="application/pdf", as_attachment=False, download_name="CONTRATO_BASE.pdf")

# NUEVO MODULO GESTION INFORMES Y REPLICAS - FUNCIONAL
@app.route('/gestion-informes')
def gestion_informes():
    act=session.get('activado',False)
    empresa=session.get('empresa','Empresa DEMO - Active en /contrato')
    rnc=session.get('rnc','001-00000-1')
    contrato=session.get('contrato','CTR-DEMO')
    historial=get_historial()
    filas=""
    if len(historial)==0:
        filas="<tr><td colspan='5' class='text-center text-muted'>No hay replicas registradas en esta auditoria.</td></tr>"
    else:
        for ev in historial[:50]:
            filas=filas+"<tr><td>"+ev["fecha"]+"</td><td><span style='background:#003366;color:white;padding:2px 6px;border-radius:4px'>"+ev["tipo"]+"</span></td><td>"+ev["descripcion"]+"<br><small>"+ev["archivo"]+"</small></td><td>"+ev["accion"]+"</td><td><a href='/api/descargar-replica/"+ev["archivo"]+"' target='_blank' style='color:#003366'>Ver</a></td></tr>"

    html = """
<html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><link rel='manifest' href='/manifest.json'><link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'><title>Gestion Informes y Replicas - BASA V12</title><style>
body{background:#0f172a;color:white;font-family:Arial}.card{border-radius:16px}.bg-basa{background:#003366}.text-basa{color:#003366}.btn-basa{background:#00d084;color:white;font-weight:bold}
</style></head><body>
<div class="container mt-3">
<h2 style='color:#00d084;text-align:center'>BASA V12 - GESTION DE INFORMES Y RECURSOS DE RECONSIDERACION</h2>
<div class="card shadow mb-4" style="color:#0f172a">
    <div class="card-header py-3 bg-primary text-white" style="background:#003366!important">
        <h5 class="m-0 font-weight-bold">Gestion de Informes y Recursos de Reconsideracion - Empresa: """ + empresa + """ - Contrato: """ + contrato + """ - RNC: """ + rnc + """</h5>
    </div>
    <div class="card-body">
        <div class="row mb-4">
            <div class="col-md-4">
                <div class="border p-3 rounded bg-light">
                    <h6><b>1. Acta de Lecturas</b> <span style="background:#00d084;color:white;padding:2px 6px;border-radius:10px;font-size:10px">NOBACI + Ley 10-07</span></h6>
                    <p style="font-size:11px;color:#475569">Acta inicial, lectura hallazgos, firma participantes</p>
                    <button class="btn btn-sm btn-info w-100 mb-2" onclick="generarInforme('acta_lectura')">Generar Acta</button>
                    <hr>
                    <label class="small fw-bold">Cargar Replica / Recurso (multiple):</label>
                    <input type="file" class="form-control form-control-sm mb-2" id="file_acta" multiple>
                    <button class="btn btn-sm btn-secondary w-100" onclick="subirReplica('acta_lectura')">Subir Replica</button>
                    <div id="lista_acta" style="font-size:11px;margin-top:6px"></div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="border p-3 rounded bg-light">
                    <h6><b>2. Informe Preliminar</b> <span style="background:#f59e0b;color:white;padding:2px 6px;border-radius:10px;font-size:10px">10 dias replica</span></h6>
                    <p style="font-size:11px;color:#475569">Informe con hallazgos, NOBACI, libramientos, inventarios, plazo 10 dias replica Reg 416-23</p>
                    <button class="btn btn-sm btn-info w-100 mb-2" onclick="generarInforme('preliminar')">Generar Preliminar</button>
                    <hr>
                    <label class="small fw-bold">Cargar Replica / Recurso (multiple):</label>
                    <input type="file" class="form-control form-control-sm mb-2" id="file_preliminar" multiple>
                    <button class="btn btn-sm btn-secondary w-100" onclick="subirReplica('preliminar')">Subir Replica</button>
                    <div id="lista_preliminar" style="font-size:11px;margin-top:6px"></div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="border p-3 rounded bg-light">
                    <h6><b>3. Informe Final</b> <span style="background:#dc2626;color:white;padding:2px 6px;border-radius:10px;font-size:10px">Definitivo TSA</span></h6>
                    <p style="font-size:11px;color:#475569">Informe final definitivo, analisis replicas, matriz riesgo final, valido TSA</p>
                    <button class="btn btn-sm btn-info w-100 mb-2" onclick="generarInforme('final')">Generar Final</button>
                    <hr>
                    <label class="small fw-bold">Cargar Recurso / Reconsideracion (multiple):</label>
                    <input type="file" class="form-control form-control-sm mb-2" id="file_final" multiple>
                    <button class="btn btn-sm btn-secondary w-100" onclick="subirReplica('final')">Subir Recurso</button>
                    <div id="lista_final" style="font-size:11px;margin-top:6px"></div>
                </div>
            </div>
        </div>
        <hr>
        <h6 class="fw-bold text-dark">Historial de Intervenciones y Replicas - Registro Completo</h6>
        <div class="table-responsive">
            <table class="table table-striped table-sm" id="tablaHistorial">
                <thead style="background:#003366;color:white"><tr><th>Fecha / Hora</th><th>Tipo Proceso</th><th>Descripcion / Archivo</th><th>Accion Registrada</th><th>Ver</th></tr></thead>
                <tbody>""" + filas + """</tbody>
            </table>
        </div>
        <div style="margin-top:10px;text-align:center">
        <a href='/contrato' class='btn btn-sm' style='background:#003366;color:white'>Contrato Funcional</a>
        <a href='/activar-modulos' class='btn btn-sm' style='background:#003366;color:white'>Activar Modulos</a>
        <a href='/b4' class='btn btn-sm' style='background:#00d084;color:white'>B4 Informe IA</a>
        <a href='/api/exportar-historial' class='btn btn-sm btn-dark'>Exportar Historial Excel/PDF</a>
        </div>
    </div>
</div>
</div>
<script>
function generarInforme(tipo){
  var empresa=""" + '"' + empresa + '"' + """;
  if(empresa.includes('DEMO')){ alert('Active contrato primero en /contrato'); window.location='/contrato'; return; }
  if(confirm('Generar '+tipo.toUpperCase()+' para '+empresa+'? Se registrara en historial.')){
    window.location.href='/api/generar-informe/'+tipo;
  }
}
function subirReplica(etapa){
  var input=document.getElementById('file_'+etapa);
  if(input.files.length===0){ alert('Seleccione archivo(s) para cargar replica.'); return; }
  var formData=new FormData();
  for(var i=0;i<input.files.length;i++){ formData.append('files', input.files[i]); }
  formData.append('etapa', etapa);
  var btn=event.target;
  btn.innerHTML='Subiendo...';
  fetch('/api/subir-replica',{method:'POST',body:formData}).then(function(r){return r.json();}).then(function(d){
    if(d.ok){
      alert('Replica(s) cargada(s) exitosamente para '+etapa.toUpperCase()+'. Historial actualizado.');
      location.reload();
    } else {
      alert('Error: '+(d.error||'No se pudo subir'));
      btn.innerHTML='Subir Replica';
    }
  });
}
</script></body></html>
"""
    return html

@app.route('/api/generar-informe/<tipo>')
def api_generar_informe(tipo):
    if tipo not in ["acta_lectura","preliminar","final"]:
        return jsonify({"error":"Tipo invalido"}), 400
    empresa=session.get('empresa','Empresa DEMO')
    rnc=session.get('rnc','001-00000-1')
    contrato=session.get('contrato','CTR-DEMO')
    if "DEMO" in empresa:
        return "<body style='font-family:Arial;padding:20px;text-align:center'><h2>Active contrato primero</h2><a href='/contrato'>Ir a Contrato Funcional</a></body>"
    contenido=generar_informe(tipo, empresa, rnc)
    add_event(tipo, "Generado "+tipo+" para "+empresa+" RNC "+rnc, tipo+"_"+contrato+".pdf", "GENERACION INFORME")
    return send_file(io.BytesIO(contenido.encode('utf-8')), mimetype="application/pdf", as_attachment=True, download_name=tipo.upper()+"_"+contrato+"_"+empresa.replace(" ","_")+".pdf")

@app.route('/api/subir-replica', methods=['POST'])
def api_subir_replica():
    etapa=request.form.get('etapa','acta_lectura')
    empresa=session.get('empresa','DEMO')
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    files=request.files.getlist('files')
    if len(files)==0:
        return jsonify({"ok":False,"error":"No files"})
    guardados=[]
    for f in files:
        if f.filename=='':
            continue
        fname=secure_filename(f.filename)
        final_name=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+"_"+etapa+"_"+fname
        path=os.path.join(UPLOAD_FOLDER, final_name)
        f.save(path)
        add_event(etapa, "Replica/Recurso cargado por entidad auditada: "+fname+" - "+empresa, final_name, "CARGA REPLICA - "+str(len(files))+" archivos")
        guardados.append(final_name)
    return jsonify({"ok":True,"files":guardados,"etapa":etapa})

@app.route('/api/descargar-replica/<fname>')
def descargar_replica(fname):
    path=os.path.join(UPLOAD_FOLDER, secure_filename(fname))
    if os.path.exists(path):
        return send_file(path, as_attachment=True, download_name=fname)
    else:
        # buscar en /tmp
        if os.path.exists("/tmp/"+fname):
            return send_file("/tmp/"+fname, as_attachment=True, download_name=fname)
        return jsonify({"error":"No encontrado"}), 404

@app.route('/api/historial')
def api_historial():
    return jsonify(get_historial())

@app.route('/api/exportar-historial')
def exportar_historial():
    hist=get_historial()
    txt="HISTORIAL INTERVENCIONES Y REPLICAS - BASA V12\nContrato: "+session.get('contrato','CTR-DEMO')+"\nEmpresa: "+session.get('empresa','DEMO')+"\nFecha export: "+datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")+"\n\n"
    for ev in hist:
        txt=txt+ev["fecha"]+" | "+ev["tipo"]+" | "+ev["descripcion"]+" | "+ev["archivo"]+" | "+ev["accion"]+"\n"
    return send_file(io.BytesIO(txt.encode('utf-8')), mimetype="application/pdf", as_attachment=True, download_name="HISTORIAL_"+session.get('contrato','CTR')+".pdf")

# Mantener compatibilidad
@app.route('/activar-modulos')
def activar_modulos():
    return "<body style='font-family:Arial;padding:20px;text-align:center'><h2>V11/V12 - Use /contrato para activar</h2><a href='/contrato' style='background:#00d084;color:white;padding:12px;border-radius:8px;text-decoration:none'>Ir a Contrato Funcional</a><br><br><a href='/gestion-informes' style='background:#003366;color:white;padding:12px;border-radius:8px;text-decoration:none'>Ir a Gestion Informes y Replicas</a></body>"

@app.route('/b4')
def b4():
    empresa=session.get('empresa','DEMO')
    return "<body style='font-family:Arial;background:#0f172a;color:white;padding:12px'><h2 style='color:#00d084'>B4 V12 + Gestion Informes</h2><div style='background:white;color:black;padding:16px;border-radius:12px;max-width:1100px;margin:auto'><p>Empresa: "+empresa+"</p><a href='/gestion-informes' style='background:#00d084;color:white;padding:10px;border-radius:8px;text-decoration:none'>Gestion Informes y Replicas NUEVO</a> <a href='/contrato' style='background:#003366;color:white;padding:10px;border-radius:8px;text-decoration:none'>Contrato</a></div></body>"

@app.route('/v8')
def v8():
    return "<body style='font-family:Arial;background:#0a192f;color:white;padding:10px'><h2 style='color:#00d084;text-align:center'>V8 V12 - NOBACI + Gestion Informes</h2><div style='background:white;color:black;padding:16px;border-radius:12px;max-width:1100px;margin:auto'><a href='/gestion-informes' style='background:#00d084;color:white;padding:10px;border-radius:8px;text-decoration:none'>Gestion Informes y Replicas</a></div></body>"

@app.route('/pago-exitoso')
def pe():
    contrato=request.args.get('contrato', session.get('contrato','CTR-V12'))
    return "<body style='font-family:Arial;background:#ecfdf5;padding:20px;text-align:center'><h1 style='color:#00a86b'>PAGO OK V12 ACTIVO</h1><div style='background:white;padding:20px;border-radius:14px;max-width:750px;margin:auto'><h2>Contrato: "+contrato+"</h2><p>Empresa: "+session.get('empresa','')+"</p><a href='/gestion-informes' style='background:#00d084;color:white;padding:12px;border-radius:8px;text-decoration:none;display:inline-block;margin:4px'>IR A GESTION INFORMES Y REPLICAS</a><a href='/api/contrato/"+contrato+"' style='background:#003366;color:white;padding:12px;border-radius:8px;text-decoration:none;display:inline-block;margin:4px'>Descargar Contrato PDF</a></div></body>"

@app.route('/demo')
def demo_zip():
    m=io.BytesIO()
    with zipfile.ZipFile(m,mode="w",compression=zipfile.ZIP_DEFLATED) as zf:
        hist_txt=json.dumps(get_historial(), indent=2, ensure_ascii=False)
        zf.writestr("GESTION_INFORMES_REPLICAS_V12.txt", "MODULO NUEVO V12 - Gestion Informes y Replicas con Historial\n1 Acta Lecturas -> Generar PDF + Subir replicas multiple\n2 Informe Preliminar -> Generar PDF + Subir replicas multiple (10 dias)\n3 Informe Final -> Generar PDF + Subir recursos reconsideracion multiple\nHistorial completo fecha/hora/tipo/archivo/accion\nAPIs: /api/generar-informe/<tipo>, /api/subir-replica, /api/historial, /api/exportar-historial\n")
        zf.writestr("HISTORIAL.json", hist_txt)
        zf.writestr("CONTRATO_FUNCIONAL.txt", "Contrato funcional en /contrato")
    m.seek(0)
    return send_file(m, mimetype="application/zip", as_attachment=True, download_name="BASA_V12_GESTION_INFORMES_REPLICAS_HISTORIAL.zip")

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get("PORT",10000)))
