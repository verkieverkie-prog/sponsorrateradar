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
    return f"${lo:,}" if lo == hi else f"${lo:,}-${hi:,}"

def mid(r):
    return (r["price_usd_low"] + r["price_usd_high"]) / 2

TODAY = datetime.date.today().isoformat()

SPONSOR = CFG.get("sponsor")  # {"name","url","line"} or None
PRICE = CFG.get("sponsor_price", 49)

def sponsor_box():
    if SPONSOR:
        return (f'<div class="sponsor">Sponsored by <a href="{esc(SPONSOR["url"])}" rel="sponsored noopener" target="_blank">'
                f'<b>{esc(SPONSOR["name"])}</b></a>: {esc(SPONSOR["line"])}</div>')
    return f'<div class="sponsor empty"><span class="tag">Sponsor</span> Selling to creators? Put your product on every page of this site. <a href="{PATH}/sponsor.html">Book the ${PRICE} slot</a></div>'

def newsletter_box():
    url = CFG.get("newsletter_url")
    if url:
        return (f'<div class="news"><b>Get 5 new brand deal receipts every week.</b> Actual creator payouts across YouTube, podcasts, and newsletters. Free. '
                f'<a class="btn" href="{esc(url)}" target="_blank" rel="noopener">Send me the rates</a></div>')
    f = CFG.get("submit_endpoint")
    if f:
        return (f'<div class="news"><div><b>Get 5 new brand deal receipts every week.</b><p>Actual creator payouts across YouTube, podcasts, and newsletters. One short email, free.</p></div>'
                f'<form class="nl" action="{esc(f)}" method="POST"><input type="hidden" name="_subject" value="NEWSLETTER signup - Sponsor Rate Radar">'
                '<input type="hidden" name="_captcha" value="false"><input type="text" name="_honey" style="display:none">'
                '<input type="email" name="email" required placeholder="you@email.com" aria-label="Email"> <button class="btn">Send me the rates</button></form></div>')
    return ('<div class="news"><b>Weekly rate drop coming soon:</b> 5 new brand deal receipts every week, free.</div>')

def page(title, desc, body, path, extra_head=""):
    canon = f"{BASE}{path}"
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}"><meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canon}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,400..800&family=Public+Sans:wght@400;500;600;700&display=swap" rel="stylesheet"><link rel="icon" href="{PATH}/favicon.svg" type="image/svg+xml"><meta name="theme-color" content="#f2f5f3"><link rel="stylesheet" href="{PATH}/style.css?v=3">{extra_head}</head><body>
<header><div class="hwrap"><a class="logo" href="{PATH}/"><svg width="30" height="30" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="9" fill="#1f5c47"/><circle cx="16" cy="18" r="3" fill="#f4f06a"/><path d="M9.5 13.5a9 9 0 0 1 13 0" stroke="#f4f06a" stroke-width="2.4" fill="none" stroke-linecap="round"/><path d="M6 9.8a14 14 0 0 1 20 0" stroke="#ffffff" stroke-width="2.4" fill="none" stroke-linecap="round" opacity=".6"/></svg>Sponsor Rate Radar</a><nav>
<a href="{PATH}/">Rates</a><a href="{PATH}/calculator.html">Calculator</a><a href="{PATH}/rates/">By niche</a><a href="{PATH}/guides/">Guides</a>
<a href="{PATH}/sponsor.html">Advertise</a><a class="navcta" href="{PATH}/submit.html">Share a rate</a></nav></div></header>
<main>{body}{sponsor_box()}{newsletter_box()}</main>
<footer><div class="fwrap"><div><a class="logo" href="{PATH}/">Sponsor Rate Radar</a><p>Sourced brand deal rates for creators. Every row links back to the original creator post, agency report, or reviewed submission. Reported payouts, not guarantees. Last updated {TODAY}.</p></div><div><a href="{PATH}/">Rates</a><a href="{PATH}/calculator.html">Calculator</a><a href="{PATH}/guides/">Guides</a><a href="{PATH}/about.html">Method</a><a href="{PATH}/sponsor.html">Advertise</a></div></div></footer>
<script data-goatcounter="https://sponsorrateradar.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</body></html>"""

