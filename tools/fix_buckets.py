import json
a = json.load(open('data/rates.json'))
for r in a:
    if r['audience_bucket'] != '<10K':
        continue
    s = r['audience_size']
    if s.startswith('per 1,000'):
        r['audience_bucket'] = 'Under 1K'
    elif s == 'Under 5,000 subscribers':
        r['audience_bucket'] = '1K-10K'
    else:
        r['audience_bucket'] = '1K-10K'
json.dump(a, open('data/rates.json', 'w'), indent=1, ensure_ascii=False)
src = open('build.py').read()
src = src.replace('BUCKETS = ["<10K", "10K-50K"', 'BUCKETS = ["Under 1K", "1K-10K", "10K-50K"')
src = src.replace('<option>TikTok</option><option>Instagram</option></select>', '<option>TikTok</option><option>Instagram</option><option>Twitch</option></select>')
open('build.py', 'w').write(src)
print('ok')
