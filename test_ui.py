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
    for use_case in USE_CASES:
        print(f"\n--- Testing: {use_case} ---")

        url = f"{BASE_URL}/signals/left-pane/{use_case}"
        response = requests.get(url)

        print("Status:", response.status_code)

        try:
            data = response.json()
            print(json.dumps(data, indent=2))
        except Exception as e:
            print("Invalid JSON Response:", response.text)


if __name__ == "__main__":
    test_api()