def table(rows):
    out = ['<div class="tw"><table><thead><tr><th>Platform</th><th>Niche</th><th>Audience</th><th>Placement</th><th>Price</th><th>CPM</th><th>Year</th><th>Source</th></tr></thead><tbody>']
    for r in rows:
        cpm = f"${r['cpm_usd']:g}" if r.get("cpm_usd") else "-"
        out.append(
            f'<tr data-platform="{esc(r["platform"])}" data-niche="{esc(r["niche"])}" data-bucket="{esc(r["audience_bucket"])}" data-placement="{esc(r["placement"])}">'
            f'<td><span class="chip c-{slug(r["platform"])}">{esc(r["platform"])}</span></td><td>{esc(r["niche"])}</td><td class="aud">{esc(r["audience_size"])}</td><td>{esc(r["placement"])}</td>'
            f'<td class="p">{money(r["price_usd_low"], r["price_usd_high"])}</td><td>{cpm}</td><td>{esc(r["year"])}</td>'
            f'<td class="src"><a href="{esc(r["source_url"])}" target="_blank" rel="noopener nofollow" title="{esc(r.get("note",""))}">{esc(r["source_name"])}</a></td></tr>')
    out.append("</tbody></table></div>")
    return "".join(out)

def opts(name, vals):
    return f'<select id="f-{name}"><option value="">All {name}s</option>' + "".join(
        f'<option>{esc(v)}</option>' for v in vals) + "</select>"

def write(rel, content):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(content)

BUCKETS = ["Under 1K", "1K-10K", "10K-50K", "50K-100K", "100K-500K", "500K-1M", "1M+"]
PORD = ["YouTube", "Shorts", "Newsletter", "Podcast", "TikTok", "Instagram", "Twitch"]
rates.sort(key=lambda r: (r["placement"] == "Benchmark", PORD.index(r["platform"]) if r["platform"] in PORD else 99, -r["year"], r["niche"]))
platforms = sorted({r["platform"] for r in rates})
niches = sorted({r["niche"] for r in rates})
placements = sorted({r["placement"] for r in rates})
buckets = [b for b in BUCKETS if any(r["audience_bucket"] == b for r in rates)]

if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)
for _f in os.listdir(os.path.join(ROOT, "static")):
    shutil.copy(os.path.join(ROOT, "static", _f), os.path.join(OUT, _f))
open(os.path.join(OUT, ".nojekyll"), "w").write("")

FILTER_JS = """<script>
const fs=['platform','niche','bucket','placement'];
function f(){const q=document.getElementById('q').value.toLowerCase();let n=0;
document.querySelectorAll('tbody tr').forEach(tr=>{let ok=fs.every(k=>{const v=document.getElementById('f-'+k).value;return !v||tr.dataset[k]===v});
if(q&&!tr.innerText.toLowerCase().includes(q))ok=false;tr.style.display=ok?'':'none';if(ok)n++});
document.getElementById('cnt').textContent=n+' rates';}
fs.forEach(k=>document.getElementById('f-'+k).onchange=f);document.getElementById('q').oninput=f;f();
</script>"""

# --- Calculator: CPMs derived only from our data
cpm_data = {}
for r in rates:
    c = r.get("cpm_usd")
    if not c and r.get("avg_views"):
        c = mid(r) / r["avg_views"] * 1000
    if c:
        cpm_data.setdefault(r["platform"], []).append((r["niche"], round(c, 2)))
calc_json = json.dumps(cpm_data)

# --- Home
yt = [mid(r) for r in rates if r["platform"] == "YouTube" and r["placement"] != "Benchmark"]
selfrep = sum(1 for r in rates if r["placement"] != "Benchmark")
srcs = len({r["source_url"] for r in rates})
HERO_PLAT = [p for p in ["YouTube", "Newsletter", "Podcast", "Shorts", "TikTok", "Instagram", "Twitch"] if p in cpm_data]
HERO_WORD = {"YouTube": "YouTube videos", "Newsletter": "a newsletter", "Podcast": "a podcast", "Shorts": "YouTube Shorts", "TikTok": "TikToks", "Instagram": "Instagram posts", "Twitch": "Twitch streams"}

