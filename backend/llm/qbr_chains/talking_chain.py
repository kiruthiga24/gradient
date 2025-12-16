from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# Talking points for KAM
def build_qbr_talk_chain(llm):
    prompt = ChatPromptTemplate.from_template(r"""
Produce short talking points (bulleted) for the KAM based on brief and deck.

You MUST return ONLY valid JSON.
Do NOT include any explanation, headings, or notes.
Do NOT wrap JSON in backticks.
Do NOT add any text before or after the JSON.
- Use decimal numbers only, no fractions
- Replace any unknown value with 0 or null
- Do not use Python None; use JSON null
                                              
Brief: {brief}
Deck: {deck}

Return ONLY JSON:
{{
  "talking_points":["..."]
}}

""")
    return prompt | llm | JsonOutputParser()
