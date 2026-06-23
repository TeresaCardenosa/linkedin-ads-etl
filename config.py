import os
from dotenv import load_dotenv
load_dotenv()

# ─── CREDENCIALES ───────────────────────────────────────
CLIENT_ID     = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
ACCESS_TOKEN  = os.getenv("ACCESS_TOKEN")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
ACCOUNT_ID    = os.getenv("ACCOUNT_ID")

# ─── LINKEDIN API ───────────────────────────────────────
AD_ACCOUNT_URN = f"urn:li:sponsoredAccount:{ACCOUNT_ID}"
TOKEN_URL      = "https://www.linkedin.com/oauth/v2/accessToken"
API_BASE_URL   = "https://api.linkedin.com/rest"
# Las versiones caducan a los 12 meses
# Versiones activas: https://learn.microsoft.com/en-us/linkedin/marketing/versioning
API_VERSION    = "202502"

# ─── FECHAS ─────────────────────────────────────────────
REPORT_DAYS_BACK = 30  # Cambia este número para ampliar o reducir el rango

# ─── OUTPUT ─────────────────────────────────────────────
OUTPUT_FILENAME = "linkedin_ads_data.xlsx"