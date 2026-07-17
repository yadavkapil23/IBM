import os
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from dotenv import load_dotenv

load_dotenv()

try:
    models = ChatNVIDIA.get_available_models()
    print("Available models:")
    for model in models:
        print(model.id)
except Exception as e:
    print("Error:", str(e))
