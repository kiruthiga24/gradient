from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def build_expansion_deck_chain(llm):
    prompt = ChatPromptTemplate.from_template(r"""
Create an internal sales deck outline.
You MUST return ONLY valid JSON.
Do NOT include any explanation, headings, or notes.
Do NOT wrap JSON in backticks.
Do NOT add any text before or after the JSON.
- Use decimal numbers only, no fractions
- Replace any unknown value with 0 or null
- Do not use Python None; use JSON null   
                                              
Input Brief:
{brief}

Return ONLY JSON:
{{
  "slides": [
    {{
      "title": "Slide title",
      "bullets": ["Bullet 1", "Bullet 2"]
    }}
  ]
}}

NO FORMATTING. NO MARKDOWN. JSON ONLY.
""")

    return prompt | llm | JsonOutputParser()
