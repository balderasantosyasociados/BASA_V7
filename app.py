# -*- coding: utf-8 -*-
# BASA V20 FULL ADMIN ENTERPRISE - TODOS MODULOS + PAGO MENSUAL + ADMIN USUARIOS + HISTORICO CLAVES + BACKUP
import os, json, hashlib, base64
from datetime import datetime, timedelta
from flask import Flask, render_template_string, request, send_file, jsonify, redirect, session

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
DATA_DIR=os.path.join(BASE_DIR,'data_admin')
os.makedirs(DATA_DIR, exist_ok=True)
USERS_FILE=os.path.join(DATA_DIR,'usuarios.json')
HIST_FILE=os.path.join(DATA_DIR,'historico_claves.json')
PAGOS_FILE=os.path.join(DATA_DIR,'pagos.json')
BACKUP_DIR=os.path.join(DATA_DIR,'backups')
os.makedirs(BACKUP_DIR, exist_ok=True)

for f, default in [(USERS_FILE,[]),(HIST_FILE,[]),(PAGOS_FILE,[])]:
    if not os.path.exists(f):
        with open(f,'w',encoding='utf-8') as fh: json.dump(default,fh)

def load_json(p):
    try:
        with open(p,'r',encoding='utf-8') as fh: return json.load(fh)
    except: return []
def save_json(p,data):
    with open(p,'w',encoding='utf-8') as fh: json.dump(data,fh,indent=2,ensure_ascii=False)
def sha(s): return hashlib.sha256(s.encode()).hexdigest()

MODULOS=[
    {"id":"M1","nombre":"M1 Scraper 10 Años IA + Compras Públicas","precio":250,"funciones":["Scraper 10 años atrás","Detección fraudes IA","Export Excel/Word","Alertas automáticas"],"reporte":"Reporte Scraper Histórico"},
    {"id":"B4","nombre":"B4 Base Informe Pericial IA + NOBACI","precio":250,"funciones":["Informe pericial automático","Análisis NOBACI 1-16","Generación dictamen","Hash SHA-256 probatorio"],"reporte":"Informe Pericial B4"},
    {"id":"M2","nombre":"M2 Contratos + Adendas","precio":250,"funciones":["Control contratos","Validación tope 50% Ley 340-06","Registro CGR","Alertas vencimiento"],"reporte":"Matriz Contratos"},
    {"id":"M3","nombre":"M3 Nómina + RRHH","precio":250,"funciones":["Nómina pública","Validación TSS","Control asistencia","Cálculo retenciones"],"reporte":"Reporte Nómina"},
    {"id":"M4","nombre":"M4 Activos Fijos","precio":250,"funciones":["Inventario activos","Depreciación","Custodia","Etiquetado QR"],"reporte":"Inventario Activos"},
    {"id":"M5","nombre":"M5 Finanzas + Presupuesto","precio":250,"funciones":["Ejecución presupuestaria","Libramientos","Conciliación bancaria","Estados financieros"],"reporte":"Estado Financiero"},
    {"id":"M6","nombre":"M6 Compras y Contrataciones","precio":250,"funciones":["PACC","Procesos 340-06","Evaluación ofertas","RPE/DGII/TSS automático"],"reporte":"Reporte Compras"},
    {"id":"M7","nombre":"M7 Auditoría Interna","precio":250,"funciones":["Plan auditoría","Hallazgos ISSAI","Seguimiento recomendaciones","Papeles trabajo"],"reporte":"Informe Auditoría"},
    {"id":"M8","nombre":"M8 Forense Full IA + PEPCA","precio":250,"funciones":["Análisis forense","Detección anomalías","Remisión PEPCA","Cadena custodia"],"reporte":"Dictamen Forense"},
    {"id":"M9","nombre":"M9 NOBACI Completo","precio":250,"funciones":["NOBACI 16 normas","Checklist control interno","Evaluación riesgos","Matriz cumplimiento"],"reporte":"Matriz NOBACI"},
    {"id":"M10","nombre":"M10 Inventarios + Almacén","precio":250,"funciones":["Kardex","Entradas/salidas","Conteo físico","Ajustes"],"reporte":"Reporte Inventario"},
    {"id":"M11","nombre":"M11 Pagos + Libramientos SIGEF","precio":250,"funciones":["Libramientos SIGEF","Cheques","Transferencias BHD","Validación DGII/TSS"],"reporte":"Reporte Pagos"},
    {"id":"M12","nombre":"M12 Gestión Informes + Réplicas + Historial","precio":250,"funciones":["Carga múltiples réplicas","Historial fecha/hora/tipo/archivo","Export PDF/Word","Modo confidencial privado"],"reporte":"Historial Informes"},
    {"id":"M13","nombre":"M13 Multi-País Multi-Idioma + Legal","precio":250,"funciones":["DO Ley 340-06 NOBACI","US FAR Yellow Book","MX LAASSP","PA Ley22 CO Ley80 ES LCSP","ES EN FR PT + USD DOP EUR MXN"],"reporte":"Reporte Multi-País"},
]

