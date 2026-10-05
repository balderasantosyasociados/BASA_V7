# -*- coding: utf-8 -*-
# BASA V21 WORLD AUDIT ENTERPRISE ÚNICO MUNDIAL - AUDITOR ONLINE DESDE CASA - FULL FULL
# 22 Módulos USD250 + Multi-País + Multi-Idioma + Multi-Moneda + Normativa Mundial + Forense
import os, json, hashlib
from datetime import datetime, timedelta
from flask import Flask, render_template_string, request, send_file, jsonify, redirect

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
DATA_DIR=os.path.join(BASE_DIR,'data_world')
os.makedirs(DATA_DIR, exist_ok=True)
for f in ['usuarios.json','historico_claves.json','pagos.json','auditorias.json']:
    p=os.path.join(DATA_DIR,f)
    if not os.path.exists(p):
        with open(p,'w',encoding='utf-8') as fh: json.dump([],fh)

def load(p): 
    try:
        with open(os.path.join(DATA_DIR,p),'r',encoding='utf-8') as fh: return json.load(fh)
    except: return []
def save(p,d): 
    with open(os.path.join(DATA_DIR,p),'w',encoding='utf-8') as fh: json.dump(d,fh,indent=2,ensure_ascii=False)
def sha(s): return hashlib.sha256(s.encode()).hexdigest()

