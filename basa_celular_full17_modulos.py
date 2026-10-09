# BASA CELULAR FULL - 17 MODULOS - AUTO-INSTALABLE
# python basa_celular_full.py --celula M3 -> Solo M3 (RD$15k) vive solo
# python basa_celular_full.py --full -> 17 células + gateway tejido FULL (RD$185k)
import sys, subprocess, json, sqlite3, hashlib, argparse, time, threading
from datetime import datetime

# Auto-instala si falta algo
try:
    import flask, pandas, requests
except:
    subprocess.run([sys.executable, "-m", "pip", "install", "flask", "pandas", "requests"])
    import flask, pandas, requests

from flask import Flask, jsonify, render_template_string
import pandas as pd

CATALOGO = {
    "M1": {"nombre":"Portal Compras vs Institucional","puerto":5001,"nobaci":"ADC-3-007.28","nicsps":"NICSP 19","riesgo":"Administrativo","precio":15000,"script":"SUMMARIZE proveedor Fraccionamiento Art 16 Ley 340-06"},
    "M2": {"nombre":"Tope 50% Adendas","puerto":5002,"nobaci":"ADC-3-007.30","nicsps":"NICSP 19","riesgo":"Contable","precio":10000,"script":"COMPUTE adendas/base >50% Art 31"},
    "M3": {"nombre":"Nomina Fantasma BHD","puerto":5003,"nobaci":"AMB-3-002.15","nicsps":"NICSP 39","riesgo":"Financiero","precio":15000,"script":"DUPLICATES cedula + cuenta BHD"},
    "M4": {"nombre":"Libramientos SUGEP/SIGEF","puerto":5004,"nobaci":"INF-3-009.10","nicsps":"NICSP 1,2","riesgo":"Financiero","precio":15000,"script":"JOIN SUGEP vs SIGEF"},
    "M5": {"nombre":"Cartera Prestamos NIIF 9","puerto":5005,"nobaci":"VAL-3-004.20","nicsps":"NIIF 9","riesgo":"Financiero","precio":20000,"script":"CLASSIFY mora >90"},
    "M6": {"nombre":"Operaciones Diarias","puerto":5006,"nobaci":"ADC-3-007.25","nicsps":"NICSP 1","riesgo":"Contable","precio":10000,"script":"GAP secuencia + Huerfanas"},
    "M7": {"nombre":"Activos Fijos NICSP 17","puerto":5007,"nobaci":"ADC-3-007.40","nicsps":"NICSP 17","riesgo":"Contable","precio":15000,"script":"JOIN fisico vs contable"},
    "M8": {"nombre":"Forense Benford","puerto":5008,"nobaci":"MON-3-011.05","nicsps":"NIA 240","riesgo":"Gestion","precio":20000,"script":"Benford desviacion >10%"},
    "M9": {"nombre":"Conciliacion Bancaria","puerto":5009,"nobaci":"ADC-3-007.35","nicsps":"NICSP 2","riesgo":"Financiero","precio":12000,"script":"JOIN libro vs extracto"},
    "M10": {"nombre":"Ingresos sin Contraprestacion NICSP 23","puerto":5010,"nobaci":"VAL-3-004.15","nicsps":"NICSP 23","riesgo":"Financiero","precio":15000,"script":"FUZZY contribuyente"},
    "M11": {"nombre":"Proveedores Fantasmas","puerto":5011,"nobaci":"AMB-3-002.10","nicsps":"NIA 550","riesgo":"Administrativo","precio":15000,"script":"JOIN proveedor.cedula=empleado.cedula"},
    "M12": {"nombre":"Viaticos y Tarjetas","puerto":5012,"nobaci":"ADC-3-007.50","nicsps":"NICSP 39","riesgo":"Gestion","precio":8000,"script":"STRATIFY viatico > tope"},
    "M13": {"nombre":"Almacen Inventarios NICSP 12","puerto":5013,"nobaci":"ADC-3-007.42","nicsps":"NICSP 12","riesgo":"Contable","precio":10000,"script":"AGE >365 obsoleto"},
    "M14": {"nombre":"Control FI-CI-PR-001","puerto":5014,"nobaci":"INF-3-009.15","nicsps":"Ley 10-07","riesgo":"Administrativo","precio":8000,"script":"Checklist 7 soportes"},
    "M15": {"nombre":"Segregacion Accesos","puerto":5015,"nobaci":"AMB-3-002.20","nicsps":"NIA 315","riesgo":"Gestion","precio":12000,"script":"SUMMARIZE crea+aprueba"},
    "M16": {"nombre":"Contratos Garantias","puerto":5016,"nobaci":"VAL-3-004.25","nicsps":"NICSP 19","riesgo":"Financiero","precio":10000,"script":"AGE garantia vencida"},
    "M17": {"nombre":"Detector Universal Orquestador","puerto":5000,"nobaci":"MON-3-011.10","nicsps":"ISSAI 400","riesgo":"Los 4","precio":35000,"script":"Orquesta M1-M16 SHA-256"},
}