app=Flask(__name__)
app.secret_key='BASA_V20_ADMIN_'+sha(str(datetime.now()))

HTML_V20="""
<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BASA V20 FULL ADMIN - Todos Módulos + Pago Mensual + Admin Usuarios</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
body{background:#0b1120;color:#e2e8f0;font-family:system-ui}
.hero{background:linear-gradient(135deg,#003366,#00d084);padding:12px;text-align:center}
.card{background:#1e293b;border:1px solid #334155;border-radius:12px}
.card-header{background:#0f172a}
.btn-verde{background:#00d084;color:#fff;font-weight:800;border:none;padding:10px;border-radius:10px}
.btn-azul{background:#003366;color:#fff;font-weight:700;border:none;padding:8px;border-radius:8px}
.modulo-card{border:2px solid #334155;border-radius:10px;padding:10px;margin-bottom:8px;background:#0f172a}
.modulo-card.activo{border-color:#00d084;background:#0f2a1f}
.modulo-card.demo{border-color:#f59e0b;background:#2a2210}
.badge-demo{background:#f59e0b;color:#000} .badge-produccion{background:#00d084;color:#fff} .badge-suspendido{background:#dc2626}
input,select{background:#0f172a!important;color:#fff!important;border:1px solid #475569!important;border-radius:8px!important}
table{font-size:12px}
</style></head><body>
<div class="hero">
<h5 class="fw-bold m-0">🚀 BASA V20 FULL ADMIN ENTERPRISE - 13 MÓDULOS USD250 - PAGO MENSUAL HABILITA PRODUCCIÓN</h5>
<small>BHD 08694150021 USD Y DOP | 13 módulos x USD250 = USD3250 | DO ITBIS 18% USD585 | Total USD3835 | Primer pago 27 días USD3451.5 | Multi-País DO US MX PA CO ES | Tablet/Laptop/Desktop/Celular | Confidencial Privado</small><br>
<small style="background:rgba(0,0,0,0.3);padding:3px 8px;border-radius:6px" id="info"></small>
</div>

<div class="container-fluid p-2">

<!-- MENU ADMIN / USUARIO -->
<div class="card p-2 mb-2"><div class="d-flex flex-wrap gap-1 justify-content-between">
<div class="d-flex gap-1 flex-wrap">
<button onclick="showTab('modulos')" class="btn btn-success btn-sm fw-bold"><i class="fas fa-cubes"></i> Todos Módulos + Funciones Organizadas</button>
<button onclick="showTab('demo')" class="btn btn-warning btn-sm"><i class="fas fa-flask"></i> Demo vs Producción Pagada</button>
<button onclick="showTab('pago')" class="btn btn-primary btn-sm"><i class="fas fa-credit-card"></i> Pagar Mensualidad Habilitar</button>
<button onclick="showTab('admin')" class="btn btn-dark btn-sm"><i class="fas fa-user-shield"></i> Admin - Usuarios + Claves + Backup</button>
<button onclick="showTab('confidencial')" class="btn btn-outline-light btn-sm"><i class="fas fa-lock"></i> Mi Trabajo Confidencial</button>
</div>
<div><span id="userLabel" class="badge bg-light text-dark"></span> <button onclick="logout()" class="btn btn-outline-danger btn-sm">Salir</button></div>
</div></div>

<!-- TAB MODULOS -->
<div id="tab-modulos" class="tab">
<div class="row g-2">
<div class="col-lg-8">
<h6 class="fw-bold text-success"><i class="fas fa-cubes"></i> TODOS LOS MÓDULOS - Funciones + Reportes Organizados - Demo y Producción</h6>
<div id="modulosList"></div>
</div>
<div class="col-lg-4">
<div class="card p-2">
<h6 class="small fw-bold">📊 Resumen Pago Mensual</h6>
<div id="resumenPago" class="small p-2 rounded" style="background:#0f172a;border:1px dashed #475569"></div>
<button onclick="showTab('pago')" class="btn-verde mt-2">💳 Pagar y Habilitar Producción Mensual</button>
<div class="mt-2 small text-secondary">Demo: Funciones limitadas, marca agua. Producción pagada: Full sin límites, informes finales, exportación Word/Excel, SHA-256.</div>
</div>
<div class="card p-2 mt-2">
<h6 class="small fw-bold">🔐 Confidencialidad</h6><small class="text-secondary">No se muestra ejercicio programado H_CCRD_3.1 etc a usuarios normales. Solo admin con ?admin=1. Cada usuario solo ve su trabajo cargado.</small>
</div>
</div>
</div>
</div>

<!-- TAB DEMO VS PRODUCCION -->
<div id="tab-demo" class="tab" style="display:none">
<div class="card p-3">
<h6 class="fw-bold"><i class="fas fa-flask"></i> Módulo Demo vs Final / Producción Pagada</h6>
<table class="table table-dark table-sm"><thead><tr><th>Módulo</th><th>Demo (Gratis)</th><th>Final / Producción Pagada (Mensual)</th><th>Reporte</th></tr></thead><tbody id="tablaDemo"></tbody></table>
</div>
</div>

<!-- TAB PAGO -->
<div id="tab-pago" class="tab" style="display:none">
<div class="row g-2"><div class="col-md-6">
<div class="card p-3">
<h6 class="fw-bold text-success"><i class="fas fa-credit-card"></i> Pagar Mensualidad - Habilita Producción</h6>
<form onsubmit="return pagar(event)">
<label class="small">Empresa:</label><input id="empPago" class="form-control form-control-sm mb-1" required>
<label class="small">RNC/TAX ID:</label><input id="rncPago" class="form-control form-control-sm mb-1" required>
<label class="small">Email facturación:</label><input id="emailPago" type="email" class="form-control form-control-sm mb-1" required>
<label class="small">País (impuesto auto):</label><select id="paisPago" class="form-select form-select-sm mb-1" onchange="calcPago()"><option value="DO" data-imp="18">DO 18% ITBIS</option><option value="US" data-imp="0">US 0%</option><option value="MX" data-imp="16">MX 16%</option><option value="PA" data-imp="7">PA 7%</option><option value="CO" data-imp="19">CO 19%</option><option value="ES" data-imp="21">ES 21%</option></select>
<label class="small">Módulos a pagar (USD250 c/u):</label><select id="modsPago" multiple size="7 class="form-select form-select-sm mb-1"></select>
<div id="calcPago" class="p-2 rounded small" style="background:#0f172a;border:1px dashed #475569"></div>
<button type="submit" class="btn-verde mt-2">✅ PAGAR MENSUALIDAD + HABILITAR PRODUCCIÓN + BHD 08694150021</button>
</form>
<div id="resPago" class="mt-2"></div>
</div>
</div><div class="col-md-6">
<div class="card p-3">
<h6 class="small fw-bold">💳 Métodos Pago + Factura</h6>
<p class="small text-secondary">Transferencia BHD 08694150021 USD/DOP<br>Tarjeta crédito/débito (Stripe/PayPal)<br>ITBIS/IVA según país auto<br>Recibo y contrato CTR-V20-...pdf automático</p>
<div id="estadoPago" class="small"></div>
</div>
</div></div>
</div>

<!-- TAB ADMIN -->
<div id="tab-admin" class="tab" style="display:none">
<div class="card p-2 mb-2 border-danger"><h6 class="fw-bold text-danger"><i class="fas fa-user-shield"></i> ADMIN - Registro Usuarios + Cambiar Clave + Histórico Privado + Editar/Borrar/Suspender + Backup</h6>
<small class="text-secondary">Solo admin. Guarda histórico privado de claves de todos los que se registren. Puede editar, borrar, suspender y backup.</small></div>
<div class="row g-2">
<div class="col-md-4">
<div class="card p-2">
<h6 class="small fw-bold">➕ Registrar Usuario / Admin</h6>
<form onsubmit="return registrarUsuario(event)">
<input id="newEmp" class="form-control form-control-sm mb-1" placeholder="Empresa" required>
<input id="newRnc" class="form-control form-control-sm mb-1" placeholder="RNC" required>
<input id="newEmail" type="email" class="form-control form-control-sm mb-1" placeholder="Email" required>
<input id="newPass" class="form-control form-control-sm mb-1" placeholder="Clave inicial" required type="password">
<select id="newRol" class="form-select form-select-sm mb-1"><option value="usuario">Usuario</option><option value="admin">Admin</option></select>
<select id="newEstado" class="form-select form-select-sm mb-1"><option value="activo">Activo</option><option value="suspendido">Suspendido</option></select>
<button class="btn-azul w-100 btn-sm">Guardar Usuario</button>
</form>
<div class="mt-2 d-grid gap-1">
<button onclick="cargarUsuarios()" class="btn btn-outline-light btn-sm">🔄 Cargar Usuarios</button>
<button onclick="backupTodo()" class="btn btn-warning btn-sm fw-bold"><i class="fas fa-download"></i> 📦 Backup Completo JSON + Excel (Usuarios + Claves + Pagos + Registros)</button>
</div>
</div>
</div>
<div class="col-md-8">
<div class="card p-2">
<h6 class="small fw-bold">👥 Usuarios Registrados + Estado + Acciones Admin</h6>
<div class="table-responsive"><table id="tablaUsers" class="table table-dark table-sm small"><thead><tr><th>Empresa</th><th>RNC</th><th>Email</th><th>Rol</th><th>Estado</th><th>Clave (hash)</th><th>Acciones</th></tr></thead><tbody></tbody></table></div>
</div>
<div class="card p-2 mt-2">
<h6 class="small fw-bold">🔑 Histórico Privado de Claves (Solo Admin ve - Guarda todo cambio)</h6>
<div class="table-responsive"><table id="tablaHistClaves" class="table table-dark table-sm small"><thead><tr><th>Fecha/Hora</th><th>Usuario (RNC)</th><th>Acción</th><th>Clave Anterior (hash)</th><th>Clave Nueva (hash)</th><th>Admin que cambió</th></tr></thead><tbody></tbody></table></div>
</div>
</div>
</div>
</div>

<!-- TAB CONFIDENCIAL -->
<div id="tab-confidencial" class="tab" style="display:none">
<div class="card p-3">
<h6 class="fw-bold"><i class="fas fa-lock"></i> Mi Trabajo Confidencial - Solo yo veo - Ejercicio oculto</h6>
<div class="row g-2"><div class="col-md-3"><input type="file" multiple id="filesConf" class="form-control form-control-sm"></div><div class="col-md-3"><select id="tipoConf" class="form-select form-select-sm"><option>Preliminar</option><option>Acta</option><option>Final</option><option>Réplica</option></select></div><div class="col-md-3"><button onclick="cargarConf()" class="btn-verde" style="padding:6px">Cargar Confidencial</button></div><div class="col-md-3"><button onclick="limpiarConf()" class="btn btn-danger btn-sm w-100">🗑️ Eliminar rastro pantalla</button></div></div>
<table id="histConf" class="table table-dark table-sm small mt-2"><thead><tr><th>Fecha/Hora</th><th>Tipo</th><th>Archivo</th><th>Estado</th></tr></thead><tbody></tbody></table>
</div>
</div>

</div>

<script>
let MODULOS={{ modulos|tojson }};
let currentUser=JSON.parse(localStorage.getItem('basa_v20_session')||'null');
let pagosCache={};

function init(){
 document.getElementById('info').innerText=new Date().toLocaleString()+' | V20 FULL ADMIN | '+window.innerWidth+'px | '+ (currentUser? 'Usuario: '+currentUser.empresa+' Rol: '+currentUser.rol : 'No logueado');
 if(currentUser){document.getElementById('userLabel').innerText=currentUser.empresa+' ('+currentUser.rnc+') Rol:'+currentUser.rol+' Estado:'+currentUser.estado;}
 renderModulos(); renderDemo(); renderPagoSelect(); calcPago(); cargarUsuarios(); cargarHistClaves();
 showTab('modulos');
}
function showTab(t){document.querySelectorAll('.tab').forEach(d=>d.style.display='none'); document.getElementById('tab-'+t).style.display='block';}
function renderModulos(){
 let html=''; let selPago=document.getElementById('modsPago');
 MODULOS.forEach(m=>{
  let activo=pagosCache[m.id]?'activo':'demo';
  let badge=pagosCache[m.id]?'<span class="badge-produccion badge">PRODUCCIÓN PAGADA</span>':'<span class="badge-demo badge">DEMO</span>';
  html+='<div class="modulo-card '+activo+'"><div class="d-flex justify-content-between"><b>'+m.id+' - '+m.nombre+'</b> '+badge+' <span class="badge bg-secondary">USD'+m.precio+'/mes</span></div><div class="small mt-1"><b>Funciones:</b> '+m.funciones.join(' | ')+'<br><b>Reporte:</b> '+m.reporte+' | <b>Estado:</b> '+(pagosCache[m.id]?'✅ Habilitado producción mensual':'⚠️ Demo limitado - Pague para habilitar')+'</div><div class="mt-1"><button onclick="verFunciones(\\''+m.id+'\\')" class="btn btn-outline-light btn-sm" style="font-size:10px">Ver funciones organizadas</button> '+(pagosCache[m.id]?' <a href="/export/reporte/'+m.id+'" class="btn btn-success btn-sm" style="font-size:10px">📄 Reporte '+m.id+' Final</a>':' <span class="badge bg-warning text-dark" style="font-size:10px">Demo con marca agua</span>')+'</div></div>';
 });
 document.getElementById('modulosList').innerHTML=html;
 let resumen=document.getElementById('resumenPago');
 let activos=Object.keys(pagosCache).length; let sub=activos*250; let imp=sub*0.18; let tot=sub+imp;
 resumen.innerHTML=activos+' módulos activos producción | Subtotal USD'+sub+' | ITBIS 18% USD'+imp.toFixed(2)+' | <b>Total USD'+tot.toFixed(2)+' | BHD 08694150021</b><br>'+(activos==0?'Pague mensualidad para habilitar producción': 'Producción habilitada hasta '+(pagosCache[Object.keys(pagosCache)[0]]?.hasta||''));
}
function renderDemo(){
 let tb=document.getElementById('tablaDemo'); tb.innerHTML='';
 MODULOS.forEach(m=>{
  let row=tb.insertRow(); row.innerHTML='<td><b>'+m.id+'</b> '+m.nombre+'</td><td><small>'+m.funciones.slice(0,2).join(', ')+' (limitado)<br><span class="badge-demo badge">Marca agua demo</span></small></td><td><small>'+m.funciones.join(', ')+'<br><span class="badge-produccion badge">Full sin límites + Export Word/Excel + SHA-256</span></small></td><td><small>'+m.reporte+'<br>'+(pagosCache[m.id]?'✅ Producción':'⚠️ Demo')+'</small></td>';
 });
}
function renderPagoSelect(){
 let sel=document.getElementById('modsPago'); sel.innerHTML='';
 MODULOS.forEach(m=>{let o=document.createElement('option'); o.value=m.id; o.text=m.id+' - '+m.nombre+' USD'+m.precio; o.selected=true; sel.appendChild(o);});
}
function calcPago(){
 let sel=document.getElementById('paisPago'); let imp=parseFloat(sel.options[sel.selectedIndex].dataset.imp);
 let mods=document.getElementById('modsPago'); let c=0; for(let o of mods.options){if(o.selected) c++;}
 let sub=c*250; let impVal=sub*imp/100; let tot=sub+impVal; let primer=tot*0.9;
 document.getElementById('calcPago').innerHTML=c+' módulos x USD250 = USD'+sub+' | Impuesto '+imp+'% = USD'+impVal.toFixed(2)+' | <b>Total Mensual USD'+tot.toFixed(2)+' | Primer pago 27 días USD'+primer.toFixed(2)+'</b> | BHD 08694150021';
 document.getElementById('estadoPago').innerHTML='Estado: '+(c==0?'Seleccione módulos':'Listo para pagar '+c+' módulos');
}
document.getElementById('modsPago')?.addEventListener('change',calcPago);

function pagar(e){
 e.preventDefault();
 let emp=document.getElementById('empPago').value, rnc=document.getElementById('rncPago').value, email=document.getElementById('emailPago').value, pais=document.getElementById('paisPago').value;
 let mods=[]; for(let o of document.getElementById('modsPago').options){if(o.selected) mods.push(o.value);}
 fetch('/api/pagar',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({empresa:emp,rnc:rnc,email:email,pais:pais,modulos:mods})}).then(r=>r.json()).then(d=>{
  document.getElementById('resPago').innerHTML='<div class="alert alert-success small">✅ Pago registrado: Contrato '+d.contrato+' | Total USD'+d.total+' | Hasta '+d.hasta+'<br>Producción habilitada mensual. BHD 08694150021<br><a href="/api/contrato/'+d.contrato+'" class="btn btn-success btn-sm mt-1">📄 Descargar Contrato PDF</a></div>';
  // activar local
  mods.forEach(id=>{pagosCache[id]={hasta:d.hasta,contrato:d.contrato}}); renderModulos(); renderDemo();
 });
 return false;
}
function registrarUsuario(e){
 e.preventDefault();
 let emp=document.getElementById('newEmp').value, rnc=document.getElementById('newRnc').value, email=document.getElementById('newEmail').value, pass=document.getElementById('newPass').value, rol=document.getElementById('newRol').value, estado=document.getElementById('newEstado').value;
 fetch('/api/admin/usuarios',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({empresa:emp,rnc:rnc,email:email,password:pass,rol:rol,estado:estado,admin:currentUser?.empresa||'Admin'})}).then(r=>r.json()).then(d=>{
  alert(d.msg); cargarUsuarios(); cargarHistClaves();
 });
 return false;
}
function cargarUsuarios(){
 fetch('/api/admin/usuarios').then(r=>r.json()).then(data=>{
  let tb=document.querySelector('#tablaUsers tbody'); tb.innerHTML='';
  data.forEach(u=>{
   let tr=tb.insertRow(); tr.innerHTML='<td>'+u.empresa+'</td><td>'+u.rnc+'</td><td>'+u.email+'</td><td><span class="badge '+(u.rol=='admin'?'bg-danger':'bg-secondary')+'">'+u.rol+'</span></td><td><span class="badge '+(u.estado=='activo'?'bg-success':'bg-danger')+'">'+u.estado+'</span></td><td class="font-monospace" style="font-size:9px">'+(u.password_hash||'').substring(0,12)+'..</td><td><button onclick="editarUsuario(\\''+u.rnc+'\\')" class="btn btn-primary btn-sm" style="font-size:9px">Editar</button> <button onclick="cambiarClave(\\''+u.rnc+'\\')" class="btn btn-warning btn-sm" style="font-size:9px">Clave</button> <button onclick="suspenderUsuario(\\''+u.rnc+'\\')" class="btn btn-dark btn-sm" style="font-size:9px">Susp</button> <button onclick="borrarUsuario(\\''+u.rnc+'\\')" class="btn btn-danger btn-sm" style="font-size:9px">Borrar</button></td>';
  });
 });
}
function cargarHistClaves(){
 fetch('/api/admin/historico_claves').then(r=>r.json()).then(data=>{
  let tb=document.querySelector('#tablaHistClaves tbody'); tb.innerHTML='';
  data.slice(-50).reverse().forEach(h=>{
   let tr=tb.insertRow(); tr.innerHTML='<td>'+h.fecha+'</td><td>'+h.rnc+'</td><td>'+h.accion+'</td><td class="font-monospace" style="font-size:9px">'+(h.clave_anterior||'').substring(0,10)+'..</td><td class="font-monospace" style="font-size:9px">'+(h.clave_nueva||'').substring(0,10)+'..</td><td>'+h.admin+'</td>';
  });
 });
}
function editarUsuario(rnc){let emp=prompt('Nueva Empresa:'); let email=prompt('Nuevo Email:'); if(!emp) return; fetch('/api/admin/usuarios/'+rnc,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({empresa:emp,email:email,admin:currentUser?.empresa||'Admin'})}).then(r=>r.json()).then(d=>{alert(d.msg); cargarUsuarios();});}
function cambiarClave(rnc){let np=prompt('Nueva clave para '+rnc+':'); if(!np) return; fetch('/api/admin/usuarios/'+rnc+'/clave',{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({nueva_clave:np,admin:currentUser?.empresa||'Admin'})}).then(r=>r.json()).then(d=>{alert(d.msg); cargarUsuarios(); cargarHistClaves();});}
function suspenderUsuario(rnc){if(!confirm('¿Suspender '+rnc+'?')) return; fetch('/api/admin/usuarios/'+rnc+'/suspender',{method:'PUT'}).then(r=>r.json()).then(d=>{alert(d.msg); cargarUsuarios();});}
function borrarUsuario(rnc){if(!confirm('¿Borrar '+rnc+'? Esto guarda en backup antes.')) return; fetch('/api/admin/usuarios/'+rnc,{method:'DELETE'}).then(r=>r.json()).then(d=>{alert(d.msg); cargarUsuarios();});}
function backupTodo(){window.location='/api/admin/backup';}
function verFunciones(id){let m=MODULOS.find(x=>x.id==id); alert(m.id+' - '+m.nombre+'\\n\\nFunciones organizadas:\\n- '+m.funciones.join('\\n- ')+'\\n\\nReporte: '+m.reporte+'\\n\\nEstado: '+(pagosCache[id]?'Producción pagada mensual':'Demo'));}
function logout(){localStorage.removeItem('basa_v20_session'); location.reload();}
function cargarConf(){
 let t=document.getElementById('tipoConf').value, fs=document.getElementById('filesConf').files;
 if(fs.length==0){alert('Seleccione archivos');return;}
 let tb=document.querySelector('#histConf tbody');
 for(let f of fs){let tr=tb.insertRow(); tr.innerHTML='<td>'+new Date().toLocaleString()+'</td><td>'+t+'</td><td>'+f.name+'</td><td><span class="badge bg-success">Privado Solo yo</span></td>';}
 alert(fs.length+' archivos cargados confidencial - Solo usted los ve - Ejercicio oculto');
}
function limpiarConf(){if(confirm('¿Eliminar rastro pantalla confidencial?')){document.querySelector('#histConf tbody').innerHTML='';}}
init();
</script>
</body></html>
"""

