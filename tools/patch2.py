import os
os.chdir(os.path.join(os.path.dirname(__file__), ".."))
s = open('build.py').read()
old = """    return ('<div class="news"><b>Weekly rate drop coming soon:</b> 5 new real sponsor rates every week, free.</div>')"""
new = """    f = CFG.get("submit_endpoint")
    if f:
        return (f'<div class="news"><b>Get 5 new real sponsor rates every week.</b> Free, one email, no fluff.'
                f'<form class="nl" action="{esc(f)}" method="POST"><input type="hidden" name="_subject" value="NEWSLETTER signup - Sponsor Rate Radar">'
                '<input type="hidden" name="_captcha" value="false"><input type="text" name="_honey" style="display:none">'
                '<input type="email" name="email" required placeholder="you@email.com" aria-label="Email"> <button class="btn">Join free</button></form></div>')
    return ('<div class="news"><b>Weekly rate drop coming soon:</b> 5 new real sponsor rates every week, free.</div>')"""
assert old in s
s = s.replace(old, new)
open('build.py', 'w').write(s)
css = open('static/style.css').read()
if '.nl{' not in css:
    css += "\n.nl{display:flex;gap:8px;flex-wrap:wrap;margin-top:8px}.nl input{flex:1;min-width:200px;padding:10px;border:1px solid #ccc;border-radius:8px;font-size:16px}\n"
    open('static/style.css', 'w').write(css)
print("patched")
