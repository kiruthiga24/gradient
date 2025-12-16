import os
import requests
import time
from utils.logger import logger
from dotenv import load_dotenv
from database import SessionLocal
from models.base_model import *
from datetime import datetime, timedelta, timezone

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.colors import HexColor

import smtplib
import uuid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

    def push_to_crm(self,payload):

        # recos = self.get_recommendations(agent_run_id)

        # if not recos:
        #     return {"status": "no recommendations found"}

        # results = []

        # for r in recos:
        #     if r.recommendation_type.lower() == "task":
        #         logger.info(f"Creating Task in CRM for recommendation id={r.id}")

        #         res = self.create_task(
        #             subject=f"Action Required: {r.recommendation_type}",
        #             description=r.recommendation_text,
        #             due_date= (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
        #             owner_id=r.kam_user_id,
        #             record_id=r.record_id,
        #             contact_id=r.customer_id,
        #             priority=r.priority
        #         )
        #         results.append(res)

        #     elif r.recommendation_type.lower() == "meeting":
        #         IST_OFFSET = timezone(timedelta(hours=5, minutes=30))
        #         start_datetime_aware = (datetime.now(IST_OFFSET) + timedelta(days=2))
        #         start_meeting_time = start_datetime_aware.strftime("%Y-%m-%dT%H:%M:%S%z")
        #         end_datetime_aware = start_datetime_aware + timedelta(minutes=30)
        #         end_meeting_time = end_datetime_aware.strftime("%Y-%m-%dT%H:%M:%S%z")

        #         start_meeting_time = start_meeting_time[:-2] + ':' + start_meeting_time[-2:]
        #         end_meeting_time = end_meeting_time[:-2] + ':' + end_meeting_time[-2:]

        #         logger.info(f"Creating Meeting Event in CRM for recommendation id={r.id}")

        #         res = self.create_meeting(
        #             event_title=f"Customer Meeting - {r.recommendation_type}",
        #             description=r.recommendation_text,
        #             start_dt=start_meeting_time,
        #             end_dt=end_meeting_time,
        #             owner_id=r.kam_user_id,
        #             record_id=r.record_id,
        #             contact_id=r.customer_id
        #         )
        #         results.append(res)
        #     self.log_response(agent_run_id, res)


        # return {"status": "success", "crm_actions": results}
        try:
            account_id = payload.get("account_id")
            agent_run_id = payload.get("agent_run_id")
            tasks = payload.get("tasks", [])

            if not account_id or not agent_run_id or not tasks:
                return {
                    "success": False,
                    "message": "account_id, agent_run_id and tasks are required",
                    "task_ids": [],
                    "created_count": 0
                }

            created_task_ids = []

            for task in tasks:
                title = task.get("title")
                description = task.get("description")

                if not title:
                    title = "Follow up with customer"
                if not description:
                    description = "Please follow up with the customer as per the action plan."

                logger.info(
                    f"Creating CRM Task | agent_run_id={agent_run_id} | title={title}"
                )

                res = self.create_task(
                    subject=f"Action Required: {title}",
                    description=description,
                    due_date= (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
                    owner_id="1152378000000427001",
                    record_id="1152378000000567616",
                    contact_id="1152378000000567537",
                    priority="High"
                )
                task_id = res["data"][0]["details"]["id"]
                created_task_ids.append(task_id)

            return {
                "success": True,
                "message": "Tasks created successfully",
                "task_ids": created_task_ids,
                "created_count": len(created_task_ids)
            }

        except Exception as e:
            logger.error(f"Error in push_to_crm(): {e}")
            return {
                "success": False,
                "message": "An Error occurred while creating tasks",
                "task_ids": [],
                "created_count": 0
            }

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

class Pdf_generator:
    def __init__(self):
        pass
    def generate_brief_pdf(self,payload: dict, file_path: str):
        """
        Generates a professional PDF brief from agent output
        """

        doc = SimpleDocTemplate(
            file_path,
            pagesize=A4,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        elements = []

        # ---------- Custom Styles ----------
        title_style = ParagraphStyle(
            "TitleStyle",
            parent=styles["Title"],
            fontSize=22,
            textColor=HexColor("#1F3A5F"),
            alignment=TA_CENTER,
            spaceAfter=20
        )

        section_header = ParagraphStyle(
            "SectionHeader",
            parent=styles["Heading2"],
            fontSize=14,
            textColor=HexColor("#1F3A5F"),
            spaceBefore=12,
            spaceAfter=8
        )

        body_text = ParagraphStyle(
            "BodyText",
            parent=styles["BodyText"],
            fontSize=11,
            leading=15,
            alignment=TA_LEFT
        )

        footer_style = ParagraphStyle(
            "Footer",
            parent=styles["Normal"],
            fontSize=9,
            textColor=HexColor("#666666"),
            alignment=TA_CENTER
        )

        # ---------- Title ----------
        company_name = payload.get("company_name", "Customer")
        elements.append(Paragraph(
            f"Account Risk & Action Brief<br/>{company_name}",
            title_style
        ))

        elements.append(Spacer(1, 0.2 * inch))

        # ---------- Executive Summary ----------
        elements.append(Paragraph("Executive Summary", section_header))
        elements.append(Paragraph(
            payload["brief"].get("executive_summary", ""),
            body_text
        ))

        # ---------- Key Findings ----------
        key_findings = payload["brief"].get("key_findings", [])
        if key_findings:
            elements.append(Spacer(1, 0.15 * inch))
            elements.append(Paragraph("Key Findings", section_header))

            findings_list = ListFlowable(
                [ListItem(Paragraph(item, body_text)) for item in key_findings],
                bulletType="bullet",
                start="circle"
            )
            elements.append(findings_list)

        # ---------- Action Plan ----------
        action_plan = payload["brief"].get("action_plan", [])
        if action_plan:
            elements.append(Spacer(1, 0.15 * inch))
            elements.append(Paragraph("Recommended Action Plan", section_header))

            action_list = ListFlowable(
                [ListItem(Paragraph(item, body_text)) for item in action_plan],
                bulletType="bullet",
                start="square"
            )
            elements.append(action_list)

        # ---------- Footer ----------
        elements.append(Spacer(1, 0.4 * inch))
        elements.append(Paragraph(
            f"Generated by Agentic AI • {datetime.utcnow().strftime('%d %b %Y')}",
            footer_style
        ))

        doc.build(elements)
        return file_path


class EmailService:

    def __init__(self):
        self.smtp_host = "smtp.gmail.com"
        self.smtp_port = 587
        self.smtp_user = os.getenv("SMTP_USERNAME")
        self.smtp_pass = os.getenv("SMTP_PASSWORD")
        self.from_email = os.getenv("SMTP_USERNAME")

    def send_email(self, to_email, subject, body):
        """
        Sends an email and returns a generated email_id
        """

        email_id = f"email-{uuid.uuid4()}"

        msg = MIMEMultipart()
        msg["From"] = self.from_email
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_pass)
                server.sendmail(self.from_email, to_email, msg.as_string())

            logger.info(f"Email sent | email_id={email_id} | to={to_email}")
            return email_id

        except Exception as e:
            logger.error(f"Failed to send email | to={to_email} | error={str(e)}")
            raise

zoho_auth = ZohoAuthService()
# zoho_crm = ZohoCRMService()