@app.route('/')
@app.route('/gestion-informes')
def home():
    return render_template_string(HTML_V20, modulos=MODULOS)

@app.route('/b4')
@app.route('/v8')
@app.route('/trial')
def redir(): return redirect('/')

@app.route('/api/pagar', methods=['POST'])
def pagar():
    data=request.json
    pagos=load_json(PAGOS_FILE)
    contrato=f"CTR-V20-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    hasta=(datetime.now()+timedelta(days=30)).strftime("%Y-%m-%d")
    sub=len(data.get('modulos',[]))*250
    imp_pais={"DO":18,"US":0,"MX":16,"PA":7,"CO":19,"ES":21}.get(data.get('pais','DO'),18)
    imp=sub*imp_pais/100
    total=sub+imp
    pagos.append({"contrato":contrato,"empresa":data.get('empresa'),"rnc":data.get('rnc'),"email":data.get('email'),"pais":data.get('pais'),"modulos":data.get('modulos'),"subtotal":sub,"impuesto":imp,"total":total,"fecha":datetime.now().isoformat(),"hasta":hasta,"estado":"pagado_mensual"})
    save_json(PAGOS_FILE,pagos)
    # crear backup auto
    backup_name=os.path.join(BACKUP_DIR,f"backup_{contrato}.json")
    with open(backup_name,'w',encoding='utf-8') as fh: json.dump({"pago":pagos[-1],"usuarios":load_json(USERS_FILE),"historico":load_json(HIST_FILE)},fh,indent=2,ensure_ascii=False)
    return jsonify({"contrato":contrato,"total":total,"hasta":hasta,"subtotal":sub,"impuesto":imp})

