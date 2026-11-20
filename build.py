#!/usr/bin/env python3
"""Builds the static Sponsor Rate Radar site into ./site from data/rates.json."""
import json, os, re, html, statistics, datetime, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
CFG = json.load(open(os.path.join(ROOT, "config.json")))
BASE = CFG["base_url"].rstrip("/")
PATH = CFG.get("base_path", "").rstrip("/")
rates = json.load(open(os.path.join(ROOT, "data", "rates.json")))

def esc(s):
    return html.escape(str(s if s is not None else ""))

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")

def money(lo, hi):
    lo, hi = int(round(lo)), int(round(hi))
    return f"${lo:,}" if lo == hi else f"${lo:,}–${hi:,}"

def mid(r):
    return (r["price_usd_low"] + r["price_usd_high"]) / 2

TODAY = datetime.date.today().isoformat()

SPONSOR = CFG.get("sponsor")  # {"name","url","line"} or None

def sponsor_box():
    if SPONSOR:
        return (f'<div class="sponsor">Sponsored by <a href="{esc(SPONSOR["url"])}" rel="sponsored noopener" target="_blank">'
                f'<b>{esc(SPONSOR["name"])}</b></a>: {esc(SPONSOR["line"])}</div>')
    return f'<div class="sponsor empty">This spot is open. <a href="{PATH}/sponsor.html">Sponsor Sponsor Rate Radar →</a></div>'

def newsletter_box():
    url = CFG.get("newsletter_url")
    if url:
        return (f'<div class="news"><b>Get 5 new real sponsor rates every week.</b> Free, one email, no fluff. '
                f'<a class="btn" href="{esc(url)}" target="_blank" rel="noopener">Join the newsletter</a></div>')
    return ('<div class="news"><b>Weekly rate drop coming soon:</b> 5 new real sponsor rates every week, free.</div>')

