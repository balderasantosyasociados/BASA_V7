# -*- coding: utf-8 -*-
# BASA V1 FINAL PROFESIONAL - SINGLE BUTTON COMPRAR MODULOS + MODAL DESPLIEGUE SELECCION + AGRUPADO PROFESIONAL SIN CARNAVAL + SCRIPTS FUNCIONALES REALES POR ROL IA DEMO / DATOS CLIENTE PRUEBA / FULL PERMANENTE
import os, json, hashlib
from datetime import datetime, timedelta
from flask import Flask, render_template_string, request, jsonify, send_file
from io import BytesIO
import zipfile

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
DATA_DIR=os.path.join(BASE_DIR,'data_v1_pro')
os.makedirs(DATA_DIR, exist_ok=True)
for f in ['usuarios.json','modulos_usuario.json','casos.json']:
    p=os.path.join(DATA_DIR,f)
    if not os.path.exists(p):
        with open(p,'w',encoding='utf-8') as fh: json.dump([],fh)

def load(f):
    try:
        with open(os.path.join(DATA_DIR,f),'r',encoding='utf-8') as fh: return json.load(fh)
    except: return []
def save(f,d):
    with open(os.path.join(DATA_DIR,f),'w',encoding='utf-8') as fh: json.dump(d,fh,indent=2,ensure_ascii=False)
def sha(s): return hashlib.sha256(s.encode()).hexdigest()

# GRUPOS PROFESIONALES - AGRUPAR MODULOS PARA USUARIO MAS IDENTIFICADO
GRUPOS={
    "GRUPO 1 - COMPRAS Y CONTRATOS": ["M1","M2"],
    "GRUPO 2 - FINANCIERO Y CONTABLE": ["M3","M4","M5","M6","M7"],
    "GRUPO 3 - FORENSE Y LEGAL": ["M8","M9","M12"],
    "GRUPO 4 - GESTION Y DOCUMENTAL": ["M10","M11"],
    "GRUPO 5 - ENTERPRISE WORLD": ["M13"]
}

