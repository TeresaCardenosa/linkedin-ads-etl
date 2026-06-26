import gspread
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd
import os
import sys
import pickle
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import GOOGLE_CREDENTIALS, SPREADSHEET_ID, SHEET_TAB_NAME

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

TOKEN_FILE = "google_token.pickle"

def get_google_client():
    """Autentica con Google y devuelve un cliente de gspread."""
    creds = None

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            print("✅ Token de Google renovado automáticamente")
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                GOOGLE_CREDENTIALS, SCOPES
            )
            creds = flow.run_local_server(port=0)
            print("✅ Autenticación con Google completada")

        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)

    return gspread.authorize(creds)

def write_to_gsheets(df_campaigns, df_ads):
    """Añade los datos del mes al Google Sheet sin sobreescribir los anteriores."""

    if df_campaigns.empty and df_ads.empty:
        print("⚠️ No hay datos para escribir en Google Sheets")
        return

    print("📡 Conectando con Google Sheets...")
    client = get_google_client()

    try:
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        print(f"✅ Google Sheet encontrado")
    except Exception as e:
        print(f"❌ No se pudo abrir el Google Sheet: {e}")
        return

    # Obtener o crear la pestaña
    try:
        worksheet = spreadsheet.worksheet(SHEET_TAB_NAME)
        print(f"   Pestaña '{SHEET_TAB_NAME}' encontrada")
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(
            title=SHEET_TAB_NAME, rows=10000, cols=50
        )
        print(f"   Pestaña '{SHEET_TAB_NAME}' creada")

    # Columnas a exportar
    columns_campaigns = [
        "campaign_name", "goal",
        "start_date", "end_date", "budget", "currency",
        "impressions", "reach", "clicks", "landing_page_clicks",
        "spend", "CTR", "CPM", "CPC",
        "video_views", "video_view_rate", "CPV",
        "video_25pct", "video_50pct", "video_75pct",
        "video_completions", "completion_rate",
        "engagements", "engagement_rate",
        "likes", "comments", "shares", "follows",
    ]

    if df_campaigns.empty:
        return

    cols = [c for c in columns_campaigns if c in df_campaigns.columns]
    df_export = df_campaigns[cols].copy()

    # Añadir columna de fecha de extracción para trazabilidad
    df_export.insert(0, "extraction_date", datetime.now().strftime("%Y-%m-%d"))

    # Comprobar si la pestaña ya tiene datos
    existing_data = worksheet.get_all_values()

    if not existing_data:
        # Pestaña vacía — escribir cabecera + datos
        data = [df_export.columns.tolist()] + df_export.astype(str).values.tolist()
        worksheet.update(data, value_input_option="USER_ENTERED")
        print(f"   ✅ {len(df_export)} filas escritas con cabecera")
    else:
        # Pestaña con datos — añadir solo las filas nuevas al final
        new_rows = df_export.astype(str).values.tolist()
        worksheet.append_rows(new_rows, value_input_option="USER_ENTERED")
        print(f"   ✅ {len(df_export)} filas añadidas al final")

    print(f"✅ Datos escritos correctamente en '{SHEET_TAB_NAME}'")