import requests

class LocalLlama3:
    """
    Local LLaMA3 wrapper compatible with LangChain 1.1.3
    """
    def __init__(self, api_url="http://localhost:11434/v1/chat/completions", model_name="llama3:latest"):
        self.api_url = api_url
        self.model_name = model_name

    # This makes the class "Runnable" for LangChain chains
    def __call__(self, prompt: str, **kwargs) -> str:
        if hasattr(prompt, "to_string"):
            prompt = prompt.to_string()
        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model_name,
                    "messages": [{"role": "user", "content": prompt}]
                },
                timeout=360
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print("LLM request failed:", e)
            return ""


_llm_instance = None

def get_llm():
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = LocalLlama3()
    return _llm_instance
