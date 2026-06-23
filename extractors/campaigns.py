import requests
import warnings
import sys
import os
warnings.filterwarnings('ignore')

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import AD_ACCOUNT_URN, API_BASE_URL, API_VERSION, ACCOUNT_ID

def get_campaigns(access_token):
    """Extrae metadatos de todas las campañas de la cuenta, con paginación."""

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type":  "application/json"
    }

    print("📡 Extrayendo metadatos de campañas...")

    all_elements = []
    start = 0
    count = 100  # Pedimos 100 por página para minimizar llamadas

    while True:
        url = (
            f"https://api.linkedin.com/v2/adCampaignsV2"
            f"?q=search"
            f"&search.account.values[0]=urn:li:sponsoredAccount:{ACCOUNT_ID}"
            f"&search.status.values[0]=ACTIVE"
            f"&search.status.values[1]=COMPLETED"
            f"&search.status.values[2]=CANCELED"
            f"&search.status.values[3]=PAUSED"
            f"&start={start}"
            f"&count={count}"
            f"&fields=id,name,status,objectiveType,totalBudget,dailyBudget,"
            f"unitCost,runSchedule"
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
            break  # No hay más páginas

        all_elements.extend(elements)
        print(f"   Página start={start}: {len(elements)} campañas")

        # Si recibimos menos de lo pedido, es la última página
        if len(elements) < count:
            break

        start += count

    if not all_elements:
        print("⚠️ No se encontraron campañas")
        return []

    from datetime import datetime, timezone

    campaigns = []
    for c in all_elements:
        run_schedule = c.get("runSchedule", {})
        total_budget = c.get("totalBudget", {})
        daily_budget = c.get("dailyBudget", {})

        start_ms = run_schedule.get("start")
        end_ms   = run_schedule.get("end")
        start_date = datetime.fromtimestamp(start_ms / 1000, tz=timezone.utc).strftime('%Y-%m-%d') if start_ms else None
        end_date   = datetime.fromtimestamp(end_ms   / 1000, tz=timezone.utc).strftime('%Y-%m-%d') if end_ms   else None

        campaigns.append({
            "campaign_id":    str(c.get("id")),
            "campaign_name":  c.get("name"),
            "status":         c.get("status"),
            "goal":           c.get("objectiveType"),
            "currency":       total_budget.get("currencyCode") or daily_budget.get("currencyCode"),
            "budget":         total_budget.get("amount") or daily_budget.get("amount"),
            "start_date":     start_date,
            "end_date":       end_date,
        })

    print(f"✅ Campañas encontradas: {len(campaigns)}")
    return campaigns

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from auth.linkedin_auth import get_access_token
    token = get_access_token()
    campaigns = get_campaigns(token)
    for c in campaigns:
        print(c)