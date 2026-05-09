from collections.abc import Iterable, Mapping
from datetime import datetime, timezone
from email import utils
import re

import models

CLEAN_HTML: re.Pattern = re.compile('<.*?>')
EXTRA_SPACE: re.Pattern = re.compile('\\s+')

def generate_stream(title: str, link: str, desc: str, items: Iterable[models.DevlogEntry], lang: str = "en-au"):
    now: datetime = datetime.now(tz=timezone.utc)
    rfc_2822: str = utils.format_datetime(now)
    feed: str = '<?xml version="1.0" encoding="UTF-8" ?><rss version="2.0"><channel>'
    feed += f"<title>{title}</title>"
    feed += f"<link>{link}</link>"
    feed += f"<description>{desc}</description>"
    feed += f"<language>{lang}</language>"
    feed += f"<lastBuildDate>{rfc_2822}</lastBuildDate>"

    for item in items:
        full_guid: str = link + "#" + item.guid
        # Clean HTML and spaces
        content: str = re.sub(CLEAN_HTML, ' ', item.content)
        content = re.sub(EXTRA_SPACE, ' ', content)
        # Format date
        rfc_2822: str = utils.format_datetime(item.published)
        feed += "<item>"
        feed += f"<title>{item.title}</title>"
        feed += f"<link>{link}</link>"
        feed += f"<description>{content}</description>"
        feed += f"<pubDate>{rfc_2822}</pubDate>"
        feed += f"<guid>{full_guid}</guid>"
        feed += "</item>"

    feed += """</channel></rss>"""
    return feed
