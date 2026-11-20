import os
os.chdir(os.path.join(os.path.dirname(__file__), ".."))
s = open('build.py').read()
old = 'shutil.copy(os.path.join(ROOT, "static", "style.css"), os.path.join(OUT, "style.css"))'
new = 'for _f in os.listdir(os.path.join(ROOT, "static")):\n    shutil.copy(os.path.join(ROOT, "static", _f), os.path.join(OUT, _f))'
assert old in s
open('build.py', 'w').write(s.replace(old, new))
print("patched")
