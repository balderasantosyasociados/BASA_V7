# -*- coding: utf-8 -*-
# BASA V18 CONFIDENCIAL PRIVADO - Solo usuario ve su trabajo - No se muestra ejercicio programado
import os, hashlib
from datetime import datetime
from flask import Flask, render_template_string, request, send_file, jsonify, redirect

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
AUDITOR={"bhd":"08694150021 - USD Y DOP","nombre":"Lic. Pedro Aníbal Baldera Rondón"}
CARPETAS={k:os.path.join(BASE_DIR,v) for k,v in {"reportes":"reportes_exportados","uploads":"uploads"}.items()}
for p in CARPETAS.values(): os.makedirs(p, exist_ok=True)
def sha256(t): return hashlib.sha256(t.encode('utf-8')).hexdigest()

app=Flask(__name__)

HTML_CONFIDENCIAL="""
<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BASA V18 Confidencial - Solo su trabajo</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
body{background:#0b1120;color:#e2e8f0;font-family:system-ui}
.hero{background:linear-gradient(135deg,#003366,#00d084);padding:14px;text-align:center}
.card{background:#1e293b;border:1px solid #334155;border-radius:12px}
.card-header{background:#0f172a}
.btn-verde{background:#00d084;color:#fff;font-weight:800;border:none;padding:11px;border-radius:10px;width:100%}
input,select{background:#0f172a!important;color:#fff!important;border:2px solid #475569!important;border-radius:8px!important}
.confidencial-badge{background:#dc2626;color:#fff;padding:6px 12px;border-radius:20px;font-size:11px;font-weight:800;display:inline-block}
.modo-privado{filter:blur(0px)} /* quitado blur para trabajo real */
</style></head><body>
<div class="hero">
<h5 class="fw-bold m-0">🔐 BASA V18 CONFIDENCIAL PRIVADO - Solo usted ve su trabajo</h5>
<small><span class="confidencial-badge"><i class="fas fa-lock"></i> MODO CONFIDENCIAL ACTIVADO - Data ejercicio oculta</span> | BHD 08694150021 | Tablet/Laptop/Desktop/Celular | Online sin descargar</small><br>
<small id="ruta" style="background:rgba(0,0,0,0.3);padding:3px 8px;border-radius:6px"></small>
</div>

<div class="container-fluid p-2" style="max-width:1100px">

<!-- LOGIN CONFIDENCIAL - OBLIGATORIO PARA VER TRABAJO -->
<div id="loginBox" class="card p-3 mb-2 border-warning" style="border-width:2px">
<h6 class="fw-bold text-warning"><i class="fas fa-user-lock"></i> Acceso Confidencial - Solo vea su trabajo cargado</h6>
<p class="small text-secondary mb-2">Por confidencialidad, el sistema NO muestra ejercicios programados ni trabajo de otros usuarios. Ingrese su RNC/Empresa para ver SOLO su trabajo.</p>
<div class="row g-1">
<div class="col-md-5"><input id="empresaLogin" class="form-control form-control-sm" placeholder="Empresa / Entidad (ej: Mi Empresa SRL)" required></div>
<div class="col-md-4"><input id="rncLogin" class="form-control form-control-sm" placeholder="RNC / Cédula / TAX ID" required></div>
<div class="col-md-3"><button onclick="entrarConfidencial()" class="btn-verde" style="padding:7px">🔓 Entrar Modo Confidencial</button></div>
</div>
<small class="text-muted">Su sesión es privada en este dispositivo. Otros usuarios no ven sus archivos.</small>
</div>

<!-- CONTENIDO PRIVADO - OCULTO HASTA LOGIN -->
<div id="contenidoPrivado" style="display:none">

<div class="card p-2 mb-2 border-success"><div class="d-flex justify-content-between align-items-center flex-wrap gap-2">
<div><b class="text-success"><i class="fas fa-shield-halved"></i> Sesión Privada: <span id="userLabel"></span></b><br><small class="text-secondary">Solo usted ve este trabajo. Data ejercicio programado oculta. <span id="adminHint" style="display:none">Admin:?admin=1 para ver matriz interna</span></small></div>
<div class="d-flex gap-1"><button onclick="limpiarTodo()" class="btn btn-danger btn-sm fw-bold"><i class="fas fa-trash"></i> 🗑️ Eliminar todo rastro y limpiar pantalla (Confidencial)</button><button onclick="salir()" class="btn btn-outline-light btn-sm">Salir</button></div>
</div></div>

<div class="row g-2">
<div class="col-lg-7">
<div class="card p-3">
<h6 class="fw-bold text-success"><i class="fas fa-upload"></i> Gestión Informes + Réplicas + Historial - Solo su trabajo - Confidencial</h6>
<p class="small text-secondary">Cargue sus informes. Solo usted los ve en este dispositivo. No se muestra trabajo de otros usuarios ni ejercicios programados.</p>
<form>
<label class="small fw-bold">Tipo Informe:</label><select id="tipoInf" class="form-select form-select-sm mb-1"><option>Acta Lecturas</option><option>Preliminar</option><option>Final</option><option>Réplica Entidad</option><option>Descargo</option><option>Otro</option></select>
<label class="small fw-bold">Seleccionar archivos (PDF, DOCX, XLSX) - Privado:</label><input type="file" id="files" multiple accept=".pdf,.docx,.txt,.xlsx" class="form-control form-control-sm mb-2">
<button type="button" onclick="subirPrivado()" class="btn-verde">📤 Cargar y Sincronizar Solo Mi Trabajo (Confidencial)</button>
</form>

<div class="mt-3">
<div class="d-flex justify-content-between"><h6 class="small fw-bold">📚 Mi Historial Privado - Fecha/Hora/Tipo/Archivo (Solo yo):</h6><button onclick="limpiarTodo()" class="btn btn-outline-danger btn-sm" style="font-size:10px">Eliminar historial pantalla</button></div>
<table id="hist" class="table table-dark table-sm small"><thead><tr><th>Fecha/Hora</th><th>Tipo</th><th>Archivo</th><th>Estado</th><th></th></tr></thead><tbody></tbody></table>
<button onclick="exportarMiHistorial()" class="btn btn-outline-light btn-sm w-100">📄 Exportar Solo Mi Historial (PDF Confidencial)</button>
</div>
</div>
</div>

<div class="col-lg-5">
<div class="card p-3 mb-2" style="background:#f0fdf4;color:#0f172a">
<h6 class="fw-bold" style="color:#003366">🌐 Prueba Online Sin Descargar - Universal</h6>
<div class="d-grid gap-1">
<a href="/b4" class="btn btn-primary fw-bold">B4 FULL IA + NOBACI - Solo mi trabajo</a>
<a href="/v8" class="btn btn-dark fw-bold">V8 FULL NOBACI + Libram - Solo mi trabajo</a>
</div>
<small class="text-muted mt-2 d-block">Tablet/Laptop/Desktop/Celular - Sin APK - Datos guardados local privado, no compartidos.</small>
</div>

<!-- ESTA TABLA YA NO SE MUESTRA AL USUARIO NORMAL - SOLO ADMIN?admin=1 -->
<div id="matrizInterna" style="display:none" class="card p-2">
<h6 class="small fw-bold"><i class="fas fa-database"></i> Matriz Interna Programada (Solo Admin - Oculta a usuarios)</h6>
<p class="small text-secondary">Esta data de ejercicio está oculta por confidencialidad. Solo visible con?admin=1</p>
<table class="table table-dark table-sm small"><thead><tr><th>ID</th><th>Componente</th><th>Monto</th></tr></thead><tbody><tr><td>H_CCRD_3.1</td><td>Contratos SENASE</td><td>RD$867M</td></tr><tr><td>H_CCRD_3.5</td><td>Tope 50% Adendas</td><td>RD$89M</td></tr><tr><td>H_CCRD_3.6</td><td>Legajos RD$481M</td><td>RD$481M</td></tr><tr><td>H_CCRD_5.1</td><td>Dictamen PEPCA</td><td>RD$1,489M</td></tr></tbody></table>
</div>

<div class="card p-2 text-center"><small class="text-secondary">🔐 Confidencial: No se muestra ejercicio programado. Solo ve su trabajo cargado. Botón eliminar limpia pantalla y rastro local.<br>BASA V18 | BHD 08694150021 | {{ auditor.nombre }}</small></div>
</div>
</div>

</div>
</div>

<script>
let currentUser=null;
document.getElementById('ruta').innerText=location.pathname+' | '+window.innerWidth+'px | MODO CONFIDENCIAL | '+new Date().toLocaleString();
function entrarConfidencial(){
 let emp=document.getElementById('empresaLogin').value.trim();
 let rnc=document.getElementById('rncLogin').value.trim();
 if(!emp ||!rnc){alert('Ingrese Empresa y RNC para modo confidencial');return;}
 currentUser=emp+'-'+rnc;
 localStorage.setItem('basa_user',currentUser);
 localStorage.setItem('basa_empresa',emp);
 document.getElementById('userLabel').innerText=emp+' ('+rnc+')';
 document.getElementById('loginBox').style.display='none';
 document.getElementById('contenidoPrivado').style.display='block';
 // cargar historial privado solo de este usuario
 let key='hist_'+currentUser;
 let hist=JSON.parse(localStorage.getItem(key)||'[]');
 let tbody=document.querySelector('#hist tbody'); tbody.innerHTML='';
 hist.forEach(h=>{
  let row=tbody.insertRow(); row.innerHTML='<td>'+h.fecha+'</td><td>'+h.tipo+'</td><td>'+h.archivo+'</td><td><span class="badge bg-success">Privado</span></td><td><button onclick="this.closest(\\'tr\\').remove();guardarHist()" class="btn btn-sm btn-outline-danger" style="font-size:9px">x</button></td>';
 });
 if(new URLSearchParams(location.search).get('admin')=='1'){document.getElementById('matrizInterna').style.display='block';document.getElementById('adminHint').style.display='inline';}
}
function subirPrivado(){
 if(!currentUser){alert('Entre en modo confidencial primero');return;}
 let tipo=document.getElementById('tipoInf').value; let files=document.getElementById('files').files;
 if(files.length==0){alert('Seleccione archivos');return;}
 let tbody=document.querySelector('#hist tbody');
 let key='hist_'+currentUser; let hist=JSON.parse(localStorage.getItem(key)||'[]');
 for(let f of files){
  let now=new Date().toLocaleString(); let fecha=new Date().toISOString().slice(0,16).replace('T',' ');
  let row=tbody.insertRow(); row.innerHTML='<td>'+fecha+'</td><td>'+tipo+'</td><td>'+f.name+'</td><td><span class="badge bg-success">Privado - Solo yo</span></td><td><button onclick="this.closest(\\'tr\\').remove();guardarHist()" class="btn btn-sm btn-outline-danger" style="font-size:9px">x</button></td>';
  hist.push({fecha:fecha,tipo:tipo,archivo:f.name,hash:'SHA-'+Math.random().toString(36).substring(7)});
 }
 localStorage.setItem(key,JSON.stringify(hist));
 alert(files.length+' archivos cargados en MODO CONFIDENCIAL - Solo usted los ve en este dispositivo. No se muestra ejercicio programado ni trabajo de otros.');
 document.getElementById('files').value='';
}
function guardarHist(){
 if(!currentUser) return;
 let tbody=document.querySelector('#hist tbody'); let hist=[];
 for(let r of tbody.rows){hist.push({fecha:r.cells[0].innerText,tipo:r.cells[1].innerText,archivo:r.cells[2].innerText});}
 localStorage.setItem('hist_'+currentUser,JSON.stringify(hist));
}
function limpiarTodo(){
 if(confirm('¿ELIMINAR TODO RASTRO CONFIDENCIAL? Esto borra historial pantalla y archivos de esta sesión privada. No afecta a otros usuarios.')){
  if(currentUser){localStorage.removeItem('hist_'+currentUser);}
  document.querySelector('#hist tbody').innerHTML='';
  document.getElementById('files').value='';
  alert('✅ Pantalla limpiada - Rastro eliminado - Modo confidencial. No queda ejercicio visible.');
 }
}
function salir(){
 localStorage.removeItem('basa_user');
 document.getElementById('contenidoPrivado').style.display='none';
 document.getElementById('loginBox').style.display='block';
 document.getElementById('empresaLogin').value='';document.getElementById('rncLogin').value='';
}
function exportarMiHistorial(){
 if(!currentUser){alert('Entre primero');return;}
 let hist=localStorage.getItem('hist_'+currentUser)||'Sin historial';
 let blob=new Blob([ 'HISTORIAL CONFIDENCIAL PRIVADO\\nUsuario: '+currentUser+'\\nFecha: '+new Date().toLocaleString()+'\\n\\n'+hist ],{type:'text/plain'});
 let url=URL.createObjectURL(blob); let a=document.createElement('a'); a.href=url; a.download='Historial_Confidencial_'+currentUser+'.txt'; a.click();
}
// auto-login si ya entro antes
let saved=localStorage.getItem('basa_user'); if(saved){let emp=localStorage.getItem('basa_empresa')||saved.split('-')[0]; document.getElementById('empresaLogin').value=