MODULOS_PRO={
    "M1":{"nombre":"Scraper 10 Años Compras Públicas","desc":"Auditoría 10 años licitaciones ComprasRD + SAM.gov USA + SECOP CO + CompraNet MX","precio":250,"ley":"Ley 340-06 Art8-30","rol_demo":"Demo IA ejemplo licitación SENASE RD$867M transcripción textual","rol_prueba":"Prueba con datos reales cliente desde link/carpeta","rol_full":"Full permanente tiempo comprado - Scraper real API + reportes + export"},
    "M2":{"nombre":"Contratos + Adendas Tope 50%","desc":"Valida 4 adendas tope 50% Ley 340-06 Art31 Dec 543-12 Art127","precio":250,"ley":"Ley 340-06 Art31 50%","rol_demo":"Demo IA ejemplo contrato RD$867M + 4 adendas = RD$956M exceso RD$89M","rol_prueba":"Prueba con contrato real cliente valida tope 50%","rol_full":"Full permanente - Validador real contratos + OCR + CGR + informe"},
    "M3":{"nombre":"Nómina Pública/Privada TSS","desc":"TSS/DGII/RPE + ISR + Código Trabajo + IMSS MX + PILA CO","precio":250,"ley":"Ley 87-01 TSS","rol_demo":"Demo IA ejemplo nómina 50 empleados TSS validada","rol_prueba":"Prueba nómina real cliente valida TSS/DGII/RPE","rol_full":"Full permanente - Validador nómina multi-país"},
    "M4":{"nombre":"Pagos + Libramientos + BHD 08694150021","desc":"SIGEF + Legajos EDEESTE + BHD Transfer 08694150021 + NOBACI 3.62","precio":250,"ley":"NOBACI 3.62 + SIGEF","rol_demo":"Demo IA ejemplo 3 libramientos RD$481M sin soportes","rol_prueba":"Prueba legajos reales cliente valida SIGEF + BHD","rol_full":"Full permanente - Validador pagos + libramientos + BHD API"},
    "M5":{"nombre":"Presupuesto + Ejecución SIGEF","desc":"Presupuesto público + ejecución + disponibilidad","precio":250,"ley":"Presupuesto público","rol_demo":"Demo IA ejemplo presupuesto RD$100M ejecución 80%","rol_prueba":"Prueba presupuesto real cliente","rol_full":"Full permanente - Control presupuesto + ejecución real"},
    "M6":{"nombre":"Contabilidad IPSAS/IFRS/NIIF","desc":"IPSAS 1-47 + IFRS + US GAAP + Balance + Resultados","precio":250,"ley":"IPSAS + IFRS","rol_demo":"Demo IA ejemplo Balance + Resultados IPSAS","rol_prueba":"Prueba contabilidad real cliente","rol_full":"Full permanente - Contabilidad IPSAS/IFRS real"},
    "M7":{"nombre":"Activos Fijos + Inventarios QR","desc":"Inventario + QR + RFID + depreciación + custodia","precio":250,"ley":"NOBACI activos","rol_demo":"Demo IA ejemplo 100 activos QR depreciación","rol_prueba":"Prueba inventario real cliente QR","rol_full":"Full permanente - QR + RFID + custodia"},
    "M8":{"nombre":"Forense Full IA + PEPCA + SHA-256 RD$1,489M","desc":"Perjuicio RD$1,489M + Const Art146,169 + CP 123,124,175 + Ley 10-04 Art49 + FCPA + SOX","precio":250,"ley":"Const Art146 + Ley 10-04 + FCPA","rol_demo":"Demo IA ejemplo forense RD$1,489M H_CCRD_3.1 RD$867M + 3.5 RD$89M + 3.6 RD$481M + 3.8 RD$52M SHA-256","rol_prueba":"Prueba datos reales cliente forense + dictamen","rol_full":"Full permanente - Forense real + SHA-256 cadena custodia + dictamen PEPCA + informe robusto"},
    "M9":{"nombre":"NOBACI 16 Normas + COSO","desc":"NOBACI 1-16 + COSO + COBIT + riesgos","precio":250,"ley":"NOBACI 1-16 + COSO","rol_demo":"Demo IA ejemplo NOBACI 16 normas evaluación","rol_prueba":"Prueba control interno real cliente","rol_full":"Full permanente - Validador NOBACI/COSO real"},
    "M10":{"nombre":"Gestión Informes + Réplicas + Historial Confidencial","desc":"Carga múltiple + réplicas + historial fecha/hora/hash + modo confidencial borra rastro + GDPR","precio":250,"ley":"GDPR + Confidencial","rol_demo":"Demo IA ejemplo informe preliminar + réplica","rol_prueba":"Prueba informes reales cliente + réplicas","rol_full":"Full permanente - Gestión informes + historial confidencial"},
    "M11":{"nombre":"Documental OCR + Firma Digital Ley 126-02","desc":"OCR IA + hash + firma digital 126-02 + eIDAS ES + ESIGN USA","precio":250,"ley":"Ley 126-02 + eIDAS + ESIGN","rol_demo":"Demo IA ejemplo OCR 10 páginas + firma digital","rol_prueba":"Prueba OCR real cliente + firma","rol_full":"Full permanente - OCR real Tesseract + Gemini + firma digital"},
    "M12":{"nombre":"B4 Informe Pericial IA Generativo","desc":"Informe pericial auto + matriz + dictamen final + peritaje","precio":250,"ley":"Pericial + Matriz","rol_demo":"Demo IA ejemplo informe pericial RD$1,489M matriz","rol_prueba":"Prueba peritaje real cliente","rol_full":"Full permanente - Generador informe pericial IA auto"},
    "M13":{"nombre":"WORLD ENTERPRISE Multi-País/Idioma/Moneda","desc":"DO US MX PA CO ES BR + ES EN FR PT + USD DOP EUR MXN + BHD 08694150021 USD y DOP + cumplimiento mundial","precio":250,"ley":"Multi-país/idioma/moneda + BHD 08694150021","rol_demo":"Demo IA ejemplo multi-país DO US MX + multi-idioma ES EN + multi-moneda USD DOP","rol_prueba":"Prueba multi-país real cliente","rol_full":"Full permanente - WORLD ENTERPRISE multi-país/idioma/moneda + BHD 08694150021"},
}

