import json

with open("table.json", "r", encoding='utf-8') as f:
    data = json.load(f)

filtered = {
    "courses": [
        {
            "id": c["id"],
            "title": c["title"],
            "instituteName": c["instituteName"],
            "professor": c["professor"],
        }
        for c in data["courses"]
    ]
}

with open("filtered_courses.json", "w") as f:
    json.dump(filtered, f, indent=2)
