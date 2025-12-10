import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from rag_store import add_documents

expansion_docs = [

    # 1. Commercial Cross-Sell Rules

    ("Cross_Sell_Expansion_Policy",
     """Customers consistently exceeding forecasted SKU usage thresholds
indicate expansion potential.

If actual usage exceeds planned consumption by >20% for 2 consecutive months → expansion signal.
If >35% in any single month → commercial acceleration trigger.
KAM engagement required within 7 business days."""),

    ("SKU_Consumption_Heuristics",
     """Stable customers typically show SKU usage growth of 2–5% monthly.
Sudden spikes >15% are classified as abnormal and require expansion analysis.
Flat usage of core SKU combined with increase in adjacent categories indicates substitution risk."""),

    ("Upsell_Eligibility_Rules",
     """Customer becomes eligible for upsell when:
- At least one SKU shows sustained overconsumption
- OR competitor SKU spend exceeds 10% of category wallet share
High-value accounts require mandatory roadmap sharing."""),

    ("Expansion_Signal_Prioritization",
     """Expansion signals ranked by impact:
1. Competitor SKU purchases
2. Overconsumption of high-margin SKUs
3. BOM-driven adjacency gaps
4. Temporary volume spikes (lowest priority)"""),

    # 2. BOM & Product Adjacency Rules

    ("BOM_Adjacency_Framework",
     """If customer purchases Component A, standard BOM recommends Bundled Components B and C.
Missing adjacent SKUs indicate cross-sell whitespace.

Example:
Resin-A used for Injection Mold → should co-occur with Resin-B and Catalyst-X."""),

    ("SKU_Compatibility_Matrix",
     """Compatible SKU groups typically purchased together:
Resin-A → Resin-B, Catalyst-X
Polymer-Q → Hardener-Y
Additive-M → Stabilizer-Z

Absence of compatible SKUs implies competitor sourcing or process inefficiency."""),

    ("Manufacturing_Process_Linkages",
     """Production process stages require consistent SKU clusters.
Deviation from standard cluster often indicates shadow suppliers or suboptimal sourcing."""),

    # 3. Competitor Intelligence

    ("Competitor_SKU_Detection_Rules",
     """If competitor SKU appears in invoice or material usage logs:
- Treat as whitespace opportunity.
- Flag for KAM review.
- Estimate wallet share loss."""),

    ("Competitor_Pricing_Benchmarks",
     """Average competitor premium:
High-performance resins: +12–18%
Standard polymers: +5–10%
Specialty chemicals: +20–30%

Higher premiums increase conversion probability if performance parity exists."""),

    ("Wallet_Share_Leakage_Model",
     """Wallet share leakage >10% of category spend → medium expansion signal.
>25% → high-priority cross-sell intervention."""),

    # 4. Revenue & Expansion Models

    ("Expansion_Revenue_Model",
     """Expansion revenue estimate =
(Current competitor volume + Overconsumption volume) × Average unit price.

Use trailing 3-month average where daily data unavailable."""),

    ("SKU_Price_Reference_Table",
     """Reference price tiers:
Resins: $4–12/kg
Polymers: $2–6/kg
Catalysts: $8–25/kg
Specialty additives: $15–50/kg""" ),

    ("Margin_Prioritization_Framework",
     """High-margin SKUs should be prioritized even with lower volumes.
If margin >35%, treat as strategic expansion targets."""),

    # 5. Sales Motion & Playbooks

    ("Expansion_Playbook_Standard",
     """Standard expansion motion:
1. Share usage insights with customer
2. Validate production roadmap
3. Propose bundled SKU optimization
4. Position as efficiency + reliability upgrade""" ),

    ("Commercial_Win_Themes",
     """Themes that resonate:
- Reduction in supplier risk
- Better process stability
- Simplified procurement
- Total cost of ownership reduction""" ),

    ("Cross_Sell_Messaging_Framework",
     """Preferred messaging tone:
Insight-led, advisory, non-aggressive.
Position product as operational improvement, not a hard sell.""" ),

    # 6. Case Studies

    ("Case_Study_Resin_Expansion",
     """Customer using Resin-A showed 28% usage growth.
Detected competitor Catalyst usage.
Converted by positioning performance + supply stability.
Result: +18% ARR growth."""),

    ("Case_Study_BOM_Whitespace_Win",
     """BOM analysis showed missing Stabilizer-Z.
Customer was sourcing from competitor without awareness of in-house alternative.
Result: 22% wallet share increase."""),

    ("Case_Study_Competitor_Displacement",
     """Detected shadow supplier for Polymer-Q.
Engaged with operational reliability pitch.
Customer consolidated vendors → incremental $240K ARR."""),

    # 7. Deck & Communication Style

    ("Upsell_Deck_Structure_Guidelines",
     """Recommended slide flow:
1. Usage Trends
2. Benchmark vs Industry
3. BOM Adjacency Gaps
4. Revenue Upside
5. Recommended SKU Portfolio Map
6. Next Steps""" ),

    ("Pricing_Quote_Standard",
     """Quotes should include:
- Current baseline volume
- Target volume
- Unit price
- Bundle discount (if approved)
No unauthorized discounts without finance approval."""),

    ("Enterprise_Commercial_Tone",
     """Tone should be data-driven, consultative, and customer-centric.
Avoid pushy language.
Present insights as operational improvements.""")

]

# -------------------------
# LOAD INTO VECTOR STORE
# -------------------------

documents = [content for (_, content) in expansion_docs]
metadatas = [{"title": title, "use_case": "expansion"} for (title, _) in expansion_docs]

print(f"Adding {len(documents)} expansion documents to ChromaDB…")
add_documents(documents, metadatas)
print("Expansion RAG seeding complete.")
