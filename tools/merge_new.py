import json
a = json.load(open('data/rates.json'))
b = json.load(open('data/new_rates.json'))
keys = set(a[0].keys())
seen = {(r['source_url'], r['placement'], r['audience_size']) for r in a}
added = 0
bad = 0
for r in b:
    if set(r.keys()) != keys or not r.get('source_url', '').startswith('http'):
        bad += 1
        continue
    lo, hi = r.get('price_usd_low'), r.get('price_usd_high')
    if lo is None and hi is None and r.get('cpm_usd') is None:
        bad += 1
        continue
    k = (r['source_url'], r['placement'], r['audience_size'])
    if k in seen:
        continue
    seen.add(k)
    a.append(r)
    added += 1
json.dump(a, open('data/rates.json', 'w'), indent=1, ensure_ascii=False)
print('added', added, 'bad', bad, 'total', len(a))
