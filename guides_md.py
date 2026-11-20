"""Tiny dependency-free markdown renderer for the guides (headings, lists, tables, code, quotes, links, bold/italic)."""
import html, re


def inline(t):
    t = html.escape(t, quote=False)
    codes = []
    t = re.sub(r"`([^`]+)`", lambda m: codes.append(m.group(1)) or f"\x00{len(codes)-1}\x00", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: f'<a href="{m.group(2)}"' + (' rel="noopener" target="_blank"' if m.group(2).startswith("http") else "") + f">{m.group(1)}</a>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*([^*\s][^*]*?)\*(?!\w)", r"<i>\1</i>", t)
    t = re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{codes[int(m.group(1))]}</code>", t)
    return t


def parse_front(text):
    meta = {}
    if text.startswith("---"):
        _, fm, text = text.split("---", 2)
        for line in fm.strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
    return meta, text.strip()


def render(md):
    lines = md.splitlines()
    out, i, n = [], 0, len(lines)
    faq = []
    in_faq = False
    while i < n:
        l = lines[i]
        s = l.strip()
        if not s:
            i += 1; continue
        if s.startswith("```"):
            j = i + 1; buf = []
            while j < n and not lines[j].strip().startswith("```"):
                buf.append(lines[j]); j += 1
            out.append("<pre><code>" + html.escape("\n".join(buf)) + "</code></pre>")
            i = j + 1; continue
        m = re.match(r"(#{1,4})\s+(.*)", s)
        if m:
            lv = len(m.group(1)); txt = m.group(2)
            if lv == 2:
                in_faq = txt.strip().lower() == "faq"
            if in_faq and lv == 3:
                faq.append([txt, []])
            out.append(f'<h{lv} id="{re.sub(r"[^a-z0-9]+", "-", txt.lower()).strip("-")}">{inline(txt)}</h{lv}>')
            i += 1; continue
        if s.startswith("|"):
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            h = "".join(f"<th>{inline(c)}</th>" for c in rows[0])
            b = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
            out.append(f'<div class="tw"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>')
            continue
        if re.match(r"[-*]\s+", s) or re.match(r"\d+\.\s+", s):
            ordered = bool(re.match(r"\d+\.\s+", s))
            pat = r"\d+\.\s+" if ordered else r"[-*]\s+"
            items = []
            while i < n and re.match(pat, lines[i].strip()):
                items.append(re.sub(pat, "", lines[i].strip(), count=1)); i += 1
                while i < n and lines[i].startswith("   ") and lines[i].strip():
                    items[-1] += " " + lines[i].strip(); i += 1
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>")
            continue
        if s.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip()); i += 1
            out.append(f"<blockquote>{inline(' '.join(buf))}</blockquote>")
            continue
        buf = []
        while i < n and lines[i].strip() and not re.match(r"(#{1,4}\s|\||```|[-*]\s|\d+\.\s|>)", lines[i].strip()):
            buf.append(lines[i].strip()); i += 1
        para = " ".join(buf)
        if in_faq and faq:
            faq[-1][1].append(para)
        out.append(f"<p>{inline(para)}</p>")
    plain = lambda t: re.sub(r"\*+", "", re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t))
    return "\n".join(out), [(plain(q), plain(" ".join(a))) for q, a in faq]
