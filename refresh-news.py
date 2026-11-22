"""Add dated publisher headlines to the Pages feed. Preserve editor-written lessons."""
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
import json
from pathlib import Path
from urllib.request import Request, urlopen
from xml.etree import ElementTree

feeds = [
    ("en", "The Indian Express", "https://indianexpress.com/section/india/feed/"),
    ("en", "BBC News", "https://feeds.bbci.co.uk/news/world/asia/india/rss.xml"),
    ("ta", "BBC தமிழ்", "https://feeds.bbci.co.uk/tamil/rss.xml"),
]
path = Path("current-affairs.json")
data = json.loads(path.read_text(encoding="utf-8"))
items = {item["url"]: item for item in data.get("dailyNews", [])}
now = datetime.now(timezone.utc)
for language, publisher, url in feeds:
    try:
        with urlopen(Request(url, headers={"User-Agent": "NoolNest daily reader/1.0"}), timeout=20) as response:
            root = ElementTree.fromstring(response.read(4_000_000))
        for item in root.findall(".//item"):
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            try:
                date = parsedate_to_datetime(item.findtext("pubDate") or "")
            except (TypeError, ValueError):
                continue
            if not title or not link.startswith("https://") or not now - timedelta(days=10) <= date <= now:
                continue
            items[link] = dict(title=title, url=link, published=int(date.timestamp()*1000),
                               language=language, publisher=publisher)
    except Exception as error:
        print(f"{publisher}: {error}")
if not items:
    raise SystemExit("No dated headlines available")
data["dailyNews"] = sorted(items.values(), key=lambda item: item["published"], reverse=True)[:240]
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