import glob as _g, re as _re
def _home_guides():
    items=[]
    for fp in sorted(_g.glob(os.path.join(ROOT,"content","guides","*.md"))):
        t=_re.search(r"^title:\s*(.+)$",open(fp).read(),_re.M)
        sl=os.path.basename(fp)[:-3]
        items.append(f'<li><a href="{PATH}/guides/{sl}.html">{esc(t.group(1).split(" - ")[0] if t else sl)}</a></li>')
    return '<h2>Pricing guides</h2><ul class="niches">'+"".join(items)+'</ul>'
HOME_GUIDES=_home_guides()
body = f"""<section class="hero" aria-labelledby="ht">
<h1 id="ht">Stop guessing what to charge sponsors.</h1>
<form class="say" onsubmit="return false">
<p>I make <select id="hp" aria-label="Platform">{''.join(f'<option value="{esc(p)}">{esc(HERO_WORD[p])}</option>' for p in HERO_PLAT)}</select>
about <select id="hn" aria-label="Niche"><option value="">anything</option>{''.join(f'<option value="{esc(n)}">{esc(n.lower())}</option>' for n in niches)}</select>
and average <input id="hv" type="number" inputmode="numeric" value="10000" min="100" step="100" aria-label="Views or opens per post"> <span id="hu">views</span>.</p>
</form>
<p class="ask" aria-live="polite">Typical ask: <mark id="hr">$200 to $316</mark></p>
<p class="basis" id="hb"></p>
<p class="heroalt">Want the raw receipts? Jump to <a href="#rates">all {len(rates)} sourced deals</a> below.</p>
</section>
<script>const HD={calc_json};
function hp(a,p){{a=[...a].sort((x,y)=>x-y);const i=(a.length-1)*p,l=Math.floor(i);return a[l]+(a[Math.ceil(i)]-a[l])*(i-l)}}
function hrun(){{const p=document.getElementById('hp').value,n=document.getElementById('hn').value,v=+document.getElementById('hv').value||0;
document.getElementById('hu').textContent=p==='Newsletter'?'opens':(p==='Podcast'?'downloads':'views');
let pts=(HD[p]||[]).filter(x=>!n||x[0]===n),note='';if(pts.length<3){{pts=HD[p]||[];if(n)note=' Still light on '+n.toLowerCase()+' data, so this pulls from all niches on '+p+'.';}}
const c=pts.map(x=>x[1]),f=x=>'$'+Math.round(x).toLocaleString();
document.getElementById('hr').textContent=f(hp(c,.25)*v/1000)+' to '+f(hp(c,.75)*v/1000);
document.getElementById('hb').textContent='Middle 50% of '+pts.length+' reported deals, scaled per 1,000 '+document.getElementById('hu').textContent+'.'+note;}}
['hp','hn','hv'].forEach(i=>document.getElementById(i).addEventListener('input',hrun));hrun();</script>
<h2 id="rates">All {len(rates)} reported deals</h2>
<div class="toolbar"><div class="filters"><input id="q" placeholder="Filter by niche, size, or placement (e.g. tech, 50K, dedicated)">
{opts('platform', platforms)}{opts('niche', niches)}<select id="f-bucket"><option value="">All sizes</option>{''.join(f'<option>{b}</option>' for b in buckets)}</select>{opts('placement', placements)}
<span id="cnt"></span></div></div>{table(rates)}
{HOME_GUIDES}
<p class="cta">Closed a sponsorship recently? <a href="{PATH}/submit.html">Share what you got paid anonymously</a> so the next creator doesn't lowball themselves.</p>
{FILTER_JS}"""
write("index.html", page("Sponsor Rate Radar | Real YouTube, Podcast & Newsletter Sponsorship Rates",
      f"See what sponsors actually pay creators. Browse {len(rates)} sourced brand deals by platform, niche, and audience size, or estimate your rate in seconds.", body, "/"))