EJEMPLO_IA={
    "M1":{"fuente":"https://comprasdominicana.gob.do/licitaciones SENASE 2019-2025 - IA Gemini buscó real","datos":"SENASE-CCC-CP-2019-0001 RD$867,282,729 - 120 páginas pliego transcripción textual precisa - Hash a1b2c3","monto":867282729},
    "M2":{"fuente":"Contrato SENASE-2019-001 + 4 Adendas - IA Mistral extrajo real","datos":"Contrato base RD$867,282,729 + 4 adendas RD$89,328,477 = Total RD$956,611,206 - Tope 50% RD$433M - Exceso RD$89,328,477 - Ley 340-06 Art31","monto":956611206},
    "M4":{"fuente":"Legajos pagos EDEESTE SIGEF + BHD 08694150021 - IA Gemini + BHD API","datos":"3 libramientos RD$481M sin soportes - BHD Transfer 08694150021 validado - NOBACI 3.62","monto":481000000},
    "M8":{"fuente":"Informe forense PEPCA + CGR - IA YOELFRI V15 - Perjuicio RD$1,489M","datos":"H_CCRD_3.1 RD$867M + H_CCRD_3.5 RD$89M + H_CCRD_3.6 RD$481M + H_CCRD_3.8 RD$52M = RD$1,489M - SHA-256 d4e5f6 - PEPCA Const Art146","monto":1489611206},
}

app=Flask(__name__)
app.secret_key='V1_PRO_SINGLE_BTN_'+sha(str(datetime.now()))

