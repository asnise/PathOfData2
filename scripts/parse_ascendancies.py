import os
import json
from bs4 import BeautifulSoup

content_path = r"C:\Users\User\.gemini\antigravity-ide\brain\b8282941-f591-4db0-b0b6-b5b371310397\.system_generated\steps\149\content.md"
output_path = r"f:\POE2 Database\data\ascendancies.json"

with open(content_path, "r", encoding="utf-8") as f:
    content = f.read()

html_start = content.find("<!DOCTYPE html>")
html_content = content[html_start:] if html_start != -1 else content

soup = BeautifulSoup(html_content, "html.parser")
tab_div = soup.find(id="Ascendancypassives")

if not tab_div:
    print("Error: Ascendancypassives tab not found!")
    exit(1)

cards = tab_div.find_all(class_=lambda x: x and "d-flex" in x and "border-top" in x)
print(f"Found {len(cards)} ascendancy passive cards.")

grouped_data = {}
flat_list = []

for idx, card in enumerate(cards):
    link_elem = card.find("a", href=True)
    href = ""
    data_hover = ""
    if link_elem:
        href = link_elem.get("href", "")
        if href.startswith("/"):
            href = "https://poe2db.tw" + href
        data_hover = link_elem.get("data-hover", "")

    name = ""
    name_elem = card.find("a", class_="PassiveSkills")
    if name_elem:
        name = name_elem.get_text(strip=True)
        if not href or href == "https://poe2db.tw":
            href = name_elem.get("href", "")
            if href.startswith("/"):
                href = "https://poe2db.tw" + href
            data_hover = name_elem.get("data-hover", "")

    ascendancy = "Unknown"
    char_class = "Unknown"
    props = card.find_all("div", class_="property")
    for p in props:
        text = p.get_text()
        if "Ascendancy:" in text:
            asc_a = p.find("a")
            if asc_a:
                ascendancy = asc_a.get_text(strip=True)
        elif "Character:" in text:
            char_a = p.find("a")
            if char_a:
                char_class = char_a.get_text(strip=True)

    stats = []
    stat_divs = card.find_all("div", class_="implicitMod")
    for s_div in stat_divs:
        txt = " ".join(s_div.get_text().split())
        if txt:
            stats.append(txt)

    img_elem = card.find("img")
    img_src = img_elem.get("src", "") if img_elem else ""

    node_data = {
        "id": idx + 1,
        "name": name,
        "url": href,
        "image": img_src,
        "character_class": char_class,
        "ascendancy_class": ascendancy,
        "stats": stats,
        "hover_data": data_hover
    }

    flat_list.append(node_data)
    
    if ascendancy not in grouped_data:
        grouped_data[ascendancy] = []
    grouped_data[ascendancy].append(node_data)

output_data = {
    "summary": {
        "total_nodes": len(flat_list),
        "total_ascendancy_classes": len(grouped_data)
    },
    "grouped": grouped_data,
    "flat": flat_list
}

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print(f"Successfully extracted and saved {len(flat_list)} skills grouped across {len(grouped_data)} ascendancies.")