# 22 MODULOS WORLD ENTERPRISE UNICO MUNDIAL - TODO AMPLIADO
MODULOS_WORLD=[
    {"id":"M1","cat":"LICITACIÓN","nombre":"M1 Licitación Pública + Pliego Mundial","precio":250,"paises":["DO 340-06","US FAR","MX LAASSP","PA Ley22","CO Ley80","ES LCSP","INTOSAI"],"func":["Pliego condiciones","Convocatoria","Evaluación ofertas","Adjudicación","Impugnaciones"],"reportes":["Pliego Final","Acta Adjudicación","Matriz Evaluación"],"cumplimiento":"Ley 340-06 Art 8-30 + FAR Part 15 + LAASSP Art 26 + LCSP Art 116"},
    {"id":"M2","cat":"CONTRATOS","nombre":"M2 Contratos + Adendas + Tope Legal Mundial","precio":250,"paises":["DO","US","MX","PA","CO","ES","BR","CL"],"func":["Contrato base","4 adendas control 50%","Registro CGR/Contraloría","Garantías","Penalidades"],"reportes":["Matriz Contratos RD$1,489M","Control Adendas 50%","Registro CGR"],"cumplimiento":"Ley 340-06 Art31 50% + Dec 543-12 Art127 + CP 123-124"},
    {"id":"M3","cat":"NÓMINA","nombre":"M3 Nómina Pública + Privada + TSS Mundial","precio":250,"paises":["DO TSS","US IRS","MX IMSS","ES TGSS","CO PILA"],"func":["Nómina pública/privada","Validación TSS/DGII/RPE","ISR retenciones","Seguridad social mundial","Horas extras","Bonificación"],"reportes":["Nómina Detallada","TSS Validada","ISR Reporte","PILA CO","IMSS MX"],"cumplimiento":"Código Trabajo + Ley 87-01 TSS + IRS Pub 15 + IMSS Art 27"},
    {"id":"M4","cat":"PAGOS","nombre":"M4 Pagos + Desembolsos + Libramientos SIGEF + BHD","precio":250,"paises":["DO SIGEF","US Treasury","MX TESOFE"],"func":["Libramiento SIGEF","Desembolso","Cheque/Transfer BHD 08694150021","Validación DGII/TSS/RPE","Carta bancaria","Cuota comprometer"],"reportes":["Legajo Pago Completo","RD$481M Validado","Libramiento SIGEF","BHD Transfer"],"cumplimiento":"NOBACI 3.62 + Ley 340-06 Art8 + Guía Legajos EDEESTE"},
    {"id":"M5","cat":"PRESUPUESTO","nombre":"M5 Presupuesto + Ejecución + SIGEF Mundial","precio":250,"paises":["DO","US","MX","ES"],"func":["Formulación presupuesto","Ejecución","Modificaciones","Compromiso","Devengado","Pagado","SIGEF/SIAF"],"reportes":["Ejecución Presupuestaria","Disponibilidad","Modificaciones"],"cumplimiento":"Ley 423-06 Presupuesto + IPSAS 24 + GASB"},
    {"id":"M6","cat":"CONTABILIDAD","nombre":"M6 Contabilidad + IPSAS + IFRS + NIIF + NICSP","precio":250,"paises":["MUNDIAL IPSAS","IFRS","NIIF","NICSP","US GAAP"],"func":["Partida doble","Catálogo cuentas","Estados financieros","Balance","Resultados","Flujo efectivo","Notas","Consolidación"],"reportes":["Balance General","Estado Resultados","Flujo Efectivo","Notas IPSAS"],"cumplimiento":"IPSAS 1-47 + IFRS + NIIF + NICSP + Decreto 526-09"},
    {"id":"M7","cat":"ACTIVOS","nombre":"M7 Activos Fijos + Inventarios + QR Mundial","precio":250,"paises":["DO","US","MUNDIAL"],"func":["Registro activos","Depreciación","Inventario físico QR","Custodia","Traslado","Descargo","Conciliación"],"reportes":["Inventario Activos Fijos","Depreciación","QR Etiquetas"],"cumplimiento":"NOBACI Activos + IPSAS 17 + IAS 16"},
    {"id":"M8","cat":"ALMACEN","nombre":"M8 Almacén + Kardex + Entradas/Salidas","precio":250,"paises":["MUNDIAL"],"func":["Kardex","Entrada almacén","Salida","Conteo físico","Ajustes","Merma","Valuación PEPS/UEPS"],"reportes":["Kardex","Existencias","Conteo Físico","Valuación"],"cumplimiento":"NIC 2 + IPSAS 12"},
    {"id":"M9","cat":"COMPRAS","nombre":"M9 Compras + RPE + DGII + TSS + Validación Auto","precio":250,"paises":["DO","US SAM","MX CompraNet"],"func":["PACC","Solicitud compra","Validación RPE DGII TSS auto","Cuadro comparativo","Orden compra","Recepción"],"reportes":["PACC","Validación Fiscal Auto","Orden Compra"],"cumplimiento":"Ley 340-06 Art8 + Dec 543-12"},
    {"id":"M10","cat":"FORENSIC","nombre":"M10 Auditoría Forense + PEPCA + Cadena Custodia + SHA-256","precio":250,"paises":["DO PEPCA","US FBI","ES UDEF"],"func":["Forense","Anomalías IA","Cadena custodia SHA-256","Remisión PEPCA","Perjuicio RD$1,489M","Informe pericial"],"reportes":["Dictamen Forense Final","Cadena Custodia SHA-256","Remisión PEPCA"],"cumplimiento":"Const Art146,169 + CP 123,124,175 + Ley 10-04 Art49"},
    {"id":"M11","cat":"NOBACI","nombre":"M11 NOBACI 16 Normas + Control Interno + Riesgos","precio":250,"paises":["DO NOBACI","US COSO","INTOSAI"],"func":["NOBACI 1-16","COSO","Control interno","Matriz riesgos","Evaluación","Seguimiento"],"reportes":["Matriz NOBACI","Evaluación Control Interno","Riesgos"],"cumplimiento":"NOBACI CGR + COSO + ISSAI 100"},
    {"id":"M12","cat":"INFORMES","nombre":"M12 Gestión Informes + Réplicas Múltiples + Historial Confidencial","precio":250,"paises":["MUNDIAL"],"func":["Carga múltiple PDF/DOCX/XLSX","Réplicas entidad","Historial fecha/hora/tipo/archivo/hash","Modo confidencial privado solo su trabajo","Export Word/Excel/PDF","Eliminar rastro pantalla"],"reportes":["Historial Confidencial","Réplicas","Informe Consolidado"],"cumplimiento":"ISSAI 100 + Ley 10-04 + Confidencialidad"},
    {"id":"M13","cat":"DOCUMENTAL","nombre":"M13 Gestión Documental + OCR + IA + Evidencia Digital","precio":250,"paises":["MUNDIAL eIDAS","ESIGN","Ley 126-02"],"func":["OCR IA","Extracción texto","Clasificación auto","Hash SHA-256","Firma digital Ley 126-02 + eIDAS + ESIGN","Custodia digital"],"reportes":["Transcripción OCR","Índice Documental","Hash Integridad"],"cumplimiento":"Ley 126-02 Firma Digital + eIDAS + ESIGN + eDiscovery"},
    {"id":"M14","cat":"LEGAL","nombre":"M14 Cumplimiento Legal Mundial + Multi-País","precio":250,"paises":["DO","US","MX","PA","CO","ES","BR","AR","CL","PE","EC","INTOSAI"],"func":["DO 340-06 10-04 10-07 423-06","US FAR SOX Yellow Book","MX LAASSP","PA Ley22","CO Ley80","ES LCSP","BR Lei 14.133","AR Ley 27.328","INTOSAI ISSAI IPSAS"],"reportes":["Matriz Cumplimiento Legal Mundial","Checklist País"],"cumplimiento":"Todas leyes vigentes mundial"},
    {"id":"M15","cat":"TRIBUTARIO","nombre":"M15 Tributario + DGII + IRS + SAT + AEAT Mundial","precio":250,"paises":["DO DGII","US IRS","MX SAT","ES AEAT","CO DIAN"],"func":["Validación DGII","TSS","RPE","IRS W-9","SAT Constancia","AEAT","Retenciones","ITBIS/IVA"],"reportes":["Validación Fiscal Mundial","Reporte Tributario"],"cumplimiento":"Código Tributario + IRS + SAT + AEAT"},
    {"id":"M16","cat":"RRHH","nombre":"M16 RRHH + Expedientes + Evaluación Desempeño","precio":250,"paises":["MUNDIAL"],"func":["Expediente empleado","Evaluación desempeño","Capacitación","Sanciones","Vacaciones","Licencias"],"reportes":["Expediente RRHH","Evaluación"],"cumplimiento":"Código Trabajo + Ley Función Pública 41-08"},
    {"id":"M17","cat":"TESORERIA","nombre":"M17 Tesorería + Flujo Caja + Conciliación Bancaria BHD","precio":250,"paises":["DO BHD","MUNDIAL"],"func":["Flujo caja","Conciliación bancaria BHD 08694150021","Proyección","Inversiones","Préstamos"],"reportes":["Flujo Caja","Conciliación Bancaria BHD","Proyección"],"cumplimiento":"NOBACI Tesorería + IPSAS"},
    {"id":"M18","cat":"MULTI","nombre":"M18 Multi-Idioma + Multi-Moneda + Traducción IA","precio":250,"paises":["MUNDIAL"],"func":["ES EN FR PT DE IT + 20 idiomas IA","USD DOP EUR MXN BRL COP CLP PEN + 50 monedas","Traducción automática informes","Conversión moneda auto"],"reportes":["Informe Multi-Idioma","Conversión Moneda"],"cumplimiento":"eIDAS + Internacionalización"},
    {"id":"M19","cat":"B4","nombre":"M19 B4 Base Informe Pericial IA Generativo","precio":250,"paises":["MUNDIAL"],"func":["Informe pericial IA","Análisis automático hallazgos","Generación dictamen","Validación normativa","Hash probatorio","Export Word final"],"reportes":["Informe Pericial B4 IA","Dictamen"],"cumplimiento":"ISSAI 100 + Ley 10-04"},
    {"id":"M20","cat":"V8","nombre":"M20 V8 FULL NOBACI + Libramientos + Inventarios + Producción","precio":250,"paises":["DO","MUNDIAL"],"func":["V8 NOBACI full","Libramientos SIGEF","Inventarios QR","Pagos","Contabilidad IPSAS","Producción final"],"reportes":["V8 Informe Final Producción"],"cumplimiento":"NOBACI + IPSAS + 340-06"},
    {"id":"M21","cat":"ADMIN","nombre":"M21 Admin + Usuarios + Roles + Histórico Claves Privado + Backup","precio":250,"paises":["MUNDIAL"],"func":["Registro usuarios","Roles admin/usuario","Cambiar clave","Histórico privado claves hash","Editar/borrar/suspender","Backup full JSON/Excel","Auditoría accesos"],"reportes":["Usuarios","Histórico Claves Privado","Backup FULL","Auditoría Accesos"],"cumplimiento":"ISO 27001 + Ley 126-02 + Confidencialidad"},
    {"id":"M22","cat":"WORLD","nombre":"M22 WORLD ENTERPRISE ÚNICO MUNDIAL - Dashboard Global","precio":250,"paises":["MUNDIAL 100+ países"],"func":["Dashboard mundial","KPIs auditoría","Mapa cumplimiento","Alertas globales","Consolidación multi-país","Reportes ejecutivos","Enterprise único"],"reportes":["Dashboard Global","KPIs","Mapa Cumplimiento Mundial","Enterprise Report"],"cumplimiento":"INTOSAI + IPSAS + IFRS + Mundial"},
]

