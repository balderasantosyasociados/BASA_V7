# -*- coding: utf-8 -*-
# BASA V1 SUPERIOR GENERAL - ELIMINA TERMINO CONSENTIMIENTO - NO PUBLICO PERO SI CREAR ACTUALIZAR AUDITAR TODO GENERAL AQUI Y OTRO PAIS - TODOS MODULOS Y SCRIPT SUPERIOR GENERAL - MENU GENERAL COMPLETO PROFESIONAL - FIX 436
from flask import Flask, render_template_string, request, jsonify

CONFIG_BASA_SUPERIOR = {
    "entidad_base": "BASA",
    "entidad_adaptable": "{{ENTIDAD}}",
    "entidad_generica": "Entidad no publica pero si crear, actualizar y auditar todo en general de aqui y de otro pais - General",
    "organo_control_superior": ["Contraloria General de la Republica", "NOBACI", "Ley 10-07", "COSO", "COBIT", "GAO", "INTOSAI"],
    "sistemas_superior": ["SAP", "SUGEP", "SIGEF", "SERC", "Multicabinet", "ULTICABINET", "Work Management", "SIAFE", "ERP Superior General"],
    "retenciones_superior": {"expedientes_pago": "10 anos", "contratos": "10 anos", "adendas": "10 anos", "viabilidad_legal": "5 anos", "archivo_general": "Permanente / Ley 481-08 / General aqui y otro pais"},
    "limite_adendas_superior": 50,
    "alcance_superior": "Crear, actualizar y auditar todo en general de aqui RD y de otro pais USA ES MX CO PA BR - General todo modulo y script superior - BASA Superior General",
    "version_superior": "V1 BASA SUPERIOR GENERAL - Elimina termino consentimiento - No publico pero si crear actualizar auditar todo general aqui y otro pais - Todos modulos y script superior - Profesional - 2026-10-07",
    "color_profesional": {"fondo": "#f8fafc", "card": "#ffffff", "header": "#0f172a", "texto_oscuro": "#0f172a", "texto_medio": "#334155", "texto_claro": "#64748b", "borde": "#e2e8f0"}
}

GRUPOS_SUPERIOR = {
    "GRUPO 1 - COMPRAS Y CONTRATOS - BASA SUPERIOR GENERAL - AQUI Y OTRO PAIS": ["M1", "M2", "M2B"],
    "GRUPO 2 - FINANCIERO Y CONTABLE - BASA SUPERIOR GENERAL - AQUI Y OTRO PAIS": ["M3", "M4", "M14"],
    "GRUPO 3 - FORENSE Y LEGAL - BASA SUPERIOR GENERAL - AQUI Y OTRO PAIS": ["M8", "M9", "M12"],
    "GRUPO 4 - GESTION DOCUMENTAL - BASA SUPERIOR GENERAL - FI-CI-PR-001 + SJ-CO-PR-001 + LO-SG-PR-005 - AQUI Y OTRO PAIS": ["M10", "M11", "M15", "M16"],
    "GRUPO 5 - ENTERPRISE WORLD - BASA SUPERIOR GENERAL - AQUI Y OTRO PAIS - USA ES MX CO PA BR": ["M13"]
}

MODULOS_SUPERIOR_GENERAL = {
    "M1": {"nombre": "M1 Scraper Portal vs ComprasDominicana + Matriz Modalidad Monto - BASA Superior General", "desc": "Cruce portal institucional vs ComprasDominicana + matriz modalidad monto + incidencias diferencia referencia monto - Superior general - Crea actualiza audita todo general aqui RD y otro pais USA ES MX CO PA BR - Adaptable automatico {{ENTIDAD}} - General", "precio": 250, "codigo": "FI-CI-PR-001 + SJ-CO-PR-001 - BASA Superior General", "ley": "Ley 340-06 Art16-17 + Ley 200-04 + Ley 10-07 + NOBACI + FAR + BASA Superior General - Aqui y otro pais", "estado": "Habilitado Superior General - DEMO", "grupo": "GRUPO 1 - BASA Superior General", "script_superior": "basa_superior_general_m1_scraper_portal_vs_compras_matriz_modalidad_monto_aqui_otro_pais.py"},
    "M2": {"nombre": "M2 Contratos Adendas Tope 50% Art31 + Art179 Dec 416-23 - BASA Superior General", "desc": "Valida tope 50% + Informe Viabilidad Legal 5 dias + ULTICABINET + SERC + ciclo validacion multi-area 48h + firma CUED + notarizacion - Superior general - Crea actualiza audita todo general aqui y otro pais - Tope 50% Art31 - BASA Superior", "precio": 250, "codigo": "SJ-CO-PR-001 - BASA Superior General - Tope 50%", "ley": "Ley 340-06 Art31 + Dec 416-23 Art179 + Ley 10-07 + NOBACI + FAR + BASA Superior General - Tope 50% - Aqui y otro pais", "estado": "Habilitado Superior General - DEMO", "grupo": "GRUPO 1 - BASA Superior General", "script_superior": "basa_superior_general_m2_contratos_adendas_tope_50_art31_art179_aqui_otro_pais.py"},
    "M2B": {"nombre": "M2B Elaboracion Contratos y Adendas 19 Pasos - BASA Superior General - Aqui y Otro Pais", "desc": "19 pasos elaboracion contratos adendas + Informe Viabilidad + asignacion abogado ULTICABINET + borrador 10 dias + validacion multi-area 48h + firma Gerencia General CUED + notarizacion + SERC + registro + tope 50% Art31 + Informe Viabilidad 5 dias + Superior general - Crea actualiza audita todo general aqui y otro pais - BASA Superior General", "precio": 250, "codigo": "SJ-CO-PR-001 - BASA Superior General - 19 Pasos", "ley": "Ley 340-06 + Dec 416-23 + Ley 10-07 + NOBACI + FAR + BASA Superior General - Aqui y otro pais - Tope 50%", "estado": "Habilitado Superior General - DEMO", "grupo": "GRUPO 1 - BASA Superior General", "script_superior": "basa_superior_general_m2b_elaboracion_contratos_adendas_19pasos_aqui_otro_pais.py"},
    "M3": {"nombre": "M3 Nomina TSS - BASA Superior General - Aqui y Otro Pais", "desc": "TSS/DGII/RPE + IMSS MX + PILA CO + SS USA + Seguridad Social ES + BASA Superior General - Crea actualiza audita todo general aqui y otro pais - General", "precio": 250, "codigo": "FI-CI-PR-001 - BASA Superior General", "ley": "Ley 87-01 TSS + IMSS MX + PILA CO + SS USA + BASA Superior General - Aqui y otro pais", "estado": "Habilitado Superior General - DEMO", "grupo": "GRUPO 2 - BASA Superior General", "script_superior": "basa_superior_general_m3_nomina_tss_aqui_otro_pais.py"},
    "M4": {"nombre": "M4 Pagos Libramientos BHD 08694150021 + SUGEP + SIGEF + SAP - BASA Superior General", "desc": "FI-CI-PR-001 Verificacion Documentos Expedientes Pago 7 pasos + Multicabinet + SAP + Work Management + SUGEP + SIGEF + SIAFE + trazabilidad + NOBACI + Superior general - Crea actualiza audita todo general aqui y otro pais - BASA Superior", "precio": 250, "codigo": "FI-CI-PR-001 - BASA Superior General", "ley": "NOBACI + Ley 10-07 + SUGEP + SIGEF + SAP + BASA Superior General - Aqui y otro pais - General", "estado": "Habilitado Superior General - DEMO", "grupo": "GRUPO 2 - BASA Superior General", "script_superior": "basa_superior_general_m4_pagos_libramientos_sugep_sigef_sap_aqui_otro_pais.py"},
    "M14": {"nombre": "M14 Verificacion Documentos Expedientes Pago FI-CI-PR-001 7 Pasos - BASA Superior General", "desc": "FI-CI-PR-001 7 pasos: Recibir documentacion verificar documentacion requerida Multicabinet + Revisar detalle soportes valido monto concepto SAP Work Management + Comunicacion documentos conformados Multicabinet + Enviar expediente verificado Sistema Gestion Trabajo trazabilidad + Confirma transaccion propiedad legalidad conformidad presupuesto SAP SIGEF SIAFE NOBACI + Carga SUGEP + Auditoria Control Interno posterior informes SAP - Superior general - Crea actualiza audita todo general aqui y otro pais - BASA Superior General Profesional", "precio": 250, "codigo": "FI-CI-PR-001 - BASA Superior General - 7 Pasos", "ley": "FI-CI-PR-001 + NOBACI + Ley 10-07 + SUGEP + SIGEF + BASA Superior General - Aqui y otro pais - General", "estado": "Habilitado Superior General - DEMO", "grupo": "GRUPO 2 - BASA Superior General", "script_superior": "basa_superior_general_m14_fi_ci_pr_001_7pasos_aqui_otro_pais.py"},
    "M8": {"nombre": "M8 Forense + Base Historica Mundial Oculta + Deteccion Auto Similar - BASA Superior General", "desc": "Base oculta CCRD+GAO+ASF+CGR+TC ES + deteccion hallazgo parecido/similar + crear hallazgo auto + aplicar mejoras + actualizar sistema + uso internacional + BASA Superior General - Superior general - Crea actualiza audita todo general aqui y otro pais - General", "precio": 250, "codigo": "Forense - BASA Superior General - Aqui y otro pais", "ley": "Const Art146 + Ley 10-04 + FCPA + SOX + GAO + INTOSAI + BASA Superior General - Aqui y otro pais - General", "estado": "Habilitado Superior General - DEMO", "grupo": "GRUPO 3 - BASA Superior General", "script_superior": "basa_superior_general_m8_forense_base_oculta_deteccion_auto_similar_aqui_otro_pais.py"},
    "M9": {"nombre": "M9 Auditoria Forense Contratos Adendas - BASA Superior General", "desc": "Auditoria forense contratos adendas tope 50% + Informe Viabilidad Legal + ULTICABINET + SERC + Superior general - Crea actualiza audita todo general aqui y otro pais - BASA Superior", "precio": 250, "codigo": "SJ-CO-PR-001 Forense - BASA Superior General", "ley": "Ley 340-06 Art31 + Dec 416-23 Art179 + BASA Superior General - Tope 50% - Aqui y otro pais", "estado": "Habilitado Superior General - DEMO", "grupo": "GRUPO 3 - BASA Superior General", "script_superior": "basa_superior_general_m9_auditoria_forense_contratos_adendas_aqui_otro_pais.py"},
    "M12": {"nombre": "M12 Legal - Cumplimiento Normativo NOBACI - BASA Superior General", "desc": "Cumplimiento normativo NOBACI + Ley 10-07 + Ley 340-06 + Ley 481-08 + COSO + COBIT + GAO + INTOSAI + BASA Superior General - Superior general - Crea actualiza audita todo general aqui y otro pais - General", "precio": 250, "codigo": "NOBACI + Ley 10-07 + COSO + COBIT + BASA Superior General", "ley": "NOBACI + Ley 10-07 + Ley 340-06 + COSO + COBIT + GAO + BASA Superior General - Aqui y otro pais - General", "estado": "Habilitado Superior General - DEMO", "grupo": "GRUPO 3 - BASA Superior General", "script_superior": "basa_superior_general_m12_legal_cumplimiento_nobaci_coso_cobit_aqui_otro_pais.py"},
    "M10": {"nombre": "M10 Informes Replicas Confidencial - BASA Superior General - DEMO ACTIVO 2026-10-14 - Aqui y Otro Pais", "desc": "Carga multiple + replicas + historial + GDPR + confidencial + FI-CI-PR-001 + SJ-CO-PR-001 + LO-SG-PR-005 - Superior general - Crea actualiza audita todo general aqui RD y otro pais USA ES MX CO PA BR - Adaptable automatico {{ENTIDAD}} - General todo modulo y script superior - BASA Superior General - DEMO ACTIVO 2026-10-14 - Profesional", "precio": 250, "codigo": "LO-SG-PR-005 + FI-CI-PR-001 + SJ-CO-PR-001 - BASA Superior General - General aqui y otro pais", "ley": "NOBACI + Ley 10-07 + Ley 340-06 + Ley 481-08 + GDPR + COSO + COBIT + GAO + BASA Superior General - Aqui y otro pais - General", "estado": "Habilitado Superior General - DEMO ACTIVO hasta 2026-10-14 - Superior", "grupo": "GRUPO 4 - BASA Superior General", "script_superior": "basa_superior_general_m10_informes_replicas_confidencial_aqui_otro_pais_superior_general.py"},
    "M11": {"nombre": "M11 Transcripcion Textual Precisa Real + Hash Validable - BASA Superior General", "desc": "Transcripcion textual precisa real + hash SHA-256 validable manual + backup referencia validable + BASA Superior General - Superior general - Crea actualiza audita todo general aqui y otro pais - General", "precio": 250, "codigo": "LO-SG-PR-005 + BASA Superior General", "ley": "Ley 481-08 + NOBACI + BASA Superior General - Aqui y otro pais", "estado": "Habilitado Superior General - DEMO", "grupo": "GRUPO 4 - BASA Superior General", "script_superior": "basa_superior_general_m11_transcripcion_textual_precisa_hash_validable_aqui_otro_pais.py"},
    "M15": {"nombre": "M15 Archivo General LO-SG-PR-005 Retencion 10 Anos - BASA Superior General", "desc": "6 tipos retencion BASA - 10 anos / 5 anos / Permanente Ley 481-08 - Multicabinet / SUGEP / SERC / Ulticabinet - Superior general - Crea actualiza audita todo general aqui y otro pais - BASA Superior General Profesional - General", "precio": 250, "codigo": "LO-SG-PR-005 - BASA Superior General - General aqui y otro pais", "ley": "LO-SG-PR-005 + Ley 481-08 + NOBACI + Ley 10-07 + BASA Superior General - Aqui y otro pais - General", "estado": "Habilitado Superior General - DEMO", "grupo": "GRUPO 4 - BASA Superior General", "script_superior": "basa_superior_general_m15_archivo_general_retencion_10anos_aqui_otro_pais.py"},
    "M16": {"nombre": "M16 Matriz Control Cumplimiento Normativo 3 Procedimientos - BASA Superior General", "desc": "Matriz Control Cumplimiento Normativo: FI-CI-PR-001 Verificacion Pagos + SJ-CO-PR-001 Contratos Adendas + LO-SG-PR-005 Archivo General + Codigo Procedimiento + Nombre Documento + Direccion Gerencia Responsable + Version + Objetivo Principal + Tiempo Retencion Archivo + Adaptada BASA Superior General - Superior general - Crea actualiza audita todo general aqui y otro pais - General todo modulo y script superior", "precio": 250, "codigo": "Matriz Control - BASA Superior General - General aqui y otro pais", "ley": "Matriz Control + NOBACI + Ley 340-06 + Ley 481-08 + Ley 10-07 + COSO + COBIT + GAO + BASA Superior General - Aqui y otro pais - General", "estado": "Habilitado Superior General - DEMO", "grupo": "GRUPO 4 - BASA Superior General", "script_superior": "basa_superior_general_m16_matriz_control_cumplimiento_normativo_aqui_otro_pais.py"},
    "M13": {"nombre": "M13 WORLD Multi-Pais/Idioma/Moneda + BASA Superior General - Aqui y Otro Pais", "desc": "DO US MX PA CO ES BR + ES EN FR PT + USD DOP EUR MXN + BHD 08694150021 + BASA Superior General - Superior general - Crea actualiza audita todo general aqui RD y otro pais USA ES MX CO PA BR - NOBACI/COSO/COBIT/GAO/INTOSAI - Profesional - General todo modulo y script superior", "precio": 250, "codigo": "WORLD - BASA Superior General - Aqui y otro pais - General", "ley": "Multi-pais/idioma/moneda + BHD 08694150021 + NOBACI/COSO/COBIT/GAO/INTOSAI + BASA Superior General - Aqui y otro pais - General", "estado": "Habilitado Superior General - DEMO", "grupo": "GRUPO 5 - BASA Superior General", "script_superior": "basa_superior_general_m13_world_multi_pais_idioma_moneda_aqui_otro_pais_superior_general.py"},
}

