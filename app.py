# -*- coding: utf-8 -*-
# BASA V19 CONFIDENCIAL LIMPIO - 100% PRIVADO - NO MUESTRA EJERCICIO PROGRAMADO NUNCA
import os
from datetime import datetime
from flask import Flask, render_template_string, jsonify, redirect, send_file

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
for p in [os.path.join(BASE_DIR,'reportes_exportados'), os.path.join(BASE_DIR,'uploads')]:
    os.makedirs(p, exist_ok=True)

app=Flask(__name__)

HTML_LIMPIO="""
<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BASA V19 Confidencial Limpio</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
body{background:#0b1120;color:#e2e8f0;font-family:system-ui}
.hero{background:linear-gradient(135deg,#003366,#00d084);padding:14px;text-align:center}
.card{background:#1e293b;border:1px solid #334155;border-radius:12px}
.card-header{background:#0f172a}
.btn-verde{background:#00d084;color:#fff;font-weight:800;border:none;padding:12px;border-radius:10px;width:100%}
input,select{background:#0f172a!important;color:#fff!important;border:2px solid #475569!important;border-radius:8px!important}
.confidencial{background:#dc2626;color:#fff;padding:5px 10px;border-radius:20px;font-size:11px;font-weight:800}
</style></head><body>
<div class="hero">
<h5 class="fw-bold m-0">🔐 BASA V19 CONFIDENCIAL - Solo su trabajo - Ejercicio oculto</h5>
<small><span class="confidencial"><i class="fas fa-lock"></i> CONFIDENCIAL - NO SE MUESTRA EJERCICIO PROGRAMADO</span> | BHD 08694150021 | Tablet/Laptop/Desktop/Celular</small><br>
<small id="info" style="background:rgba(0,0,0,0.3);padding:3px 8px;border-radius:6px"></small>
</div>

<div class="container-fluid p-2" style="max-width:900px">

<div id="login" class="card p-3 mb-2 border-warning" style="border-width:2px">
<h6 class="text-warning fw-bold"><i class="fas fa-user-lock"></i> Acceso Privado - Solo verá SU trabajo cargado</h6>
<div class="row g-1">
<div class="col-md-5"><input id="emp" class="form-control form-control-sm" placeholder="Empresa"></div>
<div class="col-md-4"><input id="rnc" class="form-control form-control-sm" placeholder="RNC / ID"></div>
<div class="col-md-3"><button onclick="entrar()" class="btn-verde" style="padding:7px">🔓 Entrar</button></div>
</div>
<small class="text-secondary">Por confidencialidad, NO se muestra matriz RD$1,489M ni expedientes demo. Solo su sesión privada.</small>
</div>

<div id="privado" style="display:none">
<div class="card p-2 mb-2 d-flex justify-content-between flex-wrap gap-2">
<span><b class="text-success">Sesión: <span id="user"></span></b> <small class="text-secondary">- Privado - Solo su trabajo</small></span>
<div><button onclick="limpiar()" class="btn btn-danger btn-sm fw-bold">🗑️ Eliminar todo rastro y limpiar pantalla</button> <button onclick="salir()" class="btn btn-outline-light btn-sm">Salir</button></div>
</div>

<div class="card p-3">
<h6 class="fw-bold"><i class="fas fa-upload"></i> Gestión Informes + Réplicas - Confidencial - Solo mi trabajo</h6>
<label class="small">Tipo:</label><select id="tipo" class="form-select form-select-sm mb-1"><option>Preliminar</option><option>Acta Lecturas</option><option>Final</option><option>Réplica</option><option>Descargo</option></select>
<label class="small">Seleccionar archivos (privado):</label><input type="file" id="files" multiple class="form-control form-control-sm mb-2">
<button onclick="cargar()" class="btn-verde">📤 Cargar Solo Mi Trabajo - Confidencial</button>

<div class="mt-3">
<div class="d-flex justify-content-between"><h6 class="small fw-bold">📚 Mi Historial Privado (Fecha/Hora/Tipo/Archivo) - Solo yo:</h6><button onclick="limpiar()" class="btn btn-outline-danger btn-sm" style="font-size:10px">Eliminar pantalla</button></div>
<table id="hist" class="table table-dark table-sm small"><thead><tr><th>Fecha/Hora</th><th>Tipo</th><th>Archivo</th><th>Estado</th><th></th></tr></thead><tbody></tbody></table>
</div>
</div>

<div class="card p-2 mt-2 text-center"><small class="text-secondary">🔐 V19 Confidencial Limpio: No se muestra H_CCRD_3.1, 3.5, 3.6, 5.1 ni Expediente_Base_EDEESTE_SENASE. Solo trabajo cargado por usted. Botón eliminar limpia todo rastro.<br>BHD 08694150021 | BASA V19</small></div>
</div>
</div>

<script>
document.getElementById('info').innerText=new Date().toLocaleString()+' | V19 CONFIDENCIAL LIMPIO | '+window.innerWidth+'px';
let cur=null;
function entrar(){
 let e=document.getElementById('emp').value.trim(), r=document.getElementById('rnc').value.trim();
 if(!e||!r){alert('Empresa y RNC');return;}
 cur=e+'-'+r; localStorage.setItem('basa_v19_user',cur); localStorage.setItem('basa_v19_emp',e);
 document.getElementById('user').innerText=e+' ('+r+')';
 document.getElementById('login').style.display='none'; document.getElementById('privado').style.display='block';
 let k='hist_v19_'+cur; let h=JSON.parse(localStorage.getItem(k)||'[]'); let tb=document.querySelector('#hist tbody'); tb.innerHTML='';
 h.forEach(o=>{let tr=tb.insertRow(); tr.innerHTML='<td>'+o.fecha+'</td><td>'+o.tipo+'</td><td>'+o.arch+'</td><td><span class="badge bg-success">Privado</span></td><td><button onclick="this.closest(\\'tr\\').remove();save()" class="btn btn-sm btn-outline-danger" style="font-size:9px">x</button></td>';});
}
function cargar(){
 let t=document.getElementById('tipo').value, fs=document.getElementById('files').files;
 if(!cur){alert('Entre primero');return;} if(fs.length==0){alert('Seleccione archivos');return;}
 let tb=document.querySelector('#hist tbody'); let k='hist_v19_'+cur; let h=JSON.parse(localStorage.getItem(k)||'[]');
 for(let f of fs){let fe=new Date().toLocaleString(); let tr=tb.insertRow(); tr.innerHTML='<td>'+fe+'</td><td>'+t+'</td><td>'+f.name+'</td><td><span class="badge bg-success">Privado Solo yo</span></td><td><button onclick="this.closest(\\'tr\\').remove();save()" class="btn btn-sm btn-outline-danger" style="font-size:9px">x</button></td>'; h.push({fecha:fe,tipo:t,arch:f.name});}
 localStorage.setItem(k,JSON.stringify(h)); document.getElementById('files').value=''; alert(fs.length+' archivos cargados CONFIDENCIAL - Solo usted los ve. Ejercicio programado oculto.');
}
function save(){let k='hist_v19_'+cur; let tb=document.querySelector('#hist tbody'); let arr=[]; for(let r of tb.rows)arr.push({fecha:r.cells[0].innerText,tipo:r.cells[1].innerText,arch:r.cells[2].innerText}); localStorage.setItem(k,JSON.stringify(arr));}
function limpiar(){if(confirm('¿Eliminar todo rastro confidencial de pantalla?')){if(cur)localStorage.removeItem('hist_v19_'+cur); document.querySelector('#hist tbody').innerHTML=''; document.getElementById('files').value=''; alert('✅ Pantalla limpiada - Rastro eliminado');}}
function salir(){localStorage.removeItem('basa_v19_user'); document.getElementById('privado').style.display='none'; document.getElementById('login').style.display='block'; document.getElementById('emp').value='';document.getElementById('rnc').value='';}
let sv=localStorage.getItem('basa_v19_user'); if(sv){let em=localStorage.getItem('basa_v19_emp')||sv.split('-')[0]; document.getElementById('emp').value=em; document.getElementById('rnc').value=sv.split('-').pop(); entrar();}
</script>
</body></html>
"""

@app.route('/')
@app.route('/gestion-informes')
def home(): return render_template_string(HTML_LIMPIO)

@app.route('/trial')
@app.route('/b4')
@app.route('/v8')
@app.route('/demo')
def redir(): return redirect('/')

@app.route('/api/auto/sync_completo')
def sync(): return jsonify({"status":"V19 CONFIDENCIAL LIMPIO - Ejercicio oculto - Solo trabajo usuario"})

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