HTML_PRO="""
<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BASA V1 Profesional - Single Button Comprar + Agrupado Profesional</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
/* DISEÑO PROFESIONAL SIN CARNAVAL - COLORES SOBRIOS */
body{background:#f8fafc;color:#1e293b;font-family:'Segoe UI',system-ui;font-size:13px}
.hero{background:#ffffff;border-bottom:1px solid #e2e8f0;padding:16px 20px}
.hero h5{color:#0f172a;font-weight:700;letter-spacing:-0.3px}
.card-pro{background:#ffffff;border:1px solid #e2e8f0;border-radius:10px;box-shadow:0 1px 3px rgba(0,0,0,0.05)}
.btn-primary-pro{background:#0f172a;color:#fff;border:none;padding:8px 16px;border-radius:8px;font-weight:600;font-size:12px;cursor:pointer}
.btn-primary-pro:hover{background:#1e293b}
.btn-secondary-pro{background:#f1f5f9;color:#334155;border:1px solid #e2e8f0;padding:7px 14px;border-radius:8px;font-weight:500;font-size:11px;cursor:pointer}
.btn-success-pro{background:#059669;color:#fff;border:none;padding:7px 14px;border-radius:8px;font-weight:600;font-size:11px;cursor:pointer}
.btn-warning-pro{background:#f59e0b;color:#000;border:none;padding:7px 14px;border-radius:8px;font-weight:600;font-size:11px;cursor:pointer}
.grupo-header{background:#f8fafc;border-bottom:1px solid #e2e8f0;padding:10px 14px;font-weight:700;color:#0f172a;font-size:12px;text-transform:uppercase;letter-spacing:0.5px}
.modulo-item{padding:12px 14px;border-bottom:1px solid #f1f5f9;display:flex;justify-content:space-between;align-items:center}
.modulo-item:last-child{border-bottom:none}
.modulo-item:hover{background:#f8fafc}
.badge-demo{background:#fef3c7;color:#92400e;padding:3px 8px;border-radius:12px;font-size:10px;font-weight:600}
.badge-activo{background:#d1fae5;color:#065f46;padding:3px 8px;border-radius:12px;font-size:10px;font-weight:600}
.badge-vencido{background:#fee2e2;color:#991b1b;padding:3px 8px;border-radius:12px;font-size:10px;font-weight:600}
.badge-nuevo{background:#e0e7ff;color:#3730a3;padding:3px 8px;border-radius:12px;font-size:10px;font-weight:600}
input,select,textarea{background:#ffffff!important;color:#1e293b!important;border:1px solid #cbd5e1!important;border-radius:8px!important;font-size:12px}
.ejec-pro{background:#ffffff;border:1px solid #e2e8f0;border-radius:10px;padding:14px;margin-top:10px}
.modal-pro{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(15,23,42,0.6);display:none;justify-content:center;align-items:center;z-index:9999}
.modal-content-pro{background:#ffffff;border-radius:12px;width:90%;max-width:900px;max-height:90vh;overflow:auto;box-shadow:0 20px 60px rgba(0,0,0,0.2)}
</style></head><body>

<div class="hero">
<div class="d-flex justify-content-between align-items-center">
<div>
<h5 class="m-0">BASA V1 • Sistema de Auditoría Forense Profesional</h5>
<small style="color:#64748b">13 módulos • Demo 7 días • Pagado full permanente • Multi-país DO US MX PA CO ES BR • Multi-idioma ES EN FR PT • Multi-moneda USD DOP EUR MXN • BHD 08694150021 • <span id="info"></span></small>
</div>
<div class="d-flex gap-2">
<button onclick="abrirModalComprar()" class="btn-primary-pro">🛒 Comprar Módulos</button>
<span id="userLabel" class="badge bg-light text-dark" style="border:1px solid #e2e8f0;padding:6px 10px;border-radius:8px"></span>
</div>
</div>
</div>

<div class="container-fluid p-3">

<div id="loginBox" class="card-pro p-3 mb-3">
<h6 style="font-weight:700;color:#0f172a">Acceso al Sistema</h6>
<div class="row g-2">
<div class="col-md-2"><input id="nombre" class="form-control form-control-sm" placeholder="Nombre completo"></div>
<div class="col-md-2"><input id="correo" type="email" class="form-control form-control-sm" placeholder="Correo"></div>
<div class="col-md-2"><input id="clave" type="password" class="form-control form-control-sm" placeholder="Clave"></div>
<div class="col-md-2"><input id="empresa" class="form-control form-control-sm" placeholder="Empresa"></div>
<div class="col-md-2"><select id="tipoAcceso" class="form-select form-select-sm"><option value="demo">Demo 7 días</option><option value="real">Real</option></select></div>
<div class="col-md-2"><button onclick="entrar()" class="btn-primary-pro w-100">Entrar</button></div>
</div>
<div class="mt-2"><button onclick="autocompleteDemo()" class="btn-secondary-pro">Autocompletar demo</button> <small style="color:#64748b">Demo ejemplo modelo vs real llena datos • Histórico clave seguro solo admin</small></div>
</div>

<div id="sistemaBox" style="display:none">

<div class="card-pro p-2 mb-3 d-flex justify-content-between">
<div class="d-flex gap-2">
<button onclick="showTab('modulos')" class="btn-secondary-pro">📊 Módulos Agrupados</button>
<button onclick="showTab('ejecucion')" class="btn-secondary-pro">⚙️ Ejecución Real</button>
<button onclick="showTab('forense')" class="btn-secondary-pro">📋 Informe Forense</button>
</div>
<div class="d-flex gap-2">
<button onclick="abrirModalComprar()" class="btn-primary-pro">🛒 Comprar Módulos - Único Botón</button>
</div>
</div>

<div id="tab-modulos">
<!-- GRUPOS PROFESIONALES - USUARIO MAS IDENTIFICADO -->
<div id="gruposContainer"></div>

<div class="card-pro p-3 mt-3">
<h6 style="font-weight:700;color:#0f172a">Ejecución Real por Rol: Demo IA Ejemplo / Prueba Datos Cliente / Full Permanente Tiempo Comprado</h6>
<div class="row g-2 mt-2">
<div class="col-md-3"><input id="fuente" class="form-control form-control-sm" placeholder="Link https:// o carpeta datos reales cliente"></div>
<div class="col-md-2"><select id="modSelect" class="form-select form-select-sm"></select></div>
<div class="col-md-7">
<button onclick="cargarReal()" class="btn-primary-pro">📥 Cargar Real</button>
<button onclick="editarReal()" class="btn-secondary-pro">✏️ Editar</button>
<button onclick="mejorarIA()" class="btn-warning-pro">🤖 Mejorar con IA</button>
<button onclick="dejarTextual()" class="btn-secondary-pro">📝 Dejar Textual</button>
<button onclick="auditarTodo()" class="btn-secondary-pro">🔍 Auditar Todo</button>
<button onclick="generarCodigo()" class="btn-success-pro">💻 Generar Código Actualizar</button>
</div>
</div>
<textarea id="textoTrans" class="form-control form-control-sm mt-2" rows="3" placeholder="Transcripción textual precisa real - Puede editar - Rol Demo IA ejemplo / Prueba datos reales cliente / Full permanente"></textarea>
<div class="row g-2 mt-2">
<div class="col-md-6"><button onclick="utilizarIA()" class="btn-warning-pro w-100">🤖 Utilizar IA Si Usuario Quiere Mejorar Contenido</button></div>
<div class="col-md-6"><button onclick="dejarComoEncontro()" class="btn-secondary-pro w-100">📝 Dejar Textualmente Como Lo Encontró</button></div>
</div>
<div id="ejecReal" class="ejec-pro mt-3" style="display:none"></div>
</div>
</div>

<div id="tab-ejecucion" style="display:none"><div class="card-pro p-3"><div id="ejecReal2"></div></div></div>
<div id="tab-forense" style="display:none"><div class="card-pro p-3"><h6 style="font-weight:700">Informe Forense Robusto - Ley + Fuente + Datos Reales + Análisis Claro y Preciso</h6><div id="informeForense" class="small p-3 rounded" style="background:#f8fafc;border:1px solid #e2e8f0"></div><div class="d-flex gap-2 mt-3"><button onclick="generarForense()" class="btn-primary-pro">📋 Generar Informe Forense Robusto</button><button onclick="exportWord()" class="btn-secondary-pro">📄 Export Word</button><button onclick="exportExcel()" class="btn-secondary-pro">📊 Export Excel</button><button onclick="unificarCorte()" class="btn-warning-pro">🔄 Unificar Corte Factura</button></div></div></div>

</div>
</div>

<!-- MODAL ÚNICO - COMPRAR MÓDULOS - DESPLIEGUE TODOS MÓDULOS SELECCIONAR/QUITAR PROBAR/COMPRAR - NO SE VE SIEMPRE EN PORTADA -->
<div id="modalComprar" class="modal-pro">
<div class="modal-content-pro">
<div class="d-flex justify-content-between align-items-center p-3" style="border-bottom:1px solid #e2e8f0">
<h6 style="font-weight:700" class="m-0">🛒 Comprar Módulos - Seleccionar o Quitar Si Deseas Probar y Si Deseas Comprarlo</h6>
<button onclick="cerrarModalComprar()" class="btn-secondary-pro">✕ Cerrar</button>
</div>
<div class="p-3">
<small style="color:#64748b">Selecciona módulos para probar demo 7 días o comprar full permanente por tiempo comprado. Demo: IA ejemplo. Prueba: datos reales cliente. Full: permanente tiempo comprado. Agrupados profesional para usuario más identificado. Quitar tanto colores - diseño profesional.</small>
<div id="modalModulos" class="mt-3"></div>
<div class="card-pro p-3 mt-3" style="background:#f8fafc">
<div class="row g-2">
<div class="col-md-4"><div id="resumenSeleccion" class="small"></div></div>
<div class="col-md-4"><div id="fechasSeleccion" class="small"></div></div>
<div class="col-md-4">
<button onclick="probarSeleccionados()" class="btn-warning-pro w-100">🧪 Probar Seleccionados Demo 7D</button>
<button onclick="comprarSeleccionados()" class="btn-primary-pro w-100 mt-2">💳 Comprar Seleccionados Full Permanente - BHD 08694150021</button>
<button onclick="unificarSeleccionados()" class="btn-secondary-pro w-100 mt-2">🔄 Unificar con Próximo Corte Factura + Días Consumibles</button>
</div>
</div>
</div>
</div>
</div>
</div>

<script>
let MODS={{ mods|tojson }};
let GRUPOS={{ grupos|tojson }};
let EJEMPLO={{ ejemplo|tojson }};
let currentUser=JSON.parse(localStorage.getItem('v1pro_user')||'null');
let modulosUsuario=JSON.parse(localStorage.getItem('v1pro_modulos')||'{}');
let seleccionados={}; // {M1:true, M2:false} para modal comprar

function init(){
 document.getElementById('info').innerText=new Date().toLocaleString();
 if(currentUser){document.getElementById('loginBox').style.display='none'; document.getElementById('sistemaBox').style.display='block'; document.getElementById('userLabel').innerText=currentUser.nombre+' • '+currentUser.rol;}
 renderGrupos(); renderModalComprar();
}
function autocompleteDemo(){
 document.getElementById('nombre').value='Lic. Pedro Baldera';
 document.getElementById('correo').value='demo@basa-demo.com';
 document.getElementById('clave').value='DemoV1*';
 document.getElementById('empresa').value='BASA Empresa';
}
function entrar(){
 let nombre=document.getElementById('nombre').value, correo=document.getElementById('correo').value, clave=document.getElementById('clave').value, empresa=document.getElementById('empresa').value, tipo=document.getElementById('tipoAcceso').value;
 if(!nombre||!correo||!clave||!empresa){alert('Complete Nombre/Correo/Clave/Empresa');return;}
 fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({nombre:nombre,correo:correo,clave:clave,empresa:empresa,tipo:tipo})}).then(r=>r.json()).then(d=>{
  currentUser=d.usuario; localStorage.setItem('v1pro_user',JSON.stringify(currentUser));
  modulosUsuario=d.modulos||{}; localStorage.setItem('v1pro_modulos',JSON.stringify(modulosUsuario));
  document.getElementById('loginBox').style.display='none'; document.getElementById('sistemaBox').style.display='block';
  document.getElementById('userLabel').innerText=currentUser.nombre+' • '+currentUser.rol;
  renderGrupos(); renderModalComprar();
 });
}
function showTab(t){
 document.getElementById('tab-modulos').style.display=t=='modulos'?'block':'none';
 document.getElementById('tab-ejecucion').style.display=t=='ejecucion'?'block':'none';
 document.getElementById('tab-forense').style.display=t=='forense'?'block':'none';
}

function renderGrupos(){
 let html='', sel=document.getElementById('modSelect'); sel.innerHTML=''; let hoy=new Date();
 Object.keys(GRUPOS).forEach(grupo=>{
  html+=`<div class="card-pro mb-3"><div class="grupo-header">${grupo}</div>`;
  GRUPOS[grupo].forEach(mid=>{
   let m=MODS[mid]; if(!m) return;
   let mu=modulosUsuario[mid]||{}; let ej=EJEMPLO[mid]||{datos:''};
   let o=document.createElement('option'); o.value=mid; o.text=mid+' '+m.nombre; sel.appendChild(o);
   let estado='', botones='';
   if(!mu.demo_inicio &&!mu.pagado_inicio){
    estado='<span class="badge-nuevo">Nuevo</span>';
    botones=`<button onclick="iniciarDemoReal('${mid}')" class="btn-secondary-pro">▶️ Demo 7D</button>
             <button onclick="abrirEjecutarReal('${mid}','demo')" class="btn-secondary-pro">Ejecutar Demo IA Ejemplo</button>`;
   } else if(mu.demo_inicio &&!mu.pagado_inicio){
    let demoFin=new Date(mu.demo_fin); let activo=hoy<=demoFin; let diasRest=Math.ceil((demoFin-hoy)/86400000);
    if(activo){
     estado=`<span class="badge-demo">Demo activo ${diasRest}d • Vigente ${mu.demo_inicio} • Venc ${mu.demo_fin}</span>`;
     botones=`<button onclick="abrirEjecutarReal('${mid}','demo')" class="btn-warning-pro">▶️ Ejecutar Demo IA Ejemplo Real</button>
              <button onclick="cargarDatosReales('${mid}')" class="btn-secondary-pro">📥 Datos Reales Cliente</button>
              <button onclick="editarMejorar('${mid}')" class="btn-secondary-pro">✏️ Editar/Mejorar IA</button>`;
    } else {
     estado=`<span class="badge-vencido">Demo vencido ${mu.demo_fin}</span>`;
     botones=`<button onclick="pagarModuloReal('${mid}')" class="btn-primary-pro">💳 Comprar Full</button>`;
    }
   } else if(mu.pagado_inicio){
    let pagadoFin=new Date(mu.pagado_fin); let activo=hoy<=pagadoFin; let diasRest=Math.ceil((pagadoFin-hoy)/86400000);
    if(activo){
     estado=`<span class="badge-activo">Full activo ${diasRest}d • Vigente ${mu.vigente} • Renovada ${mu.renovada||'Primera'} • Venc ${mu.pagado_fin}</span>`;
     botones=`<button onclick="abrirEjecutarReal('${mid}','pagado')" class="btn-success-pro">▶️ Ejecutar Full Permanente ${mu.pagado_fin}</button>
              <button onclick="cargarDatosReales('${mid}')" class="btn-primary-pro">📥 Datos Reales Cliente Full</button>
              <button onclick="generarInformeForenseModulo('${mid}')" class="btn-secondary-pro">📋 Informe Forense</button>
              <button onclick="renovarReal('${mid}')" class="btn-secondary-pro">🔄 Renovar desde fin ${mu.pagado_fin}</button>`;
    } else {
     estado=`<span class="badge-vencido">Full vencido ${mu.pagado_fin} • Vigente ${mu.vigente} • Renovada ${mu.renovada||''}</span>`;
     botones=`<button onclick="renovarReal('${mid}')" class="btn-primary-pro">🔄 Renovar desde fin primera compra ${mu.pagado_fin}</button>`;
    }
   }
   html+=`<div class="modulo-item">
   <div style="flex:1"><div style="font-weight:600;color:#0f172a">${mid} ${m.nombre} ${estado}</div><small style="color:#64748b">${m.desc} • ${m.ley} • ${m.precio} USD/mes • Demo: ${m.rol_demo.substring(0,60)}... • Prueba: ${m.rol_prueba.substring(0,40)}... • Full: ${m.rol_full.substring(0,40)}...</small></div>
   <div class="d-flex gap-1 flex-wrap" style="margin-left:10px">${botones}</div>
   </div>`;
  });
  html+=`</div>`;
 });
 document.getElementById('gruposContainer').innerHTML=html;
}

function renderModalComprar(){
 let html=''; let total=0;
 Object.keys(GRUPOS).forEach(grupo=>{
  html+=`<div class="card-pro mb-2"><div class="grupo-header">${grupo}</div>`;
  GRUPOS[grupo].forEach(mid=>{
   let m=MODS[mid]; if(!m) return;
   let mu=modulosUsuario[mid]||{}; let checked=seleccionados[mid]?'checked':'';
   let estadoDemo=mu.demo_inicio?`Demo hasta ${mu.demo_fin}`:'No demo';
   let estadoFull=mu.pagado_inicio?`Full hasta ${mu.pagado_fin} Vigente ${mu.vigente} Renovada ${mu.renovada||'Primera'}`:'No pagado';
   html+=`<div class="modulo-item">
   <div><input type="checkbox" id="chk_${mid}" ${checked} onchange="toggleSeleccion('${mid}')" style="margin-right:8px"><b>${mid} ${m.nombre}</b> - USD${m.precio}/mes<br><small style="color:#64748b">${m.desc}<br>Demo: ${estadoDemo} | Full: ${estadoFull} | Ley: ${m.ley}</small></div>
   <div class="d-flex flex-column gap-1"><button onclick="toggleSeleccion('${mid}')" class="btn-secondary-pro">Seleccionar/Quitar</button><button onclick="probarUno('${mid}')" class="btn-warning-pro">Probar Demo</button><button onclick="comprarUno('${mid}')" class="btn-primary-pro">Comprar Full</button></div>
   </div>`;
   if(seleccionados[mid]) total+=m.precio;
  });
  html+=`</div>`;
 });
 document.getElementById('modalModulos').innerHTML=html;
 document.getElementById('resumenSeleccion').innerHTML=`Seleccionados: ${Object.keys(seleccionados).filter(k=>seleccionados[k]).length} módulos<br>Total: USD${total}/mes<br>ITBIS 18%: USD${(total*0.18).toFixed(0)}<br>Total con ITBIS: USD${(total*1.18).toFixed(0)}<br>Primer pago 27 días: USD${(total*1.18*0.9).toFixed(0)}<br>BHD 08694150021 USD y DOP`;
 let fechasHtml=''; Object.keys(modulosUsuario).forEach(id=>{let mu=modulosUsuario[id]; if(mu.pagado_fin) fechasHtml+=`${id}: Vigente ${mu.vigente} | Renovada ${mu.renovada||'Primera'} | Vencimiento ${mu.pagado_fin}<br>`;});
 document.getElementById('fechasSeleccion').innerHTML=fechasHtml
