import os
os.chdir(os.path.join(os.path.dirname(__file__), ".."))
s = open("build.py").read()

def rep(old, new):
    global s
    assert old in s, old[:80]
    s = s.replace(old, new, 1)

LOGO = ('<svg width="30" height="30" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="9" fill="#0c0a09"/>'
        '<circle cx="16" cy="18" r="3" fill="#f97316"/><path d="M9.5 13.5a9 9 0 0 1 13 0" stroke="#f97316" stroke-width="2.4" fill="none" stroke-linecap="round"/>'
        '<path d="M6 9.8a14 14 0 0 1 20 0" stroke="#fdba74" stroke-width="2.4" fill="none" stroke-linecap="round" opacity=".6"/></svg>')

# head: font + favicon
rep('<link rel="stylesheet" href="{PATH}/style.css">',
    '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">'
    '<link rel="icon" href="{PATH}/favicon.svg" type="image/svg+xml"><meta name="theme-color" content="#0c0a09">'
    '<link rel="stylesheet" href="{PATH}/style.css?v=2">')

# header
rep('<header><a class="logo" href="{PATH}/">📡 Sponsor Rate Radar</a><nav>\n<a href="{PATH}/">Rates</a>',
    '<header><div class="hwrap"><a class="logo" href="{PATH}/">' + LOGO.replace("{", "{{").replace("}", "}}") + 'Sponsor Rate Radar</a><nav>\n<a href="{PATH}/">Rates</a>')
rep('<a href="{PATH}/submit.html">Share a rate</a><a href="{PATH}/sponsor.html">Sponsor</a></nav></header>',
    '<a href="{PATH}/sponsor.html">Advertise</a><a class="navcta" href="{PATH}/submit.html">Share a rate</a></nav></div></header>')

# footer
rep('<footer>Every number links to its public source or came from a creator submission we reviewed. Rates are what was reported, not guarantees.\nUpdated {TODAY}. · <a href="{PATH}/about.html">About &amp; method</a></footer>',
    '<footer><div class="fwrap"><div><a class="logo" href="{PATH}/">Sponsor Rate Radar</a><p>Real sponsorship rates for creators. Every number links to its public source or a reviewed creator submission. Rates are what was reported, not guarantees. Updated {TODAY}.</p></div>'
    '<div><a href="{PATH}/">Rates</a><a href="{PATH}/calculator.html">Calculator</a><a href="{PATH}/guides/">Guides</a><a href="{PATH}/about.html">Method</a><a href="{PATH}/sponsor.html">Advertise</a></div></div></footer>')

# sponsor strip
rep('''return f'<div class="sponsor empty">This spot is open. <a href="{PATH}/sponsor.html">Sponsor Sponsor Rate Radar →</a></div>\'''',
    '''return f'<div class="sponsor empty"><span class="tag">Sponsor</span> Reach thousands of creators who are pricing deals right now. <a href="{PATH}/sponsor.html">Advertise here →</a></div>\'''')

# newsletter
rep('''f'<div class="news"><b>Get 5 new real sponsor rates every week.</b> Free, one email, no fluff.'
                f'<form''', '''f'<div class="news"><div><b>5 new real sponsor rates, every week.</b><p>One short email. Real deals, real numbers, no fluff. Free.</p></div>'
                f'<form''')

# table chips
rep('''f'<td>{esc(r["platform"])}</td><td>{esc(r["niche"])}</td><td>{esc(r["audience_size"])}</td>''',
    '''f'<td><span class="chip c-{slug(r["platform"])}">{esc(r["platform"])}</span></td><td>{esc(r["niche"])}</td><td class="aud">{esc(r["audience_size"])}</td>''')
rep('''f'<td><a href="{esc(r["source_url"])}"''', '''f'<td class="src"><a href="{esc(r["source_url"])}"''')

# home hero
rep('''body = f"""<h1>What do sponsors actually pay creators?</h1>
<p class="lede">{len(rates)} real sponsorship rates for YouTube, Shorts, newsletters and podcasts, each linked to where it was published.
Filter by niche and audience size, or use the <a href="{PATH}/calculator.html">rate calculator</a>.</p>
<div class="filters">''',
'''selfrep = sum(1 for r in rates if r["placement"] != "Benchmark")
srcs = len({r["source_url"] for r in rates})
body = f"""<section class="hero"><span class="eyebrow"><i></i>Updated {TODAY} · {len(rates)} sourced rates</span>
<h1>Know what sponsors <em>actually pay</em> before you quote.</h1>
<p class="lede">Real sponsorship rates for YouTube, Shorts, newsletters, podcasts, TikTok, Instagram and Twitch. Every number links to where it was published.</p>
<div class="heroctas"><a class="btn" href="{PATH}/calculator.html">Calculate my rate →</a><a class="btn ghost" href="#rates">Browse all rates</a></div>
<div class="stats"><div class="stat"><b>{len(rates)}</b><span>sourced rates</span></div><div class="stat"><b>{len(platforms)}</b><span>platforms</span></div>
<div class="stat"><b>{len(niches)}</b><span>niches</span></div><div class="stat"><b>{srcs}</b><span>public sources</span></div></div></section>
<h2 id="rates">Browse every rate</h2>
<div class="toolbar"><div class="filters">''')
rep('''<span id="cnt"></span></div>{table(rates)}''', '''<span id="cnt"></span></div></div>{table(rates)}''')

# guide prose
rep('<article class="guide">', '<article class="guide prose">')

open("build.py", "w").write(s)
open("static/favicon.svg", "w").write(LOGO.replace(' aria-hidden="true"', ' xmlns="http://www.w3.org/2000/svg"'))
print("patched")
