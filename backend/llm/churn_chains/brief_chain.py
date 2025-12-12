from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


def build_brief_chain(llm):
    """
    Input variables expected:
      - rca: JSON string of the RCA output
      - account_name: string
    """
    prompt = ChatPromptTemplate.from_template(
        r"""
You are an executive customer success leader.

Account: {account_name}

RCA (JSON):
{rca}

Create a concise C-level brief. Do NOT repeat the RCA verbatim.
Focus on:
- Business / revenue risk
- Key drivers of churn risk
- Urgency level
- Who needs to be informed

Return your answer as JSON ONLY.
Do not include any explanation, commentary, prefixes, or suffixes.

The JSON must have exactly this structure:

{{
  "title": "{account_name} Churn Risk Brief",
  "exec_summary": "1–2 sentence summary of risk and impact",
  "risk_level": "Critical/High/Medium/Low",
  "key_drivers": ["driver 1", "driver 2"],
  "recommended_focus": "One short sentence on where leadership should focus"
}}
"""
    )

    return prompt | llm | JsonOutputParser()


    

