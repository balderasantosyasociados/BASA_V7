# Cada módulo en su propio puerto - No se interrumpen
python m3_nomina_independiente.py # 5001 - Administrativo
python m1_compras_independiente.py # 5002 - Administrativo
python m5_prestamos_independiente.py # 5003 - Financiero
python m8_forense_independiente.py # 5004 - Gestión

# Gateway consolida como Big4
python gateway_enterprise.py # 5000 - Orquestador
# http://localhost:5000/api/orquestar/auditoria-completa
