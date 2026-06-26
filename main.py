import sys
import os
import warnings
warnings.filterwarnings('ignore')

from auth.linkedin_auth import get_access_token
from extractors.campaigns import get_campaigns
from extractors.analytics import fetch_ad_stats
from transformers.build_dataset import build_dataset
from loaders.gsheets import write_to_gsheets

def main():
    print("=" * 50)
    print("  LinkedIn Ads ETL — La Roche Posay")
    print("=" * 50)

    # ─── PASO 1: Autenticación ───────────────────────
    print("\n[1/4] Autenticando con LinkedIn...")
    token = get_access_token()

    # ─── PASO 2: Extracción ──────────────────────────
    print("\n[2/4] Extrayendo datos de LinkedIn...")
    campaigns = get_campaigns(token)
    analytics = fetch_ad_stats(token)

    # ─── PASO 3: Transformación ──────────────────────
    print("\n[3/4] Transformando y calculando métricas...")
    df_campaigns, df_ads = build_dataset(campaigns, analytics)

    # ─── PASO 4: Exportación ─────────────────────────
    print("\n[4/4] Exportando a Google Sheets...")
    write_to_gsheets(df_campaigns, df_ads)

    print("\n" + "=" * 50)
    print("  ✅ Proceso completado")
    print("=" * 50)

if __name__ == "__main__":
    main()