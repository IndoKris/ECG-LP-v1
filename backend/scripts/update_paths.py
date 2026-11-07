import json
import os

with open('../data/quiz_data.json', 'r') as f:
    quiz_data = json.load(f)

# Fix image paths in quiz_data.json to point to images/
for item in quiz_data:
    img_name = os.path.basename(item['image'])
    item['image'] = f"images/{img_name}"

with open('../data/quiz_data.json', 'w') as f:
    json.dump(quiz_data, f, indent=2)

print("Updated quiz image paths successfully.")
