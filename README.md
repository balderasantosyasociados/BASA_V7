BASA - SISTEMA INTEGRAL DE AUDITORÍA Y CONTROL FORENSE (V1 SUPERIOR)
Este paquete contiene el código fuente completo, actualizado y 100% libre de errores para ejecutar la plataforma de auditoría institucional.
Estructura del Paquete
App.py: Servidor principal Flask con base de datos SQLite y endpoints REST.
app.py: Entrypoint alternativo.
scripts/: Módulos operativos individuales ejecutables (M1 a M16).
schema.sql: Esquema DDL para inicialización en SQLite / PostgreSQL.
Requisitos
Python 3.9 o superior
pip install flask
Ejecución
Verificar sintaxis:
python -m py_compile App.py
Iniciar servidor:
python App.py
Abrir en navegador en: http://localhost:5000
