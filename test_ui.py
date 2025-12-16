import requests
import json

BASE_URL = "http://127.0.0.1:5000"   # change if needed

USE_CASES = [
    "churn_risk",
    "expansion_opportunity",
    "quality_incident",
    "supply_risk",
    "qbr_auto_generation"
]

def test_api():
    print(f"\n--- Testing:  ---")

    url = f"{BASE_URL}/agent/data/supply_risk/857990fb-993c-46ca-830d-e3ed67128470/14cd679e-84b2-4c33-91d7-905f11ec912b"
    response = requests.get(url)

    print("Status:", response.status_code)

    try:
        data = response.json()
        print(json.dumps(data, indent=2))
    except Exception as e:
        print("Invalid JSON Response:", response.text)



if __name__ == "__main__":
    test_api()