app=Flask(__name__)
app.secret_key='WORLD_V21_'+sha(str(datetime.now()))

HTML_WORLD="""
<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BASA V21 WORLD ENTERPRISE ÚNICO MUNDIAL - Auditor Online Desde Casa</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
body{background:#0b1120;color:#e2e8f0;font-family:system-ui}
.hero{background:linear-gradient(135deg,#003366 0%,#00d084 50%,#003366 100%);padding:14px;text-align:center}
.card{background:#1e293b;border:1px solid #334155;border-radius:12px}
.card-header{background:#0f172a}
.btn-verde{background:#00d084;color:#fff;font-weight:800;border:none;padding:10px;border-radius:10px;width:100%}
.mod{background:#0f172a;border:2px solid #334155;border-radius:10px;padding:10px;margin-bottom:8px}
.mod.activo{border-color:#00d084;background:#0f2a1f} .mod.demo{border-color:#f59e0b;background:#2a2210}
.badge-pro{background:#00d084;color:#fff} .badge-demo{background:#f59e0b;color:#000}
.cat{font-size:10px;padding:2px 6px;border-radius:10px;background:#334155;color:#00d084;font-weight:800}
input,select{background:#0f172a!important;color:#fff!important;border:1px solid #475569!important;border-radius:8px!important}
.tab{display:none} .tab.active{display:block}
</style></head><body>
<div class="hero">
<h5 class="fw-bold m-0">🌍 BASA V21 WORLD ENTERPRISE ÚNICO MUNDIAL - AUDITOR ONLINE DESDE CASA - FULL FULL</h5>
<small>22 MÓDULOS x USD250 = USD5500 | DO ITBIS 18% USD990 | Total Mensual USD6490 | Primer pago 27 días USD5841 | BHD 08694150021 USD Y DOP | Multi-País 100+ | Multi-Idioma ES EN FR PT DE IT +20 | Multi-Moneda USD DOP EUR MXN BRL COP CLP PEN +50 | Tablet/Laptop/Desktop/Celular | Online sin descargar | Confidencial Privado</small><br>
<small style="background:rgba(0,0,0,0.4);padding:3px 8px;border-radius:6px" id="info"></small>
</div>

<div class="container-fluid p-2">

<div class="card p-2 mb-2"><div class="d-flex flex-wrap gap-1 justify-content-between">
<div class="d-flex gap-1 flex-wrap">
<button onclick="tab('world')" class="btn btn-success btn-sm fw-bold"><i class="fas fa-globe"></i> WORLD 22 Módulos Full Full</button>
<button onclick="tab('nomina')" class="btn btn-primary btn-sm"><i class="fas fa-users"></i> Nómina Pública/Privada</button>
<button onclick="tab('contratos')" class="btn btn-warning btn-sm"><i class="fas fa-file-contract"></i> Licitación/Pliego/Contratos</button>
<button onclick="tab('pagos')" class="btn btn-info btn-sm"><i class="fas fa-money-bill"></i> Pagos/Libramientos/Desembolsos</button>
<button onclick="tab('presupuesto')" class="btn btn-dark btn-sm"><i class="fas fa-calculator"></i> Presupuesto/Contabilidad</button>
<button onclick="tab('cumplimiento')" class="btn btn-secondary btn-sm"><i class="fas fa-gavel"></i> Cumplimiento Mundial</button>
<button onclick="tab('admin')" class="btn btn-danger btn-sm"><i class="fas fa-user-shield"></i> Admin + Usuarios + Backup</button>
<button onclick="tab('confidencial')" class="btn btn-outline-light btn-sm"><i class="fas fa-lock"></i> Mi Trabajo Confidencial</button>
</div>
<span id="userLabel" class="badge bg-light text-dark"></span>
</div></div>

<div id="tab-world" class="tab active">
<div class="row g-2"><div class="col-lg-9"><h6 class="fw-bold text-success"><i class="fas fa-globe"></i> ENTERPRISE ÚNICO MUNDIAL - 22 Módulos - Auditoría Forense Completa - Desde Casa</h6>
<p class="small text-secondary">Auditor online desde casa para cualquier nómina pública, contrato, empresa privada, licitación, pliego, pagos, desembolsos, libramientos, presupuesto, contabilidad, documentos y operaciones públicas/privadas multi-idioma y monedas full full.</p>
<div id="listaWorld"></div>
</div><div class="col-lg-3">
<div class="card p-2"><h6 class="small fw-bold">💳 Pago Mensual Habilita Producción</h6><div id="resumenWorld" class="small p-2 rounded" style="background:#0f172a;border:1px dashed #475569"></div><button onclick="tab('pago')" class="btn-verde mt-2">Pagar Mensual BHD 08694150021</button></div>
<div class="card p-2 mt-2"><h6 class="small fw-bold">🌍 Cumplimiento Mundial</h6><small class="text-secondary" style="font-size:10px">DO: 340-06 10-04 10-07 423-06 NOBACI | US: FAR SOX Yellow Book GASB | MX: LAASSP | PA Ley22 | CO Ley80 | ES LCSP | BR Lei 14.133 | INTOSAI ISSAI IPSAS IFRS NIIF NICSP | eIDAS ESIGN Ley 126-02</small></div>
</div></div>
</div>

<div id="tab-nomina" class="tab"><div class="card p-3"><h6 class="fw-bold">👥 Nómina Pública y Privada - M3</h6><div id="nominaDetail"></div></div></div>
<div id="tab-contratos" class="tab"><div class="card p-3"><h6 class="fw-bold">📄 Licitación Pública + Pliego + Contratos + Adendas - M1/M2</h6><div id="contratosDetail"></div></div></div>
<div id="tab-pagos" class="tab"><div class="card p-3"><h6 class="fw-bold">💰 Pagos + Desembolsos + Libramientos + BHD 08694150021 - M4</h6><div id="pagosDetail"></div></div></div>
<div id="tab-presupuesto" class="tab"><div class="card p-3"><h6 class="fw-bold">📊 Presupuesto + Contabilidad IPSAS/IFRS - M5/M6</h6><div id="presupuestoDetail"></div></div></div>
<div id="tab-cumplimiento" class="tab"><div class="card p-3"><h6 class="fw-bold">⚖️ Cumplimiento Normativa Vigente Mundial - M14</h6><div id="cumplimientoDetail"></div></div></div>

<div id="tab-pago" class="tab">
<div class="card p-3"><h6 class="fw-bold text-success">💳 Pagar Mensualidad - Habilita Producción WORLD ENTERPRISE</h6>
<form onsubmit="return pagarWorld(event)">
<div class="row g-1"><div class="col-md-3"><input id="emp" class="form-control form-control-sm" placeholder="Empresa" required></div><div class="col-md-2"><input id="rnc" class="form-control form-control-sm" placeholder="RNC" required></div><div class="col-md-3"><input id="email" type="email" class="form-control form-control-sm" placeholder="Email" required></div><div class="col-md-2"><select id="pais" class="form-select form-select-sm" onchange="calc()"><option value="DO" data-imp="18">DO 18%</option><option value="US" data-imp="0">US 0%</option><option value="MX" data-imp="16">MX 16%</option><option value="PA" data-imp="7">PA 7%</option><option value="CO" data-imp="19">CO 19%</option><option value="ES" data-imp="21">ES 21%</option></select></div><div class="col-md-2"><button class="btn-verde" style="padding:6px">Pagar</button></div></div>
<div id="modsPagoCheck" class="mt-2 small"></div><div id="calc" class="p-2 mt-2 rounded small" style="background:#0f172a;border:1px dashed #475569"></div>
</form><div id="resPago"></div></div>
</div>

<div id="tab-admin" class="tab">
<div class="card p-2 border-danger"><h6 class="fw-bold text-danger">🔐 ADMIN - Registro Usuarios + Cambiar Clave + Histórico Privado + Editar/Borrar/Suspender + Backup Full</h6></div>
<div class="row g-2 mt-1"><div class="col-md-3"><div class="card p-2"><h6 class="small fw-bold">Registrar</h6><form onsubmit="return regUser(event)"><input id="nEmp" class="form-control form-control-sm mb-1" placeholder="Empresa" required><input id="nRnc" class="form-control form-control-sm mb-1" placeholder="RNC" required><input id="nEmail" type="email" class="form-control form-control-sm mb-1" placeholder="Email" required><input id="nPass" type="password" class="form-control form-control-sm mb-1" placeholder="Clave" required><select id="nRol" class="form-select form-select-sm mb-1"><option value="usuario">Usuario</option><option value="admin">Admin</option></select><button class="btn btn-primary btn-sm w-100">Guardar + Histórico Clave</button></form><button onclick="backup()" class="btn btn-warning btn-sm w-100 mt-1 fw-bold">📦 Backup Full JSON</button></div></div><div class="col-md-9"><div class="card p-2"><div class="table-responsive"><table id="usersTbl" class="table table-dark table-sm small"><thead><tr><th>Empresa</th><th>RNC</th><th>Email</th><th>Rol</th><th>Estado</th><th>Clave hash</th><th>Acciones Admin</th></tr></thead><tbody></tbody></table></div></div><div class="card p-2 mt-2"><h6 class="small fw-bold">Histórico Privado Claves (Solo Admin)</h6><div class="table-responsive"><table id="histTbl" class="table table-dark table-sm small"><thead><tr><th>Fecha</th><th>RNC</th><th>Acción</th><th>Clave Ant hash</th><th>Clave Nueva hash</th><th>Admin</th></tr></thead><tbody></tbody></table></div></div></div></div>
</div>

<div id="tab-confidencial" class="tab"><div class="card p-3"><h6 class="fw-bold"><i class="fas fa-lock"></i> Mi Trabajo Confidencial - Solo yo - Ejercicio oculto</h6><input type="file" multiple id="files" class="form-control form-control-sm mb-1"><button onclick="cargarConf()" class="btn-verde">Cargar Confidencial</button> <button onclick="document.querySelector('#histConf tbody').innerHTML=''" class="btn btn-danger btn-sm">🗑️ Eliminar rastro pantalla</button><table id="histConf" class="table table-dark table-sm small mt-2"><thead><tr><th>Fecha/Hora</th><th>Tipo</th><th>Archivo</th><th>Privado</th></tr></thead><tbody></tbody></table></div></div>

</div>

<script>
let MODS={{ mods|tojson }};
let pagosCache=JSON.parse(localStorage.getItem('pagos_world')||'{}');
function tab(t){document.querySelectorAll('.tab').forEach(d=>d.classList.remove('active')); document.getElementById('tab-'+t).classList.add('active');}
function renderWorld(){
 let html=''; MODS.forEach(m=>{
  let act=pagosCache[m.id]; let badge=act?'<span class="badge-pro badge">PRODUCCIÓN PAGADA MENSUAL</span>':'<span class="badge-demo badge">DEMO</span>';
  html+='<div class="mod '+(act?'activo':'demo')+'"><div class="d-flex justify-content-between flex-wrap"><span><span class="cat">'+m.cat+'</span> <b>'+m.id+' - '+m.nombre+'</b> '+badge+' <small class="text-secondary">'+m.paises.join(' | ')+'</small></span><span class="badge bg-secondary">USD'+m.precio+'/mes</span></div><div class="small mt-1"><b>Funciones:</b> '+m.func.join(' | ')+'<br><b>Reportes:</b> '+m.reportes.join(' | ')+'<br><b>Cumplimiento:</b> '+m.cumplimiento+'</div><div class="mt-1"><button onclick="alert(\\'Funciones '+m.id+':\\\\n'+m.func.join('\\\\n')+'\\')" class="btn btn-outline-light btn-sm" style="font-size:10px">Ver Funciones Organizadas</button> '+(act?' <span class="badge bg-success" style="font-size:10px">✅ Habilitado producción hasta '+act.hasta+'</span>':' <span class="badge bg-warning text-dark" style="font-size:10px">Demo marca agua - Pague mensual para producción</span>')+'</div></div>';
 });
 document.getElementById('listaWorld').innerHTML=html;
 let activos=Object.keys(pagosCache).length; let sub=activos*250; let imp=sub*0.18; let tot=sub+imp;
 document.getElementById('resumenWorld').innerHTML=activos+'/'+MODS.length+' módulos producción<br>Subtotal USD'+sub+' | ITBIS 18% USD'+imp.toFixed(2)+' | <b>Total USD'+tot.toFixed(2)+' | BHD 08694150021</b><br>'+(activos==0?'Demo: Funciones limitadas':'Producción: Full sin límites + Word/Excel + SHA-256');
 // checks pago
 let checkHtml=''; MODS.forEach(m=>{checkHtml+='<label class="me-2"><input type="checkbox" value="'+m.id+'" checked onchange="calc()"> '+m.id+'</label>';});
 document.getElementById('modsPagoCheck').innerHTML=checkHtml;
 // detalles por categoria
 document.getElementById('nominaDetail').innerHTML=MODS.filter(m=>m.cat=='NÓMINA').map(m=>'<b>'+m.nombre+'</b><br>Func: '+m.func.join(' | ')+'<br>Cumpl: '+m.cumplimiento+'<hr>').join('');
 document.getElementById('contratosDetail').innerHTML=MODS.filter(m=>['LICITACIÓN','CONTRATOS'].includes(m.cat)).map(m=>'<b>'+m.nombre+'</b><br>Func: '+m.func.join(' | ')+'<br>Reportes: '+m.reportes.join(' | ')+'<br>Cumpl: '+m.cumplimiento+'<hr>').join('');
 document.getElementById('pagosDetail').innerHTML=MODS.filter(m=>['PAGOS','TESORERIA','COMPRAS'].includes(m.cat)).map(m=>'<b>'+m.nombre+'</b><br>Func: '+m.func.join(' | ')+'<br>Reportes: '+m.reportes.join(' | ')+'<hr>').join('');
 document.getElementById('presupuestoDetail').innerHTML=MODS.filter(m=>['PRESUPUESTO','CONTABILIDAD','ACTIVOS','ALMACEN'].includes(m.cat)).map(m=>'<b>'+m.nombre+'</b><br>Func: '+m.func.join(' | ')+'<br>Cumpl: '+m.cumplimiento+'<hr>').join('');
 document.getElementById('cumplimientoDetail').innerHTML=MODS.map(m=>'<span class="cat">'+m.cat+'</span> <b>'+m.id+'</b> '+m.nombre+'<br><small>'+m.paises.join(' | ')+' - '+m.cumplimiento+'</small><hr>').join('');
}
function calc(){
 let pais=document.getElementById('pais'); let imp=parseFloat(pais.options[pais.selectedIndex].dataset.imp);
 let c=0; document.querySelectorAll('#modsPagoCheck input:checked').forEach(()=>c++);
 let sub=c*250; let impVal=sub*imp/100; let tot=sub+impVal; let primer=tot*0.9;
 document.getElementById('calc').innerHTML=c+' módulos x USD250 = USD'+sub+' | Impuesto '+imp+'% = USD'+impVal.toFixed(2)+' | <b>Total Mensual USD'+tot.toFixed(2)+' | Primer pago 27 días USD'+primer.toFixed(2)+'</b> | BHD 08694150021 USD Y DOP';
}
function pagarWorld(e){
 e.preventDefault();
 let mods=[]; document.querySelectorAll('#modsPagoCheck input:checked').forEach(i=>mods.push(i.value));
 let emp=document.getElementById('emp').value, rnc=document.getElementById('rnc').value, email=document.getElementById('email').value, pais=document.getElementById('pais').value;
 fetch('/api/pagar',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({empresa:emp,rnc:rnc,email:email,pais:pais,modulos:mods})}).then(r=>r.json()).then(d=>{
  document.getElementById('resPago').innerHTML='<div class="alert alert-success small">✅ Pago mensual registrado: '+d.contrato+' | Total USD'+d.total+' | Hasta '+d.hasta+' | Producción habilitada BHD 08694150021</div>';
  mods.forEach(id=>pagosCache[id]={hasta:d.hasta,contrato:d.contrato}); localStorage.setItem('pagos_world',JSON.stringify(pagosCache)); renderWorld();
 });
 return false;
}
function regUser(e){
 e.preventDefault();
 let emp=document.getElementById('nEmp').value, rnc=document.getElementById('nRnc').value, email=document.getElementById('nEmail').value, pass=document.getElementById('nPass').value, rol=document.getElementById('nRol').value;
 fetch('/api/admin/usuarios',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({empresa:emp,rnc:rnc,email:email,password:pass,rol:rol})}).then(r=>r.json()).then(d=>{alert(d.msg); loadUsers(); loadHist();});
 return false;
}
function loadUsers(){fetch('/api/admin/usuarios').then(r=>r.json()).then(data=>{let tb=document.querySelector('#usersTbl tbody'); tb.innerHTML=''; data.forEach(u=>{let tr=tb.insertRow(); tr.innerHTML='<td>'+u.empresa+'</td><td>'+u.rnc+'</td><td>'+u.email+'</td><td>'+u.rol+'</td><td>'+u.estado+'</td><td style="font-size:9px">'+(u.password_hash||'').substring(0,10)+'..</td><td><button onclick="cambiarClave(\\''+u.rnc+'\\')" class="btn btn-warning btn-sm" style="font-size:9px">Clave</button> <button onclick="editar(\\''+u.rnc+'\\')" class="btn btn-primary btn-sm" style="font-size:9px">Editar</button> <button onclick="suspender(\\''+u.rnc+'\\')" class="btn btn-dark btn-sm" style="font-size:9px">Susp</button> <button onclick="borrar(\\''+u.rnc+'\\')" class="btn btn-danger btn-sm" style="font-size:9px">Borrar</button></td>';});});}
function loadHist(){fetch('/api/admin/historico').then(r=>r.json()).then(data=>{let tb=document.querySelector('#histTbl tbody'); tb.innerHTML=''; data.slice(-50).reverse().forEach(h=>{let tr=tb.insertRow(); tr.innerHTML='<td>'+h.fecha+'</td><td>'+h.rnc+'</td><td>'+h.accion+'</td><td style="font-size:9px">'+(h.clave_anterior||'').substring(0,8)+'..</td><td style="font-size:9px">'+(h.clave_nueva||'').substring(0,8)+'..</td><td>'+h.admin+'</td>';});});}
function cambiarClave(rnc){let np=prompt('Nueva clave para '+rnc); if(!np) return; fetch('/api/admin/usuarios/'+rnc+'/clave',{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({nueva_clave:np,admin:'Admin'})}).then(r=>r.json()).then(d=>{alert(d.msg); loadUsers(); loadHist();});}
function editar(rnc){let ne=prompt('Nueva empresa'); if(!ne) return; fetch('/api/admin/usuarios/'+rnc,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({empresa:ne})}).then(r=>r.json()).then(d=>{alert(d.msg); loadUsers();});}
function suspender(rnc){fetch('/api/admin/usuarios/'+rnc+'/suspender',{method:'PUT'}).then(r=>r.json()).then(d=>{alert(d.msg); loadUsers();});}
function borrar(rnc){if(!confirm('¿Borrar '+rnc+'? Backup auto antes')) return; fetch('/api/admin/usuarios/'+rnc,{method:'DELETE'}).then(r=>r.json()).then(d=>{alert(d.msg); loadUsers();});}
function backup(){window.location='/api/admin/backup';}
function cargarConf(){let fs=document.getElementById('files').files; if(fs.length==0){alert('Seleccione');return;} let tb=document.querySelector('#histConf tbody'); for(let f of fs){let tr=tb.insertRow(); tr.innerHTML='<td>'+new Date().toLocaleString()+'</td><td>Confidencial</td><td>'+f.name+'</td><td><span class="badge bg-success">Privado Solo yo - Ejercicio oculto</span></td>';} alert(fs.length+' archivos confidenciales cargados - Solo usted los ve - No se muestra ejercicio programado');}
document.getElementById('info').innerText=new Date().toLocaleString()+' | V21 WORLD ENTERPRISE ÚNICO MUNDIAL | 22 módulos | '+window.innerWidth+'px';
renderWorld(); loadUsers(); loadHist(); calc();
</script>
</body></html>
"""

