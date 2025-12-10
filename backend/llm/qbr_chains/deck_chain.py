from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# Deck: structured slide JSON
def build_qbr_deck_chain(llm):
    prompt = ChatPromptTemplate.from_template(r"""
Create a QBR deck JSON. Use brief, rca and opportunities. Keep slides concise.

You MUST return ONLY valid JSON.
Do NOT include any explanation, headings, or notes.
Do NOT wrap JSON in backticks.
Do NOT add any text before or after the JSON.
- Use decimal numbers only, no fractions
- Replace any unknown value with 0 or null
- Do not use Python None; use JSON null
                                              
Brief: {brief}
RCA: {rca}
Opportunities: {opportunities}
Account: {account_name}

Return ONLY JSON:
{{
  "deck_title":"QBR - {account_name}",
  "slides":[
    {{"title":"Executive Summary","bullets":["..."]}},
    {{"title":"Trends","bullets":["..."]}},
    {{"title":"Wins","bullets":["..."]}},
    {{"title":"Risks","bullets":["..."]}},
    {{"title":"Opportunities","bullets":["..."]}},
    {{"title":"Action Plan","bullets":["..."]}}
  ]
}}

""")
    return prompt | llm | JsonOutputParser()

