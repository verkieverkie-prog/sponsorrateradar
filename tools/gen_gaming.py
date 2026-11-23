import json
A = "https://adready.app/gaming-creators.html"
AN = "AdReady gaming creator rates (rate guide)"
L = "https://lemniagency.com/articles/youtube-sponsorship-rates-pricing-guide-2026"
LN = "Lemniscate YouTube pricing guide (rate guide)"
def row(plat, aud, bucket, place, lo, hi, cpm, sn, su, note):
    return {"platform": plat, "niche": "Gaming", "audience_size": aud, "audience_bucket": bucket,
            "avg_views": None, "placement": place, "price_usd_low": lo, "price_usd_high": hi,
            "cpm_usd": cpm, "year": 2026, "source_name": sn, "source_url": su, "note": note}
rows = []
tiers = [("5K-10K subs", "1K-10K", 150, 500, 400, 1500),
         ("10K-50K subs", "10K-50K", 500, 2000, 1500, 5000),
         ("50K-100K subs", "50K-100K", 1500, 5000, 4000, 12000),
         ("100K-500K subs", "100K-500K", 4000, 12000, 10000, 30000)]
for aud, b, ml, mh, dl, dh in tiers:
    rows.append(row("YouTube", aud, b, "Integration (60s)", ml, mh, None, AN, A, "Gaming YouTube 60s mid-roll; guide assumes $4-$12 CPM"))
    rows.append(row("YouTube", aud, b, "Dedicated video", dl, dh, None, AN, A, "Gaming YouTube dedicated video; guide assumes $4-$12 CPM"))
rows.append(row("YouTube", "500K+ subs", "500K-1M", "Integration (60s)", 10000, 10000, None, AN, A, "Floor only: source says $10,000+ for 500K+ gaming channels"))
rows.append(row("YouTube", "500K+ subs", "500K-1M", "Dedicated video", 25000, 25000, None, AN, A, "Floor only: source says $25,000+ for 500K+ gaming channels"))
for sub, lo, hi in [("PC hardware / reviews", 10, 18), ("Esports / competitive", 6, 12), ("Game reviews / analysis", 6, 10),
                    ("Let's Play / walkthrough", 3, 7), ("Mobile gaming", 5, 10)]:
    rows.append(row("YouTube", f"per 1,000 views - Gaming: {sub}", "All tiers", "Benchmark", lo, hi, lo, AN, A, f"Sponsorship CPM range for {sub} gaming content"))
rows.append(row("Twitch", "per 1,000 views - Twitch gaming streams", "All tiers", "Benchmark", 3, 6, 3, AN, A, "Twitch streaming sponsorship CPM; hourly rates often added"))
rows.append(row("Twitch", "Mid-size streamer, per hour", "All tiers", "Sponsored stream (hourly)", 100, 500, None, AN, A, "Hourly sponsored stream rate for mid-size streamers"))
rows.append(row("YouTube", "per 1,000 views - Gaming & Esports", "All tiers", "Benchmark", 14, 26, 14, LN, L, "Media-buyer CPM band for gaming & esports integrations, NA/EU"))
rows.append(row("YouTube", "Mid-tier gaming channel (25K-100K 30-day views)", "50K-100K", "Integration (60s)", 1500, 3200, None, LN, L, "Average mid-tier gaming & esports deal size"))
json.dump(rows, open("data/new_rates.json", "w"), indent=1)
print(len(rows))