def page(title, desc, body, path, extra_head=""):
    canon = f"{BASE}{path}"
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}"><meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canon}">
<link rel="stylesheet" href="{PATH}/style.css">{extra_head}</head><body>
<header><a class="logo" href="{PATH}/">📡 Sponsor Rate Radar</a><nav>
<a href="{PATH}/">Rates</a><a href="{PATH}/calculator.html">Calculator</a><a href="{PATH}/rates/">By niche</a>
<a href="{PATH}/submit.html">Share a rate</a><a href="{PATH}/sponsor.html">Sponsor</a></nav></header>
<main>{sponsor_box()}{body}{newsletter_box()}</main>
<footer>Every number links to its public source or came from a creator submission we reviewed. Rates are what was reported, not guarantees.
Updated {TODAY}. · <a href="{PATH}/about.html">About &amp; method</a></footer>
</body></html>"""

def table(rows):
    out = ['<div class="tw"><table><thead><tr><th>Platform</th><th>Niche</th><th>Audience</th><th>Placement</th><th>Price</th><th>CPM</th><th>Year</th><th>Source</th></tr></thead><tbody>']
    for r in rows:
        cpm = f"${r['cpm_usd']:g}" if r.get("cpm_usd") else "–"
        out.append(
            f'<tr data-platform="{esc(r["platform"])}" data-niche="{esc(r["niche"])}" data-bucket="{esc(r["audience_bucket"])}" data-placement="{esc(r["placement"])}">'
            f'<td>{esc(r["platform"])}</td><td>{esc(r["niche"])}</td><td>{esc(r["audience_size"])}</td><td>{esc(r["placement"])}</td>'
            f'<td class="p">{money(r["price_usd_low"], r["price_usd_high"])}</td><td>{cpm}</td><td>{esc(r["year"])}</td>'
            f'<td><a href="{esc(r["source_url"])}" target="_blank" rel="noopener nofollow" title="{esc(r.get("note",""))}">{esc(r["source_name"])}</a></td></tr>')
    out.append("</tbody></table></div>")
    return "".join(out)

def opts(name, vals):
    return f'<select id="f-{name}"><option value="">All {name}s</option>' + "".join(
        f'<option>{esc(v)}</option>' for v in vals) + "</select>"

def write(rel, content):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(content)

BUCKETS = ["<10K", "10K-50K", "50K-100K", "100K-500K", "500K-1M", "1M+"]
rates.sort(key=lambda r: (-r["year"], r["platform"], r["niche"]))
platforms = sorted({r["platform"] for r in rates})
niches = sorted({r["niche"] for r in rates})
placements = sorted({r["placement"] for r in rates})
buckets = [b for b in BUCKETS if any(r["audience_bucket"] == b for r in rates)]

if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)
shutil.copy(os.path.join(ROOT, "static", "style.css"), os.path.join(OUT, "style.css"))
open(os.path.join(OUT, ".nojekyll"), "w").write("")

FILTER_JS = """<script>
const fs=['platform','niche','bucket','placement'];
function f(){const q=document.getElementById('q').value.toLowerCase();let n=0;
document.querySelectorAll('tbody tr').forEach(tr=>{let ok=fs.every(k=>{const v=document.getElementById('f-'+k).value;return !v||tr.dataset[k]===v});
if(q&&!tr.innerText.toLowerCase().includes(q))ok=false;tr.style.display=ok?'':'none';if(ok)n++});
document.getElementById('cnt').textContent=n+' rates';}
fs.forEach(k=>document.getElementById('f-'+k).onchange=f);document.getElementById('q').oninput=f;f();
</script>"""

# --- Home
yt = [mid(r) for r in rates if r["platform"] == "YouTube" and r["placement"] != "Benchmark"]
body = f"""<h1>What do sponsors actually pay creators?</h1>
<p class="lede">{len(rates)} real sponsorship rates for YouTube, Shorts, newsletters and podcasts, each linked to where it was published.
Filter by niche and audience size, or use the <a href="{PATH}/calculator.html">rate calculator</a>.</p>
<div class="filters"><input id="q" placeholder="Search (e.g. tech, 50K, dedicated)">
{opts('platform', platforms)}{opts('niche', niches)}<select id="f-bucket"><option value="">All sizes</option>{''.join(f'<option>{b}</option>' for b in buckets)}</select>{opts('placement', placements)}
<span id="cnt"></span></div>{table(rates)}
<p class="cta">Got a real deal? <a href="{PATH}/submit.html">Share your rate anonymously</a>. It helps every creator negotiate.</p>
{FILTER_JS}"""
write("index.html", page("YouTube & Newsletter Sponsorship Rates (Real Data) | Sponsor Rate Radar",
      f"{len(rates)} real, sourced sponsorship rates for YouTubers and newsletter creators by niche, size and placement. Free rate calculator.", body, "/"))

# --- Calculator: CPMs derived only from our data
cpm_data = {}
for r in rates:
    c = r.get("cpm_usd")
    if not c and r.get("avg_views"):
        c = mid(r) / r["avg_views"] * 1000
    if c:
        cpm_data.setdefault(r["platform"], []).append((r["niche"], round(c, 2)))
calc_json = json.dumps(cpm_data)
body = f"""<h1>Sponsorship rate calculator</h1>
<p class="lede">How much should you charge for a sponsor? Enter your typical views. We estimate a range from the CPMs in our sourced data, not made-up formulas.</p>
<div class="calc"><label>Platform <select id="cp">{''.join(f'<option>{esc(p)}</option>' for p in cpm_data)}</select></label>
<label>Niche <select id="cn"><option value="">Any niche</option>{''.join(f'<option>{esc(n)}</option>' for n in niches)}</select></label>
<label>Avg views per video / opens per email <input id="cv" type="number" value="10000" min="100"></label>
<div id="out" class="out"></div></div>
<p class="small">How it works: we take the CPMs (price per 1,000 views) from matching data points, then use the 25th–75th percentile range times your views. With a niche picked and few matching points, we fall back to all niches on that platform.</p>
<script>const D={calc_json};
function pct(a,p){{a=[...a].sort((x,y)=>x-y);const i=(a.length-1)*p,l=Math.floor(i);return a[l]+(a[Math.ceil(i)]-a[l])*(i-l)}}
function run(){{const p=document.getElementById('cp').value,n=document.getElementById('cn').value,v=+document.getElementById('cv').value||0;
let pts=(D[p]||[]).filter(x=>!n||x[0]===n),note='';if(pts.length<3){{pts=D[p]||[];if(n)note=' (not enough '+n+' data yet, using all niches)';}}
if(!pts.length){{document.getElementById('out').innerHTML='Not enough data yet.';return}}
const c=pts.map(x=>x[1]),lo=pct(c,.25)*v/1000,hi=pct(c,.75)*v/1000,f=x=>'$'+Math.round(x).toLocaleString();
document.getElementById('out').innerHTML='<div class="big">'+f(lo)+' – '+f(hi)+'</div>per sponsor placement, based on '+pts.length+' data points'+note+'. Median CPM $'+pct(c,.5).toFixed(2)+'.';}}
['cp','cn','cv'].forEach(i=>document.getElementById(i).oninput=run);run();</script>"""
write("calculator.html", page("Sponsorship Rate Calculator: How Much to Charge for a YouTube Sponsor",
      "Free calculator: estimate what to charge sponsors based on your views, niche and real CPM data.", body, "/calculator.html"))

# --- Niche pages (SEO)
idx = ['<h1>Sponsorship rates by niche</h1><ul class="niches">']
for n in niches:
    rows = [r for r in rates if r["niche"] == n]
    s = slug(n)
    prices = [mid(r) for r in rows if r["placement"] != "Benchmark"]
    summ = f"Reported deals range from {money(min(prices), min(prices))} to {money(max(prices), max(prices))}." if prices else ""
    b = (f'<h1>{esc(n)} sponsorship rates</h1><p class="lede">{len(rows)} real sponsorship data points for {esc(n).lower()} creators. {summ} '
         f'Every row links to its source. Try the <a href="{PATH}/calculator.html">calculator</a> for your own numbers.</p>' + table(rows))
    write(f"rates/{s}.html", page(f"{n} Sponsorship Rates for YouTubers & Newsletters ({datetime.date.today().year}) | Sponsor Rate Radar",
          f"What sponsors pay {n.lower()} creators: {len(rows)} real, sourced rates by channel size and placement.", b, f"/rates/{s}.html"))
    idx.append(f'<li><a href="{PATH}/rates/{s}.html">{esc(n)}</a> <span>{len(rows)} rates</span></li>')
idx.append("</ul>")
write("rates/index.html", page("Sponsorship Rates by Niche | Sponsor Rate Radar", "Browse real creator sponsorship rates by niche.", "".join(idx), "/rates/"))

# --- Submit
form = CFG.get("submit_endpoint")
fields = """<label>Platform<select name="platform" required><option>YouTube</option><option>Shorts</option><option>Newsletter</option><option>Podcast</option><option>TikTok</option><option>Instagram</option></select></label>
<label>Niche<input name="niche" required placeholder="e.g. Tech, Gaming, Finance"></label>
<label>Audience size<input name="audience" required placeholder="e.g. 42K subs / 8K email subscribers"></label>
<label>Avg views or opens per post<input name="avg_views" type="number"></label>
<label>Placement<input name="placement" required placeholder="e.g. 60s integration, dedicated video, primary newsletter ad"></label>
<label>Price paid (USD)<input name="price" type="number" required></label>
<label>Month & year<input name="date" placeholder="e.g. Oct 2026"></label>
<label>Anything else? (sponsor category, how they found you)<textarea name="note"></textarea></label>
<label class="small"><input type="checkbox" required> This is a real deal I was paid for. I won't name the brand if I'm under NDA.</label>"""
if form:
    sbody = f'<form class="sub" action="{esc(form)}" method="POST"><input type="hidden" name="_subject" value="New rate submission"><input type="text" name="_honey" style="display:none">{fields}<button class="btn">Submit anonymously</button></form>'
else:
    sbody = '<p><b>Submissions open in a few days.</b> Join the newsletter to hear when they do.</p>'
write("submit.html", page("Share Your Sponsorship Rate Anonymously | Sponsor Rate Radar",
      "Help other creators negotiate: anonymously share what a sponsor paid you.",
      f'<h1>Share a sponsorship rate</h1><p class="lede">Anonymous. No brand names needed. We review every submission before it goes live and never publish your channel name.</p>{sbody}', "/submit.html"))

# --- Sponsor page
SPFORM = (f'<form class="sub" action="{esc(form)}" method="POST"><input type="hidden" name="_subject" value="SPONSOR inquiry - Sponsor Rate Radar">'
          '<input type="text" name="_honey" style="display:none"><label>Your name<input name="name" required></label>'
          '<label>Work email<input name="email" type="email" required></label><label>Company / product<input name="company" required></label>'
          '<label>Anything we should know?<textarea name="message"></textarea></label><button class="btn">Get in touch</button></form>') if form else '<p>Contact form coming soon.</p>'
contact = CFG.get("contact_email", "")
sp = f"""<h1>Sponsor Sponsor Rate Radar</h1>
<p class="lede">Every visitor here is a creator trying to figure out what to charge sponsors: YouTubers, newsletter writers and podcasters.
If you sell to creators (editing, thumbnails, gear, sponsorship marketplaces, creator finance), this is your audience.</p>
<div class="card"><h2>Founding sponsor: ${CFG.get('sponsor_price', 50)}/month</h2><ul>
<li>Your logo, link and one line at the top of every page</li><li>A sponsor line in the weekly rate newsletter</li>
<li>One sponsor at a time. No clutter, no ad networks.</li><li>Month to month, cancel any time</li></ul>
<p>Founding price, locked in for as long as you stay.</p>
{SPFORM}</div>"""
write("sponsor.html", page("Advertise to YouTubers & Creators | Sponsor Rate Radar", "Reach creators researching sponsorship rates. Founding sponsor slots.", sp, "/sponsor.html"))

# --- About
ab = """<h1>About &amp; method</h1><p>Sponsor Rate Radar collects sponsorship rates that creators, agencies and platforms have published,
plus anonymous creator submissions we review by hand.</p><ul><li>Every curated number links to its source.</li>
<li>Submissions are checked for plausibility (views vs price) before publishing.</li><li>Benchmarks are industry averages, labeled "Benchmark".</li>
<li>We never invent data. If something looks wrong, tell us and we'll fix or remove it.</li></ul>"""
write("about.html", page("About & Method | Sponsor Rate Radar", "How Sponsor Rate Radar collects and checks sponsorship rate data.", ab, "/about.html"))

# --- sitemap + robots
urls = ["/", "/calculator.html", "/rates/", "/submit.html", "/sponsor.html", "/about.html"] + [f"/rates/{slug(n)}.html" for n in niches]
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
      "".join(f"<url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls) + "</urlset>")
write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
write("data/rates.json", json.dumps(rates, indent=1))
print(f"built {len(rates)} rates, {len(niches)} niche pages")
