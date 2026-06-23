import requests
import warnings
import sys
import os
from datetime import datetime, timedelta
from urllib.parse import quote
warnings.filterwarnings('ignore')

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import AD_ACCOUNT_URN, API_BASE_URL, API_VERSION, REPORT_DAYS_BACK

def fetch_ad_stats(access_token):
    """Extrae métricas de campañas y ads en adAnalytics, con paginación."""

    end   = datetime.now()
    start_date = end - timedelta(days=REPORT_DAYS_BACK)

    date_range = (
        f"dateRange=(start:(year:{start_date.year},month:{start_date.month},day:{start_date.day}),"
        f"end:(year:{end.year},month:{end.month},day:{end.day}))"
    )

    account_encoded = quote(AD_ACCOUNT_URN, safe='')

    fields = ",".join([
        "impressions",
        "clicks",
        "costInLocalCurrency",
        "approximateMemberReach",
        "videoViews",
        "videoCompletions",
        "videoFirstQuartileCompletions",
        "videoMidpointCompletions",
        "videoThirdQuartileCompletions",
        "likes",
        "comments",
        "shares",
        "follows",
        "landingPageClicks",
        "pivotValues"
    ])

    headers = {
        "Authorization":             f"Bearer {access_token}",
        "Linkedin-Version":          API_VERSION,
        "X-Restli-Protocol-Version": "2.0.0"
    }

    print(f"📡 Llamando a LinkedIn adAnalytics API...")
    print(f"   Periodo: {start_date.strftime('%Y-%m-%d')} → {end.strftime('%Y-%m-%d')}")

    all_elements = []
    start = 0
    count = 100

    while True:
        url = (
            f"{API_BASE_URL}/adAnalytics"
            f"?q=statistics"
            f"&pivots=List(CAMPAIGN,CREATIVE)"
            f"&timeGranularity=ALL"
            f"&{date_range}"
            f"&accounts=List({account_encoded})"
            f"&start={start}"
            f"&count={count}"
            f"&fields={fields}"
        )

        r = requests.get(url, headers=headers, verify=False)

        if r.status_code == 426:
            print("❌ ERROR DE VERSIÓN DE API")
            return []

        if r.status_code != 200:
            print(f"❌ Error {r.status_code}: {r.text}")
            return []

        data = r.json()
        elements = data.get("elements", [])

        if not elements:
            break

        all_elements.extend(elements)
        print(f"   Página start={start}: {len(elements)} registros")

        if len(elements) < count:
            break

        start += count

    if not all_elements:
        print("⚠️ No se encontraron datos en el periodo indicado")
        return []

    records = []
    for e in all_elements:
        pivot_values = e.get("pivotValues", [])

        records.append({
            "campaign_id":         pivot_values[0].split(":")[-1] if len(pivot_values) > 0 else None,
            "creative_id":         pivot_values[1].split(":")[-1] if len(pivot_values) > 1 else None,
            "impressions":         int(e.get("impressions", 0)),
            "clicks":              int(e.get("clicks", 0)),
            "spend":               float(e.get("costInLocalCurrency", 0)),
            "reach":               int(e.get("approximateMemberReach", 0)),
            "video_views":         int(e.get("videoViews", 0)),
            "video_25pct":         int(e.get("videoFirstQuartileCompletions", 0)),
            "video_50pct":         int(e.get("videoMidpointCompletions", 0)),
            "video_75pct":         int(e.get("videoThirdQuartileCompletions", 0)),
            "video_completions":   int(e.get("videoCompletions", 0)),
            "likes":               int(e.get("likes", 0)),
            "comments":            int(e.get("comments", 0)),
            "shares":              int(e.get("shares", 0)),
            "follows":             int(e.get("follows", 0)),
            "landing_page_clicks": int(e.get("landingPageClicks", 0)),
        })

    print(f"✅ Registros recibidos: {len(records)}")
    return records

if __name__ == "__main__":
    from auth.linkedin_auth import get_access_token
    token = get_access_token()
    records = fetch_ad_stats(token)
    if records:
        print("\nPrimer registro de ejemplo:")
        for k, v in records[0].items():
            print(f"  {k}: {v}")