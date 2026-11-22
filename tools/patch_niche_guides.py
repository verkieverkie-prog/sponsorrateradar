p = 'build.py'
s = open(p).read()
old = "    b = (f'<h1>{esc(n)} sponsorship rates</h1>"
new = ("    ng = [os.path.basename(fp)[:-3] for fp in sorted(_g.glob(os.path.join(ROOT, 'content', 'guides', '*.md'))) if slug(n) in os.path.basename(fp)]\n"
       "    gl = ''.join(f'<p>Read the guide: <a href=\"{PATH}/guides/{g}.html\">{esc(_gtitle(g))}</a></p>' for g in ng)\n"
       + old)
assert old in s and '_gtitle' not in s
s = s.replace(old, new, 1)
old2 = "Try the <a href=\"{PATH}/calculator.html\">calculator</a> for your own numbers.</p>' + table(rows))"
assert old2 in s
s = s.replace(old2, "Try the <a href=\"{PATH}/calculator.html\">calculator</a> for your own numbers.</p>' + gl + table(rows))", 1)
helper = ("def _gtitle(g):\n"
          "    t = open(os.path.join(ROOT, 'content', 'guides', g + '.md')).read()\n"
          "    m = re.search(r'^title:\\s*(.+)$', t, re.M)\n"
          "    return m.group(1).strip() if m else g\n")
anchor = "idx = ['<h1>Sponsorship rates by niche</h1>"
s = s.replace(anchor, helper + anchor, 1)
open(p, 'w').write(s)
print('patched')
