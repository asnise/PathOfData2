content_path = r"C:\Users\User\.gemini\antigravity-ide\brain\b8282941-f591-4db0-b0b6-b5b371310397\.system_generated\steps\54\content.md"

with open(content_path, "r", encoding="utf-8") as f:
    js_content = f.read()

print("File size (chars):", len(js_content))
print("First 1000 characters:")
print(js_content[:1000])

print("\nLast 1000 characters:")
print(js_content[-1000:])