body = f"""<h1>Sponsorship rate calculator</h1>
<p class="lede">Plug in your average views, opens, or downloads. We pull the 25th to 75th percentile CPM straight from our sourced deals instead of making up a multiplier.</p>
<div class="calc"><label>Platform <select id="cp">{''.join(f'<option>{esc(p)}</option>' for p in cpm_data)}</select></label>
<label>Niche <select id="cn"><option value="">Any niche</option>{''.join(f'<option>{esc(n)}</option>' for n in niches)}</select></label>
<label>Avg views per video / opens per email <input id="cv" type="number" value="10000" min="100"></label>
<div id="out" class="out"></div></div>
<p class="small">How this works: we take the CPM (price per 1,000 views or opens) from matching deals in our database and multiply the middle 50% by your average reach. If a niche has fewer than 3 entries, we widen to all niches on that platform.</p>
<script>const D={calc_json};
function pct(a,p){{a=[...a].sort((x,y)=>x-y);const i=(a.length-1)*p,l=Math.floor(i);return a[l]+(a[Math.ceil(i)]-a[l])*(i-l)}}
function run(){{const p=document.getElementById('cp').value,n=document.getElementById('cn').value,v=+document.getElementById('cv').value||0;
let pts=(D[p]||[]).filter(x=>!n||x[0]===n),note='';if(pts.length<3){{pts=D[p]||[];if(n)note=' (not enough '+n+' entries yet, using all '+p+' niches)';}}
if(!pts.length){{document.getElementById('out').innerHTML='Not enough data yet.';return}}
const c=pts.map(x=>x[1]),lo=pct(c,.25)*v/1000,hi=pct(c,.75)*v/1000,f=x=>'$'+Math.round(x).toLocaleString();
document.getElementById('out').innerHTML='<div class="big">'+f(lo)+' to '+f(hi)+'</div>per placement, from '+pts.length+' sourced deals'+note+'. Median CPM: $'+pct(c,.5).toFixed(2)+'.';}}
['cp','cn','cv'].forEach(i=>document.getElementById(i).oninput=run);run();</script>"""
write("calculator.html", page("Sponsorship Rate Calculator: Estimate What to Charge Sponsors",
      "Estimate what to charge sponsors using real creator CPM data across YouTube, newsletters, podcasts, TikTok, and Instagram.", body, "/calculator.html"))

# --- Niche pages (SEO)
def _gtitle(g):
    t = open(os.path.join(ROOT, 'content', 'guides', g + '.md')).read()
    m = re.search(r'^title:\s*(.+)$', t, re.M)
    return m.group(1).strip() if m else g
idx = ['<h1>Sponsorship rates by niche</h1><ul class="niches">']
for n in niches:
    rows = [r for r in rates if r["niche"] == n]
    s = slug(n)
    prices = [mid(r) for r in rows if r["placement"] != "Benchmark"]
    summ = f"Reported deals range from {money(min(prices), min(prices))} to {money(max(prices), max(prices))}." if prices else ""
    ng = [os.path.basename(fp)[:-3] for fp in sorted(_g.glob(os.path.join(ROOT, 'content', 'guides', '*.md'))) if slug(n) in os.path.basename(fp)]
    gl = ''.join(f'<p>Full breakdown: <a href="{PATH}/guides/{g}.html">{esc(_gtitle(g))}</a></p>' for g in ng)
    b = (f'<h1>{esc(n)} sponsorship rates</h1><p class="lede">{len(rows)} reported brand deals for {esc(n).lower()} creators. {summ} '
         f'Click any source to see where the number came from, or run your own views through the <a href="{PATH}/calculator.html">calculator</a>.</p>' + gl + table(rows))
    write(f"rates/{s}.html", page(f"{n} Sponsorship Rates for Creators ({datetime.date.today().year}) | Sponsor Rate Radar",
          f"What sponsors actually pay {n.lower()} creators: {len(rows)} sourced deals by audience size and placement.", b, f"/rates/{s}.html"))
    idx.append(f'<li><a href="{PATH}/rates/{s}.html">{esc(n)}</a> <span>{len(rows)} rates</span></li>')