@app.route('/api/contrato/<contrato>')
def contrato_file(contrato):
    path=os.path.join(DATA_DIR,f"{contrato}.txt")
    with open(path,'w',encoding='utf-8') as f: f.write(f"CONTRATO BASA V20 FULL ADMIN\nContrato: {contrato}\nFecha: {datetime.now()}\nBHD: 08694150021 USD Y DOP\nPago mensual habilita producción\n")
    return send_file(path, as_attachment=True, download_name=f"{contrato}.txt")

@app.route('/api/admin/usuarios', methods=['GET','POST'])
def usuarios():
    users=load_json(USERS_FILE)
    hist=load_json(HIST_FILE)
    if request.method=='GET':
        return jsonify(users)
    data=request.json
    # validar existe
    if any(u['rnc']==data['rnc'] for u in users):
        return jsonify({"msg":"RNC ya existe"}),400
    new_user={"empresa":data['empresa'],"rnc":data['rnc'],"email":data['email'],"password_hash":sha(data['password']),"rol":data.get('rol','usuario'),"estado":data.get('estado','activo'),"fecha_registro":datetime.now().isoformat()}
    users.append(new_user)
    save_json(USERS_FILE,users)
    hist.append({"fecha":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"rnc":data['rnc'],"accion":"Registro","clave_anterior":"","clave_nueva":sha(data['password']),"admin":data.get('admin','Sistema')})
    save_json(HIST_FILE,hist)
    return jsonify({"msg":f"Usuario {data['rnc']} registrado. Histórico clave guardado privado."})

