import os
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return 'BASA V7-1 LIVE OK - BHD 08694150021 - V8 Modular Listo'

@app.route('/healthz')
def health():
    return 'OK'

@app.route('/activar-modulos')
def activar():
    html = """
<html><head><meta name='viewport' content='width=device-width,initial-scale=1'>
<style>body{font-family:Arial;background:#0f172a;color:white;padding:12px}.card{background:white;color:black;padding:20px;border-radius:15px;max-width:900px;margin:auto}.btn{padding:12px;border-radius:8px;font-weight:bold;cursor:pointer;border:none;margin:5px}.verde{background:#00d084;color:white}.azul{background:#003366;color:white}.mod{border:2px solid #ddd;padding:12px;margin:8px;border-radius:10px;display:flex;justify-content:space-between}</style>
</head><body>
<h1 style='text-align:center;color:#00d084'>BASA V8 - ACTIVAR MODULOS</h1>
<div class='card'>
<div class='mod'><div><b>B4 Base - Informe Pericial</b><br>RD$7500/mes</div><div><input type='checkbox' checked disabled></div></div>
<div class='mod'><div><b>M1 - Scraper Compras 10 anos</b><br>RD$2500/mes</div><div><input type='checkbox' class='chk' value='M1' onchange='calc()'></div></div>
<div class='mod'><div><b>M2 - Fraccionamiento Ley 340</b><br>RD$3500/mes</div><div><input type='checkbox' class='chk' value='M2' onchange='calc()'></div></div>
<div class='mod'><div><b>M5 - Consanguinidad</b><br>RD$4500/mes</div><div><input type='checkbox' class='chk' value='M5' onchange='calc()'></div></div>
<div style='background:#f0f7ff;padding:12px;border-radius:10px;margin-top:10px'>
<h3>Facturacion Automatica</h3>
Empresa: <input id='emp' style='width:100%;padding:8px'><br>
RNC: <input id='rnc' style='width:100%;padding:8px'>
<div id='fact'>Total Base: RD$7500 - Primer pago prorrateado calculado al activar</div>
</div>
<div style='background:#fff3cd;padding:12px;border-radius:10px;margin:10px 0'>
<input type='checkbox' id='ok'> <b>Estoy de acuerdo con contrato virtual BASA V8 - BHD 08694150021</b><br>
<a href='/api/contrato' target='_blank'>Ver Contrato Virtual</a>
</div>
<button class='btn verde' style='width:100%' onclick='activar()'>ACEPTO CONTRATO Y ACTIVAR + DESCARGAR DEMO</button>
<div id='res' style='display:none;background:#e8f5e9;padding:12px;border-radius:10px;margin-top:10px'></div>
</div>
<script>
function calc(){
  var total=7500;
  document.querySelectorAll('.chk:checked').forEach(function(c){
    if(c.value=='M1') total+=2500;
    if(c.value=='M2') total+=3500;
    if(c.value=='M5') total+=4500;
  });
  var hoy=new Date(); var dias=30-hoy.getDate()+1;
  var primer=Math.round((total/30)*dias);
  document.getElementById('fact').innerHTML='Total Mensual: RD$'+total+'<br>Primer pago ('+dias+' dias): RD$'+primer+'<br>BHD: 08694150021';
}
function activar(){
  if(!document.getElementById('ok').checked){alert('Debe aceptar contrato');return;}
  document.getElementById('res').style.display='block';
  document.getElementById('res').innerHTML='<b>Contrato CTR-V8-ACTIVO</b><br><a href="/api/contrato" class="btn azul" style="background:#003366;color:white;padding:8px;text-decoration:none;border-radius:5px">Descargar Contrato</a> <a href="/demo" class="btn verde" style="background:#00d084;color:white;padding:8px;text-decoration:none;border-radius:5px">Descargar DEMO V8</a><br><br>Demo banner desaparecera tras pago. Actualizacion automatica por leyes activada.';
}
calc();
</script>
</body></html>
"""
    return html

@app.route('/api/contrato')
def contrato():
    from flask import send_file
    import io
    txt = "CONTRATO VIRTUAL BASA V8 ENTERPRISE\nBHD 08694150021 Pedro Baldera\nMODULOS: B4 + M1 + M2 + M5\nFACTURACION: Primer mes prorrateado, luego mensual\nACTUALIZACION AUTOMATICA POR LEYES RD\nFIRMA VALIDA AL MARCAR ESTOY DE ACUERDO"
    return send_file(io.BytesIO(txt.encode()), mimetype="application/pdf", as_attachment=True, download_name="CONTRATO_BASA_V8.pdf")

@app.route('/b4')
def b4():
    return "<body style='font-family:Arial;background:#0f172a;color:white;padding:15px'><h1>B4 V8 LIVE</h1><div style='background:white;color:black;padding:15px;border-radius:12px;max-width:800px;margin:auto'><a href='/activar-modulos' style='background:#00d084;color:white;padding:10px;border-radius:8px;text-decoration:none'>Activar Modulos</a></div></body>"

@app.route('/v8')
def v8():
    return "<body style='font-family:Arial;background:#0a192f;color:white;padding:15px'><h1 style='color:#00d084'>V8 Auditoria 10 anos</h1><div style='background:white;color:black;padding:15px;border-radius:12px;max-width:800px;margin:auto'><p>Scraper, Fraccionamiento, Mismo Dueno, Accionistas, Consanguinidad, Nomina, Financiero</p><a href='/activar-modulos' style='background:#00d084;color:white;padding:10px;border-radius:8px;text-decoration:none'>Activar M1-M8</a></div></body>"

@app.route('/demo')
def demo():
    from flask import send_file
    import io, zipfile
    m=io.BytesIO()
    with zipfile.ZipFile(m,mode="w",compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("BASA_V8_DEMO/README.txt","BASA V8 LITE - BHD 08694150021")
    m.seek(0)
    return send_file(m,mimetype="application/zip",as_attachment=True,download_name="BASA_V8_DEMO.zip")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
