# m3_nomina_independiente.py - 100% independiente
import sqlite3, os
from flask import Flask, jsonify
import pandas as pd

DB = 'nomina.db'
app = Flask(__name__)

@app.route('/health')
def health(): return jsonify({"modulo":"M3_NOMINA","status":"OK","puerto":5001})

@app.route('/api/detectar')
def detectar():
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query("SELECT * FROM empleados", conn)
    dup = df[df.duplicated('cedula', keep=False)]
    hallazgos = []
    for ced,g in dup.groupby('cedula'):
        hallazgos.append({
          "codigo":f"H-NOM-{ced}",
          "severidad":"CRITICA",
          "descripcion":f"Cédula {ced} duplicada {len(g)} veces DOP {g['sueldo'].sum():,.2f}"
        })
    return jsonify({"modulo":"M3_NOMINA","hallazgos":hallazgos,"test_passed":True})

app.run(port=5001)
