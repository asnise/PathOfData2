import os
import json
from bs4 import BeautifulSoup

content_path = r"C:\Users\User\.gemini\antigravity-ide\brain\b8282941-f591-4db0-b0b6-b5b371310397\.system_generated\steps\9\content.md"
output_path = r"f:\POE2 Database\data\keystones.json"

with open(content_path, "r", encoding="utf-8") as f:
    content = f.read()

html_start = content.find("<!DOCTYPE html>")
html_content = content[html_start:] if html_start != -1 else content

soup = BeautifulSoup(html_content, "html.parser")

keystones_data = {}

for tab_id in ["KeystonePassive", "TimelessJewelKeystone"]:
    tab_div = soup.find(id=tab_id)
    if not tab_div:
        continue
        
    cards = tab_div.find_all(class_=lambda x: x and "d-flex" in x and "border-top" in x)
    tab_list = []
    
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
        title_div = card.find("div", class_="flex-grow-1")
        if title_div:
            inner_divs = title_div.find_all("div", recursive=False)
            title_link = inner_divs[0].find("a") if len(inner_divs) > 0 else None
            if title_link:
                name = title_link.get_text(strip=True)
                if not href or href == "https://poe2db.tw":
                    href = title_link.get("href", "")
                    if href.startswith("/"):
                        href = "https://poe2db.tw" + href
                    data_hover = title_link.get("data-hover", "")
                    
        desc_div = card.find("div", class_="implicitMod")
        description_lines = []
        if desc_div:
            current_line = []
            for child in desc_div.contents:
                if child.name == "br":
                    line_text = "".join(current_line).strip()
                    if line_text:
                        description_lines.append(line_text)
                    current_line = []
                else:
                    text = child.get_text() if child.name else str(child)
                    current_line.append(text)
            if current_line:
                line_text = "".join(current_line).strip()
                if line_text:
                    description_lines.append(line_text)
            
            description_lines = [" ".join(line.split()) for line in description_lines]
            description = "\n".join(description_lines)
        else:
            description = ""
            
        img_elem = card.find("img")
        img_src = img_elem.get("src", "") if img_elem else ""
        
        tab_list.append({
            "id": idx + 1,
            "name": name,
            "url": href,
            "image": img_src,
            "description": description,
            "description_lines": description_lines,
            "hover_data": data_hover
        })
        
    keystones_data[tab_id] = tab_list

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(keystones_data, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(keystones_data.get('KeystonePassive', []))} Keystone Passives and {len(keystones_data.get('TimelessJewelKeystone', []))} Timeless Jewel Keystones.")
