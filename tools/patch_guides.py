import os
p = os.path.join(os.path.dirname(__file__), "..", "build.py")
s = open(p).read()
assert "guides_md" not in s
s = s.replace('<a href="{PATH}/rates/">By niche</a>\n', '<a href="{PATH}/rates/">By niche</a><a href="{PATH}/guides/">Guides</a>\n', 1)
block = r'''
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
    body = f'<article class="guide">{body}<p class="small">Updated {TODAY}. Numbers link to their sources.</p></article><h2>More guides</h2><ul>{others}</ul>'
    head = ""
    if faq:
        ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
        head = '<script type="application/ld+json">' + json.dumps(ld).replace("</", "<\\/") + "</script>"
    write(f"guides/{gslug}.html", page(meta.get("title", gslug) + " | Sponsor Rate Radar", meta.get("description", ""), body, f"/guides/{gslug}.html", head))
gi = '<h1>Sponsorship rate guides</h1><p>Plain answers with real, sourced numbers.</p><ul class="niches">' + "".join(
    f'<li><a href="{PATH}/guides/{g}.html">{esc(m.get("title", g))}</a><br><span class="small">{esc(m.get("description", ""))}</span></li>' for g, m, _ in guides) + "</ul>"
write("guides/index.html", page("Sponsorship Rate Guides | Sponsor Rate Radar", "Guides on what to charge sponsors on YouTube, Shorts, newsletters and podcasts, with sourced 2026 numbers.", gi, "/guides/"))

# --- sitemap + robots'''
s = s.replace("\n# --- sitemap + robots", block, 1)
s = s.replace('[f"/rates/{slug(n)}.html" for n in niches]', '[f"/rates/{slug(n)}.html" for n in niches] + ["/guides/"] + [f"/guides/{g}.html" for g, _, _ in guides]', 1)
open(p, "w").write(s)
print("ok")
