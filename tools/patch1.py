import json, os
os.chdir(os.path.join(os.path.dirname(__file__), ".."))
c = json.load(open('config.json'))
c['submit_endpoint'] = 'https://formsubmit.co/46f8cb0f98199303d7b674b1dd482e14'
json.dump(c, open('config.json', 'w'), indent=1)
s = open('build.py').read()
old = """{f'<a class="btn" href="mailto:{esc(contact)}?subject=Sponsor%20Rate%20Radar%20sponsorship">Get in touch</a>' if contact else '<p>Contact form coming soon.</p>'}</div>\"\"\""""
new = """{SPFORM}</div>\"\"\""""
assert old in s
s = s.replace(old, new)
s = s.replace("# --- Sponsor page\n", """# --- Sponsor page
SPFORM = (f'<form class="sub" action="{esc(form)}" method="POST"><input type="hidden" name="_subject" value="SPONSOR inquiry - Sponsor Rate Radar">'
          '<input type="text" name="_honey" style="display:none"><label>Your name<input name="name" required></label>'
          '<label>Work email<input name="email" type="email" required></label><label>Company / product<input name="company" required></label>'
          '<label>Anything we should know?<textarea name="message"></textarea></label><button class="btn">Get in touch</button></form>') if form else '<p>Contact form coming soon.</p>'
""")
open('build.py', 'w').write(s)
print("patched")