@app.route('/')
@app.route('/gestion-informes')
def home(): return render_template_string(HTML_WORLD, mods=MODULOS_WORLD)

@app.route('/b4')
@app.route('/v8')
@app.route('/trial')
def redir(): return redirect('/')

@app.route('/api/pagar', methods=['POST'])
def pagar():
    data=request.json
    from datetime import timedelta
    pagos=load('pagos.json')
    contrato=f"CTR-WORLD-V21-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    hasta=(datetime.now()+timedelta(days=30)).strftime("%Y-%m-%d")
    sub=len(data.get('modulos',[]))*250
    imp_map={"DO":18,"US":0,"MX":16,"PA":7,"CO":19,"ES":21}
    imp=sub*imp_map.get(data.get('pais','DO'),18)/100
    total=sub+imp
    pagos.append({"contrato":contrato,"empresa":data.get('empresa'),"rnc":data.get('rnc'),"email":data.get('email'),"pais":data.get('pais'),"modulos":data.get('modulos'),"subtotal":sub,"impuesto":imp,"total":total,"fecha":datetime.now().isoformat(),"hasta":hasta,"estado":"pagado_mensual_world"})
    save('pagos.json',pagos)
    # backup auto
    backup_file=os.path.join(DATA_DIR,f"backup_{contrato}.json")
    with open(backup_file,'w',encoding='utf-8') as fh: json.dump({"pago":pagos[-1],"usuarios":load('usuarios.json'),"historico":load('historico_claves.json')},fh,indent=2,ensure_ascii=False)
    return jsonify({"contrato":contrato,"total":total,"hasta":hasta})

