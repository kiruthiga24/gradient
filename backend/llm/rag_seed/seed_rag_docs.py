import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from rag_store import add_documents

churn_docs = [
    # 1. SLA / Contract Documents
    ("SLA_Penalty_Thresholds",
     """Customers are contractually entitled to on-time delivery service levels of 95% or higher.
If on-time delivery falls below 95% for 2 consecutive months → remediation.
If below 90% in any 30-day period → high risk escalation.
Escalation timelines must not exceed 5 business days."""),

    ("Contract_Renewal_Risk",
     """Accounts with declining order volume during last 120 days → churn risk.
>20% drop requires mandatory KAM review, possible discounts or contract adjustments."""),

    ("SLA_Escalation_Rules",
     """If delivery delays exceed 3 incidents in 30 days → proactive customer notification required.
Must create a recovery plan and get approval from Customer Ops."""),

    ("Customer_Retention_Clauses",
     """Strategic accounts must be assessed monthly.
Triggers: quality failures, pricing disputes, reliability issues.
Retention interventions must be documented for high ARR accounts."""),

    ("Commercial_Remedies",
     """Approved remedies: service credits, contract extension, priority production slots, dedicated support teams.
Use based on risk score + account tier."""),

    # 2. Quality Playbooks
    ("Quality_Escalation_Playbook",
     """Any defect rate above 1.5% in a rolling 30 days triggers CAPA.
RCA must examine shift, machine, supplier lot, and material batch."""),

    ("CAPA_Framework",
     """Major/Critical quality incidents require CAPA.
Owner assigned within 24 hours.
CAPA closure must occur within 14 business days unless escalated."""),

    ("Supplier_Impact_Analysis",
     """If defects correlate to supplier lots → isolate batches immediately.
Recurring failures require supplier corrective action report."""),

    ("OEE_Quality_Linkage",
     """OEE < 85% for two reporting periods is a risk factor.
Often correlated with rising defect rates. Maintenance action required."""),

    ("Field_Complaint_Handling",
     """Customer complaints must be acknowledged within 8 hours.
Resolution timelines must be communicated clearly.
Slow response = reputational risk."""),

    # 3. Business Rules / Heuristics
    ("Churn_Risk_Thresholds",
     """Order volume drop >25% = high churn risk.
15–25% = medium.
<15% = normal noise."""),

    ("Multi_Signal_Risk_Logic",
     """High churn risk when two conditions are true:
- >20% order decline
- defect rate >1.5%
- >3 support tickets in 30 days.
Medium risk if any one triggers."""),

    ("Usage_Decline_Policy",
     """Usage reduction >20% in 14-day period indicates disengagement.
Combining usage drop + defects increases churn likelihood."""),

    ("Revenue_Exposure_Model",
     """Revenue at risk = monthly revenue × churn probability × time to renewal.
Lower confidence when data incomplete."""),

    ("Signal_Confidence_Weighting",
     """Churn weight hierarchy:
1. Delivery delays = highest
2. Usage drops = medium
3. Minor defects = low."""),

    # 4. Case Studies
    ("Case_Study_Auto_Supplier",
     """30% order decline + 3 late shipments.
No proactive engagement → lost renewal.
Lesson: escalate early."""),

    ("Case_Study_Electronics_OEM",
     """Cosmetic defects + delayed RCA → customer switched supplier.
Lesson: speed matters."""),

    ("Case_Study_Industrial_Resins",
     """Usage decline ignored for months → gradual churn.
Lesson: usage signals predict churn."""),

    ("Case_Study_Logistics_Failure",
     """Production line stoppage due to late raw materials.
No warning → trust erosion → contract termination."""),

    ("Case_Study_Recovery_Success",
     """Proactive outreach + service credits restored trust.
Account renewed + expanded."""),

    # 5. Email Style Guidelines
    ("Enterprise_Email_Tone",
     """Empathetic, transparent, non-blaming language.
Avoid technical jargon unless needed."""),

    ("Escalation_Email_Guidelines",
     """Acknowledge impact, take responsibility, explain corrective actions, offer direct contact."""),

    ("Executive_Communication_Framework",
     """Concise, outcome-focused messaging.
Focus on impact, mitigation, and next steps.""")

]

# -------------------------
# LOAD INTO CHROMADB
# -------------------------

documents = [content for (_, content) in churn_docs]
metadatas = [{"title": title, "use_case": "churn"} for (title, _) in churn_docs]

print(f"Adding {len(documents)} churn documents to ChromaDB…")
add_documents(documents, metadatas)
print("RAG seeding complete.")