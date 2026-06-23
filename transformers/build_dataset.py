import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

GOAL_LABELS = {
    "BRAND_AWARENESS":     "Brand Awareness",
    "WEBSITE_VISITS":      "Website Visits",
    "ENGAGEMENT":          "Engagement",
    "VIDEO_VIEWS":         "Video Views",
    "LEAD_GENERATION":     "Lead Generation",
    "WEBSITE_CONVERSIONS": "Website Conversions",
    "JOB_APPLICANTS":      "Job Applicants",
    "TALENT_LEADS":        "Talent Leads",
}

def build_dataset(campaigns, analytics):
    """
    Une metadatos de campañas con métricas de analytics
    y calcula todas las métricas derivadas.
    """

    if not campaigns and not analytics:
        print("⚠️ No hay datos para procesar")
        return pd.DataFrame(), pd.DataFrame()

    df_campaigns = pd.DataFrame(campaigns) if campaigns else pd.DataFrame()
    df_analytics = pd.DataFrame(analytics) if analytics else pd.DataFrame()

    print(f"📊 Campañas: {len(df_campaigns)} | Registros analytics: {len(df_analytics)}")

    # ─── DATASET NIVEL CAMPAÑA ───────────────────────────────────────────────
    if not df_campaigns.empty and not df_analytics.empty:

        df_campaign_stats = df_analytics.groupby("campaign_id").agg(
            impressions         = ("impressions",         "sum"),
            clicks              = ("clicks",              "sum"),
            spend               = ("spend",               "sum"),
            reach               = ("reach",               "max"),
            video_views         = ("video_views",         "sum"),
            video_25pct         = ("video_25pct",         "sum"),
            video_50pct         = ("video_50pct",         "sum"),
            video_75pct         = ("video_75pct",         "sum"),
            video_completions   = ("video_completions",   "sum"),
            likes               = ("likes",               "sum"),
            comments            = ("comments",            "sum"),
            shares              = ("shares",              "sum"),
            follows             = ("follows",             "sum"),
            landing_page_clicks = ("landing_page_clicks", "sum"),
        ).reset_index()

        df_campaigns["campaign_id"]       = df_campaigns["campaign_id"].astype(str)
        df_campaign_stats["campaign_id"]  = df_campaign_stats["campaign_id"].astype(str)
        df_merged = df_campaigns.merge(df_campaign_stats, on="campaign_id", how="left")
        df_merged["goal"] = df_merged["goal"].map(GOAL_LABELS).fillna(df_merged["goal"])

        df_merged["CTR"]             = (df_merged["clicks"] / df_merged["impressions"]).round(4)
        df_merged["CPM"]             = (df_merged["spend"] / df_merged["impressions"] * 1000).round(2)
        df_merged["CPC"]             = (df_merged["spend"] / df_merged["clicks"]).round(2)
        df_merged["CPV"]             = (df_merged["spend"] / df_merged["video_views"]).round(2)
        df_merged["video_view_rate"] = (df_merged["video_views"] / df_merged["impressions"]).round(4)
        df_merged["completion_rate"] = (df_merged["video_completions"] / df_merged["video_views"]).round(4)
        df_merged["engagements"]     = (
            df_merged["likes"] +
            df_merged["comments"] +
            df_merged["shares"] +
            df_merged["clicks"]
        )
        df_merged["engagement_rate"] = (df_merged["engagements"] / df_merged["impressions"]).round(4)

        df_merged = df_merged.replace([float('inf'), float('-inf')], 0)
        df_merged = df_merged.fillna(0)

        print(f"✅ Dataset campañas construido: {len(df_merged)} filas")

    else:
        df_merged = pd.DataFrame()
        print("⚠️ No hay suficientes datos para construir dataset de campañas")

    # ─── DATASET NIVEL AD / CREATIVO ─────────────────────────────────────────
    if not df_analytics.empty:

        df_ads = df_analytics.copy()

        df_ads["CTR"]             = (df_ads["clicks"] / df_ads["impressions"]).round(4)
        df_ads["CPM"]             = (df_ads["spend"] / df_ads["impressions"] * 1000).round(2)
        df_ads["CPC"]             = (df_ads["spend"] / df_ads["clicks"]).round(2)
        df_ads["CPV"]             = (df_ads["spend"] / df_ads["video_views"]).round(2)
        df_ads["video_view_rate"] = (df_ads["video_views"] / df_ads["impressions"]).round(4)
        df_ads["completion_rate"] = (df_ads["video_completions"] / df_ads["video_views"]).round(4)
        df_ads["engagements"]     = (
            df_ads["likes"] +
            df_ads["comments"] +
            df_ads["shares"] +
            df_ads["clicks"]
        )
        df_ads["engagement_rate"] = (df_ads["engagements"] / df_ads["impressions"]).round(4)

        df_ads = df_ads.replace([float('inf'), float('-inf')], 0)
        df_ads = df_ads.fillna(0)

        print(f"✅ Dataset ads construido: {len(df_ads)} filas")

    else:
        df_ads = pd.DataFrame()

    return df_merged, df_ads