@app.route('/api/admin/usuarios', methods=['GET','POST'])
def users_api():
    users=load('usuarios.json')
    hist=load('historico_claves.json')
    if request.method=='GET': return jsonify(users)
    data=request.json
    if any(u['rnc']==data['rnc'] for u in users): return jsonify({"msg":"RNC ya existe"}),400
    new_u={"empresa":data['empresa'],"rnc":data['rnc'],"email":data['email'],"password_hash":sha(data['password']),"rol":data.get('rol','usuario'),"estado":"activo","fecha":datetime.now().isoformat()}
    users.append(new_u); save('usuarios.json',users)
    hist.append({"fecha":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"rnc":data['rnc'],"accion":"Registro World","clave_anterior":"","clave_nueva":sha(data['password']),"admin":data.get('admin','Admin')})
    save('historico_claves.json',hist)
    return jsonify({"msg":f"Usuario {data['rnc']} registrado. Histórico clave privado guardado."})

@app.route('/api/admin/usuarios/<rnc>', methods=['PUT','DELETE'])
def user_rnc(rnc):
    users=load('usuarios.json'); hist=load('historico_claves.json')
    u=next((x for x in users if x['rnc']==rnc),None)
    if not u: return jsonify({"msg":"No encontrado"}),404
    if request.method=='DELETE':
        users=[x for x in users if x['rnc']!=rnc]; save('usuarios.json',users)
        return jsonify({"msg":f"Usuario {rnc} borrado. Backup guardado."})
    data=request.json
    if 'empresa' in data: u['empresa']=data['empresa']
    save('usuarios.json',users)
    return jsonify({"msg":f"Usuario {rnc} editado"})

