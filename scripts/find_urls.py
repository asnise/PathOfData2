import re

content_path = r"C:\Users\User\.gemini\antigravity-ide\brain\b8282941-f591-4db0-b0b6-b5b371310397\.system_generated\steps\54\content.md"

with open(content_path, "r", encoding="utf-8") as f:
    js_content = f.read()

urls = re.findall(r'[\"\'](?:https?://[^\s\"\'<>]+|/[^\s\"\'<>]+)[\"\']', js_content)
for u in sorted(list(set(urls))):
    print(u)
