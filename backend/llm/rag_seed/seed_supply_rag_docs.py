import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from rag_store import add_documents

supply_risk_docs = [
    # 1. Supply Risk Playbooks
    ("Supply_Risk_Playbook", 
     """SUPPLY RISK PLAYBOOK: Late Shipment Response
TRIGGER: Missed SLA or raw material shortage >7 days
IMMEDIATE ACTIONS (4h):
1. Expedite critical POs via air freight (Logistics)
2. Reroute from alternate suppliers (Supply Chain) 
3. Advance credit line to customer (Sales)
OPERATIONAL IMPACT: Line stoppage risk >30% = CRITICAL
SUCCESS: OTD recovery >95%, backorders <5%."""),

    ("Expedite_Protocol",
     """EXPEDITE PLAYBOOK:
1. PO Value >$50K OR Critical Parts → Air Freight
2. ASN Overdue >48hrs → Supplier conference call
3. Line Stop Risk → Deploy mitigation team within 4h
4. Customer Notification → Proactive email within 2h
ESCALATION: VP Supply Chain if >3 POs delayed >5 days."""),

    ("Reroute_Protocol", 
     """REROUTE PROTOCOL:
- Primary carrier delay >24h → Switch to Carrier B
- Port congestion → Inland routing via truck/rail
- Supplier delay → Activate Supplier C (backup)
- International → Air bridge from regional hub
COST THRESHOLD: <$10K penalty OK for OTD recovery."""),

    ("Line_Stop_Mitigation",
     """LINE STOP MITIGATION:
IMMEDIATE (4h):
- Deploy buffer stock from nearest DC
- Temporary production line reconfiguration
- Overtime authorization for critical lines
- Customer pre-warning + ETA commitment
PREVENTION: Safety stock = 10 days critical SKUs."""),

    # 2. Delivery Performance Signals
    ("Delivery_Performance_Signals",
     """DELIVERY PERFORMANCE SIGNALS:
- On-Time Delivery Rate Drop >10% = MEDIUM risk
- Missed SLA Count >15/week = HIGH risk
- ETA Variance >48hrs = CRITICAL risk
- Planned vs Actual Gap >3 days = Escalate
MITIGATION: Daily carrier scorecards, alternate routing."""),

    ("Supply_Chain_Signals",
     """SUPPLY CHAIN RISK SIGNALS:
- Raw Material Shortage Risk >0.7 = CRITICAL
- Inventory Coverage Ratio <1.2x = HIGH risk
- Days Stock Remaining <7 = IMMEDIATE action
RESPONSE: Top-3 supplier expedites, safety stock review."""),

    ("Customer_Impact_Signals",
     """CUSTOMER IMPACT SIGNALS:
- Line Stop Probability >25% = CRITICAL
- Backorder Volume Growth >30% = HIGH
- Critical SKU Delay Flag = IMMEDIATE
PLAYBOOK: Pre-warning emails, line stop mitigation team."""),

    # 3. Risk Scoring / Thresholds
    ("Supply_Risk_Scoring",
     """SUPPLY RISK SCORING:
CRITICAL: Line stop >30% OR Revenue >$100K risk
HIGH: OTD drop >15% OR Stock <5 days
MEDIUM: ETA variance >24h OR Backorder >20%
LOW: Monitor only, no immediate action required."""),

    ("Escalation_Thresholds",
     """ESCALATION THRESHOLDS:
- 3+ POs delayed >5 days → VP Supply Chain
- Line stop risk >25% → Executive brief
- Revenue impact >$50K → C-level notification
- Multi-supplier failure → Crisis response team."""),

    # 4. Email / Communication Guidelines
    ("Supply_Risk_Email_Guidelines",
     """SUPPLY RISK EMAIL GUIDELINES:
Subject: Clear impact + urgency (🚨 Supply Delay - Line Stop Risk)
Body: Acknowledge → Explain → Actions → Timeline → Contact
Tone: Proactive, solution-focused, transparent."""),

    ("Customer_PreWarning_Template",
     """PRE-WARNING TEMPLATE:
1. Acknowledge delay + impact
2. Current mitigation actions
3. Revised ETA commitment
4. Direct contact for escalation
5. Apology + goodwill gesture."""),

    # 5. Case Studies / Lessons Learned
    ("Case_Study_Port_Congestion",
     """PORT CONGESTION CASE: 15 POs delayed 7 days
Actions: Air freight critical SKUs, truck from inland
Result: OTD recovered to 92%, customer retained."""),

    ("Case_Study_Raw_Material_Shortage",
     """RAW MATERIAL SHORTAGE: Steel supplier failure
Actions: Alternate supplier + premium pricing
Result: Line stop avoided, 2-day delay only."""),

    ("Case_Study_Line_Stop_Recovery",
     """LINE STOP RECOVERY: Deployed buffer stock from 3 DCs
Actions: Overtime + line reconfiguration
Result: Production resumed within 6h, customer trust maintained."""),
]

# -------------------------
# LOAD INTO CHROMADB
# -------------------------
documents = [content for (_, content) in supply_risk_docs]
metadatas = [{"title": title, "use_case": "supply_risk"} for (title, _) in supply_risk_docs]

print(f"Adding {len(documents)} supply risk documents to ChromaDB…")
add_documents(documents, metadatas)
print("✅ Supply Risk RAG seeding complete.")
