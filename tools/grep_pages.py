import re, html, sys, urllib.request
pat = sys.argv[1]
for u in sys.argv[2:]:
    print("====", u)
    try:
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        t = urllib.request.urlopen(req, timeout=30).read().decode("utf8", "ignore")
    except Exception as e:
        print("ERR", e); continue
    t = re.sub(r'<script.*?</script>|<style.*?</style>', '', t, flags=re.S)
    t = re.sub(r'</t[dh]>', ' | ', t)
    t = re.sub(r'</tr>|</p>|</li>|<br\s*/?>|</h\d>', '\n', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = html.unescape(t)
    for l in t.split('\n'):
        l = l.strip()
        if re.search(pat, l, re.I) and '$' in l:
            print('-', l[:400])