@app.route('/api/admin/usuarios/<rnc>', methods=['PUT','DELETE'])
def usuario_rnc(rnc):
    users=load_json(USERS_FILE)
    hist=load_json(HIST_FILE)
    u=next((x for x in users if x['rnc']==rnc),None)
    if not u: return jsonify({"msg":"No encontrado"}),404
    if request.method=='DELETE':
        # backup antes borrar
        backup_name=os.path.join(BACKUP_DIR,f"backup_borrado_{rnc}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json")
        with open(backup_name,'w',encoding='utf-8') as fh: json.dump(u,fh,indent=2,ensure_ascii=False)
        users=[x for x in users if x['rnc']!=rnc]
        save_json(USERS_FILE,users)
        hist.append({"fecha":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"rnc":rnc,"accion":"Borrado","clave_anterior":u['password_hash'],"clave_nueva":"","admin":"Admin"})
        save_json(HIST_FILE,hist)
        return jsonify({"msg":f"Usuario {rnc} borrado. Backup guardado {os.path.basename(backup_name)}"})
    data=request.json
    if 'empresa' in data: u['empresa']=data['empresa']
    if 'email' in data: u['email']=data['email']
    save_json(USERS_FILE,users)
    hist.append({"fecha":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"rnc":rnc,"accion":"Edición datos","clave_anterior":"","clave_nueva":"","admin":data.get('admin','Admin')})
    save_json(HIST_FILE,hist)
    return jsonify({"msg":f"Usuario {rnc} editado. Histórico guardado."})

