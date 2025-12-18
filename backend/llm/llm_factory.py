from langchain_groq import ChatGroq  # note: new import path

_llm_instance = None

def get_llm():
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = ChatGroq(
            model="llama-3.1-8b-instant",  # or another Groq model
            #enter the key here
            api_key="",
            temperature=0.0,
        )
    return _llm_instance
