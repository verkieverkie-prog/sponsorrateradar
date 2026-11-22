p = 'content/guides/youtube-sponsorship-rates-1000-subscribers.md'
s = open(p).read()
old = "Those are US-audience numbers."
if 'finance-youtuber-sponsorship-rates' not in s:
    assert old in s
    s = s.replace(old, "Finance pays the most at every size. See [how much finance YouTubers charge](/sponsorrateradar/guides/finance-youtuber-sponsorship-rates.html) for bigger channels too.\n\n" + old, 1)
    open(p, 'w').write(s)
print('ok')
