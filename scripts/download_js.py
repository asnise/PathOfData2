import urllib.request

url = "https://cdn.poe2db.tw/js/passive-skill-tree.ebc5203f86aa224e.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

with urllib.request.urlopen(req) as response:
    js_content = response.read()

with open("passive-skill-tree.js", "wb") as f:
    f.write(js_content)

print("Downloaded passive-skill-tree.js, size:", len(js_content))
print("Last 1000 characters of downloaded JS:")
print(js_content[-1000:].decode("utf-8", errors="ignore"))
