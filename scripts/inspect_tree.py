import json

with open(r"f:\POE2 Database\data\passive_tree.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Top-level keys:", list(data.keys()) if isinstance(data, dict) else "Data is not a dict")

if isinstance(data, dict):
    for k in ["classes", "nodes", "tree"]:
        val = data.get(k)
        if val is not None:
            print(f"Key '{k}': type={type(val)}, len={len(val) if hasattr(val, '__len__') else 'N/A'}")
            if k == "classes" and isinstance(val, list):
                print("First item in classes:", val[0] if val else "empty")
            if k == "nodes" and isinstance(val, dict):
                first_node_key = list(val.keys())[0]
                print(f"First item in nodes ({first_node_key}):", val[first_node_key])
