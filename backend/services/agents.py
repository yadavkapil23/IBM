import os
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import ChatPromptTemplate
from services.rag import query_documents
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    # Use meta/llama3-70b-instruct available via NVIDIA API
    return ChatNVIDIA(model="meta/llama3-70b-instruct")

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
    
    chain = prompt_template | llm
    
    response = chain.invoke({
        "context": context,
        "question": question
    })
    
    return {
        "agent": agent_type,
        "response": response.content,
        "sources": [r["metadata"].get("source", "Unknown") for r in results]
    }
