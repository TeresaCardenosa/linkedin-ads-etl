import requests
import os
import warnings
import sys
warnings.filterwarnings('ignore')
from dotenv import load_dotenv
load_dotenv()

# ─── CREDENCIALES ───────────────────────────────────────
CLIENT_ID     = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TOKEN_URL

REDIRECT_URI = "https://www.google.com/" # Ver README - Puede ser cualquier URL, no se usa realmente, solo es para obtener el code en la URL de redirección
SCOPE        = "r_ads r_ads_reporting"

def get_access_token():
    """Obtiene un access token fresco usando el refresh token."""
    if not REFRESH_TOKEN:
        raise Exception("REFRESH_TOKEN no encontrado en .env")

    r = requests.post(TOKEN_URL, data={
        'grant_type':    'refresh_token',
        'refresh_token': REFRESH_TOKEN,
        'client_id':     CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }, verify=False)

    if r.status_code != 200:
        raise Exception(f"Error renovando token: {r.status_code} {r.text}")

    data = r.json()
    if 'access_token' not in data:
        raise Exception(f"No se recibió access_token: {data}")

    print("✅ Access token renovado correctamente")
    return data['access_token']

def build_auth_url():
    """Genera la URL de autorización OAuth2 para obtener el primer token."""
    from urllib.parse import quote
    url = (
        "https://www.linkedin.com/oauth/v2/authorization"
        "?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={quote(REDIRECT_URI, safe='')}"
        "&state=random123"
        f"&scope={quote(SCOPE, safe='')}"
    )
    print("\nAbre esta URL en tu navegador:\n")
    print(url)
    return url

def exchange_code_for_token(code):
    """Intercambia el code de la URL de redirección por access_token y refresh_token."""
    r = requests.post(TOKEN_URL, data={
        'grant_type':    'authorization_code',
        'code':          code,
        'redirect_uri':  REDIRECT_URI,
        'client_id':     CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }, verify=False, timeout=30)
    print("\nRespuesta de LinkedIn:")
    print(r.json())

if __name__ == "__main__":
    token = get_access_token()
    print(f"Token: {token[:30]}...")