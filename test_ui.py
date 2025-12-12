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

    url = f"{BASE_URL}/agent/data/quality/a3a575e4-dd1a-46c0-b3b3-0c9070755726/14cd679e-84b2-4c33-91d7-905f11ec912b"
    response = requests.get(url)

    print("Status:", response.status_code)

    try:
        data = response.json()
        print(json.dumps(data, indent=2))
    except Exception as e:
        print("Invalid JSON Response:", response.text)



if __name__ == "__main__":
    test_api()
