import json
import pandas as pd

# Load your JSON from the file
with open("results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

rows = []
for fruit, conditions in data.items():
    for condition, values in conditions.items():
        for item in values:
            ripeness = json.loads(item["api_response"])["ripeness_range"]
            rows.append([fruit, condition, item["image"], ripeness])

df = pd.DataFrame(rows, columns=["Fruit", "Condition", "Image", "Ripeness Range"])
df.to_excel("Ripeness_validation.xlsx", index=False)
