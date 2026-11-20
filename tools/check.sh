#!/bin/bash
B=https://verkieverkie-prog.github.io/sponsorrateradar
for p in "" calculator.html rates/ submit.html sponsor.html sitemap.xml; do
  curl -s -o /dev/null -w "/$p %{http_code}\n" "$B/$p"
done
curl -s "$B/" | grep -c "NEWSLETTER"