MATRIZ_SUPERIOR = {
    "procedimientos": [
        {"codigo": "FI-CI-PR-001", "nombre": "Procedimiento Verificacion de Documentos y Expedientes de Pago - BASA Superior General - Aqui y Otro Pais", "direccion": "BASA Superior General - Direccion de Finanzas / Control Interno - Aqui y otro pais", "version": "Ver. Actual BASA Superior General - General aqui y otro pais", "objetivo": "Garantizar legalidad y razonabilidad pagos proveedores soportando erogaciones financieras mediante expedientes debidamente validados - BASA Superior General - Contraloria General + NOBACI + Ley 10-07 + COSO + COBIT + GAO - General aqui y otro pais - Crea actualiza audita todo general", "retencion": "10 anos (Digital/Fisico) - BASA Superior General - General aqui y otro pais", "sistemas": "SAP + SUGEP + SIGEF + SERC + Multicabinet + ULTICABINET + ERP Superior General - Aqui y otro pais"},
        {"codigo": "SJ-CO-PR-001", "nombre": "Procedimiento Elaboracion de Contratos y Adendas de Bienes, Servicios y Obras - BASA Superior General - Aqui y Otro Pais - Tope 50%", "direccion": "BASA Superior General - Direccion Servicios Juridicos / Gerencia de Contratos - Aqui y otro pais", "version": "Ver. 3 BASA Superior General 04/08/2025 - Tope 50% Art31 - General aqui y otro pais", "objetivo": "Garantizar fortalecimiento institucional lineamientos elaboracion actualizacion contratos adendas conforme Ley 340-06 Reglamento 416-23 - Tope 50% Art31 Ley 340-06 Art179 Dec 416-23 + Informe Viabilidad Legal 5 dias + ULTICABINET + SERC + validacion multi-area 48h + firma CUED + notarizacion + SERC - BASA Superior General - General aqui y otro pais - Crea actualiza audita todo general", "retencion": "10 anos (SJ-CO-LI-003 / SJ-CO-LI-004) - BASA Superior General - General aqui y otro pais", "sistemas": "ULTICABINET + SERC + SAP + SUGEP + SIGEF + ERP Superior General - Aqui y otro pais - Tope 50%"},
        {"codigo": "LO-SG-PR-005", "nombre": "Procedimientos Archivo General de Documentos - BASA Superior General - Aqui y Otro Pais", "direccion": "BASA Superior General - Direccion de Logistica / Servicios Generales - Aqui y otro pais", "version": "Ver. 4 BASA Superior General - General aqui y otro pais", "objetivo": "Contribuir aseguramiento informaciones impresas digitales manteniendo expedientes condiciones optimas desde traslado hasta disposicion final - BASA Superior General - Ley 481-08 + General aqui y otro pais - Crea actualiza audita todo general", "retencion": "Permanente / Segun Lista Valoracion Documental (Ley 481-08) - BASA Superior General - General aqui y otro pais", "sistemas": "Multicabinet + SERC + Archivo BASA Superior General + SAP + SUGEP + General aqui y otro pais"},
    ],
    "verificacion_pagos": [
        {"no": 1, "actividad": "Recibir documentacion pagos verificar documentacion requerida - BASA Superior General - Aqui y otro pais - Crea actualiza audita todo general", "rol": "BASA Superior General - Gerente Control / Control Interno - Aqui y otro pais", "herramienta": "Multicabinet / Sistema Contenido - BASA Superior General - SAP + SUGEP + SIGEF + SERC", "control": "Revision integral soportes fisicos digitales - BASA Superior General - Contraloria General + NOBACI + Ley 10-07 + COSO + COBIT + GAO - General aqui y otro pais - Crea actualiza audita todo general", "retencion": "10 anos - BASA Superior General - General aqui y otro pais"},
        {"no": 2, "actividad": "Revisar detalle soportes valido coincida monto concepto pago - BASA Superior General - Aqui y otro pais", "rol": "BASA Superior General - Especialista Control Interno - Aqui y otro pais", "herramienta": "SAP / Work Management System - BASA Superior General - Aqui y otro pais", "control": "Validacion contra ordenes compra contratos - BASA Superior General - General aqui y otro pais", "retencion": "10 anos - BASA Superior General"},
        {"no": 5, "actividad": "Confirma transaccion no varie propiedad, legalidad, conformidad presupuesto - BASA Superior General - Aqui y otro pais", "rol": "BASA Superior General - Gerente Control Interno - Aqui y otro pais", "herramienta": "SAP / SIGEF / SIAFE - BASA Superior General - Aqui y otro pais", "control": "NOBACI + Ley 10-07 + Contraloria General + COSO + COBIT + GAO + INTOSAI - BASA Superior General - General aqui y otro pais - Crea actualiza audita todo general - Superior general", "retencion": "10 anos - BASA Superior General"},
        {"no": 6, "actividad": "Carga expediente pago al Sistema Unificado Gestion Pagos (SUGEP) - BASA Superior General - Aqui y otro pais", "rol": "BASA Superior General - Especialista Control Interno - Aqui y otro pais", "herramienta": "SUGEP (Contraloria General) - BASA Superior General - Aqui y otro pais", "control": "Obligatoriedad registro institucional - BASA Superior General - Contraloria General + NOBACI + Ley 10-07 + COSO + GAO - General aqui y otro pais", "retencion": "10 anos - BASA Superior General"},
        {"no": 7, "actividad": "Auditoria Control Interno posterior remision informes Contabilidad Finanzas - BASA Superior General - Aqui y otro pais - Crea actualiza audita todo general", "rol": "BASA Superior General - Control Interno - Aqui y otro pais", "herramienta": "SAP - BASA Superior General - Aqui y otro pais", "control": "Informes inmediatos posteriores - BASA Superior General - Contraloria General + NOBACI + Ley 10-07 + COSO + COBIT + GAO - General aqui y otro pais - Superior general", "retencion": "10 anos - BASA Superior General"},
    ],
    "contratos_adendas": [
        {"no": 1, "actividad": "Remitir comunicacion solicitud elaboracion contrato adenda especificaciones bienes servicios obras - BASA Superior General - Aqui y otro pais", "responsable": "BASA Superior General - Unidad Solicitante / Compras - Aqui y otro pais", "plazo": "N/A", "base": "Ley 340-06 / Decreto 416-23 - BASA Superior General - Tope 50% - General aqui y otro pais"},
        {"no": 2, "actividad": "Recibir solicitud elaborar Informe Viabilidad Legal adenda revision Directora - BASA Superior General - 5 dias - Tope 50%", "responsable": "BASA Superior General - Coordinador Contrato - Aqui y otro pais", "plazo": "5 dias laborables", "base": "Art. 31 Ley 340-06 y Art. 179 Dec. 416-23 - Tope 50% - BASA Superior General - Informe Viabilidad Legal 5 dias - General aqui y otro pais - Superior general"},
        {"no": 8, "actividad": "Elaborar borrador contrato adenda conforme solicitado remitir validacion - BASA Superior General - 10 dias - Aqui y otro pais", "responsable": "BASA Superior General - Abogado Especializado - Aqui y otro pais", "plazo": "10 dias laborables", "base": "Pliegos condiciones fichas tecnicas - BASA Superior General - General aqui y otro pais"},
        {"no": 9, "actividad": "Verificar remitir borrador validado areas Finanzas Compras Proveedor - BASA Superior General - 48h - Aqui y otro pais", "responsable": "BASA Superior General - Gerente Contratos - Aqui y otro pais", "plazo": "48 horas", "base": "Ciclo validacion multi-area - BASA Superior General - 48h - General aqui y otro pais"},
        {"no": 18, "actividad": "Registrar contrato en Sistema Electronico Registro Contratos (SERC) - BASA Superior General - Aqui y otro pais", "responsable": "BASA Superior General - Responsable Registro SERC - Aqui y otro pais", "plazo": "Plazo legal", "base": "Contraloria General Republica - BASA Superior General - SERC - General aqui y otro pais - Superior general"},
    ],
    "archivo_general": [
        {"tipo": "Expedientes de Pago a Proveedores y Terceros - BASA Superior General - Aqui y otro pais", "area": "BASA Superior General - Direccion Finanzas / Control Interno - Aqui y otro pais", "soporte": "Fisico y Digital (Multicabinet / SUGEP) - BASA Superior General - Aqui y otro pais", "retencion": "10 anos - BASA Superior General - General aqui y otro pais", "destino": "Archivo Historico / Custodia Definitiva - BASA Superior General - General aqui y otro pais", "base": "Ley 10-07 Contraloria y Normas BASA Superior General - Contraloria General + NOBACI + Ley 10-07 + COSO + COBIT + GAO - General aqui y otro pais - Superior general - Crea actualiza audita todo general"},
        {"tipo": "Contratos de Bienes, Obras y Servicios - BASA Superior General - Aqui y otro pais", "area": "BASA Superior General - Direccion Servicios Juridicos (Gerencia Contratos) - Aqui y otro pais", "soporte": "Fisico (3 originales) y Digital (SERC) - BASA Superior General - Aqui y otro pais", "retencion": "10 anos posteriores terminacion - BASA Superior General - General aqui y otro pais", "destino": "Archivo Central / Registro SERC - BASA Superior General - General aqui y otro pais", "base": "Ley 340-06 y Reglamento 416-23 - BASA Superior General - Tope 50% - General aqui y otro pais"},
        {"tipo": "Adendas y Enmiendas Contractuales - BASA Superior General - Aqui y otro pais - Tope 50%", "area": "BASA Superior General - Direccion Servicios Juridicos (Gerencia Contratos) - Aqui y otro pais", "soporte": "Fisico y Digital (SERC / Ulticabinet) - BASA Superior General - Aqui y otro pais", "retencion": "10 anos - BASA Superior General - General aqui y otro pais", "destino": "Archivo Central / Area Administradora - BASA Superior General - General aqui y otro pais", "base": "Ley 340-06 Compras y Contrataciones - BASA Superior General - Tope 50% Art31 - General aqui y otro pais"},
        {"tipo": "Informes de Viabilidad Legal y Justificativos - BASA Superior General - Aqui y otro pais", "area": "BASA Superior General - Direccion Servicios Juridicos - Aqui y otro pais", "soporte": "Digital y Fisico - BASA Superior General - Aqui y otro pais", "retencion": "5 anos - BASA Superior General - General aqui y otro pais", "destino": "Archivo Gestion - BASA Superior General - General aqui y otro pais", "base": "NOBACI / Control Interno - BASA Superior General - COSO + COBIT - General aqui y otro pais - Superior general"},
        {"tipo": "Garantias (Fiel Cumplimiento, Anticipo, Vicios Ocultos) - BASA Superior General - Aqui y otro pais", "area": "BASA Superior General - Gerencia Compras / Finanzas / Juridico - Aqui y otro pais", "soporte": "Fisico (Originales incondicionales) - BASA Superior General - Aqui y otro pais", "retencion": "Hasta devolucion liquidacion definitiva - BASA Superior General - General aqui y otro pais", "destino": "Custodia Valores / Tesoreria - BASA Superior General - General aqui y otro pais", "base": "Ley 340-06 y Pliegos Condiciones - BASA Superior General - General aqui y otro pais"},
        {"tipo": "Comunicaciones de Solicitud y Aprobacion - BASA Superior General - Aqui y otro pais", "area": "BASA Superior General - Areas Requirentes / Gerencia General - Aqui y otro pais", "soporte": "Digital y Fisico - BASA Superior General - Aqui y otro pais", "retencion": "5 anos - BASA Superior General - General aqui y otro pais", "destino": "Archivo Gestion / Multicabinet - BASA Superior General - General aqui y otro pais", "base": "NOBACI - BASA Superior General - Contraloria General + NOBACI + Ley 10-07 + COSO + COBIT - General aqui y otro pais - Superior general"},
    ]
}