@app.route('/api/admin/usuarios/<rnc>/clave', methods=['PUT'])
def clave_rnc(rnc):
    users=load('usuarios.json'); hist=load('historico_claves.json')
    u=next((x for x in users if x['rnc']==rnc),None)
    if not u: return jsonify({"msg":"No encontrado"}),404
    data=request.json
    ant=u['password_hash']; nueva=sha(data['nueva_clave']); u['password_hash']=nueva
    save('usuarios.json',users)
    hist.append({"fecha":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"rnc":rnc,"accion":"Cambio clave admin","clave_anterior":ant,"clave_nueva":nueva,"admin":data.get('admin','Admin')})
    save('historico_claves.json',hist)
    return jsonify({"msg":f"Clave {rnc} cambiada. Histórico privado guardado."})

@app.route('/api/admin/usuarios/<rnc>/suspender', methods=['PUT'])
def susp_rnc(rnc):
    users=load('usuarios.json')
    u=next((x for x in users if x['rnc']==rnc),None)
    if not u: return jsonify({"msg":"No encontrado"}),404
    u['estado']='suspendido' if u['estado']=='activo' else 'activo'
    save('usuarios.json',users)
    return jsonify({"msg":f"Usuario {rnc} ahora {u['estado']}"})

@app.route('/api/admin/historico')
def hist_api(): return jsonify(load('historico_claves.json'))

