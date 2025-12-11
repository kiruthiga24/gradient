import requests
import os
# from dotenv import load_dotenv
from utils.logger import logger

# load_dotenv()
# my https://api-console.zoho.com/client/ server based application access token, generate if these are not. 
ZOHO_ACCESS_TOKEN = "1000.e6016156bb7339cb92d1c0b2d6864706.390c1b279642e89554285591538f352d"#os.getenv("ZOHO_ACCESS_TOKEN")  
ZOHO_REFRESH_TOKEN = "1000.9cfbdd3da1803ee4ceaf02aeafbf37a3.2e49915aab0bb4599bd56be1b4d3dac0"#os.getenv("ZOHO_REFRESH_TOKEN")  
ZOHO_CLIENT_ID = "1000.3SYL9SPU7HXLEIU6EGMNYB01EJZ71E"#os.getenv("ZOHO_CLIENT_ID")
ZOHO_CLIENT_SECRET = "dbcd2bba02c9ec0b554df314c19ab71d2be7b11ce7"#os.getenv("ZOHO_CLIENT_SECRET")

# Refresh token API
def refresh_zoho_token():
    url = "https://accounts.zoho.com/oauth/v2/token"

    payload = {
        "refresh_token": ZOHO_REFRESH_TOKEN,
        "client_id": ZOHO_CLIENT_ID,
        "client_secret": ZOHO_CLIENT_SECRET,
        "grant_type": "refresh_token"
    }

    r = requests.post(url, data=payload)
    data = r.json()

    if "access_token" in data:
        new_token = data["access_token"]
        os.environ["ZOHO_ACCESS_TOKEN"] = new_token
        logger.info("Zoho access token refreshed successfully.")
        return new_token
    
    logger.error(f"Failed to refresh Zoho token: {data}")
    return None


# Create Task in Zoho CRM
def create_zoho_crm_task(subject, description):
    access_token = os.getenv("ZOHO_ACCESS_TOKEN")

    url = "https://www.zohoapis.com/crm/v2/Tasks"

    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}"
    }

    payload = {
        "data": [
            {
                "Subject": subject,
                "Description": description,
                "Status": "Not Started",
                "Priority": "High"
            }
        ]
    }

    response = requests.post(url, json=payload, headers=headers)

    # Handle token expiry
    if response.status_code == 401:
        logger.warning("Access token expired. Refreshing...")

        new_token = refresh_zoho_token()
        if not new_token:
            return None

        headers["Authorization"] = f"Zoho-oauthtoken {new_token}"
        response = requests.post(url, json=payload, headers=headers)

    return response.json()
