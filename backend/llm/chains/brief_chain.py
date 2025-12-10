from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


def build_brief_chain(llm):
    prompt = ChatPromptTemplate.from_template(r"""
Transform this RCA into C-LEVEL executive brief. NO actions/solutions.

Account: {account_name}
Root Causes: {rca}

Create BRIEF executive summary (30 words max):
1. Quantify revenue/customer risk from root causes
2. Strategic business impact  
3. Who needs to be escalated

Return ONLY JSON with these 4 keys:
- title (include account_name + "Churn Alert")
- exec_summary (revenue risk in $)
- risk_level ("Critical"/"High"/"Medium") 
- escalate_to ("CEO"/"CFO"/"Ops"/"All")

Example structure (adapt content to RCA):
{{"title": "Acme Corp Churn Alert", "exec_summary": "$450K risk", "risk_level": "Critical", "escalate_to": "CEO"}}

CRITICAL: Different content for every RCA. No copy-paste.
""")

    return prompt | llm | JsonOutputParser()


    

