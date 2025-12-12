import os
import requests
import time
from utils.logger import logger
from dotenv import load_dotenv
from database import SessionLocal
from models.base_model import *
from datetime import datetime, timedelta, timezone

load_dotenv(dotenv_path=".env", override=True)

class ZohoAuthService:

    def __init__(self):
        self.client_id = os.getenv("ZOHO_CLIENT_ID")
        self.client_secret = os.getenv("ZOHO_CLIENT_SECRET")
        self.refresh_token = os.getenv("ZOHO_REFRESH_TOKEN")
        self.accounts_url = os.getenv("ZOHO_ACCOUNTS_URL")
        self.access_token = None
        self.expiry = 0

    def get_access_token(self):
        try:
            """Return valid token, auto-refresh when expired"""
            if self.access_token and time.time() < self.expiry:
                return self.access_token
            
            params = {
                "refresh_token": self.refresh_token,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "refresh_token"
            }

            res = requests.post(self.accounts_url, params=params).json()

            if "access_token" not in res:
                logger.error(f"Zoho token refresh failed: {res}")
                raise Exception("Failed to refresh access token")

            self.access_token = res["access_token"]
            self.expiry = time.time() + 3500

            logger.info("Zoho access token refreshed successfully")
            return self.access_token
        except Exception as e:
            logger.error(f"Error in get_access_token(): {e}")


class ZohoCRMService:
    def __init__(self):
        self.zoho_crm_url = os.getenv("ZOHO_CRM_URL")

    def _post(self, endpoint, payload):
        try:
            token = zoho_auth.get_access_token()
            headers = {"Authorization": f"Zoho-oauthtoken {token}"}
            url = f"{self.zoho_crm_url}/{endpoint}"

            response = requests.post(url, json=payload, headers=headers).json()
            logger.info(f"Zoho CRM Response: {response}")
            return response
        except Exception as e:
            logger.error(f"Error in _post(): {e}")
            return None

    # ---------------- CREATE TASK ----------------
    def create_task(self, subject, description, due_date, owner_id, record_id, contact_id, priority):
        payload = {
            "data": [
                {
                    "Owner": {"id": owner_id},
                    "Who_Id": {"id": contact_id},
                    "What_Id": {"id": record_id},
                    "$se_module": "Deals",
                    "Subject": subject,
                    "Description": description,
                    "Due_Date": due_date,
                    "Priority": priority,
                    "Status": "Not Started",
                    "send_notification": True
                }
            ]
        }
        return self._post("Tasks", payload)

    # ---------------- CREATE MEETING EVENT ----------------
    def create_meeting(self, event_title, description, start_dt, end_dt, owner_id, record_id, contact_id):
        payload = {
            "data": [
                {
                    "Owner": {"id": owner_id},
                    "Who_Id": {"id": contact_id},
                    "What_Id": {"id": record_id},
                    "$se_module": "Deals",
                    "Event_Title": event_title,
                    "Description": description,
                    "Start_DateTime": start_dt,
                    "End_DateTime": end_dt,
                    "Venue": "Virtual Meeting",
                    "send_notification": True,
                    "Participants": [
                        {"type": "contact", "participant": contact_id},
                        {"type": "user", "participant": owner_id}
                    ]
                }
            ]
        }
        return self._post("Events", payload)
    
    def get_recommendations(self,agent_run_id):
        db = SessionLocal()
        items = db.query(ExpansionRecommendation).filter(
            ExpansionRecommendation.agent_run_id == agent_run_id
        ).all()
        db.close()
        
        # return {"recommendations": [item.to_dict() for item in items]}
        return items
    
    def push_to_crm(self,agent_run_id):

        recos = self.get_recommendations(agent_run_id)
        
        if not recos:
            return {"status": "no recommendations found"}

        results = []

        for r in recos:
            if r.recommendation_type.lower() == "task":
                logger.info(f"Creating Task in CRM for recommendation id={r.id}")

                res = self.create_task(
                    subject=f"Action Required: {r.recommendation_type}",
                    description=r.recommendation_text,
                    due_date= (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
                    owner_id=r.kam_user_id,
                    record_id=r.record_id,
                    contact_id=r.customer_id,
                    priority=r.priority
                )
                results.append(res)

            elif r.recommendation_type.lower() == "meeting":
                IST_OFFSET = timezone(timedelta(hours=5, minutes=30))
                start_datetime_aware = (datetime.now(IST_OFFSET) + timedelta(days=2))
                start_meeting_time = start_datetime_aware.strftime("%Y-%m-%dT%H:%M:%S%z")
                end_datetime_aware = start_datetime_aware + timedelta(minutes=30)
                end_meeting_time = end_datetime_aware.strftime("%Y-%m-%dT%H:%M:%S%z")

                start_meeting_time = start_meeting_time[:-2] + ':' + start_meeting_time[-2:]
                end_meeting_time = end_meeting_time[:-2] + ':' + end_meeting_time[-2:]

                logger.info(f"Creating Meeting Event in CRM for recommendation id={r.id}")

                res = self.create_meeting(
                    event_title=f"Customer Meeting - {r.recommendation_type}",
                    description=r.recommendation_text,
                    start_dt=start_meeting_time,
                    end_dt=end_meeting_time,
                    owner_id=r.kam_user_id,
                    record_id=r.record_id,
                    contact_id=r.customer_id
                )
                results.append(res)
            self.log_response(agent_run_id, res)


        return {"status": "success", "crm_actions": results}

    def log_response(self, agent_run_id, crm_response):
        db = SessionLocal()

        record = CRMActionAudit(
            agent_run_id=agent_run_id,
            crm_response=crm_response
        )

        db.add(record)
        db.commit()
        db.close()

        logger.info(f"CRM audit logged for agent_run_id={agent_run_id}")


zoho_auth = ZohoAuthService()
# zoho_crm = ZohoCRMService()