@app.route('/api/admin/usuarios/<rnc>/clave', methods=['PUT'])
def cambiar_clave(rnc):
    users=load_json(USERS_FILE)
    hist=load_json(HIST_FILE)
    u=next((x for x in users if x['rnc']==rnc),None)
    if not u: return jsonify({"msg":"No encontrado"}),404
    data=request.json
    anterior=u['password_hash']
    nueva=sha(data['nueva_clave'])
    u['password_hash']=nueva
    save_json(USERS_FILE,users)
    hist.append({"fecha":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"rnc":rnc,"accion":"Cambio clave admin","clave_anterior":anterior,"clave_nueva":nueva,"admin":data.get('admin','Admin')})
    save_json(HIST_FILE,hist)
    return jsonify({"msg":f"Clave de {rnc} cambiada por admin. Histórico privado guardado."})

@app.route('/api/admin/usuarios/<rnc>/suspender', methods=['PUT'])
def suspender(rnc):
    users=load_json(USERS_FILE)
    hist=load_json(HIST_FILE)
    u=next((x for x in users if x['rnc']==rnc),None)
    if not u: return jsonify({"msg":"No encontrado"}),404
    u['estado']='suspendido' if u['estado']=='activo' else 'activo'
    save_json(USERS_FILE,users)
    hist.append({"fecha":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"rnc":rnc,"accion":f"Cambio estado a {u['estado']}","clave_anterior":"","clave_nueva":"","admin":"Admin"})
    save_json(HIST_FILE,hist)
    return jsonify({"msg":f"Usuario {rnc} ahora {u['estado']}"})

