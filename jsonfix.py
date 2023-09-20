import json

# Load your JSON from the file
with open("results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for fruit, conditions in data.items():
    for condition, values in conditions.items():
        for item in values:
            try:
                api_response = json.loads(
                    item["api_response"].strip()
                )  # Added the strip() function
                ripeness = api_response["ripeness_range"]
            except KeyError:
                print(
                    f"KeyError for fruit: {fruit}, condition: {condition}, image: {item['image']}"
                )
                print("api_response:", item["api_response"])
            except json.JSONDecodeError:
                print(
                    f"JSON decode error for fruit: {fruit}, condition: {condition}, image: {item['image']}"
                )
                print("api_response:", item["api_response"])
