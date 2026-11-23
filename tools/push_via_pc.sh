#!/bin/bash
# Push local commits ahead of origin/main through Rocky's PC (gh auth there).
set -e
cd ~/sponsorrateradar
git fetch -q origin 2>/dev/null || true
rm -f /tmp/srr.patch
git format-patch origin/main --stdout > /tmp/srr.patch
echo "patch bytes: $(wc -c < /tmp/srr.patch)"
gzip -c /tmp/srr.patch | base64 -w0 > /tmp/srr.patch.b64
D=/mnt/windows/aios-run/side-hustle-ceo/push-$(date +%s)
ssh pc "mkdir -p $D && base64 -d > $D/p.gz" < /tmp/srr.patch.b64
ssh pc "set -e; cd $D && gunzip p.gz && git clone -q https://github.com/verkieverkie-prog/sponsorrateradar.git repo && cd repo && git -c user.name='Sponsor Rate Radar' -c user.email=sponsorrateradar@proton.me am -q ../p && git push -q origin main && git log --oneline -1; cd / && rm -rf $D"