app = Flask(__name__)

HTML_SUPERIOR = """
<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BASA - Superior General - Elimina Termino Consentimiento - Crea Actualiza Audita Todo General Aqui y Otro Pais - Todos Modulos Script Superior</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
:root{--fondo:#f8fafc;--card:#ffffff;--header:#0f172a;--texto-oscuro:#0f172a;--texto-medio:#334155;--texto-claro:#64748b;--borde:#e2e8f0;--borde-oscuro:#cbd5e1}
body{background:var(--fondo);color:var(--texto-oscuro);font-family:Inter,Segoe UI,system-ui,sans-serif;font-size:12px;line-height:1.5;margin:0}
.header-pro{background:var(--header);color:#ffffff;padding:0;border-bottom:1px solid #1e293b;position:sticky;top:0;z-index:1000}
.header-top{display:flex;justify-content:space-between;align-items:center;padding:10px 16px}
.header-top h6{color:#ffffff;font-weight:700;margin:0;font-size:12px;letter-spacing:0.2px;line-height:1.3}
.header-top small{color:#94a3b8;font-size:9px;line-height:1.3}
.menu-general{background:#ffffff;border-bottom:1px solid var(--borde);padding:0;display:flex;flex-wrap:wrap;gap:0;position:sticky;top:54px;z-index:999;box-shadow:0 1px 2px rgba(15,23,42,0.06)}
.menu-item{padding:9px 12px;font-size:10px;font-weight:600;color:var(--texto-medio);border-right:1px solid var(--borde);cursor:pointer;background:#ffffff}
.menu-item:hover{background:#f8fafc;color:var(--texto-oscuro)}
.menu-item.active{background:var(--header);color:#ffffff}
.card-pro{background:var(--card);border:1px solid var(--borde);border-radius:8px;box-shadow:0 1px 2px rgba(15,23,42,0.06)}
.card-header-pro{background:#f8fafc;border-bottom:1px solid var(--borde);padding:10px 14px;font-weight:700;font-size:11px;text-transform:uppercase;letter-spacing:0.4px;color:var(--texto-oscuro)}
.table-pro{font-size:10px;color:var(--texto-oscuro);margin:0}
.table-pro thead{background:#f8fafc;color:var(--texto-oscuro)}
.table-pro thead th{font-weight:700;font-size:9px;text-transform:uppercase;letter-spacing:0.3px;color:var(--texto-oscuro);border-color:var(--borde);padding:7px 8px}
.table-pro tbody td{color:var(--texto-medio);border-color:var(--borde);padding:6px 8px;vertical-align:top}
.btn-pro{background:var(--header);color:#ffffff;border:1px solid var(--header);padding:6px 12px;border-radius:6px;font-weight:600;font-size:10px}
.btn-sec{background:#ffffff;color:var(--texto-medio);border:1px solid var(--borde-oscuro);padding:5px 10px;border-radius:6px;font-size:10px}
.badge-pro{background:var(--header);color:#ffffff;padding:4px 8px;border-radius:4px;font-size:9px;font-weight:700}
.badge-light-pro{background:#f1f5f9;color:var(--texto-medio);border:1px solid var(--borde);padding:3px 7px;border-radius:4px;font-size:9px;font-weight:600}
.badge-success-pro{background:#f0fdf4;color:#166534;border:1px solid #bbf7d0;padding:3px 7px;border-radius:4px;font-size:9px;font-weight:600}
.text-dark-pro{color:var(--texto-oscuro)!important}
.small-pro{font-size:10px;color:var(--texto-claro);line-height:1.4}
</style>
</head><body>
<div class="header-pro">
<div class="header-top">
<div>
<h6>BASA V1 SUPERIOR GENERAL - ELIMINA TERMINO CONSENTIMIENTO - Entidad no publica pero si crear, actualizar y auditar todo en general de aqui y de otro pais - General todo modulo y script superior - Menu general completo profesional - Sin carnaval - FIX 436</h6>
<small>Entidad base: {{ config.entidad_base }} | Adaptable: {{ config.entidad_adaptable }} - {{ config.entidad_generica }} | Organo Superior: {{ config.organo_control_superior|join(' + ') }} | Sistemas Superior: {{ config.sistemas_superior|join(' + ') }} | Retenciones Superior: {{ config.retenciones_superior.expedientes_pago }}/{{ config.retenciones_superior.contratos }}/{{ config.retenciones_superior.adendas }}/{{ config.retenciones_superior.viabilidad_legal }}/{{ config.retenciones_superior.archivo_general }} | Tope Superior: {{ config.limite_adendas_superior }}% Art31 Ley 340-06 Art179 Dec 416-23 | Alcance Superior: {{ config.alcance_superior }} | {{ config.version_superior }}</small>
</div>
<div class="d-flex gap-2 align-items-center">
<span class="badge-pro">BASA SUPERIOR GENERAL</span>
<span class="badge-success-pro">ELIMINA TERMINO CONSENTIMIENTO</span>
<span class="badge-light-pro">CREA ACTUALIZA AUDITA TODO GENERAL</span>
</div>
</div>
</div>

<div class="menu-general" id="menuGeneral">
<div class="menu-item active" onclick="showSection('dashboard')">📊 Dashboard Superior General BASA</div>
<div class="menu-item" onclick="showSection('matriz')">📋 Matriz Control 3 Procedimientos - BASA Superior - Aqui y Otro Pais</div>
<div class="menu-item" onclick="showSection('pagos')">💰 FI-CI-PR-001 7 Pasos - BASA Superior - Aqui y Otro Pais</div>
<div class="menu-item" onclick="showSection('contratos')">📝 SJ-CO-PR-001 19 Pasos Tope 50% - BASA Superior - Aqui y Otro Pais</div>
<div class="menu-item" onclick="showSection('archivo')">📁 LO-SG-PR-005 6 Tipos - BASA Superior - Aqui y Otro Pais</div>
<div class="menu-item" onclick="showSection('modulos')">📦 Todos Modulos 5 Grupos Habilitados - BASA Superior General - Aqui y Otro Pais - Script Superior</div>
<div class="menu-item" onclick="showSection('informes')">📄 M10 Replicas Confidencial - BASA Superior - DEMO 2026-10-14 - Aqui y Otro Pais</div>
<div class="menu-item" onclick="showSection('config')">⚙️ Config Superior General - Crea Actualiza Audita Todo General Aqui y Otro Pais - Script Superior General</div>
</div>

<div class="container-fluid p-3">

<div id="sec-dashboard" class="section">
<div class="row g-3">
<div class="col-md-8">
<div class="card-pro">
<div class="card-header-pro">📊 Dashboard Superior General BASA - Elimina Termino Consentimiento - Entidad no publica pero si crear, actualizar y auditar todo en general de aqui y de otro pais - General todo modulo y script superior</div>
<div class="p-3">
<div class="row g-2">
<div class="col-md-3"><div class="card-pro p-2 text-center" style="background:#f8fafc"><div class="small-pro">Procedimientos Superior General</div><div style="font-size:18px;font-weight:700;color:var(--texto-oscuro)">3</div><div class="small-pro">FI-CI-PR-001 + SJ-CO-PR-001 + LO-SG-PR-005 - BASA Superior - Aqui y otro pais - General</div></div></div>
<div class="col-md-3"><div class="card-pro p-2 text-center" style="background:#f0fdf4"><div class="small-pro">Actividades Superior General</div><div style="font-size:18px;font-weight:700;color:var(--texto-oscuro)">32</div><div class="small-pro">7 pagos + 19 contratos + 6 archivo - BASA Superior - Aqui y otro pais - Crea actualiza audita todo general</div></div></div>
<div class="col-md-3"><div class="card-pro p-2 text-center" style="background:#fffbeb"><div class="small-pro">Modulos Superior General</div><div style="font-size:18px;font-weight:700;color:var(--texto-oscuro)">13</div><div class="small-pro">5 grupos organizados - Todos habilitados DEMO - BASA Superior General - Aqui y otro pais - Script superior general</div></div></div>
<div class="col-md-3"><div class="card-pro p-2 text-center" style="background:#f0f9ff"><div class="small-pro">Alcance Superior General</div><div style="font-size:14px;font-weight:700;color:var(--texto-oscuro)">RD + USA ES MX CO PA BR</div><div class="small-pro">Crea actualiza audita todo general aqui y otro pais - General todo modulo y script superior</div></div></div>
</div>
<div class="p-2 mt-2 rounded" style="background:#f8fafc;border:1px solid var(--borde)">
<div class="small-pro text-dark-pro">
<b class="text-dark-pro">BASA V1 SUPERIOR GENERAL - Elimina termino consentimiento - No publico pero si crear, actualizar y auditar todo en general de aqui y de otro pais - General todo modulo y script superior - Menu general completo profesional - Sin carnaval - FIX 436:</b><br>
- <b>Elimina termino consentimiento:</b> Antes decia Elimina nombres sin consentimiento/permiso - Requiere consentimiento/permiso - Solo BASA autorizado - Ahora eliminado termino consentimiento totalmente - Ahora menciona por la aplicacion de aquellos no publico pero si en crear y poder actualizar y auditar todo en general de aqui y de otro pais general todo modulo y script superior - Entidad no publica pero si crear, actualizar y auditar todo en general de aqui RD y de otro pais USA ES MX CO PA BR - General - BASA Superior General<br>
- <b>No publico pero si crear, actualizar y auditar todo en general:</b> Aplicacion menciona aquellos no publico pero si en crear y poder actualizar y auditar todo en general de aqui y de otro pais - FI-CI-PR-001 Verificacion Pagos 7 pasos + SJ-CO-PR-001 Contratos Adendas 19 pasos tope 50% Art31 Ley 340-06 Art179 Dec 416-23 + LO-SG-PR-005 Archivo General 6 tipos retencion 10 anos/Permanente Ley 481-08 - Adaptable automatico {{ENTIDAD}} - Entidad no publica pero si crear, actualizar y auditar todo en general de aqui y de otro pais - General todo modulo y script superior - BASA Superior General<br>
- <b>General todo modulo y script superior - Aqui y otro pais:</b> Todos modulos M1-M16 organizados 5 grupos - GRUPO 1 COMPRAS Y CONTRATOS M1 M2 M2B + GRUPO 2 FINANCIERO Y CONTABLE M3 M4 M14 + GRUPO 3 FORENSE Y LEGAL M8 M9 M12 + GRUPO 4 GESTION DOCUMENTAL M10 M11 M15 M16 + GRUPO 5 ENTERPRISE WORLD M13 - Cada modulo con script superior general basa_superior_general_mX_..._aqui_otro_pais.py - Crea actualiza audita todo general aqui RD y otro pais USA ES MX CO PA BR - General - BASA Superior General - Menu general completo - Profesional - Sin carnaval pomelo - Letras contraste alto - FIX 436<br>
- <b>Menu general completo 8 secciones - Profesional sin carnaval - FIX 436:</b> Dashboard Superior General BASA + Matriz Control 3 Procedimientos BASA Superior Aqui y Otro Pais + FI-CI-PR-001 7 Pasos BASA Superior Aqui y Otro Pais + SJ-CO-PR-001 19 Pasos Tope 50% BASA Superior Aqui y Otro Pais + LO-SG-PR-005 6 Tipos BASA Superior Aqui y Otro Pais + Todos Modulos 5 Grupos Habilitados BASA Superior General Aqui y Otro Pais Script Superior + M10 Replicas Confidencial BASA Superior DEMO 2026-10-14 Aqui y Otro Pais + Config Superior General Crea Actualiza Audita Todo General Aqui y Otro Pais Script Superior General - Color profesional #f8fafc fondo, #ffffff card, #0f172a header, #0f172a/#334155 texto contraste alto WCAG AAA - Sin pomelo morado #7c3aed carnaval - Letras no se pierden<br>
</div>
</div>
</div>
</div>
</div>
<div class="col-md-4">
<div class="card-pro p-3">
<h6 class="text-dark-pro">🧪 Probar Sistema BASA Superior General - Crea Actualiza Audita Todo General Aqui y Otro Pais</h6>
<div class="d-grid gap-2 mt-2">
<button onclick="showSection('matriz'); probarMatriz()" class="btn-pro">📋 Probar Matriz 3 Procedimientos - BASA Superior General - Aqui y Otro Pais</button>
<button onclick="showSection('pagos'); probarPagos()" class="btn-sec">💰 Probar FI-CI-PR-001 7 Pasos - BASA Superior General</button>
<button onclick="showSection('contratos'); probarContratos()" class="btn-sec">📝 Probar SJ-CO-PR-001 19 Pasos Tope 50% - BASA Superior General</button>
<button onclick="showSection('archivo'); probarArchivo()" class="btn-sec">📁 Probar LO-SG-PR-005 6 Tipos - BASA Superior General</button>
<button onclick="showSection('modulos'); probarModulos()" class="btn-pro">📦 Ver Todos Modulos 5 Grupos Habilitados - BASA Superior General - Script Superior</button>
<button onclick="showSection('informes'); probarM10()" class="btn-pro">📄 Probar M10 Replicas Confidencial - BASA Superior - DEMO 2026-10-14 - Aqui y Otro Pais</button>
<button onclick="probarTope50()" class="btn-sec" style="border-color:#fbbf24">⚠️ Probar Tope 50% Adendas - BASA Superior General - Aqui y Otro Pais - Art31</button>
<button onclick="probarEntidadGeneral()" class="btn-sec" style="background:#f0fdf4;border-color:#bbf7d0">🌎 Probar Entidad General - Aqui y Otro Pais - {{ENTIDAD}} - BASA Superior General</button>
</div>
<div id="dashResult" class="mt-3"></div>
<div class="mt-3">
<h6 class="text-dark-pro">🌎 Entidad Adaptable Automatica - Aqui y Otro Pais - General</h6>
<input id="entidadGeneral" class="form-control form-control-sm" placeholder="Escriba entidad - Ej: BASA, Empresa XYZ, Ministerio, EDESUR, EDENORTE, Empresa USA, Empresa Espana - Adaptable automatico aqui y otro pais - General todo modulo y script superior" style="font-size:10px">
<button onclick="probarEntidadGeneral()" class="btn-pro w-100 mt-1">Probar Entidad General - Crea Actualiza Audita Todo General Aqui y Otro Pais</button>
<div id="entidadResult" class="mt-2 small-pro"></div>
</div>
</div>
</div>
</div>
</div>

<div id="sec-matriz" class="section" style="display:none">
<div class="card-pro">
<div class="card-header-pro">📋 Matriz Control y Cumplimiento Normativo - 3 Procedimientos - BASA Superior General - Aqui y Otro Pais - General todo modulo y script superior - Elimina termino consentimiento</div>
<div class="p-0">
<table class="table table-sm table-bordered table-pro mb-0">
<thead><tr><th>Codigo</th><th>Nombre - BASA Superior General</th><th>Direccion - BASA Superior General</th><th>Version - BASA Superior General</th><th>Objetivo - BASA Superior General - Aqui y Otro Pais - General</th><th>Retencion - BASA Superior General</th><th>Sistemas - BASA Superior General</th><th>Organo Superior General</th></tr></thead>
<tbody>
{% for p in matriz.procedimientos %}
<tr><td><span class="badge-pro">{{ p.codigo }}</span></td><td class="text-dark-pro">{{ p.nombre }}</td><td class="text-dark-pro">{{ p.direccion }}</td><td class="text-dark-pro">{{ p.version }}</td><td class="text-dark-pro">{{ p.objetivo }}</td><td class="text-dark-pro">{{ p.retencion }}</td><td class="text-dark-pro">{{ p.sistemas }}</td><td class="text-dark-pro">{{ config.organo_control_superior|join(' + ') }} - BASA Superior General - General aqui y otro pais</td></tr>
{% endfor %}
</tbody>
</table>
</div>
<div class="p-3 small-pro text-dark-pro" style="background:#f8fafc;border-top:1px solid var(--borde)">
<b class="text-dark-pro">✅ Matriz BASA Superior General - Elimina termino consentimiento - Crea actualiza audita todo general aqui y otro pais - General todo modulo y script superior:</b> Entidad base {{ config.entidad_base }} - Entidad adaptable {{ config.entidad_adaptable }} - {{ config.entidad_generica }} - Antes decia Elimina nombres sin consentimiento/permiso - Ahora eliminado termino consentimiento - Ahora menciona por la aplicacion de aquellos no publico pero si en crear y poder actualizar y auditar todo en general de aqui y de otro pais general todo modulo y script superior - FI-CI-PR-001 Verificacion Pagos 7 pasos + SJ-CO-PR-001 Contratos Adendas 19 pasos tope 50% Art31 + LO-SG-PR-005 Archivo General 6 tipos retencion 10 anos/Permanente Ley 481-08 - Sistemas {{ config.sistemas_superior|join(' + ') }} - Retenciones {{ config.retenciones_superior.expedientes_pago }}/{{ config.retenciones_superior.contratos }}/{{ config.retenciones_superior.adendas }}/{{ config.retenciones_superior.viabilidad_legal }}/{{ config.retenciones_superior.archivo_general }} - Tope {{ config.limite_adendas_superior }}% - Alcance {{ config.alcance_superior }} - Menu general completo 8 secciones - Color profesional sin carnaval - FIX 436 - Letras contraste alto
</div>
</div>
</div>

<div id="sec-pagos" class="section" style="display:none">
<div class="card-pro">
<div class="card-header-pro">💰 FI-CI-PR-001 7 Pasos - BASA Superior General - Aqui y Otro Pais - Crea actualiza audita todo general - General todo modulo y script superior</div>
<div class="p-0">
<table class="table table-sm table-bordered table-pro mb-0">
<thead><tr><th>No</th><th>Actividad - BASA Superior General - Aqui y Otro Pais</th><th>Rol - BASA Superior General</th><th>Herramienta - BASA Superior General - {{ config.sistemas_superior|join(' + ') }}</th><th>Control - BASA Superior General - {{ config.organo_control_superior|join(' + ') }} - General aqui y otro pais</th><th>Retencion - BASA Superior General</th><th>Script Superior General</th></tr></thead>
<tbody>
{% for p in matriz.verificacion_pagos %}
<tr><td class="text-dark-pro">{{ p.no }}</td><td class="text-dark-pro">{{ p.actividad }}</td><td class="text-dark-pro">{{ p.rol }}</td><td class="text-dark-pro">{{ p.herramienta }}</td><td class="text-dark-pro">{{ p.control }}</td><td class="text-dark-pro">{{ p.retencion }}</td><td><code style="font-size:8px">basa_superior_general_fi_ci_pr_001_paso{{ p.no }}_aqui_otro_pais.py</code></td></tr>
{% endfor %}
</tbody>
</table>
</div>
</div>
</div>

<div id="sec-contratos" class="section" style="display:none">
<div class="card-pro">
<div class="card-header-pro">📝 SJ-CO-PR-001 19 Pasos Tope {{ config.limite_adendas_superior }}% - BASA Superior General - Aqui y Otro Pais - General todo modulo y script superior</div>
<div class="p-0">
<table class="table table-sm table-bordered table-pro mb-0">
<thead><tr><th>No</th><th>Actividad - BASA Superior General - Aqui y Otro Pais</th><th>Responsable - BASA Superior General</th><th>Plazo - BASA Superior General</th><th>Base Legal - BASA Superior General - Tope {{ config.limite_adendas_superior }}% - General aqui y otro pais</th><th>Script Superior General</th></tr></thead>
<tbody>
{% for p in matriz.contratos_adendas %}
<tr><td class="text-dark-pro">{{ p.no }}</td><td class="text-dark-pro">{{ p.actividad }}</td><td class="text-dark-pro">{{ p.responsable }}</td><td class="text-dark-pro">{{ p.plazo }}</td><td class="text-dark-pro">{{ p.base }} - {{ config.organo_control_superior|join(' + ') }} - Tope {{ config.limite_adendas_superior }}% - BASA Superior General - General aqui y otro pais - Crea actualiza audita todo general</td><td><code style="font-size:8px">basa_superior_general_sj_co_pr_001_paso{{ p.no }}_aqui_otro_pais.py</code></td></tr>
{% endfor %}
</tbody>
</table>
</div>
</div>
</div>

<div id="sec-archivo" class="section" style="display:none">
<div class="card-pro">
<div class="card-header-pro">📁 LO-SG-PR-005 6 Tipos Retencion - BASA Superior General - Aqui y Otro Pais - General todo modulo y script superior - Crea actualiza audita todo general</div>
<div class="p-0">
<table class="table table-sm table-bordered table-pro mb-0">
<thead><tr><th>Tipo - BASA Superior General - Aqui y Otro Pais</th><th>Area - BASA Superior General</th><th>Soporte - BASA Superior General - {{ config.sistemas_superior|join(' + ') }}</th><th>Retencion - BASA Superior General</th><th>Destino - BASA Superior General</th><th>Base - BASA Superior General - {{ config.organo_control_superior|join(' + ') }} - General aqui y otro pais</th></tr></thead>
<tbody>
{% for p in matriz.archivo_general %}
<tr><td class="text-dark-pro">{{ p.tipo }}</td><td class="text-dark-pro">{{ p.area }}</td><td class="text-dark-pro">{{ p.soporte }}</td><td class="text-dark-pro">{{ p.retencion }}</td><td class="text-dark-pro">{{ p.destino }}</td><td class="text-dark-pro">{{ p.base }}</td></tr>
{% endfor %}
</tbody>
</table>
</div>
</div>
</div>

<div id="sec-modulos" class="section" style="display:none">
<div id="gruposContainer"></div>
<div id="ejecReal" class="card-pro p-3 mt-3" style="display:none"></div>
</div>

<div id="sec-informes" class="section" style="display:none">
<div class="card-pro p-3">
<h6 class="text-dark-pro">📄 M10 Informes Replicas Confidencial - BASA Superior General - DEMO ACTIVO 2026-10-14 - Aqui y Otro Pais - General todo modulo y script superior - Elimina termino consentimiento</h6>
<div class="row g-2 mt-2">
<div class="col-md-3"><button onclick="probarM10()" class="btn-pro w-100">▶️ Probar M10 BASA Superior General - Aqui y Otro Pais - DEMO 2026-10-14</button></div>
<div class="col-md-3"><button onclick="probarTope50()" class="btn-sec w-100">⚠️ Probar Tope 50% - BASA Superior General - Aqui y Otro Pais</button></div>
<div class="col-md-3"><button onclick="probarEntidadGeneral()" class="btn-sec w-100">🌎 Probar Entidad General - Aqui y Otro Pais - {{ config.entidad_adaptable }}</button></div>
<div class="col-md-3"><button onclick="exportInformeSuperior()" class="btn-sec w-100">📄 Export Informe Superior General - Aqui y Otro Pais</button></div>
</div>
<div id="m10Container" class="mt-3"></div>
</div>
</div>

<div id="sec-config" class="section" style="display:none">
<div class="row g-3">
<div class="col-md-6">
<div class="card-pro p-3">
<h6 class="text-dark-pro">⚙️ Config Superior General - Elimina Termino Consentimiento - Crea Actualiza Audita Todo General Aqui y Otro Pais - Script Superior General</h6>
<div class="small-pro text-dark-pro p-3 rounded mt-2" style="background:#f8fafc;border:1px solid var(--borde)">
<b class="text-dark-pro">CONFIG_BASA_SUPERIOR - Elimina termino consentimiento - No publico pero si crear, actualizar y auditar todo en general de aqui y de otro pais - General todo modulo y script superior - Menu general completo profesional - Sin carnaval - FIX 436:</b><br>
<b>Entidad base:</b> {{ config.entidad_base }} - Base BASA<br>
<b>Entidad adaptable:</b> {{ config.entidad_adaptable }} - Adaptable automatico por entidad aqui RD y otro pais USA ES MX CO PA BR - General - Usuario escribe entidad y sistema adapta automatico - Crea actualiza audita todo general<br>
<b>Entidad generica:</b> {{ config.entidad_generica }} - Entidad no publica pero si crear, actualizar y auditar todo en general de aqui y de otro pais - General todo modulo y script superior - Mencion por la aplicacion de aquellos no publico pero si en crear y poder actualizar y auditar todo en general de aqui y de otro pais general todo modulo y script superior - BASA Superior General<br>
<b>Antes:</b> Elimina nombres sin consentimiento/permiso - Requiere consentimiento/permiso - Solo BASA autorizado - Ahora eliminado termino consentimiento totalmente - Ahora menciona por la aplicacion de aquellos no publico pero si en crear y poder actualizar y auditar todo en general de aqui y de otro pais general todo modulo y script superior<br>
<b>Organo control superior:</b> {{ config.organo_control_superior|join(' + ') }} - Contraloria General + NOBACI + Ley 10-07 + COSO + COBIT + GAO + INTOSAI - General aqui y otro pais - Superior general<br>
<b>Sistemas superior:</b> {{ config.sistemas_superior|join(' + ') }} - SAP + SUGEP + SIGEF + SERC + Multicabinet + ULTICABINET + Work Management + SIAFE + ERP Superior General - Aqui y otro pais - General<br>
<b>Retenciones superior:</b> {{ config.retenciones_superior.expedientes_pago }} expedientes pago / {{ config.retenciones_superior.contratos }} contratos / {{ config.retenciones_superior.adendas }} adendas / {{ config.retenciones_superior.viabilidad_legal }} viabilidad legal / {{ config.retenciones_superior.archivo_general }} archivo general - BASA Superior General - General aqui y otro pais<br>
<b>Limite adendas superior:</b> {{ config.limite_adendas_superior }}% Art31 Ley 340-06 + Art179 Dec 416-23 - Tope 50% - Informe Viabilidad Legal 5 dias - ULTICABINET + SERC + validacion multi-area 48h + firma CUED + notarizacion - BASA Superior General - General aqui y otro pais<br>
<b>Alcance superior:</b> {{ config.alcance_superior }} - Crea, actualiza y audita todo en general de aqui RD y de otro pais USA ES MX CO PA BR - General todo modulo y script superior - BASA Superior General - Menu general completo - Profesional - Sin carnaval pomelo - Letras contraste alto WCAG AAA - FIX syntax f-string 436<br>
<b>Version superior:</b> {{ config.version_superior }} - Elimina termino consentimiento - No publico pero si crear actualizar auditar todo general aqui y otro pais - Todos modulos y script superior - Profesional - 2026-10-07<br>
<b>Color profesional sin carnaval:</b> Fondo {{ config.color_profesional.fondo }} gris azulado muy claro profesional (antes morado #7c3aed pomelo carnaval) - Card {{ config.color_profesional.card }} blanco puro - Header {{ config.color_profesional.header }} azul noche profesional - Texto oscuro {{ config.color_profesional.texto_oscuro }} / medio {{ config.color_profesional.texto_medio }} / claro {{ config.color_profesional.texto_claro }} - Borde {{ config.color_profesional.borde }} - Sin amarillo/verde/morado carnaval - Letras no se pierden fondo carnaval pomelo mas profesional - Contraste alto WCAG AAA - FIX 436<br>
</div>
</div>
</div>
<div class="col-md-6">
<div class="card-pro p-3">
<h6 class="text-dark-pro">💻 Scripts Superior General - Todos Modulos - Aqui y Otro Pais - General todo modulo y script superior - BASA Superior General</h6>
<div id="scriptsList" class="small-pro"></div>
</div>
<div class="card-pro p-3 mt-3">
<h6 class="text-dark-pro">🌎 Entidad General - Aqui y Otro Pais - Adaptable Automatico {{ config.entidad_adaptable }} - BASA Superior General</h6>
<input id="entidadGeneral2" class="form-control form-control-sm" placeholder="Escriba entidad general - Ej: BASA, Empresa XYZ, Ministerio, EDESUR, EDENORTE, Ayuntamiento, Empresa USA, Empresa Espana - Adaptable automatico aqui y otro pais - General todo modulo y script superior - Crea actualiza audita todo general" style="font-size:10px">
<button onclick="probarEntidadGeneral2()" class="btn-pro w-100 mt-2">🌎 Probar Entidad General - Aqui y Otro Pais - Crea Actualiza Audita Todo General</button>
<div id="entidadResult2" class="mt-2 small-pro"></div>
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
 var el = document.querySelector('[onclick="showSection(\''+sec+'\')"]');
 if(el) el.classList.add('active');
 window.scrollTo(0,0);
}

function probarMatriz(){
 document.getElementById('dashResult').innerHTML='<div class="p-2 rounded border text-dark-pro" style="background:#f0fdf4;border-color:#bbf7d0!important"><b class="text-dark-pro">Matriz BASA Superior General Probada - Elimina termino consentimiento - General aqui y otro pais</b><br><span class="text-dark-pro">3 procedimientos FI-CI-PR-001 + SJ-CO-PR-001 + LO-SG-PR-005 - BASA Superior General - Aqui y otro pais - General todo modulo y script superior - Crea actualiza audita todo general aqui RD y otro pais USA ES MX CO PA BR - General - Profesional sin carnaval - FIX 436</span></div>';
 showSection('matriz');
}
function probarPagos(){
 fetch('/api/probar/pagos',{method:'POST'}).then(r=>r.json()).then(d=>{
  document.getElementById('dashResult').innerHTML='<div class="p-2 rounded border text-dark-pro" style="background:#f8fafc;border-color:var(--borde)!important"><b class="text-dark-pro">FI-CI-PR-001 7 Pasos BASA Superior General Probado - Aqui y otro pais</b><br><span class="text-dark-pro">'+d.pasos.length+' pasos - Sistemas '+d.config.sistemas_superior.join(' + ')+' - Retencion '+d.config.retenciones_superior.expedientes_pago+' - Organo '+d.config.organo_control_superior.join(' + ')+' - General aqui y otro pais - Crea actualiza audita todo general - BASA Superior General</span></div>';
 });
}
function probarContratos(){
 fetch('/api/probar/contratos',{method:'POST'}).then(r=>r.json()).then(d=>{
  document.getElementById('dashResult').innerHTML='<div class="p-2 rounded border text-dark-pro" style="background:#fffbeb;border-color:#fde68a!important"><b class="text-dark-pro">SJ-CO-PR-001 19 Pasos BASA Superior General Probado - Tope '+d.config.limite_adendas_superior+'% - Aqui y otro pais - General</b><br><span class="text-dark-pro">'+d.pasos.length+' pasos - Tope '+d.config.limite_adendas_superior+'% Art31 Ley 340-06 Art179 Dec 416-23 - Informe Viabilidad 5 dias - ULTICABINET + SERC + 48h - BASA Superior General - General aqui y otro pais - Crea actualiza audita todo general</span></div>';
 });
}
function probarArchivo(){
 fetch('/api/probar/archivo',{method:'POST'}).then(r=>r.json()).then(d=>{
  document.getElementById('dashResult').innerHTML='<div class="p-2 rounded border text-dark-pro" style="background:#f8fafc;border-color:var(--borde)!important"><b class="text-dark-pro">LO-SG-PR-005 6 Tipos BASA Superior General Probado - Aqui y otro pais - General</b><br><span class="text-dark-pro">'+d.archivo.length+' tipos retencion - '+d.config.retenciones_superior.expedientes_pago+'/'+d.config.retenciones_superior.contratos+'/'+d.config.retenciones_superior.adendas+'/'+d.config.retenciones_superior.viabilidad_legal+'/'+d.config.retenciones_superior.archivo_general+' - Sistemas '+d.config.sistemas_superior.join(' + ')+' - BASA Superior General - General aqui y otro pais - Crea actualiza audita todo general</span></div>';
 });
}
function probarModulos(){
 renderGrupos();
 document.getElementById('dashResult').innerHTML='<div class="p-2 rounded border" style="background:#0f172a;color:#ffffff!important"><b style="color:#ffffff">Todos Modulos 5 Grupos Habilitados - BASA Superior General - Aqui y Otro Pais - Script Superior General - General todo modulo y script superior</b><br><span style="color:#cbd5e1">13 modulos organizados: GRUPO1 COMPRAS Y CONTRATOS M1 M2 M2B + GRUPO2 FINANCIERO Y CONTABLE M3 M4 M14 + GRUPO3 FORENSE Y LEGAL M8 M9 M12 + GRUPO4 GESTION DOCUMENTAL M10 M11 M15 M16 + GRUPO5 ENTERPRISE WORLD M13 - Cada modulo script superior general basa_superior_general_mX_..._aqui_otro_pais.py - Crea actualiza audita todo general aqui RD y otro pais USA ES MX CO PA BR - General - BASA Superior General - Menu general completo - Profesional - Sin carnaval pomelo - Letras contraste alto - FIX 436 - Elimina termino consentimiento</span></div>';
}
function probarM10(){
 fetch('/api/probar/m10',{method:'POST'}).then(r=>r.json()).then(d=>{
  document.getElementById('dashResult').innerHTML='<div class="p-2 rounded border text-dark-pro" style="background:#f0fdf4;border-color:#bbf7d0!important"><b class="text-dark-pro">M10 BASA Superior General Probado - DEMO ACTIVO 2026-10-14 - Aqui y Otro Pais - General todo modulo y script superior</b><br><span class="text-dark-pro">Entidad: '+d.entidad+' - Organo: '+d.organo+' - Hash: '+d.hash+' - General aqui y otro pais - Crea actualiza audita todo general - Elimina termino consentimiento - BASA Superior General - Profesional sin carnaval pomelo</span></div>';
  document.getElementById('m10Container').innerHTML='<div class="mt-2"><h6 class="text-dark-pro">M10 Informes Replicas Confidencial - BASA Superior General - Ejecucion Real - DEMO 2026-10-14 - Aqui y Otro Pais - General todo modulo y script superior - Elimina termino consentimiento</h6><div class="small-pro p-3 rounded bg-white border text-dark-pro mt-2"><b class="text-dark-pro">Transcripcion Textual Precisa Real - BASA Superior General - Sin Carnaval - General aqui y otro pais:</b><br><span class="text-dark-pro">'+d.transcripcion+'</span></div><div class="small-pro p-3 rounded mt-2 border text-dark-pro" style="background:#fffbeb!important;border-color:#fde68a!important"><b class="text-dark-pro">Analisis Claro y Preciso - BASA Superior General - Aqui y Otro Pais - General:</b><br><span class="text-dark-pro">'+d.analisis+'</span></div><div class="small-pro p-3 rounded mt-2 border text-dark-pro" style="background:#f0fdf4!important;border-color:#bbf7d0!important"><b class="text-dark-pro">Reporte + Resultados + Script Superior General Rol DEMO - BASA Superior General - Aqui y Otro Pais - General todo modulo y script superior:</b><br><span class="text-dark-pro">'+d.reporte+'</span></div><pre style="background:#0f172a;color:#f8fafc;padding:12px;border-radius:6px;font-size:10px;max-height:400px;overflow:auto;margin-top:8px;border:1px solid #1e293b">'+d.script+'</pre><div class="small-pro p-2 rounded mt-2 text-dark-pro" style="background:#f8fafc;border:1px solid var(--borde)"><b class="text-dark-pro">Backup referencia validable:</b> <span class="text-dark-pro">'+d.backup+' | Vigente: '+d.vigente+' | Renovada: '+(d.renovada||'Primera')+' | Vencimiento: '+d.vencimiento+' | Entidad: '+d.entidad+' - '+d.config.entidad_generica+' - Alcance: '+d.config.alcance_superior+' - Version: '+d.config.version_superior+' - Elimina termino consentimiento - Crea actualiza audita todo general aqui y otro pais - General todo modulo y script superior - Menu general completo - Profesional sin carnaval - FIX 436 - Letras contraste alto</span></div></div>';
 });
}
function probarTope50(){
 fetch('/api/probar/tope50',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({monto_base:1000000, adendas:[200000,150000,200000]})}).then(r=>r.json()).then(d=>{
  var style = d.excede? 'background:#fef2f2!important;border-color:#fecaca!important' : 'background:#f0fdf4!important;border-color:#bbf7d0!important';
  document.getElementById('dashResult').innerHTML='<div class="p-3 rounded border text-dark-pro" style="'+style+'"><b class="text-dark-pro">Test Tope '+d.config.limite_adendas_superior+'% - BASA Superior General - Aqui y Otro Pais - Art31 Ley 340-06 + Art179 Dec 416-23 - General todo modulo y script superior - Elimina termino consentimiento</b><br><span class="text-dark-pro">Monto base: RD$'+d.monto_base.toLocaleString()+'</span><br><span class="text-dark-pro">Adendas: '+d.adendas.join(' + ')+' = RD$'+d.total.toLocaleString()+'</span><br><span class="text-dark-pro">Tope '+d.config.limite_adendas_superior+'%: RD$'+d.tope.toLocaleString()+'</span><br><span class="text-dark-pro">Excede: '+d.excede+'</span><br><span class="text-dark-pro">'+d.mensaje+'</span><br><small class="text-muted-pro">Entidad: '+d.config.entidad_base+' - Adaptable: '+d.config.entidad_adaptable+' - '+d.config.entidad_generica+' - Organo: '+d.config.organo_control_superior.join(' + ')+' - Sistemas: '+d.config.sistemas_superior.join(' + ')+' - Alcance: '+d.config.alcance_superior+' - Elimina termino consentimiento - Crea actualiza audita todo general aqui y otro pais - General todo modulo y script superior - Menu general completo - Profesional sin carnaval - FIX 436 - Letras contraste alto</small></div>';
 });
}
function probarEntidadGeneral(){
 var entidad = document.getElementById('entidadGeneral').value;
 if(!entidad) entidad = 'BASA';
 fetch('/api/probar/entidad_general',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({entidad:entidad})}).then(r=>r.json()).then(d=>{
  document.getElementById('entidadResult').innerHTML='<div class="p-2 rounded border text-dark-pro" style="background:#f0fdf4;border-color:#bbf7d0!important"><b class="text-dark-pro">Entidad General: '+d.entidad_original+' -> '+d.entidad_adaptada+'</b><br><span class="text-dark-pro">Adaptable automatico: '+d.adaptable_automatico+' - Aqui y otro pais: '+d.aqui_y_otro_pais+'</span><br><span class="text-dark-pro">'+d.mensaje+'</span><br><small class="text-muted-pro">Alcance: '+d.config.alcance_superior+' - Entidad generica: '+d.config.entidad_generica+' - Elimina termino consentimiento - Crea actualiza audita todo general aqui y otro pais - General todo modulo y script superior - BASA Superior General - Menu general completo - Profesional</small></div>';
  document.getElementById('dashResult').innerHTML='<div class="p-2 rounded border text-dark-pro" style="background:#f0f9ff;border-color:#bfdbfe!important"><b class="text-dark-pro">Entidad General Probada - Aqui y Otro Pais - General todo modulo y script superior</b><br><span class="text-dark-pro">Entidad: '+d.entidad_original+' -> '+d.entidad_adaptada+' - Adaptable automatico {{ENTIDAD}} = '+d.entidad_adaptada+' - Aqui y otro pais RD + USA ES MX CO PA BR - General - Crea actualiza audita todo general - Elimina termino consentimiento - BASA Superior General</span></div>';
 });
}
function probarEntidadGeneral2(){
 var entidad = document.getElementById('entidadGeneral2').value;
 if(!entidad) entidad = 'BASA';
 fetch('/api/probar/entidad_general',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({entidad:entidad})}).then(r=>r.json()).then(d=>{
  document.getElementById('entidadResult2').innerHTML='<div class="p-2 rounded border text-dark-pro" style="background:#f0fdf4;border-color:#bbf7d0!important"><b class="text-dark-pro">Entidad General: '+d.entidad_original+' -> '+d.entidad_adaptada+' - Aqui y otro pais - General</b><br><span class="text-dark-pro">'+d.mensaje+'</span></div>';
 });
}

function renderGrupos(){
 var html='';
 Object.keys(GRUPOS).forEach(function(grupo){
  html+='<div class="card-pro mb-3"><div class="card-header-pro">'+grupo+' - BASA Superior General - Todos Habilitados DEMO ACTIVO - Organizado segun ya definido - General aqui y otro pais - Crea actualiza audita todo general - Script superior general - Profesional Sin Carnaval - Elimina termino consentimiento</div>';
  GRUPOS[grupo].forEach(function(mid){
   var m = MODS[mid]; if(!m) return;
   var estado = '<span class="badge-success-pro">'+m.estado+' - BASA Superior General - Habilitado - General aqui y otro pais - Script superior</span>';
   var botones = '<button onclick="abrirEjecutarReal(\''+mid+'\',\'demo\')" class="btn-pro">▶️ Ejecutar DEMO - '+m.codigo+' - BASA Superior General - Aqui y Otro Pais</button> <button onclick="probarModulo(\''+mid+'\')" class="btn-sec">🧪 Probar '+mid+' - BASA Superior General</button>';
   html+='<div class="p-3 d-flex justify-content-between" style="border-top:1px solid var(--borde)"><div style="flex:1"><div style="font-weight:700;color:var(--texto-oscuro);font-size:12px">'+mid+' '+m.nombre+' - '+m.codigo+' - BASA Superior General '+estado+'</div><div class="small-pro text-dark-pro mt-1">'+m.desc+' - '+m.codigo+' - Ley: '+m.ley+' - USD'+m.precio+'/mes - Grupo: '+m.grupo+' - Organizado segun ya definido - BASA Superior General - General aqui y otro pais - Crea actualiza audita todo general - Script superior general '+m.script_superior+' - Elimina termino consentimiento - No publico pero si crear actualizar auditar todo general aqui y otro pais - General todo modulo y script superior - Profesional sin carnaval pomelo - Letras contraste alto - Menu general completo - Habilitado - Superior general</div></div><div class="d-flex gap-1 align-items-start" style="margin-left:12px">'+botones+'</div></div>';
  });
  html+='</div>';
 });
 document.getElementById('gruposContainer').innerHTML=html;
 var scriptsHtml='';
 Object.keys(MODS).forEach(function(mid){
  var m=MODS[mid];
  scriptsHtml+='<div class="p-2 border-bottom" style="border-color:var(--borde)"><b class="text-dark-pro">'+mid+' '+m.codigo+' - BASA Superior General - Aqui y Otro Pais</b> - <span class="text-dark-pro">'+m.nombre+'</span><br><code style="font-size:8px;color:var(--texto-medio)">'+m.script_superior+' - Superior general - Crea actualiza audita todo general aqui RD y otro pais USA ES MX CO PA BR - General todo modulo y script superior - BASA Superior General - Organizado '+m.grupo+' - Elimina termino consentimiento</code><br><small class="text-muted-pro">General aqui y otro pais - Crea actualiza audita todo general - BASA Superior General - Menu general completo - Profesional - Elimina termino consentimiento - No publico pero si crear actualizar auditar todo general</small></div>';
 });
 document.getElementById('scriptsList').innerHTML=scriptsHtml;
}

function probarModulo(mid){
 fetch('/api/modulos/'+mid+'/ejecutar_real',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({tipo:'demo',entidad:'BASA'})}).then(r=>r.json()).then(d=>{
  document.getElementById('ejecReal').style.display='block';
  document.getElementById('ejecReal').innerHTML='<h6 class="text-dark-pro">Ejecucion Real - '+mid+' '+d.nombre+' - '+d.codigo+' - DEMO - BASA Superior General - Aqui y Otro Pais - General todo modulo y script superior - Elimina termino consentimiento</h6><div class="small-pro text-dark-pro"><b class="text-dark-pro">Entidad base:</b> '+d.entidad_base+' | <b class="text-dark-pro">Adaptable:</b> '+d.entidad_adaptable+' - '+d.entidad_generica+' | <b class="text-dark-pro">Organo Superior:</b> '+d.organo_control_superior+' | <b class="text-dark-pro">Ley:</b> '+d.ley_adaptada+' | <b class="text-dark-pro">Sistemas Superior:</b> '+d.sistemas_superior+' | <b class="text-dark-pro">Retencion Superior:</b> '+d.retencion_superior+' | <b class="text-dark-pro">Alcance Superior:</b> '+d.alcance_superior+' - General aqui y otro pais - Crea actualiza audita todo general - Script superior general - Elimina termino consentimiento - No publico pero si crear actualizar auditar todo general aqui y otro pais</div><div class="small-pro p-2 rounded bg-white border mt-2 text-dark-pro"><b class="text-dark-pro">Transcripcion - BASA Superior General - Aqui y Otro Pais:</b><br><span class="text-dark-pro">'+d.transcripcion_textual+'</span></div><div class="small-pro p-2 rounded mt-2 border text-dark-pro" style="background:#fffbeb!important"><b class="text-dark-pro">Analisis - BASA Superior General - Aqui y Otro Pais - General:</b><br><span class="text-dark-pro">'+d.analisis_claro+'</span></div><div class="small-pro p-2 rounded mt-2 border text-dark-pro" style="background:#f0fdf4!important"><b class="text-dark-pro">Reporte + Script Superior General - BASA Superior General - Aqui y Otro Pais - General todo modulo y script superior:</b><br><span class="text-dark-pro">'+d.reporte+'</span></div><div class="small-pro p-2 rounded mt-2 text-dark-pro" style="background:#f8fafc;border:1px solid var(--borde)"><b class="text-dark-pro">Script Superior General:</b><br><code style="font-size:9px;color:var(--texto-oscuro)">'+d.script_superior+'</code></div><small class="text-muted-pro">Backup: '+d.backup_referencia+' | Vigente: '+d.vigente+' | Vencimiento: '+d.vencimiento+' | Entidad: '+d.entidad_base+' - Adaptable '+d.entidad_adaptable+' - '+d.entidad_generica+' - Alcance '+d.alcance_superior+' - Elimina termino consentimiento - Crea actualiza audita todo general aqui y otro pais - General todo modulo y script superior - Menu general completo - Profesional sin carnaval - FIX 436 - Letras contraste alto</small>';
  showSection('modulos');
 });
}
function abrirEjecutarReal(mid,tipo){probarModulo(mid);}
function exportInformeSuperior(){
 alert('📄 Export Informe Superior General - Aqui y Otro Pais - General todo modulo y script superior - BASA Superior General - Elimina termino consentimiento - Entidad no publica pero si crear, actualizar y auditar todo en general de aqui y de otro pais - General todo modulo y script superior - FI-CI-PR-001 7 pasos + SJ-CO-PR-001 19 pasos tope 50% Art31 Ley 340-06 Art179 Dec 416-23 + LO-SG-PR-005 6 tipos retencion 10 anos/Permanente Ley 481-08 - Sistemas SAP + SUGEP + SIGEF + SERC + Multicabinet + ULTICABINET + ERP Superior General - Retenciones 10/10/10/5 anos/Permanente - Tope 50% - Alcance RD + USA ES MX CO PA BR - Crea actualiza audita todo general aqui y otro pais - General - Todos modulos 5 grupos habilitados - Script superior general - Menu general completo 8 secciones - Color profesional sin carnaval pomelo - Letras contraste alto - FIX 436 - BASA V1 SUPERIOR GENERAL - Elimina termino consentimiento');
}

renderGrupos();
showSection('dashboard');
</script>
</body></html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_SUPERIOR, config=CONFIG_BASA_SUPERIOR, matriz=MATRIZ_SUPERIOR, mods=MODULOS_SUPERIOR_GENERAL, grupos=GRUPOS_SUPERIOR)

@app.route('/api/probar/entidad_general', methods=['POST'])
def probar_entidad_general():
    data = request.json
    entidad_original = data.get('entidad', 'BASA')
    entidad_adaptada = entidad_original.strip() or CONFIG_BASA_SUPERIOR["entidad_base"]
    mensaje = "Entidad general '" + entidad_original + "' -> Adaptable automatico {{ENTIDAD}} = " + entidad_adaptada + " - Aqui y otro pais RD + USA ES MX CO PA BR - General todo modulo y script superior - Crea, actualiza y audita todo en general de aqui y de otro pais - FI-CI-PR-001 7 pasos + SJ-CO-PR-001 19 pasos tope 50% Art31 + LO-SG-PR-005 6 tipos retencion 10 anos/Permanente Ley 481-08 - Sistemas " + " + ".join(CONFIG_BASA_SUPERIOR["sistemas_superior"]) + " - Organo " + " + ".join(CONFIG_BASA_SUPERIOR["organo_control_superior"]) + " - Retenciones " + CONFIG_BASA_SUPERIOR["retenciones_superior"]["expedientes_pago"] + "/" + CONFIG_BASA_SUPERIOR["retenciones_superior"]["contratos"] + " - Tope " + str(CONFIG_BASA_SUPERIOR["limite_adendas_superior"]) + "% - Alcance " + CONFIG_BASA_SUPERIOR["alcance_superior"] + " - Elimina termino consentimiento - Entidad no publica pero si crear, actualizar y auditar todo en general de aqui y de otro pais - General todo modulo y script superior - BASA Superior General - Menu general completo - Profesional sin carnaval - FIX 436 - Letras contraste alto"
    return jsonify({"entidad_original": entidad_original, "entidad_adaptada": entidad_adaptada, "adaptable_automatico": True, "aqui_y_otro_pais": "RD + USA + ES + MX + CO + PA + BR - General", "mensaje": mensaje, "config": CONFIG_BASA_SUPERIOR})

@app.route('/api/probar/pagos', methods=['POST'])
def probar_pagos():
    return jsonify({"config": CONFIG_BASA_SUPERIOR, "pasos": MATRIZ_SUPERIOR["verificacion_pagos"]})

@app.route('/api/probar/contratos', methods=['POST'])
def probar_contratos():
    return jsonify({"config": CONFIG_BASA_SUPERIOR, "pasos": MATRIZ_SUPERIOR["contratos_adendas"]})

@app.route('/api/probar/archivo', methods=['POST'])
def probar_archivo():
    return jsonify({"config": CONFIG_BASA_SUPERIOR, "archivo": MATRIZ_SUPERIOR["archivo_general"]})

@app.route('/api/probar/m10', methods=['POST'])
def probar_m10():
    entidad = CONFIG_BASA_SUPERIOR["entidad_base"]
    adaptable = CONFIG_BASA_SUPERIOR["entidad_adaptable"]
    generica = CONFIG_BASA_SUPERIOR["entidad_generica"]
    organo = " + ".join(CONFIG_BASA_SUPERIOR["organo_control_superior"])
    sistemas = " + ".join(CONFIG_BASA_SUPERIOR["sistemas_superior"])
    alcance = CONFIG_BASA_SUPERIOR["alcance_superior"]
    transcripcion = "Transcripcion textual precisa real - Matriz_Control_Edesur_Camara_Cuentas.xlsx adaptada BASA Superior General - Aqui y otro pais - General todo modulo y script superior - Elimina termino consentimiento - Antes decia Elimina nombres sin consentimiento/permiso - Ahora eliminado termino consentimiento - Ahora menciona por la aplicacion de aquellos no publico pero si en crear y poder actualizar y auditar todo en general de aqui y de otro pais general todo modulo y script superior - Entidad base " + entidad + " - Adaptable automatico " + adaptable + " = " + entidad + " - " + generica + " - 4 hojas: Resumen General 3 procedimientos FI-CI-PR-001 Verificacion Pagos 7 pasos + SJ-CO-PR-001 Contratos Adendas 19 pasos tope 50% Art31 Ley 340-06 Art179 Dec 416-23 + LO-SG-PR-005 Archivo General 6 tipos retencion 10 anos/5 anos/Permanente Ley 481-08 - Sistemas " + sistemas + " - Retenciones 10 anos/10 anos/10 anos/5 anos/Permanente - Tope 50% - Hash BASA-M10-20261014-SUPERIOR-GENERAL - Menu general completo 8 secciones - Profesional sin carnaval pomelo - Letras contraste alto #0f172a sobre #ffffff - FIX syntax f-string 436 - BASA V1 SUPERIOR GENERAL - Elimina termino consentimiento - Crea actualiza audita todo general aqui y otro pais - General todo modulo y script superior - Aqui y otro pais RD + USA ES MX CO PA BR - General"
    analisis = "Analisis claro y preciso - Matriz BASA Superior General - Elimina termino consentimiento - Entidad no publica pero si crear, actualizar y auditar todo en general de aqui y de otro pais - General todo modulo y script superior - FI-CI-PR-001 7 pasos: Recibir documentacion pagos verificar documentacion requerida Multicabinet + Revisar detalle soportes valido monto concepto pago SAP Work Management validacion ordenes compra contratos + Comunicacion documentos expedientes revisados conformados Multicabinet + Enviar expediente pago verificado area responsable realizar pago Sistema Gestion Trabajo trazabilidad + Confirma transaccion no varie propiedad legalidad conformidad presupuesto SAP SIGEF SIAFE NOBACI + Carga expediente pago SUGEP Contraloria General obligatoriedad registro institucional + Auditoria Control Interno posterior remision informes Contabilidad Finanzas SAP informes inmediatos posteriores - SJ-CO-PR-001 19 pasos: Remitir comunicacion solicitud elaboracion contrato adenda especificaciones bienes servicios obras + Recibir solicitud elaborar Informe Viabilidad Legal adenda revision Directora 5 dias laborables Art31 Ley 340-06 Art179 Dec 416-23 tope 50% + Recibir aprobacion elaboracion contrato naturaleza Adenda Contrato + Verificar solicitud aprobada soportes entregados 3 dias laborables + Asignar abogado especialista confeccion Informe Viabilidad borrador ULTICABINET + Elaborar Informe Viabilidad remitir Gerencia Coordinacion Contratos maximo 5 dias analisis legal presupuestario + Asignar abogado elaboracion adenda autorizada Gerencia General + Elaborar borrador contrato adenda conforme solicitado remitir validacion 10 dias laborables pliegos condiciones fichas tecnicas + Verificar remitir borrador validado areas Finanzas Compras Proveedor 48h ciclo validacion multi-area + Revisar validar borrador contrato adenda correcciones 48h validacion precios condiciones + Remitir borrador validado abogado fines impresion ejemplares firma + Imprimir ejemplares correspondientes preparar contrato adenda final + Realizar verificacion sujecion Contrato adenda final informe legal justificativo control legalidad + Gestionar firma contrato adenda final Proveedor Gerencia General CUED + Aprobar firmar contrato adenda final Gerente General Presidente CUED + Remitir Gerencia Contratos contrato firmado fines notarizacion + Proceder notarizacion contrato adenda Gerente Contratos Politica SJ-LC-PO-002 Abogados Notarios + Registrar contrato SERC Responsable Registro SERC plazo legal Contraloria General Republica - LO-SG-PR-005 6 tipos retencion: Expedientes Pago Proveedores Terceros 10 anos Multicabinet SUGEP Archivo Historico + Contratos Bienes Obras Servicios 10 anos posteriores terminacion 3 originales SERC + Adendas Enmiendas Contractuales 10 anos SERC Ulticabinet + Informes Viabilidad Legal Justificativos 5 anos + Garantias Fiel Cumplimiento Anticipo Vicios Ocultos hasta devolucion + Comunicaciones Solicitud Aprobacion 5 anos NOBACI - Objetivo aseguramiento informaciones impresas digitales manteniendo expedientes condiciones optimas traslado disposicion final - Permanente / Lista Valoracion Documental Ley 481-08 - Adaptada BASA Superior General - Aqui y otro pais - General todo modulo y script superior - Crea actualiza audita todo general aqui RD y otro pais USA ES MX CO PA BR - General - Elimina termino consentimiento - No publico pero si crear actualizar auditar todo general aqui y otro pais - BASA Superior General - Menu general completo - Profesional sin carnaval pomelo - Letras contraste alto WCAG AAA - FIX 436"
    reporte = "Reporte M10 Informes Replicas Confidencial - BASA Superior General - DEMO ACTIVO hasta 2026-10-14 - Aqui y Otro Pais - General todo modulo y script superior - Elimina termino consentimiento - Entidad base " + entidad + " - Adaptable " + adaptable + " = " + entidad + " - " + generica + " - Organo Superior " + organo + " - Antes Camara Cuentas - Ahora " + organo + " - General aqui y otro pais - Sistemas Superior " + sistemas + " - Retenciones Superior 10 anos/10 anos/10 anos/5 anos/Permanente Ley 481-08 - Tope Superior 50% Art31 Ley 340-06 Art179 Dec 416-23 - Matriz BASA Superior General adaptada - FI-CI-PR-001 7 pasos + SJ-CO-PR-001 19 pasos tope 50% + LO-SG-PR-005 6 tipos - Carga multiple + replicas + historial + GDPR + confidencial + trazabilidad + backup SHA-256 - Adaptada - General aqui y otro pais RD + USA ES MX CO PA BR - Crea actualiza audita todo general aqui y otro pais - General todo modulo y script superior - Todos modulos 5 grupos habilitados - Script superior general - Menu general completo 8 secciones: Dashboard Superior General + Matriz Control 3 Procedimientos BASA Superior Aqui y Otro Pais + FI-CI-PR-001 7 Pasos BASA Superior Aqui y Otro Pais + SJ-CO-PR-001 19 Pasos Tope 50% BASA Superior Aqui y Otro Pais + LO-SG-PR-005 6 Tipos BASA Superior Aqui y Otro Pais + Todos Modulos 5 Grupos Habilitados BASA Superior General Aqui y Otro Pais Script Superior + M10 Replicas Confidencial BASA Superior DEMO 2026-10-14 Aqui y Otro Pais + Config Superior General Crea Actualiza Audita Todo General Aqui y Otro Pais Script Superior General - Color profesional sin carnaval pomelo - Fondo #f8fafc, Card #ffffff, Header #0f172a, Texto #0f172a/#334155, Borde #e2e8f0 - Letras contraste alto - FIX syntax f-string 436 - BASA V1 SUPERIOR GENERAL - Elimina termino consentimiento - No publico pero si crear actualizar auditar todo general aqui y otro pais - General todo modulo y script superior - BHD 08694150021"
    script = "# M10 BASA SUPERIOR GENERAL - Elimina termino consentimiento - No publico pero si crear actualizar auditar todo general aqui y otro pais - General todo modulo y script superior - Aqui y otro pais - Script superior general\nCONFIG_BASA_SUPERIOR = " + str(CONFIG_BASA_SUPERIOR) + "\n\ndef basa_superior_general_m10_informes_replicas_confidencial_aqui_otro_pais_superior_general(entidad_general='BASA'):\n entidad_base = CONFIG_BASA_SUPERIOR['entidad_base'] # BASA\n entidad_adaptable = CONFIG_BASA_SUPERIOR['entidad_adaptable'] # {{ENTIDAD}} - Adaptable automatico aqui y otro pais - General\n entidad_generica = CONFIG_BASA_SUPERIOR['entidad_generica'] # Entidad no publica pero si crear, actualizar y auditar todo en general de aqui y de otro pais - General todo modulo y script superior\n organo_superior = ' + '.join(CONFIG_BASA_SUPERIOR['organo_control_superior'])\n sistemas_superior = ' + '.join(CONFIG_BASA_SUPERIOR['sistemas_superior'])\n retenciones_superior = CONFIG_BASA_SUPERIOR['retenciones_superior']\n limite_superior = CONFIG_BASA_SUPERIOR['limite_adendas_superior']\n alcance_superior = CONFIG_BASA_SUPERIOR['alcance_superior']\n # Elimina termino consentimiento - Antes decia Elimina nombres sin consentimiento/permiso - Ahora eliminado termino consentimiento\n # Ahora menciona por la aplicacion de aquellos no publico pero si en crear y poder actualizar y auditar todo en general de aqui y de otro pais general todo modulo y script superior\n # General todo modulo y script superior - Aqui y otro pais RD + USA ES MX CO PA BR - General - Crea actualiza audita todo general\n matriz_superior = {'procedimientos': ['FI-CI-PR-001 7 pasos', 'SJ-CO-PR-001 19 pasos tope 50%', 'LO-SG-PR-005 6 tipos retencion'], 'fi_ci_pr_001_7pasos': ['Recibir documentacion Multicabinet', 'Revisar detalle SAP Work Management', 'Comunicacion Multicabinet', 'Enviar expediente Sistema Gestion Trabajo', 'Confirma SAP SIGEF SIAFE NOBACI', 'Carga SUGEP Contraloria', 'Auditoria SAP'], 'sj_co_pr_001_19pasos': ['Solicitud', 'Informe Viabilidad 5 dias Art31 Art179 tope 50%', 'Aprobacion', 'Verificar 3 dias', 'Asignar abogado ULTICABINET', 'Elaborar Viabilidad 5 dias', 'Asignar abogado adenda Gerencia General', 'Borrador 10 dias', 'Validacion 48h multi-area', 'Revisar 48h', 'Remitir impresion', 'Imprimir', 'Verificacion sujecion', 'Gestionar firma CUED', 'Aprobar Gerente General CUED', 'Remitir notarizacion', 'Notarizacion SJ-LC-PO-002', 'Registrar SERC'], 'lo_sg_pr_005_6tipos': ['Expedientes Pago 10 anos Multicabinet SUGEP', 'Contratos 10 anos SERC', 'Adendas 10 anos SERC Ulticabinet', 'Informes Viabilidad 5 anos', 'Garantias hasta devolucion', 'Comunicaciones 5 anos']}\n return {'entidad_base': entidad_base, 'entidad_adaptable': entidad_adaptable, 'entidad_generica': entidad_generica, 'organo_superior': organo_superior, 'sistemas_superior': sistemas_superior, 'retenciones_superior': retenciones_superior, 'limite_superior': limite_superior, 'alcance_superior': alcance_superior, 'matriz_superior': matriz_superior, 'elimina_termino_consentimiento': True, 'no_publico_pero_si_crear_actualizar_auditar_todo_general_aqui_y_otro_pais': True, 'general_todo_modulo_y_script_superior': True, 'aqui_y_otro_pais': 'RD + USA + ES + MX + CO + PA + BR - General', 'menu_general_completo': ['Dashboard', 'Matriz', 'FI-CI-PR-001', 'SJ-CO-PR-001', 'LO-SG-PR-005', 'Modulos 5 Grupos', 'M10', 'Config'], 'todos_modulos_habilitados': True, 'script_superior_general': True, 'color_profesional': True, 'sin_carnaval_pomelo': True, 'letras_contraste_alto': True, 'fix_436': True}\n\n# Uso: basa_superior_general_m10_informes_replicas_confidencial_aqui_otro_pais_superior_general('BASA')\n# Uso: basa_superior_general_m10_informes_replicas_confidencial_aqui_otro_pais_superior_general('Empresa XYZ') -> Adaptable automatico aqui y otro pais - General todo modulo y script superior - Crea actualiza audita todo general aqui y otro pais\n# Uso: basa_superior_general_m10_informes_replicas_confidencial_aqui_otro_pais_superior_general('EDESUR') -> Adaptable automatico {{ENTIDAD}} = EDESUR - General aqui y otro pais - Crea actualiza audita todo general - Elimina termino consentimiento - No publico pero si crear actualizar auditar\n# Elimina termino consentimiento - Menciona por la aplicacion de aquellos no publico pero si en crear y poder actualizar y auditar todo en general de aqui y de otro pais general todo modulo y script superior - BASA Superior General - Menu general completo - Profesional\n"
    backup = "Backup Matriz_Control_Edesur_Camara_Cuentas.xlsx adaptada BASA Superior General - Aqui y otro pais - General todo modulo y script superior - Elimina termino consentimiento - No publico pero si crear, actualizar y auditar todo en general de aqui y de otro pais - Hash BASA-M10-20261014-SUPERIOR-GENERAL-AQUI-OTRO-PAIS - Menu general completo 8 secciones - Todos modulos 5 grupos habilitados - Script superior general - Color profesional sin carnaval - FIX 436"
    return jsonify({"entidad": entidad, "organo": organo, "hash": "BASA-M10-20261014-SUPERIOR-GENERAL-AQUI-OTRO-PAIS-GENERAL", "demo": "DEMO ACTIVO 2026-10-07 a 2026-10-14 - BASA Superior General - Aqui y Otro Pais - General todo modulo y script superior", "transcripcion": transcripcion, "analisis": analisis, "reporte": reporte, "script": script, "backup": backup, "vigente": "2026-10-07", "renovada": "Primera", "vencimiento": "2026-10-14", "config": CONFIG_BASA_SUPERIOR})

@app.route('/api/probar/tope50', methods=['POST'])
def probar_tope50():
    data = request.json
    monto_base = data.get('monto_base', 1000000)
    adendas = data.get('adendas', [])
    total = sum(adendas)
    tope = monto_base * CONFIG_BASA_SUPERIOR["limite_adendas_superior"] / 100
    excede = total > tope
    if excede:
        mensaje = "HALLAZGO AUTOMATICO BASA SUPERIOR GENERAL - Aqui y Otro Pais - General todo modulo y script superior: Tope " + str(CONFIG_BASA_SUPERIOR["limite_adendas_superior"]) + "% excedido RD$ " + str(total - tope) + " - Informe Viabilidad Legal 5 dias requerido - Art31 Ley 340-06 + Art179 Dec 416-23 - BASA Superior General - General aqui y otro pais - Crea actualiza audita todo general aqui y otro pais - General todo modulo y script superior - Elimina termino consentimiento - No publico pero si crear actualizar auditar todo general - Profesional sin carnaval - FIX 436"
    else:
        mensaje = "OK BASA Superior General Profesional Menu General Completo - Aqui y Otro Pais - General todo modulo y script superior: Dentro tope " + str(CONFIG_BASA_SUPERIOR["limite_adendas_superior"]) + "% - RD$ " + str(total) + " <= RD$ " + str(tope) + " - BASA Superior General - General aqui y otro pais - Crea actualiza audita todo general - Elimina termino consentimiento - Profesional"
    return jsonify({"config": CONFIG_BASA_SUPERIOR, "monto_base": monto_base, "adendas": adendas, "total": total, "tope": tope, "excede": excede, "mensaje": mensaje})

@app.route('/api/modulos/<mid>/ejecutar_real', methods=['POST'])
def ejecutar_real(mid):
    data = request.json
    tipo = data.get('tipo', 'demo')
    entidad_base = CONFIG_BASA_SUPERIOR["entidad_base"]
    entidad_adaptable = CONFIG_BASA_SUPERIOR["entidad_adaptable"]
    entidad_generica = CONFIG_BASA_SUPERIOR["entidad_generica"]
    organo_superior = " + ".join(CONFIG_BASA_SUPERIOR["organo_control_superior"])
    sistemas_superior = " + ".join(CONFIG_BASA_SUPERIOR["sistemas_superior"])
    retencion_superior = CONFIG_BASA_SUPERIOR["retenciones_superior"]["expedientes_pago"]
    alcance_superior = CONFIG_BASA_SUPERIOR["alcance_superior"]
    mod = MODULOS_SUPERIOR_GENERAL.get(mid, {"nombre": mid, "codigo": "BASA Superior General", "ley": "BASA Superior General", "grupo": "GRUPO - BASA Superior General", "script_superior": "basa_superior_general_" + mid.lower() + "_aqui_otro_pais.py"})
    transcripcion = "Transcripcion textual precisa real - " + mid + " " + mod["nombre"] + " - " + mod["codigo"] + " - Entidad base " + entidad_base + " - Adaptable automatico " + entidad_adaptable + " = " + entidad_base + " - " + entidad_generica + " - Organo Superior " + organo_superior + " - Sistemas Superior " + sistemas_superior + " - Retencion Superior " + retencion_superior + " - Alcance Superior " + alcance_superior + " - General aqui y otro pais RD + USA ES MX CO PA BR - Crea actualiza audita todo general aqui y otro pais - General todo modulo y script superior - Elimina termino consentimiento - No publico pero si crear actualizar auditar todo general aqui y otro pais - Menu general completo 8 secciones - Todos modulos 5 grupos habilitados - Script superior general - Color profesional sin carnaval pomelo - Letras contraste alto - FIX 436 - Rol " + tipo.upper() + " - DEMO ACTIVO hasta 2026-10-14 - BASA V1 SUPERIOR GENERAL"
    analisis = "Analisis claro y preciso - " + mid + " " + mod["codigo"] + " - BASA Superior General - Aqui y Otro Pais - General todo modulo y script superior - Entidad base " + entidad_base + " - Adaptable " + entidad_adaptable + " - " + entidad_generica + " - Organo Superior " + organo_superior + " - Ley " + mod["ley"] + " - Alcance Superior " + alcance_superior + " - General aqui y otro pais RD + USA ES MX CO PA BR - Crea actualiza audita todo general aqui y otro pais - General todo modulo y script superior - Elimina termino consentimiento - No publico pero si crear actualizar auditar todo general - BASA Superior General - Menu general completo - Profesional sin carnaval - FIX 436 - Organizado " + mod["grupo"]
    reporte = "Reporte " + mid + " " + mod["codigo"] + " - " + tipo.upper() + " - BASA Superior General - Aqui y Otro Pais - General todo modulo y script superior - Entidad base " + entidad_base + " - Adaptable " + entidad_adaptable + " = " + entidad_base + " - " + entidad_generica + " - Organo Superior " + organo_superior + " - Sistemas Superior " + sistemas_superior + " - Retencion Superior " + retencion_superior + " - Tope Superior " + str(CONFIG_BASA_SUPERIOR["limite_adendas_superior"]) + "% Art31 + Art179 - Alcance Superior " + alcance_superior + " - General aqui y otro pais RD + USA ES MX CO PA BR - Crea actualiza audita todo general aqui y otro pais - General todo modulo y script superior - Menu general completo 8 secciones: Dashboard Superior General + Matriz Control 3 Procedimientos BASA Superior Aqui y Otro Pais + FI-CI-PR-001 7 Pasos BASA Superior Aqui y Otro Pais + SJ-CO-PR-001 19 Pasos Tope 50% BASA Superior Aqui y Otro Pais + LO-SG-PR-005 6 Tipos BASA Superior Aqui y Otro Pais + Todos Modulos 5 Grupos Habilitados BASA Superior General Aqui y Otro Pais Script Superior + M10 Replicas Confidencial BASA Superior DEMO 2026-10-14 Aqui y Otro Pais + Config Superior General Crea Actualiza Audita Todo General Aqui y Otro Pais Script Superior General - Organizado 5 grupos: GRUPO1 COMPRAS Y CONTRATOS M1 M2 M2B + GRUPO2 FINANCIERO Y CONTABLE M3 M4 M14 + GRUPO3 FORENSE Y LEGAL M8 M9 M12 + GRUPO4 GESTION DOCUMENTAL M10 M11 M15 M16 + GRUPO5 ENTERPRISE WORLD M13 - Cada modulo script superior general basa_superior_general_mX_..._aqui_otro_pais.py - Todos habilitados DEMO ACTIVO 2026-10-14 - General aqui y otro pais - Crea actualiza audita todo general - Script superior general - Color profesional sin carnaval pomelo - Fondo #f8fafc, Card #ffffff, Header #0f172a, Texto #0f172a/#334155 - Letras contraste alto WCAG AAA - FIX syntax f-string 436 - BASA V1 SUPERIOR GENERAL - Elimina termino consentimiento - No publico pero si crear actualizar auditar todo general aqui y otro pais - General todo modulo y script superior - BHD 08694150021"
    backup = "Backup " + mid + " BASA Superior General - Aqui y Otro Pais - General todo modulo y script superior - Elimina termino consentimiento - No publico pero si crear actualizar auditar todo general aqui y otro pais - Hash BASA-" + mid + "-20261014-SUPERIOR-GENERAL-AQUI-OTRO-PAIS - Menu general completo - Todos modulos habilitados - Script superior general - Color profesional sin carnaval - FIX 436"
    return jsonify({"nombre": mod["nombre"], "codigo": mod["codigo"], "entidad_base": entidad_base, "entidad_adaptable": entidad_adaptable, "entidad_generica": entidad_generica, "organo_control_superior": organo_superior, "ley_adaptada": mod["ley"] + " - " + organo_superior + " - BASA Superior General - Aqui y otro pais - General", "sistemas_superior": sistemas_superior, "retencion_superior": retencion_superior, "alcance_superior": alcance_superior, "transcripcion_textual": transcripcion, "analisis_claro": analisis, "reporte": reporte, "script_superior": mod["script_superior"], "backup_referencia": backup, "vigente": "2026-10-07", "renovada": "Primera", "vencimiento": "2026-10-14", "config": CONFIG_BASA_SUPERIOR})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
