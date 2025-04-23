import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone


def generate_rss_feed(channel_info, items, output_file="feed.xml"):
    """
    生成RSS XML文件
    """
    # 创建根元素<rss>，并设置版本属性
    rss = ET.Element(
        "rss",
        {
            "version": "2.0",
            "xmlns:atom": "http://www.w3.org/2005/Atom",
            "xmlns:dc": "http://purl.org/dc/elements/1.1/",
        },
    )

    channel = ET.SubElement(rss, "channel")
    for key, value in channel_info.items():
        if key == "atom:link":
            atom_link = ET.SubElement(channel, "atom:link")
            for attr_key, attr_value in value.items():
                atom_link.set(attr_key, attr_value)
        else:
            ET.SubElement(channel, key).text = value
    for item in items:
        item_elem = ET.SubElement(channel, "item")
        for key, value in item.items():
            ET.SubElement(item_elem, key).text = value
    tree = ET.ElementTree(rss)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)


# 频道信息
channel_info = {
    "title": "哔哩哔哩开屏插画集锦",
    "description": "每日更新哔哩哔哩开屏插画",
    "link": "https://bilibili.yangz.site",
    "atom:link": {
        "href": "https://bilibili.yangz.site/feed.xml",
        "rel": "self",
        "type": "application/rss+xml",
    },
    "language": "zh-cn",
    "managingEditor": "Zhang, Yang",
    "docs": "https://github.com/AIboy996/bilibili_poster",
    "pubDate": datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0800"),
    "lastBuildDate": datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0800"),
    "ttl": "1440",
}

# 条目列表
items = []
with open("database.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    for item in list(data)[::-1]:
        # 处理每个条目
        name = data[item]["thumb_name"]
        url = data[item]["thumb"]
        date = data[item]["date"]
        item_info = {
            "title": name,
            "link": f"https://bilibili.yangz.site/imgs/{name}.webp",
            "guid": f"https://bilibili.yangz.site/imgs/{name}.webp",
            "description": f"""
{name}快乐！<br>
<img src="https://bilibili.yangz.site/imgs/{name}.webp" alt="{name}"><br>
""",
            "pubDate": date,
        }
        items.append(item_info)

if __name__ == "__main__":
    # 生成RSS文件
    generate_rss_feed(channel_info, items, "feed.xml")
