import os
os.chdir(os.path.join(os.path.dirname(__file__), ".."))
s = open("build.py").read()
def rep(old, new):
    global s
    assert old in s, old[:80]
    s = s.replace(old, new, 1)
rep('rates.sort(key=lambda r: (-r["year"], r["platform"], r["niche"]))',
    'PORD = ["YouTube", "Shorts", "Newsletter", "Podcast", "TikTok", "Instagram", "Twitch"]\n'
    'rates.sort(key=lambda r: (r["placement"] == "Benchmark", PORD.index(r["platform"]) if r["platform"] in PORD else 99, -r["year"], r["niche"]))')
rep('<main>{sponsor_box()}{body}{newsletter_box()}</main>', '<main>{body}{sponsor_box()}{newsletter_box()}</main>')
open("build.py", "w").write(s)
c = open("static/style.css").read()
c = c.replace(".sponsor{display:flex;gap:10px;align-items:center;justify-content:center;font-size:13.5px;color:var(--muted);padding:9px 14px;margin:0 0 22px;",
              ".sponsor{display:flex;gap:10px;align-items:center;justify-content:center;flex-wrap:wrap;font-size:14px;color:var(--muted);padding:14px 18px;margin:40px 0 0;")
open("static/style.css", "w").write(c)
print("ok")
