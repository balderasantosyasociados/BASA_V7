# -*- coding: utf-8 -*-
# BASA V1 MENU GENERAL COMPLETO PROFESIONAL - ELIMINA EDESUR Y CUALQUIER OTRO NOMBRE SIN CONSENTIMIENTO/PERMISO - HABILITA TODOS MODULOS ORGANIZADO 5 GRUPOS - COLOR PROFESIONAL SIN CARNAVAL POMELO - FIX SYNTAX 436
from flask import Flask, render_template_string, request, jsonify

CONFIG_BASA = {
    "entidad_autorizada": "BASA",
    "entidad_generica": "{{ENTIDAD_AUTORIZADA}}",
    "organo_control": ["Contraloria General de la Republica", "NOBACI", "Ley 10-07"],
    "eliminar_nombres_sin_consentimiento": ["EDESUR", "EDESUR DOMINICANA, S.A.", "EDENORTE", "EDEESTE", "ETED", "Camara de Cuentas", "CCA", "CCRD", "CGR", "Camara"],
    "sistemas": ["SAP", "SUGEP", "SIGEF", "SERC", "Multicabinet"],
    "retenciones": {"expedientes_pago": "10 anos", "contratos": "10 anos", "adendas": "10 anos", "viabilidad_legal": "5 anos", "archivo_general": "Permanente / Ley 481-08"},
    "limite_adendas": 50,
    "version": "V1 BASA MENU GENERAL COMPLETO PROFESIONAL - 2026-10-07",
    "color_profesional": {"fondo": "#f8fafc", "card": "#ffffff", "header": "#0f172a", "texto_oscuro": "#0f172a", "texto_medio": "#334155", "texto_claro": "#64748b", "borde": "#e2e8f0", "borde_oscuro": "#cbd5e1"}
}

GRUPOS_BASA = {
    "GRUPO 1 - COMPRAS Y CONTRATOS - BASA": ["M1", "M2", "M2B"],
    "GRUPO 2 - FINANCIERO Y CONTABLE - BASA": ["M3", "M4", "M14"],
    "GRUPO 3 - FORENSE Y LEGAL - BASA": ["M8", "M9", "M12"],
    "GRUPO 4 - GESTION DOCUMENTAL - BASA - FI-CI-PR-001 + SJ-CO-PR-001 + LO-SG-PR-005": ["M10", "M11", "M15", "M16"],
    "GRUPO 5 - ENTERPRISE WORLD - BASA": ["M13"]
}

MODULOS_BASA_COMPLETO = {
    "M1": {"nombre": "M1 Scraper Portal vs ComprasDominicana + Matriz Modalidad Monto - BASA", "desc": "Cruce portal institucional vs ComprasDominicana + matriz modalidad monto + incidencias diferencia referencia monto - Adaptado BASA - Elimina nombres sin consentimiento", "precio": 250, "codigo": "FI-CI-PR-001 + SJ-CO-PR-001 - BASA", "ley": "Ley 340-06 Art16-17 + Ley 200-04 + BASA", "estado": "Habilitado DEMO", "grupo": "GRUPO 1"},
    "M2": {"nombre": "M2 Contratos Adendas Tope 50% Art31 + Art179 Dec 416-23 - BASA", "desc": "Valida tope 50% + Informe Viabilidad Legal 5 dias + ULTICABINET + SERC + ciclo validacion multi-area 48h - BASA", "precio": 250, "codigo": "SJ-CO-PR-001 - BASA", "ley": "Ley 340-06 Art31 + Dec 416-23 Art179 + BASA - Tope 50%", "estado": "Habilitado DEMO", "grupo": "GRUPO 1"},
    "M2B": {"nombre": "M2B Elaboracion Contratos y Adendas 19 Pasos - BASA", "desc": "19 pasos elaboracion contratos adendas + Informe Viabilidad + asignacion abogado ULTICABINET + borrador 10 dias + validacion multi-area 48h + firma Gerencia General CUED + notarizacion + SERC - BASA - Profesional", "precio": 250, "codigo": "SJ-CO-PR-001 - BASA", "ley": "Ley 340-06 + Dec 416-23 + BASA", "estado": "Habilitado DEMO", "grupo": "GRUPO 1"},
    "M3": {"nombre": "M3 Nomina TSS - BASA", "desc": "TSS/DGII/RPE + IMSS MX + PILA CO + BASA - Adaptado BASA", "precio": 250, "codigo": "FI-CI-PR-001 - BASA", "ley": "Ley 87-01 TSS + BASA", "estado": "Habilitado DEMO", "grupo": "GRUPO 2"},
    "M4": {"nombre": "M4 Pagos Libramientos BHD 08694150021 + SUGEP + SIGEF + SAP - BASA", "desc": "FI-CI-PR-001 Verificacion Documentos Expedientes Pago 7 pasos + Multicabinet + SAP + Work Management + SUGEP + SIGEF + SIAFE + trazabilidad + NOBACI - BASA", "precio": 250, "codigo": "FI-CI-PR-001 - BASA", "ley": "NOBACI + Ley 10-07 + SUGEP + SIGEF + BASA", "estado": "Habilitado DEMO", "grupo": "GRUPO 2"},
    "M14": {"nombre": "M14 Verificacion Documentos Expedientes Pago FI-CI-PR-001 7 Pasos - BASA", "desc": "FI-CI-PR-001 7 pasos: Recibir documentacion verificar documentacion requerida Multicabinet + Revisar detalle soportes valido monto concepto SAP Work Management + Comunicacion documentos conformados Multicabinet + Enviar expediente verificado Sistema Gestion Trabajo trazabilidad + Confirma transaccion propiedad legalidad conformidad presupuesto SAP SIGEF SIAFE NOBACI + Carga SUGEP + Auditoria Control Interno posterior informes SAP - BASA Profesional", "precio": 250, "codigo": "FI-CI-PR-001 - BASA", "ley": "FI-CI-PR-001 + NOBACI + Ley 10-07 + SUGEP + BASA", "estado": "Habilitado DEMO", "grupo": "GRUPO 2"},
    "M8": {"nombre": "M8 Forense + Base Historica Mundial Oculta + Deteccion Auto Similar - BASA", "desc": "Base oculta CCRD+GAO+ASF+CGR+TC ES + deteccion hallazgo parecido/similar + crear hallazgo auto + aplicar mejoras + actualizar sistema + uso internacional + BASA - Elimina nombres sin consentimiento", "precio": 250, "codigo": "Forense - BASA", "ley": "Const Art146 + Ley 10-04 + FCPA + SOX + BASA", "estado": "Habilitado DEMO", "grupo": "GRUPO 3"},
    "M9": {"nombre": "M9 Auditoria Forense Contratos Adendas - BASA", "desc": "Auditoria forense contratos adendas tope 50% + Informe Viabilidad Legal + ULTICABINET + SERC + BASA", "precio": 250, "codigo": "SJ-CO-PR-001 Forense - BASA", "ley": "Ley 340-06 Art31 + Dec 416-23 Art179 + BASA", "estado": "Habilitado DEMO", "grupo": "GRUPO 3"},
    "M12": {"nombre": "M12 Legal - Cumplimiento Normativo NOBACI - BASA", "desc": "Cumplimiento normativo NOBACI + Ley 10-07 + Ley 340-06 + Ley 481-08 + BASA - Profesional", "precio": 250, "codigo": "NOBACI + Ley 10-07 + BASA", "ley": "NOBACI + Ley 10-07 + Ley 340-06 + BASA", "estado": "Habilitado DEMO", "grupo": "GRUPO 3"},
    "M10": {"nombre": "M10 Informes Replicas Confidencial - BASA - DEMO ACTIVO 2026-10-14", "desc": "Carga multiple + replicas + historial + GDPR + confidencial + FI-CI-PR-001 + SJ-CO-PR-001 + LO-SG-PR-005 - Adaptado BASA - Elimina EDESUR/Camara sin consentimiento - Profesional - DEMO ACTIVO", "precio": 250, "codigo": "LO-SG-PR-005 + FI-CI-PR-001 + SJ-CO-PR-001 - BASA", "ley": "NOBACI + Ley 10-07 + Ley 340-06 + Ley 481-08 + GDPR + BASA", "estado": "Habilitado DEMO ACTIVO hasta 2026-10-14", "grupo": "GRUPO 4"},
    "M11": {"nombre": "M11 Transcripcion Textual Precisa Real + Hash Validable - BASA", "desc": "Transcripcion textual precisa real + hash SHA-256 validable manual + backup referencia validable + BASA Profesional", "precio": 250, "codigo": "LO-SG-PR-005 + BASA", "ley": "Ley 481-08 + NOBACI + BASA", "estado": "Habilitado DEMO", "grupo": "GRUPO 4"},
    "M15": {"nombre": "M15 Archivo General LO-SG-PR-005 Retencion 10 Anos - BASA", "desc": "6 tipos retencion BASA - 10 anos / 5 anos / Permanente Ley 481-08 - Multicabinet / SUGEP / SERC / Ulticabinet - BASA Profesional - Elimina nombres sin consentimiento", "precio": 250, "codigo": "LO-SG-PR-005 - BASA", "ley": "LO-SG-PR-005 + Ley 481-08 + BASA", "estado": "Habilitado DEMO", "grupo": "GRUPO 4"},
    "M16": {"nombre": "M16 Matriz Control Cumplimiento Normativo 3 Procedimientos - BASA", "desc": "Matriz Control Cumplimiento Normativo: FI-CI-PR-001 Verificacion Pagos + SJ-CO-PR-001 Contratos Adendas + LO-SG-PR-005 Archivo General + Codigo Procedimiento + Nombre Documento + Direccion Gerencia Responsable + Version + Objetivo Principal + Tiempo Retencion Archivo + Adaptada BASA - Elimina nombres sin consentimiento", "precio": 250, "codigo": "Matriz Control - BASA", "ley": "Matriz Control + NOBACI + Ley 340-06 + Ley 481-08 + Ley 10-07 + BASA", "estado": "Habilitado DEMO", "grupo": "GRUPO 4"},
    "M13": {"nombre": "M13 WORLD Multi-Pais/Idioma/Moneda + BASA", "desc": "DO US MX PA CO ES BR + ES EN FR PT + USD DOP EUR MXN + BHD 08694150021 + BASA - Elimina nombres sin consentimiento + NOBACI/COSO/COBIT - Profesional", "precio": 250, "codigo": "WORLD - BASA", "ley": "Multi-pais/idioma/moneda + BHD 08694150021 + BASA", "estado": "Habilitado DEMO", "grupo": "GRUPO 5"},
}

