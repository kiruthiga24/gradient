import requests
import json

BASE_URL = "http://127.0.0.1:5000/signals/run"

def run_signal_detection():
    try:
        print("Calling Signal Detection API...\n")

        response = requests.post(BASE_URL, timeout=30)

        print(f"Status Code: {response.status_code}\n")

        try:
            data = response.json()
            print("Response JSON:")
            print(json.dumps(data, indent=4))
        except Exception:
            print("Raw Response:")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"API call failed: {str(e)}")


def run_expansion_llm():
    try:
        print("Calling Expansion LLM API...\n")
        BASE_URL= "http://127.0.0.1:5000/run/expansion/from-table"

        response = requests.post(BASE_URL, timeout=360)

        print(f"Status Code: {response.status_code}\n")

        try:
            data = response.json()
            print("Response JSON:")
            print(json.dumps(data, indent=4))
        except Exception:
            print("Raw Response:")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"API call failed: {str(e)}")

def run_qbr_llm():
    try:
        print("Calling QBR LLM API...\n")
        BASE_URL= "http://127.0.0.1:5000/run/qbr/from-table"
        response = requests.post(BASE_URL, timeout=360)
        try:
            data = response.json()
            print("Response JSON:")
            print(json.dumps(data, indent=4))
        except Exception:
            print("Raw Response:")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"API call failed: {str(e)}")

def run_churn_llm():
    try:
        print("Calling Churn LLM API...\n")
        BASE_URL= "http://127.0.0.1:5000/run/churn-risk"

        response = requests.post(BASE_URL, timeout=360)

        print(f"Status Code: {response.status_code}\n")

        try:
            data = response.json()
            print("Response JSON:")
            print(json.dumps(data, indent=4))
        except Exception:
            print("Raw Response:")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"API call failed: {str(e)}")
    
def run_supply_llm():
    try:
        print("Calling Supply LLM API...\n")
        BASE_URL= "http://127.0.0.1:5000/run/supply-risk"

        response = requests.post(BASE_URL, timeout=360)

        print(f"Status Code: {response.status_code}\n")

        try:
            data = response.json()
            print("Response JSON:")
            print(json.dumps(data, indent=4))
        except Exception:
            print("Raw Response:")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"API call failed: {str(e)}")

def run_quality_llm():
    try:
        print("Calling QBR LLM API...\n")
        BASE_URL= "http://127.0.0.1:5000/run/quality/from-table"

        response = requests.post(BASE_URL, timeout=360)

        print(f"Status Code: {response.status_code}\n")

        try:
            data = response.json()
            print("Response JSON:")
            print(json.dumps(data, indent=4))
        except Exception:
            print("Raw Response:")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"API call failed: {str(e)}")

def get_middle_pane():
    try:
        print("Middle Pane API...\n")
        BASE_URL= "http://127.0.0.1:5000/churn_risk/middle-pane"

        response = requests.get(BASE_URL, timeout=360)

        print(f"Status Code: {response.status_code}\n")

        try:
            data = response.json()
            print("Response JSON:")
            print(json.dumps(data, indent=4))
        except Exception:
            print("Raw Response:")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"API call failed: {str(e)}")


if __name__ == "__main__":
    # run_signal_detection()
    # run_expansion_llm()
    # run_qbr_llm()
    # run_quality_llm()
    # run_churn_llm()
    run_qbr_llm()