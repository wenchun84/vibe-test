#!/usr/bin/env python3
"""Fetch latest headlines from 7 Taiwanese news sources -> news.json (rows)."""
import html, json, re, sys, urllib.request, email.utils
from datetime import datetime, timedelta, timezone

TW = timezone(timedelta(hours=8))
NOW = datetime.now(TW)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
LIMIT = 25


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "zh-TW"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            import gzip
            data = gzip.decompress(data)
    return data.decode("utf-8", "ignore")


def clean(t):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", t or ""))).strip()


def iso(dt):
    return dt.astimezone(TW).strftime("%Y-%m-%dT%H:%M:%S+08:00") if dt else None


def row(source, title, url, dt, category=""):
    return {"source": source, "title": clean(title), "url": url, "published": iso(dt), "category": clean(category)}


def ettoday():
    s = get("https://feeds.feedburner.com/ettoday/realtime")
    out = []
    for it in re.findall(r"<item>(.*?)</item>", s, re.S):
        t = re.search(r"<title>\s*<!\[CDATA\[(.*?)\]\]>", it, re.S)
        l = re.search(r"<link>\s*<!\[CDATA\[(.*?)\]\]>", it, re.S)
        d = re.search(r"<pubDate>(.*?)</pubDate>", it, re.S)
        dt = None
        if d:
            try:
                dt = datetime.strptime(re.sub(r"\s+", " ", d.group(1).replace(",", ", ")).strip(), "%a, %d %b %Y %H:%M:%S %z")
            except ValueError:
                dt = email.utils.parsedate_to_datetime(d.group(1))
        host = re.match(r"https?://([a-z]+)\.ettoday", l.group(1)) if l else None
        cat = {"sports": "運動", "star": "影劇", "travel": "旅遊", "health": "健康", "game": "遊戲", "pets": "寵物", "speed": "車", "house": "房產", "finance": "財經"}.get(host.group(1) if host else "", "")
        if t and l:
            out.append(row("ETtoday", t.group(1), l.group(1).strip(), dt, cat))
    return out


def udn_break():
    out = []
    for page in (1, 2):
        d = json.loads(get(f"https://udn.com/api/more?page={page}&id=&channelId=1&cate_id=99&type=breaknews"))
        for it in d.get("lists", []):
            dt = datetime.strptime(it["time"]["date"], "%Y-%m-%d %H:%M").replace(tzinfo=TW)
            url = "https://udn.com" + it["titleLink"].split("?")[0]
            out.append(row("聯合新聞網即時", it["title"], url, dt, it.get("cate_title") or it.get("category") or ""))
    return out


def udn_index():
    s = get("https://udn.com/news/index")
    out, seen = [], set()
    for m in re.finditer(r'<a\s[^>]*href="((?:https://udn\.com)?/news/story/\d+/\d+)[^"]*"[^>]*>', s):
        tag = m.group(0)
        title = re.search(r'title="([^"]+)"', tag)
        if not title:
            continue
        url = m.group(1) if m.group(1).startswith("http") else "https://udn.com" + m.group(1)
        if url in seen:
            continue
        seen.add(url)
        lst = re.search(r'data-story_list="list_([^"]*)"', tag)
        tm = re.search(r'<time[^>]*>\s*([^<]+?)\s*</time>', s[m.end():m.end() + 1500].split('story-list__news', 1)[0])
        dt = None
        if tm:
            v = tm.group(1)
            full = re.match(r"(\d{4})-(\d{2})-(\d{2}) (\d{1,2}):(\d{2})", v)
            hm = re.match(r"(\d{1,2}):(\d{2})$", v)
            if full:
                dt = datetime(*map(int, full.groups()), tzinfo=TW)
            elif hm:
                dt = NOW.replace(hour=int(hm.group(1)), minute=int(hm.group(2)), second=0, microsecond=0)
                if dt > NOW + timedelta(minutes=5):
                    dt -= timedelta(days=1)
        out.append(row("聯合新聞", title.group(1), url, dt, lst.group(1) if lst else ""))
    return out


