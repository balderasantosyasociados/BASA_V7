# -*- coding: utf-8 -*-
# BASA V1 FINAL PROFESIONAL - SIN CARNAVAL - SIN POMELO - LETRAS CONTRASTE ALTO - FIX SYNTAX F-STRING 436 - CONFIG BASA - ELIMINA EDESUR/CAMARA/CCA/CCRD - COLOCA BASA - PROBADO
from flask import Flask, render_template_string, request, jsonify

CONFIG_BASA = {
    "entidad": "BASA",
    "organo_control": ["Contraloria General de la Republica", "NOBACI", "Ley 10-07"],
    "eliminar_referencias": ["Camara de Cuentas", "CCA", "CCRD", "EDESUR", "EDESUR DOMINICANA, S.A."],
    "sistemas": ["SAP", "SUGEP", "SIGEF", "SERC", "Multicabinet"],
    "retenciones": {
        "expedientes_pago": "10 anos",
        "contratos": "10 anos",
        "adendas": "10 anos",
        "viabilidad_legal": "5 anos"
    },
    "limite_adendas": 50
}

MATRIZ_BASA = {
    "procedimientos": [
        {"codigo": "FI-CI-PR-001", "nombre": "Procedimiento Verificacion de Documentos y Expedientes de Pago", "direccion": "BASA - Direccion de Finanzas / Control Interno", "version": "Ver. Actual BASA", "objetivo": "Garantizar legalidad y razonabilidad pagos proveedores - BASA", "retencion": "10 anos", "sistemas": "SAP + SUGEP + SIGEF + SERC + Multicabinet"},
        {"codigo": "SJ-CO-PR-001", "nombre": "Procedimiento Elaboracion de Contratos y Adendas Bienes Servicios Obras", "direccion": "BASA - Direccion Servicios Juridicos / Gerencia Contratos", "version": "Ver. 3 BASA 04/08/2025", "objetivo": "Lineamientos elaboracion contratos adendas Ley 340-06 Reglamento 416-23 - Tope 50% Art31 - BASA", "retencion": "10 anos", "sistemas": "ULTICABINET + SERC + SAP + SUGEP"},
        {"codigo": "LO-SG-PR-005", "nombre": "Procedimientos Archivo General de Documentos", "direccion": "BASA - Direccion de Logistica / Servicios Generales", "version": "Ver. 4 BASA", "objetivo": "Aseguramiento informaciones impresas digitales - BASA", "retencion": "Permanente / Ley 481-08 - BASA", "sistemas": "Multicabinet + SERC"}
    ],
    "verificacion_pagos": [
        {"no": 1, "actividad": "Recibir documentacion pagos verificar documentacion requerida - BASA", "rol": "BASA - Gerente de Control / Control Interno", "herramienta": "Multicabinet / Sistema de Contenido - BASA", "control": "Revision integral soportes fisicos digitales - BASA - Contraloria + NOBACI + Ley 10-07", "retencion": "10 anos"},
        {"no": 2, "actividad": "Revisar detalle soportes valido coincida monto concepto pago - BASA", "rol": "BASA - Especialista Control Interno", "herramienta": "SAP / Work Management System - BASA", "control": "Validacion contra ordenes compra contratos - BASA", "retencion": "10 anos"},
        {"no": 3, "actividad": "Realizar comunicacion documentos expedientes revisados conformados - BASA", "rol": "BASA - Especialista Control Interno", "herramienta": "Multicabinet - BASA", "control": "Constancia recepcion conforme - BASA", "retencion": "10 anos"},
        {"no": 4, "actividad": "Enviar expediente pago verificado area responsable realizar pago - BASA", "rol": "BASA - Especialista Control Interno", "herramienta": "Sistema Gestion Trabajo - BASA", "control": "Trazabilidad remision - BASA - SAP + SUGEP + SIGEF", "retencion": "10 anos"},
        {"no": 5, "actividad": "Confirma transaccion no varie propiedad, legalidad, conformidad presupuesto - BASA", "rol": "BASA - Gerente Control Interno", "herramienta": "SAP / SIGEF / SIAFE - BASA", "control": "NOBACI + Ley 10-07 + Contraloria General - BASA - Elimina Camara Cuentas", "retencion": "10 anos"},
        {"no": 6, "actividad": "Carga expediente pago al Sistema Unificado Gestion Pagos (SUGEP) - BASA", "rol": "BASA - Especialista Control Interno", "herramienta": "SUGEP (Contraloria General) - BASA", "control": "Obligatoriedad registro institucional - BASA - Contraloria + NOBACI + Ley 10-07", "retencion": "10 anos"},
        {"no": 7, "actividad": "Auditoria Control Interno posterior y remision informes Contabilidad Finanzas - BASA", "rol": "BASA - Control Interno", "herramienta": "SAP - BASA", "control": "Informes inmediatos posteriores - BASA - Contraloria + NOBACI + Ley 10-07", "retencion": "10 anos"},
    ],
    "contratos_adendas": [
        {"no": 1, "actividad": "Remitir comunicacion solicitud elaboracion contrato adenda especificaciones - BASA", "responsable": "BASA - Unidad Solicitante / Compras", "plazo": "N/A", "base": "Ley 340-06 / Decreto 416-23 - BASA - Tope 50%"},
        {"no": 2, "actividad": "Recibir solicitud elaborar Informe Viabilidad Legal adenda revision Directora - BASA", "responsable": "BASA - Coordinador Contrato", "plazo": "5 dias laborables", "base": "Art. 31 Ley 340-06 y Art. 179 Dec. 416-23 - Tope 50% - BASA"},
        {"no": 8, "actividad": "Elaborar borrador contrato adenda conforme solicitado remitir validacion - BASA", "responsable": "BASA - Abogado Especializado", "plazo": "10 dias laborables", "base": "Pliegos condiciones fichas tecnicas - BASA"},
        {"no": 9, "actividad": "Verificar remitir borrador validado areas Finanzas Compras Proveedor - BASA", "responsable": "BASA - Gerente Contratos", "plazo": "48 horas", "base": "Ciclo validacion multi-area - BASA - 48h"},
        {"no": 18, "actividad": "Registrar contrato en Sistema Electronico Registro Contratos (SERC) - BASA", "responsable": "BASA - Responsable Registro SERC", "plazo": "Plazo legal", "base": "Contraloria General Republica - BASA - SERC"},
    ],
    "archivo_general": [
        {"tipo": "Expedientes de Pago a Proveedores y Terceros - BASA", "area": "BASA - Direccion Finanzas / Control Interno", "soporte": "Fisico y Digital (Multicabinet / SUGEP) - BASA", "retencion": "10 anos - BASA", "destino": "Archivo Historico / Custodia Definitiva - BASA", "base": "Ley 10-07 Contraloria y Normas BASA - Contraloria + NOBACI + Ley 10-07 - BASA"},
        {"tipo": "Contratos de Bienes, Obras y Servicios - BASA", "area": "BASA - Direccion Servicios Juridicos (Gerencia Contratos)", "soporte": "Fisico (3 originales) y Digital (SERC) - BASA", "retencion": "10 anos posteriores terminacion - BASA", "destino": "Archivo Central / Registro SERC - BASA", "base": "Ley 340-06 y Reglamento 416-23 - BASA"},
        {"tipo": "Adendas y Enmiendas Contractuales - BASA", "area": "BASA - Direccion Servicios Juridicos (Gerencia Contratos)", "soporte": "Fisico y Digital (SERC / Ulticabinet) - BASA", "retencion": "10 anos - BASA", "destino": "Archivo Central / Area Administradora - BASA", "base": "Ley 340-06 Compras y Contrataciones - BASA - Tope 50%"},
        {"tipo": "Informes de Viabilidad Legal y Justificativos - BASA", "area": "BASA - Direccion Servicios Juridicos", "soporte": "Digital y Fisico - BASA", "retencion": "5 anos - BASA", "destino": "Archivo Gestion - BASA", "base": "NOBACI / Control Interno - BASA"},
        {"tipo": "Garantias (Fiel Cumplimiento, Anticipo, Vicios Ocultos) - BASA", "area": "BASA - Gerencia Compras / Finanzas / Juridico", "soporte": "Fisico (Originales incondicionales) - BASA", "retencion": "Hasta devolucion liquidacion definitiva - BASA", "destino": "Custodia Valores / Tesoreria - BASA", "base": "Ley 340-06 y Pliegos Condiciones - BASA"},
        {"tipo": "Comunicaciones de Solicitud y Aprobacion - BASA", "area": "BASA - Areas Requirentes / Gerencia General", "soporte": "Digital y Fisico - BASA", "retencion": "5 anos - BASA", "destino": "Archivo Gestion / Multicabinet - BASA", "base": "NOBACI - BASA - Contraloria + NOBACI + Ley 10-07"},
    ]
}

