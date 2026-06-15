import os
import json
from bs4 import BeautifulSoup

# Paths
content_path = r"C:\Users\User\.gemini\antigravity\brain\e7a488fb-e2da-4343-894d-4a9504037c8e\.system_generated\steps\3\content.md"
output_path = r"f:\POE2 Database\data\gems.json"

print(f"Reading content from: {content_path}")
with open(content_path, "r", encoding="utf-8") as f:
    content = f.read()

# Locate HTML content
html_start = content.find("<!DOCTYPE html>")
html_content = content[html_start:] if html_start != -1 else content

print("Parsing HTML content...")
soup = BeautifulSoup(html_content, "html.parser")
gems_summary = soup.find(id="GemsSummary")

if not gems_summary:
    print("Error: GemsSummary container not found in HTML.")
    exit(1)

gem_cards = gems_summary.find_all(class_=lambda x: x and "d-flex" in x and "border-top" in x)
print(f"Found {len(gem_cards)} gem cards.")

gems_data = []

for idx, card in enumerate(gem_cards):
    # Name, URL, Class color, Hover data from the link element
    # Check if there is an 'a' tag with class starting with "gem_"
    link_elem = card.find("a", class_=lambda x: x and "gem_" in x)
    class_color = ""
    href = ""
    data_hover = ""
    name = ""
    
    if link_elem:
        classes = link_elem.get("class", [])
        gem_class = [c for c in classes if c.startswith("gem_")]
        if gem_class:
            class_color = gem_class[0]
        href = link_elem.get("href", "")
        # Resolve to full URL if relative
        if href.startswith("/"):
            href = "https://poe2db.tw" + href
        data_hover = link_elem.get("data-hover", "")
    
    # Title element inside flex-grow-1
    title_div = card.find("div", class_="flex-grow-1")
    if title_div:
        # Resolve name from title div link if name is empty
        inner_divs = title_div.find_all("div", recursive=False)
        title_link = inner_divs[0].find("a") if len(inner_divs) > 0 else None
        if title_link:
            name = title_link.get_text(strip=True)
            if not href or href == "https://poe2db.tw":
                url_path = title_link.get("href", "")
                if url_path.startswith("/"):
                    href = "https://poe2db.tw" + url_path
                else:
                    href = url_path
        
        # Tags from div class="default"
        tags_div = title_div.find("div", class_="default")
        tags = []
        if tags_div:
            tags = [t.get_text(strip=True) for t in tags_div.find_all("a")]
        
        # Description is everything in title_div except the title link's div and tags div
        desc_parts = []
        for child in title_div.contents:
            if child.name == "div":
                # Skip the tags div
                if "default" in child.get("class", []):
                    continue
                # Skip the title div (which contains the gem link)
                if child.find("a", class_=lambda x: x and "gem_" in x):
                    continue
                desc_parts.append(child.get_text())
            else:
                desc_parts.append(str(child))
                
        raw_desc = "".join(desc_parts).strip()
        desc_soup = BeautifulSoup(raw_desc, "html.parser")
        description = desc_soup.get_text(separator=" ").strip()
        description = " ".join(description.split())
    else:
        tags = []
        description = ""

    # Image URL
    img_elem = card.find("img")
    img_src = img_elem.get("src", "") if img_elem else ""

    # Add to dataset
    gems_data.append({
        "id": idx + 1,
        "name": name,
        "url": href,
        "class_color": class_color,
        "image": img_src,
        "tags": tags,
        "description": description,
        "hover_data": data_hover
    })

# Write to JSON
print(f"Writing {len(gems_data)} gems to {output_path}...")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(gems_data, f, ensure_ascii=False, indent=2)

print("Extraction completed successfully!")
