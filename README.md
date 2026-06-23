# LinkedIn Ads ETL — CLIENTE

Script Python para extraer métricas de campañas publicitarias de LinkedIn Ads y exportarlas a un documento Excel.

## ¿Qué hace este proyecto?

Conecta con la API de LinkedIn Ads, extrae las métricas de todas las campañas activas en un rango de fechas y genera un fichero Excel estructurado.

## Requisitos

- Python 3.12+
- App creada en LinkedIn Developer aprobada, con acceso a Advertising API y permisos `r_ads` y `r_ads_reporting`

## Instalación

1. Descarga o clona el proyecto
2. Crea y activa el entorno virtual:
```
   python -m venv venv
   venv\Scripts\Activate.ps1
```
   Si PowerShell bloquea la ejecución de scripts:
```
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
3. Instala las dependencias:
```
   pip install -r requirements.txt
```

## Configuración

Crea un fichero `.env` en la raíz del proyecto con este contenido:
```
CLIENT_ID=tu_client_id 
CLIENT_SECRET=tu_client_secret 
ACCESS_TOKEN=tu_access_token 
REFRESH_TOKEN=tu_refresh_token 
ACCOUNT_ID=tu_account_id 
```

### ¿Dónde encontrar cada valor?

- `CLIENT_ID` y `CLIENT_SECRET`: LinkedIn Developer Portal → Tu app → pestaña Auth → Authentication keys
- `ACCOUNT_ID`: LinkedIn Campaign Manager → URL del navegador → el número en la URL
- `ACCESS_TOKEN` y `REFRESH_TOKEN`: se generan al ejecutar el script de autenticación → Solicita copiar y pegar URL en navegador, loguearte en LinkedIn y tienes que devolverle el code de la URL de tu web, la que hayas autorizado en Developers LinkedIn 

## Generar el ACCESS_TOKEN (primera vez y cada 60 días)

El `ACCESS_TOKEN` caduca cada 60 días. El `REFRESH_TOKEN` caduca cada 365 días.
Para regenerarlos:

1. Ejecuta el script de autenticación:
```
   python auth/linkedin_auth.py
```
2. Copia la URL que aparece en el terminal y ábrela en el navegador
3. Inicia sesión en LinkedIn y autoriza la app
4. LinkedIn te redirigirá a UNAWEB con una URL así:
```
   https://www.UNAWEB.com/?code=XXXXXXX&state=random123
```
5. Copia el valor entre `?code=` y `&state=`
6. Pégalo en el terminal cuando el script te lo pida
7. El script imprimirá el `access_token` y `refresh_token` nuevos
8. Actualiza el fichero `.env` con los valores nuevos

> **Nota**: el `code` de la URL caduca en aproximadamente 30 segundos.
> Hay que pegarlo en el terminal inmediatamente.

> **Nota**: a partir de la segunda ejecución el `ACCESS_TOKEN` se renueva
> automáticamente usando el `REFRESH_TOKEN`. No es necesario repetir el
> proceso OAuth2 hasta que caduque el `REFRESH_TOKEN` (365 días).

## Ejecutar el script

Con el entorno virtual activo y el `.env` configurado:
```
python main.py
```

El script ejecuta 4 pasos:
1. Autenticación con LinkedIn (renueva el token automáticamente)
2. Extracción de metadatos de campañas y métricas analytics
3. Transformación y cálculo de métricas derivadas
4. Exportación a `linkedin_ads_data.xlsx` en la carpeta del proyecto

## Configurar el rango de fechas

En `config.py` puedes ajustar el rango de datos:
```python
REPORT_DAYS_BACK = 30  # Cambia este número
```

## Métricas extraídas

### Nivel campaña (tab: campaigns)
| Métrica | Descripción |
|---|---|
| campaign_name | Nombre de la campaña |
| goal | Objetivo de la campaña (Brand Awareness, Video Views, etc.) |
| start_date / end_date | Periodo de la campaña |
| budget | Presupuesto total |
| currency | Moneda de la cuenta |
| impressions | Impresiones |
| reach | Alcance |
| clicks | Clicks |
| landing_page_clicks | Clicks a landing page |
| spend | Gasto total |
| CTR | Click-through rate (clicks / impresiones) |
| CPM | Coste por mil impresiones |
| CPC | Coste por click |
| video_views | Visualizaciones de vídeo |
| video_view_rate | Tasa de visualización (video views / impresiones) |
| CPV | Coste por visualización |
| video_25pct | Vídeos vistos al 25% |
| video_50pct | Vídeos vistos al 50% |
| video_75pct | Vídeos vistos al 75% |
| video_completions | Vídeos completados al 100% |
| completion_rate | Tasa de completion (completions / video views) |
| engagements | Total interacciones (likes + comments + shares + follows + clicks) |
| engagement_rate | Tasa de engagement (engagements / impresiones) |
| likes | Likes |
| comments | Comentarios |
| shares | Compartidos |
| follows | Nuevos seguidores |


## Estructura 

```
linkedin_etl/
├── auth/
│   └── linkedin_auth.py          # Autenticación OAuth2 con LinkedIn
├── extractors/
│   ├── campaigns.py              # Extrae metadatos de campañas
│   └── analytics.py              # Extrae métricas de la API adAnalytics
├── transformers/
│   └── build_dataset.py          # Join y cálculo de métricas derivadas
├── loaders/
│   └── excel_export.py           # Exporta datos a fichero Excel
├── venv/                         # Entorno virtual (no tocar)
├── .env                          # Credenciales 
├── config.py                     # Variables globales del proyecto
├── main.py                       # Orquestador principal
├── requirements.txt              # Dependencias del proyecto
└── README.md                     # Este fichero
```