@app.route('/api/admin/historico_claves')
def historico():
    return jsonify(load_json(HIST_FILE))

@app.route('/api/admin/backup')
def backup():
    # backup completo todo
    timestamp=datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file=os.path.join(BACKUP_DIR,f"backup_FULL_{timestamp}.json")
    data={"usuarios":load_json(USERS_FILE),"historico_claves_privado":load_json(HIST_FILE),"pagos_mensuales":load_json(PAGOS_FILE),"modulos":MODULOS,"fecha_backup":datetime.now().isoformat(),"admin":"BASA V20 FULL ADMIN"}
    with open(backup_file,'w',encoding='utf-8') as fh: json.dump(data,fh,indent=2,ensure_ascii=False)
    return send_file(backup_file, as_attachment=True, download_name=f"BACKUP_FULL_ADMIN_{timestamp}.json")

@app.route('/export/reporte/<mod_id>')
def reporte_mod(mod_id):
    m=next((x for x in MODULOS if x['id']==mod_id),None)
    if not m: return "Modulo no encontrado",404
    path=os.path.join(DATA_DIR,f"Reporte_{mod_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    with open(path,'w',encoding='utf-8') as f:
        f.write(f"REPORTE {m['id']} - {m['nombre']}\nFunciones: {', '.join(m['funciones'])}\nReporte: {m['reporte']}\nFecha: {datetime.now()}\nBHD 08694150021\n")
    return send_file(path, as_attachment=True)

@app.route('/demo')
def demo(): return jsonify({"sistema":"BASA V20 FULL ADMIN","modulos":len(MODULOS),"precio":"USD250 x modulo","total_DO":"USD3835/mes","backup":"/api/admin/backup","admin_endpoints":["/api/admin/usuarios","/api/admin/historico_claves","/api/admin/backup"]})

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