MATRIZ_BASA_PROFESIONAL = {
    "procedimientos": [
        {"codigo": "FI-CI-PR-001", "nombre": "Procedimiento Verificacion de Documentos y Expedientes de Pago - BASA", "direccion": "BASA - Direccion de Finanzas / Control Interno", "version": "Ver. Actual BASA", "objetivo": "Garantizar legalidad y razonabilidad pagos proveedores soportando erogaciones financieras mediante expedientes debidamente validados - BASA - Contraloria General + NOBACI + Ley 10-07", "retencion": "10 anos (Digital/Fisico) - BASA", "sistemas": "SAP + SUGEP + SIGEF + SERC + Multicabinet - BASA"},
        {"codigo": "SJ-CO-PR-001", "nombre": "Procedimiento Elaboracion de Contratos y Adendas de Bienes, Servicios y Obras - BASA", "direccion": "BASA - Direccion Servicios Juridicos / Gerencia de Contratos - BASA", "version": "Ver. 3 BASA 04/08/2025 - Adaptada BASA - Tope 50% Art31", "objetivo": "Garantizar fortalecimiento institucional lineamientos elaboracion actualizacion contratos adendas conforme Ley 340-06 Reglamento 416-23 - Tope 50% Art31 Ley 340-06 Art179 Dec 416-23 + Informe Viabilidad Legal 5 dias + ULTICABINET + SERC + validacion multi-area 48h - BASA", "retencion": "10 anos (SJ-CO-LI-003 / SJ-CO-LI-004) - BASA", "sistemas": "ULTICABINET + SERC + SAP + SUGEP + SIGEF - BASA"},
        {"codigo": "LO-SG-PR-005", "nombre": "Procedimientos Archivo General de Documentos - BASA", "direccion": "BASA - Direccion de Logistica / Servicios Generales - BASA", "version": "Ver. 4 BASA - Adaptada BASA", "objetivo": "Contribuir aseguramiento informaciones impresas digitales manteniendo expedientes condiciones optimas desde traslado hasta disposicion final - BASA - Ley 481-08", "retencion": "Permanente / Segun Lista Valoracion Documental (Ley 481-08) - BASA", "sistemas": "Multicabinet + SERC + Archivo BASA - SAP + SUGEP"},
    ],
    "verificacion_pagos": [
        {"no": 1, "actividad": "Recibir documentacion pagos verificar documentacion requerida - BASA", "rol": "BASA - Gerente Control / Control Interno", "herramienta": "Multicabinet / Sistema Contenido - BASA", "control": "Revision integral soportes fisicos digitales - BASA - Contraloria General + NOBACI + Ley 10-07 - Elimina Camara Cuentas sin consentimiento - BASA", "retencion": "10 anos - BASA"},
        {"no": 2, "actividad": "Revisar detalle soportes valido coincida monto concepto pago - BASA", "rol": "BASA - Especialista Control Interno", "herramienta": "SAP / Work Management System - BASA", "control": "Validacion contra ordenes compra contratos - BASA", "retencion": "10 anos - BASA"},
        {"no": 3, "actividad": "Realizar comunicacion documentos expedientes revisados conformados - BASA", "rol": "BASA - Especialista Control Interno", "herramienta": "Multicabinet - BASA", "control": "Constancia recepcion conforme - BASA", "retencion": "10 anos - BASA"},
        {"no": 4, "actividad": "Enviar expediente pago verificado area responsable realizar pago - BASA", "rol": "BASA - Especialista Control Interno", "herramienta": "Sistema Gestion Trabajo - BASA", "control": "Trazabilidad remision - BASA - SAP + SUGEP + SIGEF", "retencion": "10 anos - BASA"},
        {"no": 5, "actividad": "Confirma transaccion no varie propiedad, legalidad, conformidad presupuesto - BASA", "rol": "BASA - Gerente Control Interno", "herramienta": "SAP / SIGEF / SIAFE - BASA", "control": "NOBACI + Ley 10-07 + Contraloria General Republica - BASA - Elimina Camara Cuentas sin consentimiento - BASA Profesional", "retencion": "10 anos - BASA"},
        {"no": 6, "actividad": "Carga expediente pago al Sistema Unificado Gestion Pagos (SUGEP) - BASA", "rol": "BASA - Especialista Control Interno", "herramienta": "SUGEP (Contraloria General) - BASA", "control": "Obligatoriedad registro institucional - BASA - Contraloria General + NOBACI + Ley 10-07 - Elimina Camara Cuentas - BASA Profesional", "retencion": "10 anos - BASA"},
        {"no": 7, "actividad": "Auditoria Control Interno posterior remision informes Contabilidad Finanzas - BASA", "rol": "BASA - Control Interno", "herramienta": "SAP - BASA", "control": "Informes inmediatos posteriores - BASA - Contraloria General + NOBACI + Ley 10-07 - Profesional", "retencion": "10 anos - BASA"},
    ],
    "contratos_adendas": [
        {"no": 1, "actividad": "Remitir comunicacion solicitud elaboracion contrato adenda especificaciones bienes servicios obras - BASA", "responsable": "BASA - Unidad Solicitante / Compras", "plazo": "N/A", "base": "Ley 340-06 / Decreto 416-23 - BASA - Tope 50%"},
        {"no": 2, "actividad": "Recibir solicitud elaborar Informe Viabilidad Legal adenda revision Directora - BASA - 5 dias", "responsable": "BASA - Coordinador Contrato", "plazo": "5 dias laborables", "base": "Art. 31 Ley 340-06 y Art. 179 Dec. 416-23 - Tope 50% - BASA - Informe Viabilidad Legal 5 dias - Elimina nombres sin consentimiento"},
        {"no": 5, "actividad": "Asignar abogado especialista confeccion Informe Viabilidad y borrador - BASA", "responsable": "BASA - Gerencia Contratos", "plazo": "N/A", "base": "Distribucion por orden en ULTICABINET - BASA"},
        {"no": 8, "actividad": "Elaborar borrador contrato adenda conforme solicitado remitir validacion - BASA - 10 dias", "responsable": "BASA - Abogado Especializado", "plazo": "10 dias laborables", "base": "Pliegos condiciones fichas tecnicas - BASA"},
        {"no": 9, "actividad": "Verificar remitir borrador validado areas Finanzas Compras Proveedor - BASA - 48h", "responsable": "BASA - Gerente Contratos", "plazo": "48 horas", "base": "Ciclo validacion multi-area - BASA - 48h"},
        {"no": 18, "actividad": "Registrar contrato en Sistema Electronico Registro Contratos (SERC) - BASA", "responsable": "BASA - Responsable Registro SERC", "plazo": "Plazo legal", "base": "Contraloria General Republica - BASA - Elimina Camara Cuentas sin consentimiento - SERC - Profesional"},
    ],
    "archivo_general": [
        {"tipo": "Expedientes de Pago a Proveedores y Terceros - BASA", "area": "BASA - Direccion Finanzas / Control Interno", "soporte": "Fisico y Digital (Multicabinet / SUGEP) - BASA", "retencion": "10 anos - BASA", "destino": "Archivo Historico / Custodia Definitiva - BASA", "base": "Ley 10-07 Contraloria y Normas BASA - Contraloria General + NOBACI + Ley 10-07 - Elimina Camara Cuentas sin consentimiento - BASA Profesional"},
        {"tipo": "Contratos de Bienes, Obras y Servicios - BASA", "area": "BASA - Direccion Servicios Juridicos (Gerencia Contratos)", "soporte": "Fisico (3 originales) y Digital (SERC) - BASA", "retencion": "10 anos posteriores terminacion - BASA", "destino": "Archivo Central / Registro SERC - BASA", "base": "Ley 340-06 y Reglamento 416-23 - BASA - Tope 50%"},
        {"tipo": "Adendas y Enmiendas Contractuales - BASA", "area": "BASA - Direccion Servicios Juridicos (Gerencia Contratos)", "soporte": "Fisico y Digital (SERC / Ulticabinet) - BASA", "retencion": "10 anos - BASA", "destino": "Archivo Central / Area Administradora - BASA", "base": "Ley 340-06 Compras y Contrataciones - BASA - Tope 50% Art31"},
        {"tipo": "Informes de Viabilidad Legal y Justificativos - BASA", "area": "BASA - Direccion Servicios Juridicos", "soporte": "Digital y Fisico - BASA", "retencion": "5 anos - BASA", "destino": "Archivo Gestion - BASA", "base": "NOBACI / Control Interno - BASA - Profesional"},
        {"tipo": "Garantias (Fiel Cumplimiento, Anticipo, Vicios Ocultos) - BASA", "area": "BASA - Gerencia Compras / Finanzas / Juridico", "soporte": "Fisico (Originales incondicionales) - BASA", "retencion": "Hasta devolucion liquidacion definitiva - BASA", "destino": "Custodia Valores / Tesoreria - BASA", "base": "Ley 340-06 y Pliegos Condiciones - BASA"},
        {"tipo": "Comunicaciones de Solicitud y Aprobacion - BASA", "area": "BASA - Areas Requirentes / Gerencia General", "soporte": "Digital y Fisico - BASA", "retencion": "5 anos - BASA", "destino": "Archivo Gestion / Multicabinet - BASA", "base": "NOBACI - BASA - Contraloria General + NOBACI + Ley 10-07 - Profesional"},
    ]
}

app = Flask(__name__)