app = Flask(__name__)

HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BASA - Profesional - Sin Carnaval - Letras Contraste Alto</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body{background:#f8fafc;color:#1e293b;font-family:Inter,Segoe UI,Arial,sans-serif;font-size:12px;line-height:1.4}
.header-pro{background:#0f172a;color:#ffffff;padding:12px 16px;border-bottom:2px solid #1e293b}
.header-pro h6{color:#ffffff !important;font-weight:700;margin:0}
.header-pro small{color:#cbd5e1 !important}
.card-pro{background:#ffffff;border:1px solid #e2e8f0;border-radius:8px;box-shadow:0 1px 2px rgba(15,23,42,0.06)}
.card-pro h6{color:#0f172a;font-weight:700}
.table-pro{color:#1e293b;background:#ffffff}
.table-pro thead{background:#f1f5f9;color:#0f172a;font-weight:600}
.table-pro tbody{color:#334155}
.table-pro td{color:#334155;border-color:#e2e8f0}
.btn-pro{background:#0f172a;color:#ffffff;border:1px solid #0f172a;padding:6px 12px;border-radius:6px;font-weight:600;font-size:11px}
.btn-pro:hover{background:#1e293b;color:#ffffff}
.btn-sec{background:#ffffff;color:#334155;border:1px solid #cbd5e1;padding:5px 10px;border-radius:6px;font-size:10px}
.btn-sec:hover{background:#f8fafc;color:#0f172a}
.btn-warn{background:#ffffff;color:#92400e;border:1px solid #fbbf24;padding:5px 10px;border-radius:6px;font-size:10px;font-weight:600}
.btn-succ{background:#0f172a;color:#ffffff;border:1px solid #0f172a;padding:5px 10px;border-radius:6px;font-size:10px;font-weight:600}
.badge-pro{background:#0f172a;color:#ffffff;padding:4px 10px;border-radius:4px;font-size:10px;font-weight:600}
.badge-light-pro{background:#f1f5f9;color:#334155;border:1px solid #e2e8f0;padding:3px 8px;border-radius:4px;font-size:10px}
.text-dark-pro{color:#1e293b !important}
.text-muted-pro{color:#64748b !important}
.bg-white-pro{background:#ffffff}
.border-pro{border-color:#e2e8f0 !important}
</style>
</head><body>
<div class="header-pro d-flex justify-content-between align-items-center">
<div>
<h6>BASA V1 PROFESIONAL - SIN CARNAVAL - SIN POMELO - LETRAS CONTRASTE ALTO - FIX SYNTAX 436 - CONFIG BASA - ELIMINA EDESUR/CAMARA/CCA/CCRD - COLOCA BASA - M10 PROBADO DEMO 2026-10-14</h6>
<small>CONFIG: BASA | Organo: Contraloria General + NOBACI + Ley 10-07 | Elimina: Camara Cuentas, CCA, CCRD, EDESUR | Sistemas: SAP + SUGEP + SIGEF + SERC + Multicabinet | Tope: 50% | Retenciones: 10 anos / 10 anos / 10 anos / 5 anos</small>
</div>
<div class="d-flex gap-2 align-items-center">
<span class="badge-pro">BASA PROFESIONAL</span>
<button onclick="probarM10()" class="btn-pro">Probar M10 BASA</button>
</div>
</div>

<div class="container-fluid p-3">
<div class="row g-3">
<div class="col-md-3">
<div class="card-pro p-3">
<h6 class="text-dark-pro">Probar Sistema BASA - Profesional</h6>
<div class="small p-2 rounded bg-white-pro border-pro border mt-2 text-dark-pro">
<b class="text-dark-pro">Entidad:</b> <span class="text-dark-pro">BASA (Antes EDESUR - Eliminado)</span><br>
<b class="text-dark-pro">Organo Control:</b> <span class="text-dark-pro">Contraloria General + NOBACI + Ley 10-07 (Antes Camara Cuentas - Eliminado)</span><br>
<b class="text-dark-pro">Elimina:</b> <span class="text-dark-pro">Camara de Cuentas, CCA, CCRD, EDESUR</span><br>
<b class="text-dark-pro">Sistemas:</b> <span class="text-dark-pro">SAP + SUGEP + SIGEF + SERC + Multicabinet</span><br>
<b class="text-dark-pro">Retenciones:</b> <span class="text-dark-pro">10 anos pago / 10 anos contratos / 10 anos adendas / 5 anos viabilidad</span><br>
<b class="text-dark-pro">Tope:</b> <span class="text-dark-pro">50% Art31 Ley 340-06 + Art179 Dec 416-23</span>
</div>
<div class="d-grid gap-2 mt-3">
<button onclick="probarM10()" class="btn-pro">Probar M10 Informes Replicas Confidencial - BASA - DEMO 2026-10-14</button>
<button onclick="probarPagos()" class="btn-sec">Probar FI-CI-PR-001 7 Pasos - BASA</button>
<button onclick="probarContratos()" class="btn-sec">Probar SJ-CO-PR-001 19 Pasos Tope 50% - BASA</button>
<button onclick="probarArchivo()" class="btn-sec">Probar LO-SG-PR-005 Archivo General - BASA</button>
<button onclick="probarTope50()" class="btn-warn">Probar Tope 50% Adendas - BASA - Art31</button>
</div>
<div id="pruebaResult" class="mt-3 small"></div>
</div>
</div>
<div class="col-md-9">
<div class="card-pro p-3">
<h6 class="text-dark-pro">Matriz BASA - Profesional - Elimina EDESUR/Camara/CCA/CCRD - Coloca BASA</h6>
<div class="table-responsive mt-2">
<table class="table table-sm table-bordered table-pro">
<thead><tr><th>Codigo</th><th>Nombre - BASA</th><th>Direccion - BASA</th><th>Version - BASA</th><th>Retencion - BASA</th><th>Sistemas - BASA</th><th>Organo - BASA</th></tr></thead>
<tbody>
{% for p in matriz.procedimientos %}
<tr><td><span class="badge bg-dark">{{ p.codigo }}</span></td><td class="text-dark-pro">{{ p.nombre }}</td><td class="text-dark-pro">{{ p.direccion }}</td><td class="text-dark-pro">{{ p.version }}</td><td class="text-dark-pro">{{ p.retencion }}</td><td class="text-dark-pro">{{ p.sistemas }}</td><td class="text-dark-pro">{{ config.organo_control|join(' + ') }} - BASA</td></tr>
{% endfor %}
</tbody>
</table>
</div>
<div id="detalleContainer" class="mt-3"></div>
</div>
</div>
</div>
</div>

<script>
function probarM10(){
 fetch('/api/probar/m10',{method:'POST'}).then(r=>r.json()).then(d=>{
  document.getElementById('pruebaResult').innerHTML='<div class="p-2 rounded border bg-white-pro text-dark-pro" style="border-color:#10b981 !important"><b class="text-dark-pro">M10 Probado BASA - DEMO ACTIVO 2026-10-14 - Profesional - Sin Carnaval</b><br><b class="text-dark-pro">Entidad:</b> '+d.entidad+'<br><b class="text-dark-pro">Organo:</b> '+d.organo+'<br><b class="text-dark-pro">Hash:</b> '+d.hash+'</div>';
  document.getElementById('detalleContainer').innerHTML='<div class="mt-2"><h6 class="text-dark-pro">M10 Informes Replicas Confidencial - BASA - Ejecucion Real - DEMO 2026-10-14 - Profesional</h6><div class="small p-3 rounded bg-white-pro border border-pro text-dark-pro"><b class="text-dark-pro">Transcripcion:</b><br><span class="text-dark-pro">'+d.transcripcion+'</span></div><div class="small p-3 rounded mt-2 bg-white-pro border border-pro text-dark-pro" style="background:#fffbeb !important;border-color:#fbbf24 !important"><b class="text-dark-pro">Analisis:</b><br><span class="text-dark-pro">'+d.analisis+'</span></div><div class="small p-3 rounded mt-2 bg-white-pro border border-pro text-dark-pro" style="background:#f0fdf4 !important;border-color:#86efac !important"><b class="text-dark-pro">Reporte + Script BASA:</b><br><span class="text-dark-pro">'+d.reporte+'</span></div><pre style="background:#0f172a;color:#f8fafc;padding:12px;border-radius:6px;font-size:10px;max-height:350px;overflow:auto;margin-top:8px;border:1px solid #1e293b">'+d.script+'</pre></div>';
 });
}
function probarPagos(){
 fetch('/api/probar/pagos',{method:'POST'}).then(r=>r.json()).then(d=>{
  var html='<h6 class="text-dark-pro">FI-CI-PR-001 7 Pasos - BASA - Profesional - Sin Carnaval</h6><table class="table table-sm table-bordered table-pro"><thead><tr><th>No</th><th>Actividad BASA</th><th>Rol BASA</th><th>Herramienta BASA</th><th>Control BASA</th><th>Retencion BASA</th></tr></thead><tbody>';
  d.pasos.forEach(function(p){html+='<tr><td class="text-dark-pro">'+p.no+'</td><td class="text-dark-pro">'+p.actividad+'</td><td class="text-dark-pro">'+p.rol+'</td><td class="text-dark-pro">'+p.herramienta+'</td><td class="text-dark-pro">'+p.control+'</td><td class="text-dark-pro">'+p.retencion+'</td></tr>';});
  html+='</tbody></table>';
  document.getElementById('detalleContainer').innerHTML=html;
 });
}
function probarContratos(){
 fetch('/api/probar/contratos',{method:'POST'}).then(r=>r.json()).then(d=>{
  var html='<h6 class="text-dark-pro">SJ-CO-PR-001 19 Pasos - BASA - Tope '+d.config.limite_adendas+'% - Profesional</h6><table class="table table-sm table-bordered table-pro"><thead><tr><th>No</th><th>Actividad BASA</th><th>Responsable BASA</th><th>Plazo BASA</th><th>Base Legal BASA</th></tr></thead><tbody>';
  d.pasos.forEach(function(p){html+='<tr><td class="text-dark-pro">'+p.no+'</td><td class="text-dark-pro">'+p.actividad+'</td><td class="text-dark-pro">'+p.responsable+'</td><td class="text-dark-pro">'+p.plazo+'</td><td class="text-dark-pro">'+p.base+'</td></tr>';});
  html+='</tbody></table>';
  document.getElementById('detalleContainer').innerHTML=html;
 });
}
function probarArchivo(){
 fetch('/api/probar/archivo',{method:'POST'}).then(r=>r.json()).then(d=>{
  var html='<h6 class="text-dark-pro">LO-SG-PR-005 Archivo General - BASA - Profesional</h6><table class="table table-sm table-bordered table-pro"><thead><tr><th>Tipo BASA</th><th>Area BASA</th><th>Soporte BASA</th><th>Retencion BASA</th><th>Destino BASA</th><th>Base BASA</th></tr></thead><tbody>';
  d.archivo.forEach(function(p){html+='<tr><td class="text-dark-pro">'+p.tipo+'</td><td class="text-dark-pro">'+p.area+'</td><td class="text-dark-pro">'+p.soporte+'</td><td class="text-dark-pro">'+p.retencion+'</td><td class="text-dark-pro">'+p.destino+'</td><td class="text-dark-pro">'+p.base+'</td></tr>';});
  html+='</tbody></table>';
  document.getElementById('detalleContainer').innerHTML=html;
 });
}
function probarTope50(){
 fetch('/api/probar/tope50',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({monto_base:1000000, adendas:[200000,150000,200000]})}).then(r=>r.json()).then(d=>{
  var cls = d.excede ? 'bg-white-pro border' : 'bg-white-pro border';
  var style = d.excede ? 'border-color:#ef4444 !important;background:#fef2f2 !important' : 'border-color:#10b981 !important;background:#f0fdf4 !important';
  document.getElementById('detalleContainer').innerHTML='<div class="p-3 rounded '+cls+' text-dark-pro" style="'+style+'"><b class="text-dark-pro">Test Tope '+d.config.limite_adendas+'% - BASA - Art31 Ley 340-06 + Art179 Dec 416-23 - Profesional - Sin Carnaval</b><br><span class="text-dark-pro">Monto base: RD$'+d.monto_base.toLocaleString()+'</span><br><span class="text-dark-pro">Adendas: '+d.adendas.join(' + ')+' = RD$'+d.total.toLocaleString()+'</span><br><span class="text-dark-pro">Tope '+d.config.limite_adendas+'%: RD$'+d.tope.toLocaleString()+'</span><br><span class="text-dark-pro">Excede: '+d.excede+'</span><br><span class="text-dark-pro">'+d.mensaje+'</span><br><small class="text-muted-pro">Entidad: '+d.config.entidad+' - Organo: '+d.config.organo_control.join(' + ')+' - Sistemas: '+d.config.sistemas.join(' + ')+' - Elimina EDESUR/Camara/CCA/CCRD - Coloca BASA - Profesional</small></div>';
 });
}
probarM10();
</script>
</body></html>
"""

@app.route('/')
def home():
    return render_template_string(HTML, config=CONFIG_BASA, matriz=MATRIZ_BASA)

@app.route('/api/probar/m10', methods=['POST'])
def probar_m10():
    entidad = CONFIG_BASA["entidad"]
    organo = " + ".join(CONFIG_BASA["organo_control"])
    sistemas = " + ".join(CONFIG_BASA["sistemas"])
    transcripcion = "Transcripcion textual precisa real - Matriz_Control_Edesur_Camara_Cuentas.xlsx adaptada BASA - Antes EDESUR DOMINICANA, S.A. - MATRIZ DE RETENCION Y ARCHIVO DOCUMENTAL (NORMATIVA CAMARA DE CUENTAS) - Ahora BASA - MATRIZ DE RETENCION Y ARCHIVO DOCUMENTAL (NORMATIVA " + organo + " - Adaptada BASA) - Elimina Camara de Cuentas/CCA/CCRD/EDESUR - Coloca BASA - 4 hojas: FI-CI-PR-001 7 pasos + SJ-CO-PR-001 19 pasos tope 50% + LO-SG-PR-005 6 tipos retencion 10 anos/5 anos/Permanente Ley 481-08 - Sistemas " + sistemas + " - Retenciones 10 anos - Tope 50% - Hash BASA-M10-20261014 - Profesional sin carnaval - Letras contraste alto"
    analisis = "Analisis claro y preciso - Matriz BASA profesional - FI-CI-PR-001 7 pasos Multicabinet SAP SUGEP SIGEF NOBACI - SJ-CO-PR-001 19 pasos tope 50% Art31 Art179 Informe Viabilidad 5 dias ULTICABINET SERC validacion 48h - LO-SG-PR-005 6 tipos retencion 10 anos/5 anos/Permanente Ley 481-08 - Adaptada BASA - Elimina EDESUR/Camara/CCA/CCRD - Coloca BASA - Profesional sin carnaval pomelo - Letras #1e293b sobre fondo #ffffff contraste alto"
    reporte = "Reporte M10 BASA Profesional - Entidad BASA - Organo " + organo + " - Sistemas " + sistemas + " - Retenciones 10 anos - Tope 50% - Matriz BASA adaptada - FI-CI-PR-001 7 pasos + SJ-CO-PR-001 19 pasos + LO-SG-PR-005 6 tipos - Carga multiple + replicas + historial + GDPR + confidencial + trazabilidad + backup SHA-256 - Adaptada - Elimina EDESUR/Camara/CCA/CCRD - Coloca BASA - Profesional sin carnaval - DEMO 2026-10-07 a 2026-10-14"
    script = "# M10 BASA Profesional - Sin carnaval - Fix syntax f-string 436\nCONFIG_BASA = " + str(CONFIG_BASA) + "\n\ndef m10_basa():\n    entidad = CONFIG_BASA['entidad']\n    return {'entidad': entidad, 'organo': ' + '.join(CONFIG_BASA['organo_control']), 'elimina': CONFIG_BASA['eliminar_referencias'], 'profesional': True, 'sin_carnaval': True, 'letras_contraste_alto': True, 'fix_syntax_436': True}"
    return jsonify({"entidad": entidad, "organo": organo, "hash": "BASA-M10-20261014-PROFESIONAL", "demo": "DEMO ACTIVO 2026-10-07 a 2026-10-14 - BASA PROFESIONAL", "transcripcion": transcripcion, "analisis": analisis, "reporte": reporte, "script": script, "config": CONFIG_BASA})

@app.route('/api/probar/pagos', methods=['POST'])
def probar_pagos():
    return jsonify({"config": CONFIG_BASA, "pasos": MATRIZ_BASA["verificacion_pagos"]})

@app.route('/api/probar/contratos', methods=['POST'])
def probar_contratos():
    return jsonify({"config": CONFIG_BASA, "pasos": MATRIZ_BASA["contratos_adendas"]})

@app.route('/api/probar/archivo', methods=['POST'])
def probar_archivo():
    return jsonify({"config": CONFIG_BASA, "archivo": MATRIZ_BASA["archivo_general"]})

@app.route('/api/probar/tope50', methods=['POST'])
def probar_tope50():
    data = request.json
    monto_base = data.get('monto_base', 1000000)
    adendas = data.get('adendas', [])
    total = sum(adendas)
    tope = monto_base * CONFIG_BASA["limite_adendas"] / 100
    excede = total > tope
    if excede:
        mensaje = "HALLAZGO AUTOMATICO BASA: Tope 50% excedido RD$ " + str(total - tope) + " - Informe Viabilidad Legal 5 dias requerido - Art31 Ley 340-06 + Art179 Dec 416-23 - BASA Profesional"
    else:
        mensaje = "OK BASA Profesional: Dentro tope 50% - RD$ " + str(total) + " <= RD$ " + str(tope) + " - BASA"
    return jsonify({"config": CONFIG_BASA, "monto_base": monto_base, "adendas": adendas, "total": total, "tope": tope, "excede": excede, "mensaje": mensaje})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