def line_today():
    s = get("https://today.line.me/tw/v3/tab")
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', s, re.S)
    data = json.loads(m.group(1))
    found, seen = [], set()

    def walk(o):
        if isinstance(o, dict):
            if "title" in o and "publisher" in o and isinstance(o.get("url"), dict) and o["url"].get("hash"):
                h = o["url"]["hash"]
                if h not in seen and o.get("contentType", "GENERAL") == "GENERAL":
                    seen.add(h)
                    ts = o.get("publishTimeUnix")
                    dt = datetime.fromtimestamp(ts / 1000, TW) if ts else None
                    found.append(row("LINE TODAY", o["title"], f"https://today.line.me/tw/v3/article/{h}", dt, o.get("publisher", "")))
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(data)
    return found


def setn():
    s = get("https://www.setn.com/ViewAll.aspx")
    out = []
    for blk in re.findall(r'<div class="news_list_item[^"]*">(.*?)<div class="time">(.*?)</div>', s, re.S):
        body, rel = blk
        t = re.search(r'title_pc"><a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', body, re.S)
        c = re.search(r'class="tab smart-link"[^>]*>(.*?)</a>', body, re.S)
        if not t:
            continue
        url = t.group(1)
        if url.startswith("/"):
            url = "https://www.setn.com" + url
        out.append(row("三立新聞網", t.group(2), url, rel_time(clean(rel)), c.group(1) if c else ""))
    return out


def rel_time(txt):
    m = re.match(r"(\d+)\s*(分鐘|小時|天)前", txt)
    if m:
        n = int(m.group(1))
        return NOW - {"分鐘": timedelta(minutes=n), "小時": timedelta(hours=n), "天": timedelta(days=n)}[m.group(2)]
    if "剛剛" in txt:
        return NOW
    m = re.match(r"(\d{4})/(\d{1,2})/(\d{1,2})\s+(\d{1,2}):(\d{2})", txt)
    if m:
        return datetime(*map(int, m.groups()), tzinfo=TW)
    return None


def astro(v):
    """Decode Astro's serialized props ([type, value])."""
    if isinstance(v, list) and len(v) == 2 and isinstance(v[0], int):
        t, x = v
        if t == 0:
            return {k: astro(y) for k, y in x.items()} if isinstance(x, dict) else x
        if t == 1:
            return [astro(y) for y in x]
        return x
    if isinstance(v, dict):
        return {k: astro(y) for k, y in v.items()}
    return v


def tvbs():
    s = get("https://news.tvbs.com.tw/realtime")
    m = re.search(r'component-url="[^"]*RealTimeListArticles[^"]*"[^>]*props="([^"]+)"', s)
    props = astro(json.loads(html.unescape(m.group(1))))
    arts = props["initialArticles"]["data"]
    return [row("TVBS 新聞", a["title"], a["articleUrl"], datetime.fromtimestamp(a["publishedAt"], TW), a.get("categoryName", "")) for a in arts]


def chinatimes():
    s = get("https://www.chinatimes.com/realtimenews/?chdtv")
    out = []
    for blk in re.findall(r'<h3 class="title">(.*?)<p class="intro">', s, re.S):
        a = re.search(r'<a href="([^"]+)">(.*?)</a>', blk, re.S)
        d = re.search(r'<time datetime="([^"]+)"', blk)
        c = re.search(r'class="category"><a[^>]*>(.*?)</a>', blk, re.S)
        if a:
            dt = datetime.strptime(d.group(1), "%Y-%m-%d %H:%M").replace(tzinfo=TW) if d else None
            out.append(row("中時新聞網", a.group(2), "https://www.chinatimes.com" + a.group(1).split("?")[0] + "?chdtv", dt, c.group(1) if c else ""))
    return out


SOURCES = [ettoday, udn_index, udn_break, line_today, setn, tvbs, chinatimes]

if __name__ == "__main__":
    rows, status = [], []
    for fn in SOURCES:
        try:
            r = fn()
            r = sorted(r, key=lambda x: x["published"] or "", reverse=True) if fn is not udn_index and fn is not line_today else r
            rows += r[:LIMIT]
            status.append(f"{fn.__name__}: {len(r)}")
        except Exception as e:  # keep the other sources
            status.append(f"{fn.__name__}: FAILED {type(e).__name__}: {e}")
    fetched = iso(datetime.now(TW))
    for r in rows:
        r["fetched"] = fetched
    out = sys.argv[1] if len(sys.argv) > 1 else "news.json"
    json.dump(rows, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print("\n".join(status), file=sys.stderr)
    print(f"{len(rows)} rows -> {out}", file=sys.stderr)
