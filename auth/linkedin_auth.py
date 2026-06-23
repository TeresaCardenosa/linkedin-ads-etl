import requests
import os
import warnings
warnings.filterwarnings('ignore')
from dotenv import load_dotenv
load_dotenv()

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN, TOKEN_URL

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

if __name__ == "__main__":
    token = get_access_token()
    print(f"Token: {token[:30]}...")