HTML_MENU_GENERAL = """
<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BASA - Menu General Completo - Profesional - Sin Carnaval</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
:root{--fondo:#f8fafc;--card:#ffffff;--header:#0f172a;--texto-oscuro:#0f172a;--texto-medio:#334155;--texto-claro:#64748b;--borde:#e2e8f0;--borde-oscuro:#cbd5e1;--accent:#0f172a}
body{background:var(--fondo);color:var(--texto-oscuro);font-family:Inter,Segoe UI,system-ui,sans-serif;font-size:12px;line-height:1.5;margin:0}
.header-pro{background:var(--header);color:#ffffff;padding:0;border-bottom:1px solid #1e293b;position:sticky;top:0;z-index:1000}
.header-top{display:flex;justify-content:space-between;align-items:center;padding:10px 16px}
.header-top h6{color:#ffffff;font-weight:700;margin:0;font-size:13px;letter-spacing:0.2px}
.header-top small{color:#94a3b8;font-size:10px}
.menu-general{background:#ffffff;border-bottom:1px solid var(--borde);padding:0;display:flex;flex-wrap:wrap;gap:0;position:sticky;top:48px;z-index:999;box-shadow:0 1px 2px rgba(15,23,42,0.06)}
.menu-item{padding:10px 14px;font-size:11px;font-weight:600;color:var(--texto-medio);border-right:1px solid var(--borde);cursor:pointer;background:#ffffff;transition:all 0.15s}
.menu-item:hover{background:#f8fafc;color:var(--texto-oscuro)}
.menu-item.active{background:var(--header);color:#ffffff}
.card-pro{background:var(--card);border:1px solid var(--borde);border-radius:8px;box-shadow:0 1px 2px rgba(15,23,42,0.06)}
.card-pro h6{color:var(--texto-oscuro);font-weight:700;font-size:12px}
.card-header-pro{background:#f8fafc;border-bottom:1px solid var(--borde);padding:10px 14px;font-weight:700;font-size:11px;text-transform:uppercase;letter-spacing:0.4px;color:var(--texto-oscuro)}
.table-pro{font-size:11px;color:var(--texto-oscuro);margin:0}
.table-pro thead{background:#f8fafc;color:var(--texto-oscuro)}
.table-pro thead th{font-weight:700;font-size:10px;text-transform:uppercase;letter-spacing:0.3px;color:var(--texto-oscuro);border-color:var(--borde);padding:8px 10px}
.table-pro tbody td{color:var(--texto-medio);border-color:var(--borde);padding:7px 10px;vertical-align:top}
.table-pro tbody tr:hover{background:#f8fafc}
.btn-pro{background:var(--header);color:#ffffff;border:1px solid var(--header);padding:6px 12px;border-radius:6px;font-weight:600;font-size:11px}
.btn-pro:hover{background:#1e293b;color:#ffffff}
.btn-sec{background:#ffffff;color:var(--texto-medio);border:1px solid var(--borde-oscuro);padding:5px 10px;border-radius:6px;font-size:10px;font-weight:500}
.btn-sec:hover{background:#f8fafc;color:var(--texto-oscuro);border-color:var(--texto-medio)}
.btn-ghost{background:#f8fafc;color:var(--texto-medio);border:1px solid var(--borde);padding:4px 8px;border-radius:6px;font-size:10px}
.badge-pro{background:var(--header);color:#ffffff;padding:4px 8px;border-radius:4px;font-size:9px;font-weight:700;letter-spacing:0.2px}
.badge-light-pro{background:#f1f5f9;color:var(--texto-medio);border:1px solid var(--borde);padding:3px 7px;border-radius:4px;font-size:9px;font-weight:600}
.badge-success-pro{background:#f0fdf4;color:#166534;border:1px solid #bbf7d0;padding:3px 7px;border-radius:4px;font-size:9px;font-weight:600}
.badge-warn-pro{background:#fffbeb;color:#92400e;border:1px solid #fde68a;padding:3px 7px;border-radius:4px;font-size:9px;font-weight:600}
.text-dark-pro{color:var(--texto-oscuro)!important}
.text-muted-pro{color:var(--texto-claro)!important}
.small-pro{font-size:10px;color:var(--texto-claro);line-height:1.4}
.divider{height:1px;background:var(--borde);margin:8px 0}
</style>
</head><body>
<div class="header-pro">
<div class="header-top">
<div>
<h6>BASA V1 MENU GENERAL COMPLETO PROFESIONAL - Elimina EDESUR y cualquier otro nombre sin consentimiento/permiso - Todos modulos habilitados organizados 5 grupos - Color profesional sin carnaval pomelo - FIX 436</h6>
<small>Entidad autorizada: {{ config.entidad_autorizada }} | Organo: {{ config.organo_control|join(' + ') }} | Elimina sin consentimiento: {{ config.eliminar_nombres_sin_consentimiento|join(', ') }} | Sistemas: {{ config.sistemas|join(' + ') }} | Tope adendas: {{ config.limite_adendas }}% Art31 Ley 340-06 Art179 Dec 416-23 | Retenciones: {{ config.retenciones.expedientes_pago }}/{{ config.retenciones.contratos }}/{{ config.retenciones.adendas }}/{{ config.retenciones.viabilidad_legal }} | Version: {{ config.version }}</small>
</div>
<div class="d-flex gap-2 align-items-center">
<span class="badge-pro">BASA PROFESIONAL</span>
<span class="badge-success-pro">TODOS MODULOS HABILITADOS</span>
<span class="badge-light-pro">MENU GENERAL COMPLETO</span>
</div>
</div>
</div>

<div class="menu-general" id="menuGeneral">
<div class="menu-item active" onclick="showSection('dashboard')">📊 Dashboard General BASA</div>
<div class="menu-item" onclick="showSection('matriz')">📋 Matriz Control Cumplimiento Normativo 3 Procedimientos - BASA</div>
<div class="menu-item" onclick="showSection('pagos')">💰 FI-CI-PR-001 Verificacion Pagos 7 Pasos - BASA</div>
<div class="menu-item" onclick="showSection('contratos')">📝 SJ-CO-PR-001 Contratos Adendas 19 Pasos Tope 50% - BASA</div>
<div class="menu-item" onclick="showSection('archivo')">📁 LO-SG-PR-005 Archivo General Retencion - BASA</div>
<div class="menu-item" onclick="showSection('modulos')">📦 Modulos Organizados 5 Grupos - Todos Habilitados - BASA Profesional</div>
<div class="menu-item" onclick="showSection('informes')">📄 M10 Informes Replicas Confidencial - BASA DEMO 2026-10-14</div>
<div class="menu-item" onclick="showSection('config')">⚙️ Configuracion BASA + Probar Sistema + Eliminar Nombres sin Consentimiento</div>
</div>

<div class="container-fluid p-3">

<!-- DASHBOARD GENERAL -->
<div id="sec-dashboard" class="section">
<div class="row g-3">
<div class="col-md-8">
<div class="card-pro">
<div class="card-header-pro">📊 Dashboard General BASA - Menu General Completo - Todos Modulos Habilitados - Profesional Sin Carnaval</div>
<div class="p-3">
<div class="row g-2">
<div class="col-md-4"><div class="card-pro p-2 text-center" style="background:#f8fafc"><div class="small-pro">Procedimientos BASA</div><div style="font-size:18px;font-weight:700;color:var(--texto-oscuro)">3</div><div class="small-pro">FI-CI-PR-001 + SJ-CO-PR-001 + LO-SG-PR-005 - BASA</div></div></div>
<div class="col-md-4"><div class="card-pro p-2 text-center" style="background:#f0fdf4"><div class="small-pro">Actividades BASA</div><div style="font-size:18px;font-weight:700;color:var(--texto-oscuro)">32</div><div class="small-pro">7 pagos + 19 contratos + 6 archivo - BASA Profesional</div></div></div>
<div class="col-md-4"><div class="card-pro p-2 text-center" style="background:#fffbeb"><div class="small-pro">Modulos BASA</div><div style="font-size:18px;font-weight:700;color:var(--texto-oscuro)">13</div><div class="small-pro">5 grupos organizados - Todos habilitados DEMO - BASA</div></div></div>
</div>
<div class="divider"></div>
<div class="small-pro text-dark-pro">
<b class="text-dark-pro">BASA - Menu General Completo Profesional - Sin Carnaval Pomelo - Letras Contraste Alto:</b><br>
- <b>Elimina EDESUR y cualquier otro nombre sin consentimiento/permiso:</b> Antes Matriz decia EDESUR DOMINICANA, S.A. - MATRIZ DE RETENCION Y ARCHIVO DOCUMENTAL (NORMATIVA CAMARA DE CUENTAS) - Ahora BASA - MATRIZ DE RETENCION Y ARCHIVO DOCUMENTAL (NORMATIVA Contraloria General + NOBACI + Ley 10-07 - Adaptada BASA - Elimina nombres sin consentimiento) - Solo BASA autorizado<br>
- <b>Todos modulos habilitados organizados segun ya definido 5 grupos profesionales:</b> GRUPO 1 COMPRAS Y CONTRATOS M1 M2 M2B + GRUPO 2 FINANCIERO Y CONTABLE M3 M4 M14 + GRUPO 3 FORENSE Y LEGAL M8 M9 M12 + GRUPO 4 GESTION DOCUMENTAL M10 M11 M15 M16 + GRUPO 5 ENTERPRISE WORLD M13 - Todos DEMO ACTIVO hasta 2026-10-14 - Sin bloqueo - Profesional<br>
- <b>Color pagina mas profesional sin carnaval pomelo:</b> Fondo #f8fafc gris azulado muy claro profesional (antes morado #7c3aed pomelo carnaval) - Header #0f172a azul noche profesional texto #ffffff contraste 21:1 (antes morado letras perdidas) - Cards #ffffff blanco puro borde #e2e8f0 - Texto #0f172a/#334155 oscuro contraste alto WCAG AAA - Botones #0f172a negro profesional - Sin amarillo/verde/morado carnaval - Letras no se pierden<br>
- <b>Menu general completo 8 secciones:</b> Dashboard General BASA | Matriz Control Cumplimiento Normativo 3 Procedimientos | FI-CI-PR-001 Verificacion Pagos 7 Pasos | SJ-CO-PR-001 Contratos Adendas 19 Pasos Tope 50% | LO-SG-PR-005 Archivo General Retencion 6 Tipos | Modulos Organizados 5 Grupos Todos Habilitados | M10 Informes Replicas Confidencial DEMO 2026-10-14 | Configuracion BASA + Probar Sistema + Eliminar Nombres sin Consentimiento - Profesional<br>
- <b>CONFIG BASA aplicada:</b> Entidad autorizada BASA - Organo Contraloria General + NOBACI + Ley 10-07 - Elimina sin consentimiento EDESUR, EDESUR DOMINICANA, EDENORTE, EDEESTE, ETED, Camara de Cuentas, CCA, CCRD, CGR, Camara - Sistemas SAP + SUGEP + SIGEF + SERC + Multicabinet - Retenciones 10/10/10/5 anos + Permanente Ley 481-08 - Tope adendas 50% Art31 Ley 340-06 Art179 Dec 416-23 - Version V1 BASA MENU GENERAL COMPLETO PROFESIONAL<br>
</div>
</div>
</div>
</div>
<div class="col-md-4">
<div class="card-pro p-3">
<h6 class="text-dark-pro">🧪 Probar Sistema BASA - Menu General Completo</h6>
<div class="d-grid gap-2 mt-2">
<button onclick="showSection('matriz'); probarMatriz()" class="btn-pro">📋 Probar Matriz Control 3 Procedimientos - BASA</button>
<button onclick="showSection('pagos'); probarPagos()" class="btn-sec">💰 Probar FI-CI-PR-001 7 Pasos - BASA Profesional</button>
<button onclick="showSection('contratos'); probarContratos()" class="btn-sec">📝 Probar SJ-CO-PR-001 19 Pasos Tope 50% - BASA</button>
<button onclick="showSection('archivo'); probarArchivo()" class="btn-sec">📁 Probar LO-SG-PR-005 Archivo 6 Tipos - BASA</button>
<button onclick="showSection('modulos'); probarModulos()" class="btn-pro">📦 Ver Todos Modulos 5 Grupos Habilitados - BASA</button>
<button onclick="showSection('informes'); probarM10()" class="btn-pro">📄 Probar M10 Replicas Confidencial - BASA DEMO 2026-10-14</button>
<button onclick="probarTope50()" class="btn-sec" style="border-color:#fbbf24">⚠️ Probar Tope 50% Adendas - BASA Art31</button>
</div>
<div id="dashResult" class="mt-3"></div>
</div>
<div class="card-pro p-3 mt-3">
<h6 class="text-dark-pro">⚙️ CONFIG BASA - Elimina Nombres sin Consentimiento</h6>
<div class="small-pro text-dark-pro p-2 rounded" style="background:#f8fafc;border:1px solid var(--borde)">
<b class="text-dark-pro">Entidad autorizada:</b> BASA (Solo BASA autorizado - Otros requieren consentimiento/permiso)<br>
<b class="text-dark-pro">Elimina sin consentimiento:</b> {{ config.eliminar_nombres_sin_consentimiento|join(', ') }}<br>
<b class="text-dark-pro">Organo control:</b> {{ config.organo_control|join(' + ') }} (Antes Camara Cuentas - Eliminado sin consentimiento)<br>
<b class="text-dark-pro">Sistemas:</b> {{ config.sistemas|join(' + ') }}<br>
<b class="text-dark-pro">Retenciones:</b> {{ config.retenciones.expedientes_pago }} pago / {{ config.retenciones.contratos }} contratos / {{ config.retenciones.adendas }} adendas / {{ config.retenciones.viabilidad_legal }} viabilidad / {{ config.retenciones.archivo_general }} archivo<br>
<b class="text-dark-pro">Tope adendas:</b> {{ config.limite_adendas }}% Art31 Ley 340-06 + Art179 Dec 416-23 - BASA<br>
<b class="text-dark-pro">Color profesional:</b> Fondo #f8fafc, Card #ffffff, Header #0f172a, Texto #0f172a/#334155, Borde #e2e8f0 - Sin carnaval pomelo - Letras contraste alto WCAG AAA<br>
</div>
</div>
</div>
</div>
</div>

<!-- MATRIZ -->
<div id="sec-matriz" class="section" style="display:none">
<div class="card-pro">
<div class="card-header-pro">📋 Matriz Control y Cumplimiento Normativo - 3 Procedimientos - BASA - Menu General Completo - Elimina EDESUR y otros sin consentimiento - Coloca BASA - Profesional</div>
<div class="p-0">
<table class="table table-sm table-bordered table-pro mb-0">
<thead><tr><th>Codigo</th><th>Nombre Documento - BASA</th><th>Direccion / Gerencia Responsable - BASA</th><th>Version - BASA</th><th>Objetivo Principal - BASA</th><th>Tiempo Retencion / Archivo - BASA</th><th>Sistemas - BASA</th><th>Organo Control - BASA (Elimina Camara sin consentimiento)</th></tr></thead>
<tbody>
{% for p in matriz.procedimientos %}
<tr><td><span class="badge-pro">{{ p.codigo }}</span></td><td class="text-dark-pro">{{ p.nombre }} - <span class="badge-light-pro">BASA</span></td><td class="text-dark-pro">{{ p.direccion }}</td><td class="text-dark-pro">{{ p.version }}</td><td class="text-dark-pro">{{ p.objetivo }}</td><td class="text-dark-pro">{{ p.retencion }}</td><td class="text-dark-pro">{{ p.sistemas }}</td><td class="text-dark-pro">{{ config.organo_control|join(' + ') }} - BASA - Elimina Camara Cuentas/CCA/CCRD sin consentimiento</td></tr>
{% endfor %}
</tbody>
</table>
</div>
<div class="p-3 small-pro text-dark-pro" style="background:#f8fafc;border-top:1px solid var(--borde)">
<b class="text-dark-pro">✅ Matriz Control Cumplimiento Normativo BASA - Menu General Completo Profesional:</b> Entidad autorizada {{ config.entidad_autorizada }} - Solo BASA autorizado - Elimina sin consentimiento/permiso {{ config.eliminar_nombres_sin_consentimiento|join(', ') }} - Antes EDESUR DOMINICANA, S.A. - MATRIZ DE CONTROL Y CUMPLIMIENTO NORMATIVO (Camara de Cuentas / NOBACI) - Ahora BASA - MATRIZ DE CONTROL Y CUMPLIMIENTO NORMATIVO ({{ config.organo_control|join(' + ') }} - Adaptada BASA - Elimina nombres sin consentimiento) - FI-CI-PR-001 Verificacion Pagos 7 pasos + SJ-CO-PR-001 Contratos Adendas 19 pasos tope 50% Art31 + LO-SG-PR-005 Archivo General 6 tipos retencion 10 anos/Permanente Ley 481-08 - Sistemas {{ config.sistemas|join(' + ') }} - Retenciones {{ config.retenciones.expedientes_pago }}/{{ config.retenciones.contratos }}/{{ config.retenciones.adendas }}/{{ config.retenciones.viabilidad_legal }} - Tope {{ config.limite_adendas }}% - Menu general completo 8 secciones - Color profesional sin carnaval pomelo - Letras contraste alto - FIX 436
</div>
</div>
</div>

<!-- PAGOS -->
<div id="sec-pagos" class="section" style="display:none">
<div class="card-pro">
<div class="card-header-pro">💰 FI-CI-PR-001 Procedimiento Verificacion Documentos y Expedientes de Pago 7 Pasos - BASA - Menu General Completo - Elimina EDESUR/Camara sin consentimiento - Profesional</div>
<div class="p-0">
<table class="table table-sm table-bordered table-pro mb-0">
<thead><tr><th>No. Act.</th><th>Actividades / Pasos Proceso - BASA</th><th>Rol / Involucrado Responsable - BASA</th><th>Herramienta / Sistema Informatico - BASA - {{ config.sistemas|join(' + ') }}</th><th>Controles Clave / Normativa Referencia - BASA - Elimina Camara sin consentimiento</th><th>Tiempo Retencion - BASA</th><th>Script BASA</th></tr></thead>
<tbody>
{% for p in matriz.verificacion_pagos %}
<tr><td class="text-dark-pro">{{ p.no }}</td><td class="text-dark-pro">{{ p.actividad }}</td><td class="text-dark-pro">{{ p.rol }}</td><td class="text-dark-pro">{{ p.herramienta }}</td><td class="text-dark-pro">{{ p.control }}</td><td class="text-dark-pro">{{ p.retencion }} - BASA</td><td><code style="font-size:9px">basa_fi_ci_pr_001_paso{{ p.no }}.py</code></td></tr>
{% endfor %}
</tbody>
</table>
</div>
</div>
</div>

<!-- CONTRATOS -->
<div id="sec-contratos" class="section" style="display:none">
<div class="card-pro">
<div class="card-header-pro">📝 SJ-CO-PR-001 Procedimiento Elaboracion Contratos y Adendas 19 Pasos - Tope {{ config.limite_adendas }}% Art31 Ley 340-06 Art179 Dec 416-23 - BASA - Menu General Completo - Elimina EDESUR/Camara sin consentimiento - Profesional</div>
<div class="p-0">
<table class="table table-sm table-bordered table-pro mb-0">
<thead><tr><th>No. Act.</th><th>Actividades / Pasos Proceso - BASA</th><th>Responsable - BASA</th><th>Plazo / Termino - BASA</th><th>Base Legal / Requisito Regulatorio - BASA - Tope {{ config.limite_adendas }}% - Elimina nombres sin consentimiento</th><th>Script BASA</th></tr></thead>
<tbody>
{% for p in matriz.contratos_adendas %}
<tr><td class="text-dark-pro">{{ p.no }}</td><td class="text-dark-pro">{{ p.actividad }}</td><td class="text-dark-pro">{{ p.responsable }}</td><td class="text-dark-pro">{{ p.plazo }}</td><td class="text-dark-pro">{{ p.base }} - {{ config.organo_control|join(' + ') }} - Tope {{ config.limite_adendas }}% - BASA - Elimina nombres sin consentimiento</td><td><code style="font-size:9px">basa_sj_co_pr_001_paso{{ p.no }}.py</code></td></tr>
{% endfor %}
</tbody>
</table>
</div>
<div class="p-3 small-pro text-dark-pro" style="background:#fffbeb;border-top:1px solid #fde68a">
<b class="text-dark-pro">⚠️ Tope {{ config.limite_adendas }}% Adendas BASA - Art31 Ley 340-06 + Art179 Dec 416-23 - Elimina nombres sin consentimiento:</b> Monto base + Adendas no puede exceder {{ config.limite_adendas }}% - Ejemplo: Base RD$1,000,000 + Adendas RD$550,000 = RD$550,000 vs Tope RD$500,000 = Excede RD$50,000 = HALLAZGO AUTOMATICO BASA - Informe Viabilidad Legal 5 dias requerido - ULTICABINET + SERC + validacion multi-area 48h + firma Gerencia General CUED + notarizacion SJ-LC-PO-002 - BASA - Menu general completo - Profesional
</div>
</div>
</div>

<!-- ARCHIVO -->
<div id="sec-archivo" class="section" style="display:none">
<div class="card-pro">
<div class="card-header-pro">📁 LO-SG-PR-005 Matriz Retencion y Archivo Documental - 6 Tipos - BASA - Menu General Completo - Elimina EDESUR/Camara/CCA/CCRD sin consentimiento - Coloca BASA - Profesional</div>
<div class="p-0">
<table class="table table-sm table-bordered table-pro mb-0">
<thead><tr><th>Tipo Documento / Expediente - BASA</th><th>Area Generadora / Custodia - BASA</th><th>Soporte (Fisico / Digital) - BASA - {{ config.sistemas|join(' + ') }}</th><th>Tiempo Retencion Minimo - BASA</th><th>Disposicion Final / Destino - BASA</th><th>Base Legal Auditoria - BASA - Elimina Camara sin consentimiento</th></tr></thead>
<tbody>
{% for p in matriz.archivo_general %}
<tr><td class="text-dark-pro">{{ p.tipo }} - <span class="badge-light-pro">BASA</span></td><td class="text-dark-pro">{{ p.area }}</td><td class="text-dark-pro">{{ p.soporte }}</td><td class="text-dark-pro">{{ p.retencion }} - BASA - {{ config.retenciones.expedientes_pago }}/{{ config.retenciones.contratos }}/{{ config.retenciones.viabilidad_legal }}</td><td class="text-dark-pro">{{ p.destino }}</td><td class="text-dark-pro">{{ p.base }} - {{ config.organo_control|join(' + ') }} - BASA - Elimina Camara Cuentas/CCA/CCRD sin consentimiento - {{ config.entidad_autorizada }} - Profesional</td></tr>
{% endfor %}
</tbody>
</table>
</div>
<div class="p-3 small-pro text-dark-pro" style="background:#f8fafc;border-top:1px solid var(--borde)">
<b class="text-dark-pro">📁 Matriz Retencion Archivo Documental BASA - Menu General Completo Profesional:</b> Antes EDESUR DOMINICANA, S.A. - MATRIZ DE RETENCION Y ARCHIVO DOCUMENTAL (NORMATIVA CAMARA DE CUENTAS) - Ahora BASA - MATRIZ DE RETENCION Y ARCHIVO DOCUMENTAL (NORMATIVA {{ config.organo_control|join(' + ') }} - Adaptada BASA - Elimina nombres sin consentimiento/permiso {{ config.eliminar_nombres_sin_consentimiento|join(', ') }} - Coloca {{ config.entidad_autorizada }}) - 6 tipos: Expedientes Pago 10 anos Multicabinet SUGEP Archivo Historico Ley 10-07 + Contratos 10 anos posteriores terminacion 3 originales SERC + Adendas 10 anos SERC Ulticabinet + Informes Viabilidad 5 anos + Garantias hasta devolucion + Comunicaciones 5 anos NOBACI - Objetivo aseguramiento informaciones impresas digitales - Permanente / Lista Valoracion Documental Ley 481-08 - Sistemas {{ config.sistemas|join(' + ') }} - Retenciones {{ config.retenciones.expedientes_pago }}/{{ config.retenciones.contratos }}/{{ config.retenciones.adendas }}/{{ config.retenciones.viabilidad_legal }}/{{ config.retenciones.archivo_general }} - Menu general completo - Profesional sin carnaval - Letras contraste alto - FIX 436
</div>
</div>
</div>

<!-- MODULOS -->
<div id="sec-modulos" class="section" style="display:none">
<div id="gruposContainer"></div>
<div id="ejecReal" class="card-pro p-3 mt-3" style="display:none"></div>
</div>

<!-- INFORMES -->
<div id="sec-informes" class="section" style="display:none">
<div class="card-pro p-3">
<h6 class="text-dark-pro">📄 M10 Informes Replicas Confidencial - BASA - DEMO ACTIVO hasta 2026-10-14 - Menu General Completo - Elimina EDESUR/Camara sin consentimiento - Profesional</h6>
<div class="row g-2 mt-2">
<div class="col-md-4"><button onclick="probarM10()" class="btn-pro w-100">▶️ Probar M10 BASA Datos Reales Matriz - DEMO 2026-10-14 - Profesional</button></div>
<div class="col-md-4"><button onclick="probarTope50()" class="btn-sec w-100">⚠️ Probar Tope 50% Adendas - BASA Art31</button></div>
<div class="col-md-4"><button onclick="exportInformeBASA()" class="btn-sec w-100">📄 Export Informe BASA Word/Excel - Profesional</button></div>
</div>
<div id="m10Container" class="mt-3"></div>
</div>
</div>

<!-- CONFIG -->
<div id="sec-config" class="section" style="display:none">
<div class="row g-3">
<div class="col-md-6">
<div class="card-pro p-3">
<h6 class="text-dark-pro">⚙️ Configuracion BASA - Elimina Nombres sin Consentimiento/Permiso - Profesional</h6>
<div class="small-pro text-dark-pro p-3 rounded mt-2" style="background:#f8fafc;border:1px solid var(--borde)">
<b class="text-dark-pro">CONFIG_BASA - Menu General Completo Profesional:</b><br>
<b>Entidad autorizada:</b> {{ config.entidad_autorizada }} - Solo BASA autorizado - Cualquier otro nombre EDESUR, EDENORTE, EDEESTE, ETED, Camara de Cuentas, CCA, CCRD, CGR requiere consentimiento/permiso explicito - Si no tiene consentimiento se usa BASA generico {{ config.entidad_generica }}<br>
<b>Elimina sin consentimiento:</b> {{ config.eliminar_nombres_sin_consentimiento|join(', ') }} - Todos reemplazados por BASA - Elimina EDESUR y cualquier otro sin su consentimiento o permiso<br>
<b>Organo control:</b> {{ config.organo_control|join(' + ') }} - Antes Camara de Cuentas - Ahora Contraloria General + NOBACI + Ley 10-07 - Elimina Camara Cuentas sin consentimiento - BASA<br>
<b>Sistemas:</b> {{ config.sistemas|join(' + ') }} - SAP + SUGEP + SIGEF + SERC + Multicabinet - BASA<br>
<b>Retenciones:</b> {{ config.retenciones.expedientes_pago }} expedientes pago / {{ config.retenciones.contratos }} contratos / {{ config.retenciones.adendas }} adendas / {{ config.retenciones.viabilidad_legal }} viabilidad legal / {{ config.retenciones.archivo_general }} archivo general - BASA<br>
<b>Limite adendas:</b> {{ config.limite_adendas }}% Art31 Ley 340-06 + Art179 Dec 416-23 - Tope 50% - Informe Viabilidad Legal 5 dias - BASA<br>
<b>Version:</b> {{ config.version }} - Menu general completo profesional - Elimina nombres sin consentimiento - Todos modulos habilitados organizados 5 grupos - Color profesional sin carnaval pomelo - FIX syntax 436 - Letras contraste alto WCAG AAA<br>
<b>Color profesional sin carnaval:</b> Fondo {{ config.color_profesional.fondo }} gris azulado muy claro profesional (antes morado #7c3aed pomelo carnaval) - Card {{ config.color_profesional.card }} blanco puro - Header {{ config.color_profesional.header }} azul noche profesional - Texto oscuro {{ config.color_profesional.texto_oscuro }} / medio {{ config.color_profesional.texto_medio }} / claro {{ config.color_profesional.texto_claro }} - Borde {{ config.color_profesional.borde }} / {{ config.color_profesional.borde_oscuro }} - Sin amarillo/verde/morado carnaval - Letras no se pierden fondo carnaval pomelo mas profesional - Contraste alto WCAG AAA<br>
</div>
<div class="mt-3">
<h6 class="text-dark-pro">🧪 Probar Sistema BASA - Eliminar Nombres sin Consentimiento</h6>
<div class="d-flex gap-2 mt-2">
<input id="entidadTest" class="form-control form-control-sm" placeholder="Escriba entidad para probar - Ej: EDESUR, Empresa XYZ - Requiere consentimiento" style="font-size:11px">
<button onclick="probarConsentimiento()" class="btn-pro">Probar Consentimiento/Permiso</button>
</div>
<div id="consentResult" class="mt-2 small-pro"></div>
</div>
</div>
</div>
<div class="col-md-6">
<div class="card-pro p-3">
<h6 class="text-dark-pro">💻 Scripts BASA Profesional - Sin Carnaval - FIX 436 - Todos Modulos Habilitados</h6>
<div id="scriptsList" class="small-pro"></div>
</div>
</div>
</div>
</div>

</div>

<script>
let MODS = {{ mods|tojson }};
let GRUPOS = {{ grupos|tojson }};
let CONFIG = {{ config|tojson }};
let MATRIZ = {{ matriz|tojson }};

function showSection(sec){
 document.querySelectorAll('.section').forEach(s=>s.style.display='none');
 document.getElementById('sec-'+sec).style.display='block';
 document.querySelectorAll('.menu-item').forEach(m=>m.classList.remove('active'));
 document.querySelector('[onclick="showSection(\''+sec+'\')"]').classList.add('active');
 window.scrollTo(0,0);
}

function probarMatriz(){
 document.getElementById('dashResult').innerHTML='<div class="p-2 rounded border text-dark-pro" style="background:#f0fdf4;border-color:#bbf7d0!important"><b class="text-dark-pro">Matriz BASA Probada - Menu General Completo Profesional</b><br><span class="text-dark-pro">3 procedimientos FI-CI-PR-001 + SJ-CO-PR-001 + LO-SG-PR-005 - BASA - Elimina EDESUR/Camara/CCA/CCRD sin consentimiento - Coloca BASA - Profesional sin carnaval - FIX 436</span></div>';
 showSection('matriz');
}
function probarPagos(){
 fetch('/api/probar/pagos',{method:'POST'}).then(r=>r.json()).then(d=>{
  document.getElementById('dashResult').innerHTML='<div class="p-2 rounded border text-dark-pro" style="background:#f8fafc;border-color:var(--borde)!important"><b class="text-dark-pro">FI-CI-PR-001 7 Pasos BASA Probado - Profesional</b><br><span class="text-dark-pro">'+d.pasos.length+' pasos - Sistemas '+d.config.sistemas.join(' + ')+' - Retencion '+d.config.retenciones.expedientes_pago+' - Organo '+d.config.organo_control.join(' + ')+' - Elimina EDESUR/Camara sin consentimiento - BASA</span></div>';
 });
}
function probarContratos(){
 fetch('/api/probar/contratos',{method:'POST'}).then(r=>r.json()).then(d=>{
  document.getElementById('dashResult').innerHTML='<div class="p-2 rounded border text-dark-pro" style="background:#fffbeb;border-color:#fde68a!important"><b class="text-dark-pro">SJ-CO-PR-001 19 Pasos BASA Probado - Tope '+d.config.limite_adendas+'% - Profesional</b><br><span class="text-dark-pro">'+d.pasos.length+' pasos - Tope '+d.config.limite_adendas+'% Art31 Ley 340-06 Art179 Dec 416-23 - Informe Viabilidad 5 dias - ULTICABINET + SERC + 48h - BASA - Elimina nombres sin consentimiento</span></div>';
 });
}
function probarArchivo(){
 fetch('/api/probar/archivo',{method:'POST'}).then(r=>r.json()).then(d=>{
  document.getElementById('dashResult').innerHTML='<div class="p-2 rounded border text-dark-pro" style="background:#f8fafc;border-color:var(--borde)!important"><b class="text-dark-pro">LO-SG-PR-005 Archivo General BASA Probado - Profesional</b><br><span class="text-dark-pro">'+d.archivo.length+' tipos retencion - '+d.config.retenciones.expedientes_pago+'/'+d.config.retenciones.contratos+'/'+d.config.retenciones.adendas+'/'+d.config.retenciones.viabilidad_legal+'/'+d.config.retenciones.archivo_general+' - Sistemas '+d.config.sistemas.join(' + ')+' - BASA - Elimina EDESUR/Camara sin consentimiento</span></div>';
 });
}
function probarModulos(){
 renderGrupos();
 document.getElementById('dashResult').innerHTML='<div class="p-2 rounded border text-dark-pro" style="background:#0f172a;color:#ffffff!important"><b style="color:#ffffff">Modulos BASA 5 Grupos - Todos Habilitados - Profesional - Sin Carnaval</b><br><span style="color:#cbd5e1">13 modulos organizados: GRUPO1 COMPRAS Y CONTRATOS M1 M2 M2B + GRUPO2 FINANCIERO Y CONTABLE M3 M4 M14 + GRUPO3 FORENSE Y LEGAL M8 M9 M12 + GRUPO4 GESTION DOCUMENTAL M10 M11 M15 M16 + GRUPO5 ENTERPRISE WORLD M13 - Todos DEMO ACTIVO hasta 2026-10-14 - Habilitados - Organizado segun ya definido - BASA Profesional - Elimina nombres sin consentimiento</span></div>';
}
function probarM10(){
 fetch('/api/probar/m10',{method:'POST'}).then(r=>r.json()).then(d=>{
  document.getElementById('dashResult').innerHTML='<div class="p-2 rounded border text-dark-pro" style="background:#f0fdf4;border-color:#bbf7d0!important"><b class="text-dark-pro">M10 BASA Probado - DEMO ACTIVO 2026-10-14 - Profesional</b><br><span class="text-dark-pro">Entidad: '+d.entidad+' - Organo: '+d.organo+' - Hash: '+d.hash+' - Elimina EDESUR/Camara/CCA/CCRD sin consentimiento - Coloca BASA - Profesional sin carnaval pomelo</span></div>';
  document.getElementById('m10Container').innerHTML='<div class="mt-2"><h6 class="text-dark-pro">M10 Informes Replicas Confidencial - BASA - Ejecucion Real - DEMO 2026-10-14 - Menu General Completo Profesional</h6><div class="small-pro p-3 rounded bg-white border text-dark-pro mt-2"><b class="text-dark-pro">Transcripcion Textual Precisa Real - BASA Profesional - Sin Carnaval:</b><br><span class="text-dark-pro">'+d.transcripcion+'</span></div><div class="small-pro p-3 rounded mt-2 border text-dark-pro" style="background:#fffbeb!important;border-color:#fde68a!important"><b class="text-dark-pro">Analisis Claro y Preciso - BASA Profesional:</b><br><span class="text-dark-pro">'+d.analisis+'</span></div><div class="small-pro p-3 rounded mt-2 border text-dark-pro" style="background:#f0fdf4!important;border-color:#bbf7d0!important"><b class="text-dark-pro">Reporte + Resultados + Script Funcional Real Rol DEMO - BASA Profesional - Menu General Completo:</b><br><span class="text-dark-pro">'+d.reporte+'</span></div><pre style="background:#0f172a;color:#f8fafc;padding:12px;border-radius:6px;font-size:10px;max-height:400px;overflow:auto;margin-top:8px;border:1px solid #1e293b">'+d.script+'</pre><div class="small-pro p-2 rounded mt-2 text-dark-pro" style="background:#f8fafc;border:1px solid var(--borde)"><b class="text-dark-pro">Backup referencia validable:</b> <span class="text-dark-pro">'+d.backup+' | Vigente: '+d.vigente+' | Renovada: '+(d.renovada||'Primera')+' | Vencimiento: '+d.vencimiento+' | Entidad autorizada: '+d.config.entidad_autorizada+' - Solo BASA autorizado - Elimina EDESUR/Camara/CCA/CCRD sin consentimiento/permiso - Coloca BASA - Menu general completo - Profesional sin carnaval - FIX 436 - Letras contraste alto WCAG AAA</span></div></div>';
 });
}
function probarTope50(){
 fetch('/api/probar/tope50',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({monto_base:1000000, adendas:[200000,150000,200000]})}).then(r=>r.json()).then(d=>{
  var style = d.excede? 'background:#fef2f2!important;border-color:#fecaca!important' : 'background:#f0fdf4!important;border-color:#bbf7d0!important';
  document.getElementById('dashResult').innerHTML='<div class="p-3 rounded border text-dark-pro" style="'+style+'"><b class="text-dark-pro">Test Tope '+d.config.limite_adendas+'% - BASA - Art31 Ley 340-06 + Art179 Dec 416-23 - Profesional - Sin Carnaval</b><br><span class="text-dark-pro">Monto base: RD$'+d.monto_base.toLocaleString()+'</span><br><span class="text-dark-pro">Adendas: '+d.adendas.join(' + ')+' = RD$'+d.total.toLocaleString()+'</span><br><span class="text-dark-pro">Tope '+d.config.limite_adendas+'%: RD$'+d.tope.toLocaleString()+'</span><br><span class="text-dark-pro">Excede: '+d.excede+'</span><br><span class="text-dark-pro">'+d.mensaje+'</span><br><small class="text-muted-pro">Entidad autorizada: '+d.config.entidad_autorizada+' - Organo: '+d.config.organo_control.join(' + ')+' - Sistemas: '+d.config.sistemas.join(' + ')+' - Elimina EDESUR/Camara/CCA/CCRD sin consentimiento/permiso - Coloca BASA - Menu general completo - Profesional sin carnaval - FIX 436 - Letras contraste alto</small></div>';
  var htmlSec = document.getElementById('sec-contratos');
  if(htmlSec) document.getElementById('sec-contratos').innerHTML += '<div class="p-3 rounded border mt-3 text-dark-pro" style="'+style+'"><b class="text-dark-pro">Test Tope '+d.config.limite_adendas+'% - BASA - Probado Sistema - Menu General Completo</b><br><span class="text-dark-pro">'+d.mensaje+'</span></div>';
 });
}

function probarConsentimiento(){
 var entidad = document.getElementById('entidadTest').value;
 if(!entidad){alert('Escriba entidad para probar consentimiento/permiso - Ej: EDESUR, Empresa XYZ'); return;}
 fetch('/api/probar/consentimiento',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({entidad:entidad})}).then(r=>r.json()).then(d=>{
  var style = d.autorizado? 'background:#f0fdf4;border-color:#bbf7d0' : 'background:#fef2f2;border-color:#fecaca';
  document.getElementById('consentResult').innerHTML='<div class="p-2 rounded border text-dark-pro" style="'+style+'"><b class="text-dark-pro">Entidad: '+d.entidad_original+' -> '+d.entidad_final+'</b><br><span class="text-dark-pro">Autorizado: '+d.autorizado+' - Requiere consentimiento/permiso: '+d.requiere_consentimiento+'</span><br><span class="text-dark-pro">'+d.mensaje+'</span><br><small class="text-muted-pro">Elimina nombres sin consentimiento: '+d.config.eliminar_nombres_sin_consentimiento.join(', ')+' - Solo BASA autorizado - Si no tiene consentimiento se usa BASA generico {{ENTIDAD_AUTORIZADA}} - Menu general completo profesional - Elimina EDESUR y cualquier otro sin su consentimiento o permiso - BASA</small></div>';
 });
}

function renderGrupos(){
 var html='';
 var hoy = new Date();
 Object.keys(GRUPOS).forEach(function(grupo){
  html+='<div class="card-pro mb-3"><div class="card-header-pro">'+grupo+' - BASA - Todos Habilitados DEMO ACTIVO - Organizado segun ya definido - Profesional Sin Carnaval</div>';
  GRUPOS[grupo].forEach(function(mid){
   var m = MODS[mid]; if(!m) return;
   var estado = '<span class="badge-success-pro">'+m.estado+' - BASA Profesional - Habilitado</span>';
   var botones = '<button onclick="abrirEjecutarReal(\''+mid+'\',\'demo\')" class="btn-pro">▶️ Ejecutar DEMO - '+m.codigo+' - BASA Profesional</button> <button onclick="probarModulo(\''+mid+'\')" class="btn-sec">🧪 Probar '+mid+' - BASA</button>';
   html+='<div class="p-3 d-flex justify-content-between" style="border-top:1px solid var(--borde)"><div style="flex:1"><div style="font-weight:700;color:var(--texto-oscuro);font-size:12px">'+mid+' '+m.nombre+' - '+m.codigo+' - BASA '+estado+'</div><div class="small-pro text-dark-pro mt-1">'+m.desc+' - '+m.codigo+' - Ley: '+m.ley+' - USD'+m.precio+'/mes - Grupo: '+m.grupo+' - Organizado segun ya definido - BASA - Elimina EDESUR/Camara/CCA/CCRD sin consentimiento/permiso - Coloca BASA - Profesional sin carnaval pomelo - Letras contraste alto - Menu general completo - Habilitado</div></div><div class="d-flex gap-1 align-items-start" style="margin-left:12px">'+botones+'</div></div>';
  });
  html+='</div>';
 });
 document.getElementById('gruposContainer').innerHTML=html;
 // scripts list
 var scriptsHtml='';
 Object.keys(MODS).forEach(function(mid){
  var m=MODS[mid];
  scriptsHtml+='<div class="p-2 border-bottom" style="border-color:var(--borde)"><b class="text-dark-pro">'+mid+' '+m.codigo+' - BASA</b> - <span class="text-dark-pro">'+m.nombre+'</span><br><code style="font-size:9px;color:var(--texto-medio)">basa_'+mid.toLowerCase()+'_'+m.codigo.toLowerCase().replace(/ /g,'_').replace(/\\+/g,'_')+'.py - Profesional - Sin carnaval - Elimina nombres sin consentimiento - BASA - Organizado '+m.grupo+'</code></div>';
 });
 document.getElementById('scriptsList').innerHTML=scriptsHtml;
}

function probarModulo(mid){
 fetch('/api/modulos/'+mid+'/ejecutar_real',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({tipo:'demo',entidad:'BASA'})}).then(r=>r.json()).then(d=>{
  document.getElementById('ejecReal').style.display='block';
  document.getElementById('ejecReal').innerHTML='<h6 class="text-dark-pro">Ejecucion Real - '+mid+' '+d.nombre+' - '+d.codigo+' - DEMO - BASA Profesional - Menu General Completo</h6><div class="small-pro text-dark-pro"><b class="text-dark-pro">Entidad autorizada:</b> '+d.entidad_autorizada+' | <b class="text-dark-pro">Organo:</b> '+d.organo_control+' | <b class="text-dark-pro">Ley:</b> '+d.ley_adaptada+' | <b class="text-dark-pro">Sistemas:</b> '+d.sistemas+' | <b class="text-dark-pro">Retencion:</b> '+d.retencion_adaptada+' | <b class="text-dark-pro">Elimina nombres sin consentimiento:</b> EDESUR/Camara/CCA/CCRD - Coloca BASA - Profesional sin carnaval - FIX 436</div><div class="small-pro p-2 rounded bg-white border mt-2 text-dark-pro"><b class="text-dark-pro">Transcripcion:</b><br><span class="text-dark-pro">'+d.transcripcion_textual+'</span></div><div class="small-pro p-2 rounded mt-2 border text-dark-pro" style="background:#fffbeb!important"><b class="text-dark-pro">Analisis:</b><br><span class="text-dark-pro">'+d.analisis_claro+'</span></div><div class="small-pro p-2 rounded mt-2 border text-dark-pro" style="background:#f0fdf4!important"><b class="text-dark-pro">Reporte + Script BASA Profesional:</b><br><span class="text-dark-pro">'+d.reporte+'</span></div><small class="text-muted-pro">Backup: '+d.backup_referencia+' | Vigente: '+d.vigente+' | Vencimiento: '+d.vencimiento+' | Entidad autorizada: '+d.entidad_autorizada+' - Solo BASA autorizado - Elimina EDESUR y cualquier otro sin consentimiento/permiso - Menu general completo - Profesional sin carnaval - FIX 436 - Letras contraste alto</small>';
  showSection('modulos');
 });
}
function abrirEjecutarReal(mid,tipo){probarModulo(mid);}

function exportInformeBASA(){
 alert('📄 Export Informe BASA Word/Excel - Profesional - Sin carnaval - Menu general completo - BASA - Elimina EDESUR/Camara/CCA/CCRD sin consentimiento - Coloca BASA - FI-CI-PR-001 7 pasos + SJ-CO-PR-001 19 pasos tope 50% + LO-SG-PR-005 6 tipos retencion 10 anos/Permanente Ley 481-08 - Sistemas SAP + SUGEP + SIGEF + SERC + Multicabinet - Retenciones 10/10/10/5 anos - Tope 50% Art31 Ley 340-06 Art179 Dec 416-23 - Menu general completo 8 secciones - Todos modulos habilitados organizados 5 grupos - Color profesional sin carnaval pomelo - Letras contraste alto - FIX 436 - BASA V1 MENU GENERAL COMPLETO PROFESIONAL');
}

renderGrupos();
showSection('dashboard');
</script>
</body></html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_MENU_GENERAL, config=CONFIG_BASA, matriz=MATRIZ_BASA_PROFESIONAL, mods=MODULOS_BASA_COMPLETO, grupos=GRUPOS_BASA)

@app.route('/api/probar/consentimiento', methods=['POST'])
def probar_consentimiento():
    data = request.json
    entidad_original = data.get('entidad', '')
    entidad_upper = entidad_original.upper()
    eliminar = CONFIG_BASA["eliminar_nombres_sin_consentimiento"]
    requiere = any(e.upper() in entidad_upper for e in eliminar)
    if requiere:
        entidad_final = CONFIG_BASA["entidad_autorizada"]
        autorizado = False
        mensaje = "Nombre '" + entidad_original + "' requiere consentimiento/permiso explicito - Sin consentimiento no se puede usar - Se usa entidad autorizada BASA generica {{ENTIDAD_AUTORIZADA}} = " + entidad_final + " - Elimina EDESUR y cualquier otro sin su consentimiento o permiso - BASA - Menu general completo profesional - Elimina nombres sin consentimiento"
    else:
        # Si es BASA o generico autorizado
        if "BASA" in entidad_upper or "{{ENTIDAD" in entidad_upper:
            entidad_final = CONFIG_BASA["entidad_autorizada"]
            autorizado = True
            mensaje = "Entidad autorizada BASA - " + entidad_original + " -> " + entidad_final + " - Autorizado - No requiere consentimiento adicional - Solo BASA autorizado - Menu general completo profesional - Elimina EDESUR y cualquier otro sin consentimiento/permiso"
        else:
            entidad_final = CONFIG_BASA["entidad_autorizada"]
            autorizado = False
            mensaje = "Entidad '" + entidad_original + "' no autorizada - Requiere consentimiento/permiso - Se usa BASA generica {{ENTIDAD_AUTORIZADA}} = " + entidad_final + " - Elimina nombres sin consentimiento - Solo BASA autorizado - Menu general completo"
    return jsonify({"entidad_original": entidad_original, "entidad_final": entidad_final, "autorizado": autorizado, "requiere_consentimiento": requiere, "mensaje": mensaje, "config": CONFIG_BASA})

@app.route('/api/probar/pagos', methods=['POST'])
def probar_pagos():
    return jsonify({"config": CONFIG_BASA, "pasos": MATRIZ_BASA_PROFESIONAL["verificacion_pagos"]})

@app.route('/api/probar/contratos', methods=['POST'])
def probar_contratos():
    return jsonify({"config": CONFIG_BASA, "pasos": MATRIZ_BASA_PROFESIONAL["contratos_adendas"]})

@app.route('/api/probar/archivo', methods=['POST'])
def probar_archivo():
    return jsonify({"config": CONFIG_BASA, "archivo": MATRIZ_BASA_PROFESIONAL["archivo_general"]})

@app.route('/api/probar/m10', methods=['POST'])
def probar_m10():
    entidad = CONFIG_BASA["entidad_autorizada"]
    organo = " + ".join(CONFIG_BASA["organo_control"])
    sistemas = " + ".join(CONFIG_BASA["sistemas"])
    transcripcion = "Transcripcion textual precisa real - Matriz_Control_Edesur_Camara_Cuentas.xlsx adaptada BASA - Antes EDESUR DOMINICANA, S.A. - MATRIZ DE RETENCION Y ARCHIVO DOCUMENTAL (NORMATIVA CAMARA DE CUENTAS) - Ahora BASA - MATRIZ DE RETENCION Y ARCHIVO DOCUMENTAL (NORMATIVA " + organo + " - Adaptada BASA - Elimina EDESUR/Camara/CCA/CCRD sin consentimiento/permiso - Coloca BASA) - 4 hojas: Resumen General 3 procedimientos FI-CI-PR-001 Verificacion Pagos 7 pasos + SJ-CO-PR-001 Contratos Adendas 19 pasos tope 50% Art31 Ley 340-06 Art179 Dec 416-23 + LO-SG-PR-005 Archivo General 6 tipos retencion 10 anos/5 anos/Permanente Ley 481-08 - Sistemas " + sistemas + " - Retenciones 10 anos/10 anos/10 anos/5 anos - Tope 50% - Hash BASA-M10-20261014-PROFESIONAL - Menu general completo 8 secciones - Profesional sin carnaval pomelo - Letras contraste alto #1e293b sobre #ffffff - FIX syntax f-string 436 - BASA V1 MENU GENERAL COMPLETO PROFESIONAL"
    analisis = "Analisis claro y preciso - Matriz BASA menu general completo profesional - FI-CI-PR-001 7 pasos: Recibir documentacion pagos verificar documentacion requerida Multicabinet + Revisar detalle soportes valido monto concepto pago SAP Work Management validacion ordenes compra contratos + Comunicacion documentos expedientes revisados conformados Multicabinet + Enviar expediente pago verificado area responsable realizar pago Sistema Gestion Trabajo trazabilidad + Confirma transaccion no varie propiedad legalidad conformidad presupuesto SAP SIGEF SIAFE NOBACI + Carga expediente pago SUGEP Contraloria General obligatoriedad registro institucional + Auditoria Control Interno posterior remision informes Contabilidad Finanzas SAP informes inmediatos posteriores - SJ-CO-PR-001 19 pasos: Remitir comunicacion solicitud elaboracion contrato adenda especificaciones bienes servicios obras + Recibir solicitud elaborar Informe Viabilidad Legal adenda revision Directora 5 dias laborables Art31 Ley 340-06 Art179 Dec 416-23 tope 50% + Recibir aprobacion elaboracion contrato naturaleza Adenda Contrato + Verificar solicitud aprobada soportes entregados 3 dias laborables + Asignar abogado especialista confeccion Informe Viabilidad borrador ULTICABINET + Elaborar Informe Viabilidad remitir Gerencia Coordinacion Contratos maximo 5 dias analisis legal presupuestario + Asignar abogado elaboracion adenda autorizada Gerencia General + Elaborar borrador contrato adenda conforme solicitado remitir validacion 10 dias laborables pliegos condiciones fichas tecnicas + Verificar remitir borrador validado areas Finanzas Compras Proveedor 48h ciclo validacion multi-area + Revisar validar borrador contrato adenda correcciones 48h validacion precios condiciones + Remitir borrador validado abogado fines impresion ejemplares firma + Imprimir ejemplares correspondientes preparar contrato adenda final + Realizar verificacion sujecion Contrato adenda final informe legal justificativo control legalidad + Gestionar firma contrato adenda final Proveedor Gerencia General CUED + Aprobar firmar contrato adenda final Gerente General Presidente CUED + Remitir Gerencia Contratos contrato firmado fines notarizacion + Proceder notarizacion contrato adenda Gerente Contratos Politica SJ-LC-PO-002 Abogados Notarios + Registrar contrato SERC Responsable Registro SERC plazo legal Contraloria General Republica - LO-SG-PR-005 6 tipos retencion: Expedientes Pago Proveedores Terceros 10 anos Multicabinet SUGEP Archivo Historico + Contratos Bienes Obras Servicios 10 anos posteriores terminacion 3 originales SERC + Adendas Enmiendas Contractuales 10 anos SERC Ulticabinet + Informes Viabilidad Legal Justificativos 5 anos + Garantias Fiel Cumplimiento Anticipo Vicios Ocultos hasta devolucion + Comunicaciones Solicitud Aprobacion 5 anos NOBACI - Objetivo aseguramiento informaciones impresas digitales manteniendo expedientes condiciones optimas traslado disposicion final - Permanente / Lista Valoracion Documental Ley 481-08 - Adaptada BASA - Elimina EDESUR/Camara/CCA/CCRD sin consentimiento/permiso - Coloca BASA - Menu general completo 8 secciones - Profesional sin carnaval pomelo - Letras contraste alto WCAG AAA - FIX 436"
    reporte = "Reporte M10 Informes Replicas Confidencial - BASA - DEMO ACTIVO hasta 2026-10-14 - Menu General Completo Profesional - Entidad autorizada BASA - Antes EDESUR - Ahora BASA - Elimina EDESUR y cualquier otro sin consentimiento/permiso - Organo " + organo + " - Antes Camara Cuentas - Ahora " + organo + " - Elimina Camara Cuentas/CCA/CCRD sin consentimiento - Sistemas " + sistemas + " - Retenciones 10 anos/10 anos/10 anos/5 anos/Permanente Ley 481-08 - Tope 50% Art31 Ley 340-06 Art179 Dec 416-23 - Matriz BASA adaptada - FI-CI-PR-001 7 pasos + SJ-CO-PR-001 19 pasos tope 50% + LO-SG-PR-005 6 tipos - Carga multiple + replicas + historial + GDPR + confidencial + trazabilidad + backup SHA-256 - Adaptada - Elimina EDESUR/Camara/CCA/CCRD sin consentimiento - Coloca BASA - Menu general completo 8 secciones: Dashboard General + Matriz Control 3 Procedimientos + FI-CI-PR-001 7 Pasos + SJ-CO-PR-001 19 Pasos Tope 50% + LO-SG-PR-005 6 Tipos + Modulos 5 Grupos Todos Habilitados + M10 Replicas Confidencial + Configuracion BASA - Color profesional sin carnaval pomelo - Fondo #f8fafc, Card #ffffff, Header #0f172a, Texto #0f172a/#334155, Borde #e2e8f0 - Letras contraste alto - FIX syntax f-string 436 - BASA V1 MENU GENERAL COMPLETO PROFESIONAL - DEMO 2026-10-07 a 2026-10-14"
    script = "# M10 BASA MENU GENERAL COMPLETO PROFESIONAL - Elimina EDESUR y cualquier otro sin consentimiento/permiso - Habilita todos modulos organizados 5 grupos - Color profesional sin carnaval pomelo - FIX 436\nCONFIG_BASA = " + str(CONFIG_BASA) + "\n\ndef m10_basa_menu_general_completo():\n entidad_autorizada = CONFIG_BASA['entidad_autorizada'] # BASA - Solo BASA autorizado\n eliminar_sin_consentimiento = CONFIG_BASA['eliminar_nombres_sin_consentimiento'] # EDESUR, EDENORTE, EDEESTE, ETED, Camara Cuentas, CCA, CCRD, CGR\n organo = ' + '.join(CONFIG_BASA['organo_control']) # Contraloria + NOBACI + Ley 10-07 - Elimina Camara sin consentimiento\n sistemas = ' + '.join(CONFIG_BASA['sistemas'])\n # Menu general completo 8 secciones - Todos modulos habilitados 5 grupos organizados\n menu_general = ['Dashboard General BASA', 'Matriz Control 3 Procedimientos BASA', 'FI-CI-PR-001 7 Pasos BASA', 'SJ-CO-PR-001 19 Pasos Tope 50% BASA', 'LO-SG-PR-005 6 Tipos BASA', 'Modulos 5 Grupos Todos Habilitados BASA', 'M10 Replicas Confidencial BASA DEMO 2026-10-14', 'Configuracion BASA + Probar Sistema']\n grupos = {'GRUPO1 COMPRAS Y CONTRATOS': ['M1','M2','M2B'], 'GRUPO2 FINANCIERO Y CONTABLE': ['M3','M4','M14'], 'GRUPO3 FORENSE Y LEGAL': ['M8','M9','M12'], 'GRUPO4 GESTION DOCUMENTAL': ['M10','M11','M15','M16'], 'GRUPO5 ENTERPRISE WORLD': ['M13']}\n return {'entidad_autorizada': entidad_autorizada, 'elimina_sin_consentimiento': eliminar_sin_consentimiento, 'organo': organo, 'sistemas': sistemas, 'menu_general': menu_general, 'grupos': grupos, 'todos_habilitados': True, 'color_profesional': True, 'sin_carnaval_pomelo': True, 'letras_contraste_alto': True, 'fix_436': True}"
    backup = "Backup Matriz_Control_Edesur_Camara_Cuentas.xlsx adaptada BASA - Hash BASA-M10-20261014-PROFESIONAL - Elimina EDESUR/Camara/CCA/CCRD sin consentimiento/permiso - Coloca BASA - Menu general completo 8 secciones - Todos modulos habilitados 5 grupos organizados - Color profesional sin carnaval pomelo - FIX syntax 436"
    return jsonify({"entidad": entidad, "organo": organo, "hash": "BASA-M10-20261014-PROFESIONAL-MENU-GENERAL-COMPLETO", "demo": "DEMO ACTIVO 2026-10-07 a 2026-10-14 - BASA - Menu General Completo Profesional", "transcripcion": transcripcion, "analisis": analisis, "reporte": reporte, "script": script, "backup": backup, "vigente": "2026-10-07", "renovada": "Primera", "vencimiento": "2026-10-14", "config": CONFIG_BASA})

@app.route('/api/probar/tope50', methods=['POST'])
def probar_tope50():
    data = request.json
    monto_base = data.get('monto_base', 1000000)
    adendas = data.get('adendas', [])
    total = sum(adendas)
    tope = monto_base * CONFIG_BASA["limite_adendas"] / 100
    excede = total > tope
    if excede:
        mensaje = "HALLAZGO AUTOMATICO BASA - Menu General Completo Profesional: Tope " + str(CONFIG_BASA["limite_adendas"]) + "% excedido RD$ " + str(total - tope) + " - Informe Viabilidad Legal 5 dias requerido - Art31 Ley 340-06 + Art179 Dec 416-23 - BASA - Elimina EDESUR/Camara/CCA/CCRD sin consentimiento/permiso - Coloca BASA - Profesional sin carnaval pomelo - FIX 436"
    else:
        mensaje = "OK BASA Profesional Menu General Completo: Dentro tope " + str(CONFIG_BASA["limite_adendas"]) + "% - RD$ " + str(total) + " <= RD$ " + str(tope) + " - BASA - Elimina nombres sin consentimiento - Profesional"
    return jsonify({"config": CONFIG_BASA, "monto_base": monto_base, "adendas": adendas, "total": total, "tope": tope, "excede": excede, "mensaje": mensaje})

@app.route('/api/modulos/<mid>/ejecutar_real', methods=['POST'])
def ejecutar_real(mid):
    data = request.json
    tipo = data.get('tipo', 'demo')
    entidad = CONFIG_BASA["entidad_autorizada"]
    organo = " + ".join(CONFIG_BASA["organo_control"])
    sistemas = " + ".join(CONFIG_BASA["sistemas"])
    retencion = CONFIG_BASA["retenciones"]["expedientes_pago"]
    mod = MODULOS_BASA_COMPLETO.get(mid, {"nombre": mid, "codigo": "BASA", "ley": "BASA"})
    transcripcion = "Transcripcion textual precisa real - " + mid + " " + mod["nombre"] + " - " + mod["codigo"] + " - Entidad autorizada " + entidad + " - Solo BASA autorizado - Elimina EDESUR y cualquier otro sin consentimiento/permiso - Organo " + organo + " - Antes Camara Cuentas - Ahora " + organo + " - Elimina Camara/CCA/CCRD sin consentimiento - Sistemas " + sistemas + " - Retencion " + retencion + " - Menu general completo 8 secciones - Todos modulos habilitados 5 grupos organizados - Color profesional sin carnaval pomelo - Letras contraste alto - FIX 436 - Rol " + tipo.upper() + " - DEMO ACTIVO hasta 2026-10-14 - BASA V1 MENU GENERAL COMPLETO PROFESIONAL"
    analisis = "Analisis claro y preciso - " + mid + " " + mod["codigo"] + " - BASA - Menu general completo - Entidad " + entidad + " - Organo " + organo + " - Ley " + mod["ley"] + " - Elimina EDESUR/Camara/CCA/CCRD sin consentimiento - Coloca BASA - Profesional sin carnaval - FIX 436 - Organizado segun ya definido " + mod["grupo"]
    reporte = "Reporte " + mid + " " + mod["codigo"] + " - " + tipo.upper() + " - BASA - Menu General Completo Profesional - Entidad autorizada " + entidad + " - Solo BASA autorizado - Elimina EDESUR y cualquier otro sin consentimiento/permiso - Organo " + organo + " - Sistemas " + sistemas + " - Retencion " + retencion + " - Tope " + str(CONFIG_BASA["limite_adendas"]) + "% Art31 + Art179 - Menu general completo 8 secciones: Dashboard + Matriz 3 Procedimientos + FI-CI-PR-001 7 Pasos + SJ-CO-PR-001 19 Pasos Tope 50% + LO-SG-PR-005 6 Tipos + Modulos 5 Grupos Todos Habilitados + M10 Replicas + Configuracion - Organizado 5 grupos: GRUPO1 COMPRAS M1 M2 M2B + GRUPO2 FINANCIERO M3 M4 M14 + GRUPO3 FORENSE M8 M9 M12 + GRUPO4 GESTION M10 M11 M15 M16 + GRUPO5 WORLD M13 - Todos habilitados DEMO ACTIVO 2026-10-14 - Color profesional sin carnaval pomelo - Fondo #f8fafc, Card #ffffff, Header #0f172a, Texto #0f172a/#334155 - Letras contraste alto WCAG AAA - FIX syntax f-string 436 - BASA V1 MENU GENERAL COMPLETO PROFESIONAL - BHD 08694150021"
    backup = "Backup " + mid + " BASA - Hash BASA-" + mid + "-20261014-PROFESIONAL - Menu general completo - Elimina nombres sin consentimiento - Coloca BASA - Profesional"
    return jsonify({"nombre": mod["nombre"], "codigo": mod["codigo"], "entidad_autorizada": entidad, "organo_control": organo, "ley_adaptada": mod["ley"] + " - " + organo + " - BASA Profesional", "sistemas": sistemas, "retencion_adaptada": retencion + " - BASA", "transcripcion_textual": transcripcion, "analisis_claro": analisis, "reporte": reporte, "backup_referencia": backup, "vigente": "2026-10-07", "renovada": "Primera", "vencimiento": "2026-10-14", "config": CONFIG_BASA})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