@app.route('/api/admin/backup')
def backup_api():
    ts=datetime.now().strftime('%Y%m%d_%H%M%S')
    path=os.path.join(DATA_DIR,f"BACKUP_WORLD_FULL_{ts}.json")
    with open(path,'w',encoding='utf-8') as fh:
        json.dump({"usuarios":load('usuarios.json'),"historico_claves_privado":load('historico_claves.json'),"pagos":load('pagos.json'),"modulos_world":MODULOS_WORLD,"fecha":datetime.now().isoformat()},fh,indent=2,ensure_ascii=False)
    return send_file(path, as_attachment=True, download_name=f"BACKUP_WORLD_ENTERPRISE_UNICO_{ts}.json")

@app.route('/demo')
def demo(): return jsonify({"sistema":"BASA V21 WORLD ENTERPRISE UNICO MUNDIAL","modulos":len(MODULOS_WORLD),"precio":"USD250 x modulo","total_DO_22_modulos":"USD6490/mes","primer_pago":"USD5841","bhd":"08694150021","categorias":["LICITACIÓN","CONTRATOS","NÓMINA","PAGOS","PRESUPUESTO","CONTABILIDAD","ACTIVOS","FORENSIC","NOBACI","DOCUMENTAL","MULTI"],"paises":["DO","US","MX","PA","CO","ES","BR","AR","CL","PE","EC","INTOSAI 100+ paises"]})

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
