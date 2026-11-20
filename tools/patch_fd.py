"""Redesign per anthropics/skills frontend-design: sentence calculator hero, pine + highlighter palette."""
import os, re
os.chdir(os.path.join(os.path.dirname(__file__), ".."))
s = open("build.py").read()
def rep(old, new, count=1):
    global s
    assert old in s, old[:90]
    s = s.replace(old, new, count)

# fonts + theme
s = re.sub(r'family=Inter:wght@[^"]*', 'family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,400..800&family=Public+Sans:wght@400;500;600;700&display=swap', s, 1)
rep('<meta name="theme-color" content="#0c0a09">', '<meta name="theme-color" content="#f2f5f3">')
rep('style.css?v=2', 'style.css?v=3')
# logo colors (header svg)
s = s.replace('fill="#0c0a09"', 'fill="#1f5c47"').replace('fill="#f97316"', 'fill="#f4f06a"').replace('stroke="#f97316"', 'stroke="#f4f06a"').replace('stroke="#fdba74"', 'stroke="#ffffff"')

# drop arrows in sponsor box
rep('<a href="{PATH}/sponsor.html">Advertise here →</a>', '<a href="{PATH}/sponsor.html">Advertise here</a>')

# move CPM computation above home so the hero can use it
calc_start = s.index("# --- Calculator: CPMs derived only from our data")
calc_end = s.index("calc_json = json.dumps(cpm_data)") + len("calc_json = json.dumps(cpm_data)")
calc_block = s[calc_start:calc_end]
s = s[:calc_start] + s[calc_end:]
rep("# --- Home\n", calc_block + "\n\n# --- Home\n")

# hero: sentence calculator
hero_old_start = s.index('body = f"""<section class="hero">')
hero_old_end = s.index('<h2 id="rates">Browse every rate</h2>')
hero = '''HERO_PLAT = [p for p in ["YouTube", "Newsletter", "Podcast", "Shorts", "TikTok", "Instagram", "Twitch"] if p in cpm_data]
HERO_WORD = {"YouTube": "YouTube videos", "Newsletter": "a newsletter", "Podcast": "a podcast", "Shorts": "YouTube Shorts", "TikTok": "TikToks", "Instagram": "Instagram posts", "Twitch": "Twitch streams"}
body = f"""<section class="hero" aria-labelledby="ht">
<h1 id="ht">What should you charge a sponsor?</h1>
<form class="say" onsubmit="return false">
<p>I make <select id="hp" aria-label="Platform">{''.join(f'<option value="{esc(p)}">{esc(HERO_WORD[p])}</option>' for p in HERO_PLAT)}</select>
about <select id="hn" aria-label="Niche"><option value="">anything</option>{''.join(f'<option value="{esc(n)}">{esc(n.lower())}</option>' for n in niches)}</select>
and each one gets about <input id="hv" type="number" inputmode="numeric" value="10000" min="100" step="100" aria-label="Views or opens per post"> <span id="hu">views</span>.</p>
</form>
<p class="ask" aria-live="polite">Ask for <mark id="hr">$200 to $316</mark></p>
<p class="basis" id="hb"></p>
<p class="heroalt">Or skip the estimate and <a href="#rates">read {len(rates)} real deals</a>, each linked to where it was published.</p>
</section>
<script>const HD={calc_json};
function hp(a,p){{a=[...a].sort((x,y)=>x-y);const i=(a.length-1)*p,l=Math.floor(i);return a[l]+(a[Math.ceil(i)]-a[l])*(i-l)}}
function hrun(){{const p=document.getElementById('hp').value,n=document.getElementById('hn').value,v=+document.getElementById('hv').value||0;
document.getElementById('hu').textContent=p==='Newsletter'?'opens':(p==='Podcast'?'downloads':'views');
let pts=(HD[p]||[]).filter(x=>!n||x[0]===n),note='';if(pts.length<3){{pts=HD[p]||[];if(n)note=' We only have a few '+n.toLowerCase()+' deals so far, so this uses every niche.';}}
const c=pts.map(x=>x[1]),f=x=>'$'+Math.round(x).toLocaleString();
document.getElementById('hr').textContent=f(hp(c,.25)*v/1000)+' to '+f(hp(c,.75)*v/1000);
document.getElementById('hb').textContent='The middle half of '+pts.length+' sourced deals, priced per 1,000 '+document.getElementById('hu').textContent+'.'+note;}}
['hp','hn','hv'].forEach(i=>document.getElementById(i).addEventListener('input',hrun));hrun();</script>
'''
s = s[:hero_old_start] + hero + s[hero_old_end:]
rep('<h2 id="rates">Browse every rate</h2>', '<h2 id="rates">Every deal we have found</h2>')
rep(' – ', ' to ') if " – '+" in s else None
open("build.py", "w").write(s)

fav = open("static/favicon.svg").read()
fav = fav.replace('#0c0a09', '#1f5c47').replace('#f97316', '#f4f06a').replace('#fdba74', '#ffffff')
open("static/favicon.svg", "w").write(fav)
print("patched")
