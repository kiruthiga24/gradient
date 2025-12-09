import os
from langchain_openai import AzureChatOpenAI
from langchain_community.llms import Ollama

def get_llm():
    """Get LLM instance - Azure OpenAI or local Ollama fallback"""
    azure_endpoint = "https://eastus.api.cognitive.microsoft.com/"
    azure_api_key = "c47297e0a3ba46df968a0edd814c4ce6"
    azure_deployment = "ai_blazers-parithi-gpt4o"
    azure_api_version = "2024-12-01-preview"
    
    # Try Azure OpenAI first
    if azure_endpoint and azure_api_key:
        return AzureChatOpenAI(
            azure_endpoint=azure_endpoint,
            api_key=azure_api_key,
            azure_deployment=azure_deployment,
            api_version=azure_api_version,
            temperature=0,
            max_tokens=2000
        )
    # Fallback to local Ollama
    else:
        print("No Azure OpenAI env vars found, using Ollama")
        print("Install Ollama: curl https://ollama.ai/install.sh | sh")
        print("Run: ollama pull llama3.2")
        return Ollama(model="llama3.2")
