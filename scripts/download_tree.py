import urllib.request
import json

url = "https://poe2db.tw/data/passive-skill-tree/4.5/data_us.json"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

with urllib.request.urlopen(req) as response:
    raw_data = response.read()

data = json.loads(raw_data.decode("utf-8"))

with open(r"f:\POE2 Database\data\passive_tree.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Saved passive_tree.json successfully!")
print("Classes:", [c.get("name") for c in data.get("classes", [])])
print("Total nodes:", len(data.get("nodes", {})))
print("Tree type:", data.get("tree"))