idx.append("</ul>")
write("rates/index.html", page("Sponsorship Rates by Niche | Sponsor Rate Radar", "Browse sourced creator sponsorship rates by niche.", "".join(idx), "/rates/"))

# --- Submit
form = CFG.get("submit_endpoint")
fields = """<label>Platform<select name="platform" required><option>YouTube</option><option>Shorts</option><option>Newsletter</option><option>Podcast</option><option>TikTok</option><option>Instagram</option><option>Twitch</option></select></label>
<label>Niche<input name="niche" required placeholder="e.g. Tech, Gaming, Finance"></label>
<label>Audience size<input name="audience" required placeholder="e.g. 42K subs / 8K email subscribers"></label>
<label>Avg views or opens per post<input name="avg_views" type="number"></label>
<label>Placement<input name="placement" required placeholder="e.g. 60s integration, dedicated video, primary newsletter ad"></label>
<label>Price paid (USD)<input name="price" type="number" required></label>
<label>Month & year<input name="date" placeholder="e.g. Nov 2026"></label>
<label>Context (optional: sponsor category, usage rights, how they reached out)<textarea name="note"></textarea></label>
<label class="small"><input type="checkbox" required> This is a real deal I got paid for (no NDA-protected brand names included).</label>"""
if form:
    sbody = f'<form class="sub" action="{esc(form)}" method="POST"><input type="hidden" name="_subject" value="New rate submission"><input type="text" name="_honey" style="display:none">{fields}<button class="btn">Send rate anonymously</button></form>'
else:
    sbody = '<p><b>Submissions open soon.</b> Join the weekly email to hear when they go live.</p>'
write("submit.html", page("Share Your Sponsorship Rate Anonymously | Sponsor Rate Radar",
      "Help other creators price their work: anonymously share what a sponsor paid you.",
      f'<h1>Share what a sponsor paid you</h1><p class="lede">100% anonymous. Keep the brand name out of it if you signed an NDA. We review every entry before adding it and never publish your channel or name.</p>{sbody}', "/submit.html"))

# --- Sponsor page
SPFORM = (f'<form class="sub" action="{esc(form)}" method="POST"><input type="hidden" name="_subject" value="SPONSOR inquiry - Sponsor Rate Radar">'
          '<input type="text" name="_honey" style="display:none"><label>Your name<input name="name" required></label>'
          '<label>Work email<input name="email" type="email" required></label><label>Company / product<input name="company" required></label>'
          '<label>Anything we should know?<textarea name="message"></textarea></label><button class="btn">Send inquiry</button></form>') if form else '<p>Contact form coming soon.</p>'
contact = CFG.get("contact_email", "")
CHECKOUT = CFG.get("sponsor_checkout_url", "")
RESERVE = (f'<p><a class="btn" href="{esc(CHECKOUT)}" target="_blank" rel="noopener">Claim the 30-day slot (${PRICE})</a></p>'
           f'<p class="small">Instant Stripe checkout. Drop your URL and one-line pitch on the checkout screen and we will put your banner live within 24 hours.</p>') if CHECKOUT else (
           (f'<form class="sub" action="{esc(form)}" method="POST"><input type="hidden" name="_subject" value="PAID INTENT - ${PRICE} sponsor slot - Sponsor Rate Radar">'
            f'<input type="hidden" name="message" value="paid intent, ${PRICE} slot, we\'ll email a payment link"><input type="text" name="_honey" style="display:none">'
            f'<p class="small">Slot opening soon. Leave your email and we will send a payment link as soon as it opens.</p>'
            f'<label>Work email<input name="email" type="email" required></label><button class="btn">Reserve this slot (${PRICE} / 30 days)</button></form>') if form else '')
