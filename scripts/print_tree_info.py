import json

with open(r"f:\POE2 Database\data\passive_tree.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("=== Passive Tree Overview ===")
print("Tree Type:", data.get("tree"))
print("Bounds: x=[{}, {}], y=[{}, {}]".format(data.get("min_x"), data.get("max_x"), data.get("min_y"), data.get("max_y")))

print("\n=== Classes & Ascendancies ===")
for idx, c in enumerate(data.get("classes", [])):
    asc_names = [a.get("name") for a in c.get("ascendancies", []) if not a.get("name", "").startswith("[DNT")]
    if asc_names:
        print(f"{idx+1}. {c.get('name')} -> {', '.join(asc_names)}")
    else:
        print(f"{idx+1}. {c.get('name')} (No active ascendancies)")

nodes = data.get("nodes", {})
normal_count = 0
notable_count = 0
keystone_count = 0
mastery_count = 0
other_count = 0

for nid, node in nodes.items():
    if node.get("isKeystone"):
        keystone_count += 1
    elif node.get("isNotable"):
        notable_count += 1
    elif node.get("isMastery"):
        mastery_count += 1
    elif node.get("name") or node.get("stats"):
        normal_count += 1
    else:
        other_count += 1

print("\n=== Node Counts ===")
print(f"Total Nodes: {len(nodes)}")
print(f"  - Normal Nodes: {normal_count}")
print(f"  - Notable Nodes: {notable_count}")
print(f"  - Keystone Nodes: {keystone_count}")
print(f"  - Mastery Nodes: {mastery_count}")
print(f"  - System/Other Nodes: {other_count}")
