# SISTEMA BASA V7 - AUDIT INTELLIGENCE USA (v7.0 FINAL CERTIFICADO PARA RENDER.COM)
**Servicio en Render:** [https://dashboard.render.com/web/srv-db0s008u01pc73bmtl90/settings](https://dashboard.render.com/web/srv-db0s008u01pc73bmtl90/settings)  
**Repositorio GitHub:** [https://github.com/balderasantosyasociados/BASA_V7-system-](https://github.com/balderasantosyasociados/BASA_V7-system-)  
**Ruta de Prueba Gratuita:** [https://audit-intelligence-usa.com/trial](https://audit-intelligence-usa.com/trial)  
**Titular:** Pedro Baldera | **BHD León:** 08694150021 | **WhatsApp:** +1 829-771-7390

---

## ⚙️ CONFIGURACIÓN EXACTA PARA RENDER.COM (SETTINGS)

En el panel de configuración de tu servicio en Render (`srv-db0s008u01pc73bmtl90/settings`):

| Campo en Render | Valor Requerido |
| :--- | :--- |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app --bind 0.0.0.0:$PORT` |
| **Health Check Path** | `/healthz` |
| **Auto-Deploy** | `Yes` (despliega automáticamente al hacer push en GitHub) |

### Variables de Entorno en Render (Environment Variables):
- `PYTHON_VERSION` = `3.11.9`
- `SECRET` = `BHD_08694150021_Pedro_Baldera_2026_Audit_USA`
- `BHD_CUENTA` = `08694150021`
- `BHD_TITULAR` = `Pedro Baldera`
- `EMAIL_ADMIN` = `licpedrobaldera@gmail.com`
- `WHATSAPP_ADMIN` = `18297717390`

---

## 🚀 Despliegue Local o con Cloudflare Tunnel

```bash
# 1. Instalar requerimientos
pip install -r requirements.txt

# 2. Iniciar servidor local
python app.py

# 3. Iniciar el túnel de Cloudflare
./setup_tunnel.sh
```