sp = f"""<h1>Advertise on Sponsor Rate Radar</h1>
<p class="lede">Creators land here right before they reply to a brand inquiry or send a rate card.
If you build tools, agencies, gear, or services for YouTubers, podcasters, and newsletter writers, this puts your product directly in front of them.</p>
<div class="card"><h2>Sitewide sponsor slot: ${PRICE} for 30 days</h2><ul>
<li>Your brand name, link, and one-line pitch on every page of the site</li><li>Featured mention in our weekly rate drop email</li>
<li>Exclusive slot: only one sponsor runs at a time</li><li>Flat 30-day run, renew only if it works for you</li></ul>
<p>Early-bird rate: lock in ${PRICE}/mo for as long as you keep the slot.</p>
{RESERVE}
<p class="small">Want to book multiple months or ask a quick question first? Send a note below.</p>
{SPFORM}</div>"""
write("sponsor.html", page("Advertise to YouTubers & Creators | Sponsor Rate Radar", f"Reach creators pricing their next brand deal. Exclusive sitewide sponsor slot, ${PRICE} for 30 days.", sp, "/sponsor.html"))

# --- About
ab = """<h1>How we collect these rates</h1><p>Sponsor Rate Radar tracks real sponsorship payouts shared publicly by creators, talent managers, and industry reports, alongside anonymous deals submitted by creators.</p><ul><li>Every public entry links directly to the original video, thread, or report.</li>
<li>Anonymous submissions are sanity-checked (payout vs. views and placement) before they go live.</li><li>Industry-wide averages are tagged as "Benchmark" so you can separate them from single creator deals.</li>
<li>Zero made-up numbers. Spot a broken link or an outdated rate? Let us know and we will fix or pull it.</li></ul>"""
write("about.html", page("How We Collect These Rates | Sponsor Rate Radar", "How Sponsor Rate Radar sources and checks creator sponsorship rates.", ab, "/about.html"))

# --- Guides (content/guides/*.md)
import sys, glob
sys.path.insert(0, ROOT)
from guides_md import parse_front, render
guides = []
for fp in sorted(glob.glob(os.path.join(ROOT, "content", "guides", "*.md"))):
    meta, md = parse_front(open(fp, encoding="utf-8").read())
    gslug = meta.get("slug") or os.path.splitext(os.path.basename(fp))[0]
    guides.append((gslug, meta, md))
for gslug, meta, md in guides:
    body, faq = render(md)
    others = "".join(f'<li><a href="{PATH}/guides/{g}.html">{esc(m.get("title", g))}</a></li>' for g, m, _ in guides if g != gslug)
    body = f'<article class="guide prose">{body}<p class="small">Updated {TODAY}. Every number links to its source.</p></article><h2>More guides</h2><ul>{others}</ul>'
    head = ""
    if faq:
        ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
        head = '<script type="application/ld+json">' + json.dumps(ld).replace("</", "<\\/") + "</script>"
    write(f"guides/{gslug}.html", page(meta.get("title", gslug) + " | Sponsor Rate Radar", meta.get("description", ""), body, f"/guides/{gslug}.html", head))

gi = '<h1>Creator sponsorship pricing guides</h1><p>Breakdowns by platform, channel size, and niche, backed by the deals in our database.</p><ul class="niches">' + "".join(
    f'<li><a href="{PATH}/guides/{g}.html">{esc(m.get("title", g))}</a><br><span class="small">{esc(m.get("description", ""))}</span></li>' for g, m, _ in guides) + "</ul>"
write("guides/index.html", page("Creator Sponsorship Pricing Guides | Sponsor Rate Radar", "Breakdowns on what to charge sponsors across YouTube, Shorts, newsletters, podcasts, TikTok, and Instagram, backed by real 2026 numbers.", gi, "/guides/"))

# --- sitemap + robots
urls = ["/", "/calculator.html", "/rates/", "/submit.html", "/sponsor.html", "/about.html"] + [f"/rates/{slug(n)}.html" for n in niches] + ["/guides/"] + [f"/guides/{g}.html" for g, _, _ in guides]
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
      "".join(f"<url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls) + "</urlset>")
write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
write("data/rates.json", json.dumps(rates, indent=1))
print(f"built {len(rates)} rates, {len(niches)} niche pages")
