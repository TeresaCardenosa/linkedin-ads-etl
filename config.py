import os
from dotenv import load_dotenv
load_dotenv()

# ─── LINKEDIN API ───────────────────────────────────────
ACCOUNT_ID     = os.getenv("ACCOUNT_ID")
AD_ACCOUNT_URN = f"urn:li:sponsoredAccount:{ACCOUNT_ID}"
TOKEN_URL      = "https://www.linkedin.com/oauth/v2/accessToken"
API_BASE_URL   = "https://api.linkedin.com/rest"
# Las versiones caducan a los 12 meses
# Versiones activas: https://learn.microsoft.com/en-us/linkedin/marketing/versioning
API_VERSION    = "202502"

# ─── FECHAS ─────────────────────────────────────────────
REPORT_DAYS_BACK = 30  # Cambia este número para ampliar o reducir el rango

# ─── OUTPUT ─────────────────────────────────────────────
SPREADSHEET_ID   = os.getenv("SPREADSHEET_ID")
SHEET_TAB_NAME   = os.getenv("SHEET_TAB_NAME")
GOOGLE_CREDENTIALS = "google_credentials.json"