def crear_app_celula(codigo):
    info = CATALOGO[codigo]
    app = Flask(f"celula_{codigo}")
    db_path = f"{codigo.lower()}.db"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    if codigo=="M3":
        cur.execute("CREATE TABLE IF NOT EXISTS empleados (id INTEGER PRIMARY KEY, nombre TEXT, cedula TEXT, sueldo REAL, cuenta TEXT, depto TEXT)")
        if cur.execute("SELECT COUNT(*) FROM empleados").fetchone()[0]==0:
            cur.executemany("INSERT INTO empleados VALUES (NULL,?,?,?,?,?)",[
                ("Manuel Alcantara","001-0982341-2",185000,"BHD-10029384","Operaciones"),
                ("Rosaura Pena","001-4433221-9",95000,"BHD-00998811","Compras"),
                ("Duplicado","001-4433221-9",35000,"BHD-00998811","Logistica")])
            conn.commit()
    elif codigo=="M1":
        cur.execute("CREATE TABLE IF NOT EXISTS procesos (id INTEGER PRIMARY KEY, codigo TEXT, proveedor TEXT, monto REAL, entidad TEXT)")
        if cur.execute("SELECT COUNT(*) FROM procesos").fetchone()[0]==0:
            cur.executemany("INSERT INTO procesos VALUES (NULL,?,?,?,?)",[
                ("EDESUR-CCC-CP-2026-0004","Postes del Caribe S.R.L.",1495000,"Edesur"),
                ("EDESUR-CCC-CP-2026-0005","Postes del Caribe S.R.L.",1492000,"Edesur"),
                ("EDESUR-CCC-CP-2026-0006","Postes del Caribe S.R.L.",1488000,"Edesur")])
            conn.commit()
    conn.close()

    @app.route('/health')
    def health(): return jsonify({"celula":codigo,"status":"VIVA","puerto":info["puerto"],"precio":info["precio"],"acumulable":True})
    @app.route('/api/detectar')
    def detectar():
        hallazgos=[]
        if codigo=="M3":
            conn=sqlite3.connect(db_path)
            df=pd.read_sql_query("SELECT * FROM empleados", conn); conn.close()
            for ced,g in df[df.duplicated('cedula',keep=False)].groupby('cedula'):
                hallazgos.append({"codigo":f"H-{codigo}-{ced}","severidad":"CRITICA","descripcion":f"Cedula {ced} {len(g)} veces DOP {g['sueldo'].sum()} NOBACI {info['nobaci']}"})
        elif codigo=="M1":
            conn=sqlite3.connect(db_path)
            df=pd.read_sql_query("SELECT * FROM procesos", conn); conn.close()
            for prov,g in df.groupby('proveedor'):
                if len(g)>=2: hallazgos.append({"codigo":f"H-{codigo}","severidad":"CRITICA","descripcion":f"{prov} {len(g)} ordenes DOP {g['monto'].sum()} Art16"})
        else:
            hallazgos.append({"codigo":f"H-{codigo}-DEMO","descripcion":f"{info['nombre']} - {info['script']} - {info['nobaci']} {info['nicsps']}"})
        return jsonify({"celula":codigo,"manifest":info,"hallazgos":hallazgos})
    @app.route('/api/programa-auditoria')
    def programa(): return jsonify({"programa":f"PA-{codigo}","modulo":info["nombre"],"nobaci":info["nobaci"],"nicsps":info["nicsps"],"procedimiento":info["script"]})
    return app

def crear_gateway():
    app=Flask("gateway")
    @app.route('/')
    def home():
        return render_template_string("""
        <body style="background:#020617;color:white;font-family:monospace;padding:20px">
        <h1>🧬 BASA CELULAR FULL 17 MODULOS - NOBACI+NICSP+NIIF+BIG4</h1>
        <button onclick="fetch('/api/orquestar/full',{method:'POST'}).then(r=>r.json()).then(d=>document.getElementById('r').innerText=JSON.stringify(d,null,2))" style="background:#2563eb;padding:10px">ORQUESTAR 17 CELULAS</button>
        <pre id="r" style="background:#0f172a;padding:20px;margin-top:20px"></pre>
        </body>""")
    @app.route('/api/orquestar/full',methods=['POST'])
    def full():
        resultados={}; total=0
        for codigo,info in CATALOGO.items():
            if codigo=="M17": continue
            try:
                import requests
                r=requests.get(f"http://localhost:{info['puerto']}/api/detectar",timeout=1)
                resultados[codigo]=r.json(); total+=len(r.json().get('hallazgos',[]))
            except: resultados[codigo]={"status":"DORMIDA","puerto":info["puerto"]}
        return jsonify({"tejido":"BASA FULL 17","total_hallazgos":total,"resultados":resultados})
    return app

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--celula',help='M3, M1, etc')
    parser.add_argument('--full',action='store_true')
    parser.add_argument('--gateway',action='store_true')
    args=parser.parse_args()
    if args.celula:
        c=args.celula.upper(); app=crear_app_celula(c)
        print(f"CELULA {c} VIVA SOLA puerto {CATALOGO[c]['puerto']} RD${CATALOGO[c]['precio']}")
        app.run(port=CATALOGO[c]['puerto'])
    elif args.full:
        for codigo in CATALOGO:
            if codigo=="M17": continue
            threading.Thread(target=lambda c=codigo: crear_app_celula(c).run(port=CATALOGO[c]['puerto'],use_reloader=False),daemon=True).start()
            time.sleep(0.3)
        print("17 CELULAS LEVANTADAS - Gateway http://localhost:5000"); crear_gateway().run(port=5000)
    elif args.gateway: crear_gateway().run(port=5000)
    else: print("Uso: --celula M3 | --full | --gateway")
