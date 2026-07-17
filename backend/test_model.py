import os
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from dotenv import load_dotenv

load_dotenv()
os.environ["NVIDIA_MODEL_NAME"] = "nvidia/nemotron-mini-4b-instruct"

try:
    model_name = os.getenv("NVIDIA_MODEL_NAME")
    print("Testing model:", model_name)
    llm = ChatNVIDIA(model=model_name)
    response = llm.invoke("Hello, who are you?")
    print("Success:", response.content)
except Exception as e:
    print("Error:", str(e))
