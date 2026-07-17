import os
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from services.rag import query_documents
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    # Use Nemotron Mini available via NVIDIA API or configurable via .env
    model_name = os.getenv("NVIDIA_MODEL_NAME", "nvidia/nemotron-mini-4b-instruct")
    base_url = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
    return ChatNVIDIA(model=model_name, base_url=base_url)

PROMPTS = {
    "financial": """You are an expert Financial Due Diligence Agent. Your role is to analyze financial documents and extract key financial risks, revenue numbers, and inconsistencies.
Use the following context to answer the user's question. If you don't know the answer, say you don't know based on the provided context.

Context:
{context}

Question: {question}""",
    
    "legal": """You are an expert Legal Due Diligence Agent. Your role is to review legal contracts, identify liabilities, clauses, and potential legal disputes.
Use the following context to answer the user's question. If you don't know the answer, say you don't know based on the provided context.

Context:
{context}

Question: {question}""",
    
    "compliance": """You are an expert Compliance Due Diligence Agent. Your role is to review company policies, HR policies, and security standards to ensure regulatory compliance and identify compliance risks.
Use the following context to answer the user's question. If you don't know the answer, say you don't know based on the provided context.

Context:
{context}

Question: {question}""",

    "cross_analysis": """You are an expert Due Diligence Auditor. Your task is to analyze the provided context extracted from multiple documents.
Specifically look for inconsistencies, contradictions, or matching confirmations across different sources (e.g., comparing what Document A says vs Document B).
Point out any discrepancies clearly, referencing the specific Source headers.

Context:
{context}

Question/Topic to analyze: {question}""",

    "risk_scoring": """You are an expert Risk Assessment Engine. Evaluate the provided context and calculate an overall risk score from 0 to 100, where 100 means extreme risk and 0 means no risk.
You MUST format your output strictly as a JSON object matching the following structure exactly, with no additional text or markdown formatting outside the JSON:

{{
  "score": <0-100>,
  "risk_level": "Low" | "Medium" | "High",
  "reasons": ["<reason 1>", "<reason 2>"]
}}

Context:
{context}

Question: {question}""",

    "executive_report": """You are a Lead Due Diligence Executive. Your task is to compile a comprehensive Executive Summary Report based on the provided context extracted from multiple company documents.
Please structure your report in Markdown format with the following sections:
1. **Overview**: A high-level summary of the company's status.
2. **Financial Health**: Key revenue numbers, financial risks, and anomalies.
3. **Legal & Compliance**: Key contracts, liabilities, disputes, and regulatory compliance.
4. **Key Risks & Discrepancies**: Any major red flags or inconsistencies across documents.
5. **Final Recommendation**: A concluding assessment (e.g., Proceed, Proceed with Caution, or Do Not Proceed).

Context:
{context}

Generate the report now."""
}


def analyze_with_agent(agent_type: str, question: str):
    if agent_type not in PROMPTS:
        raise ValueError(f"Unknown agent type: {agent_type}")

    # Retrieve context from vector store. Fetch more chunks for cross analysis.
    k = 10 if agent_type == "cross_analysis" else 5
    results = query_documents(question, k=k)
    
    context = ""
    for r in results:
        context += f"\nSource: {r['metadata'].get('source', 'Unknown')}\n{r['content']}\n"
        
    prompt_template = ChatPromptTemplate.from_template(PROMPTS[agent_type])
    llm = get_llm()
    
    if agent_type == "risk_scoring":
        parser = JsonOutputParser()
        chain = prompt_template | llm | parser
        response_content = chain.invoke({
            "context": context,
            "question": question
        })
    else:
        chain = prompt_template | llm
        response = chain.invoke({
            "context": context,
            "question": question
        })
        response_content = response.content
    
    return {
        "agent": agent_type,
        "response": response_content,
        "sources": [r["metadata"].get("source", "Unknown") for r in results]
    }

def generate_executive_report():
    # Broad query to fetch diverse context
    query = "company overview, financial status, revenue, legal risks, contracts, HR compliance, discrepancies"
    
    # Retrieve a large amount of context
    results = query_documents(query, k=20)
    
    context = ""
    for r in results:
        context += f"\nSource: {r['metadata'].get('source', 'Unknown')}\n{r['content']}\n"
        
    prompt_template = ChatPromptTemplate.from_template(PROMPTS["executive_report"])
    llm = get_llm()
    
    chain = prompt_template | llm
    
    response = chain.invoke({
        "context": context
    })
    
    return {
        "report": response.content,
        "sources": list(set([r["metadata"].get("source", "Unknown") for r in results]))
    }

