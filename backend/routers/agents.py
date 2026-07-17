from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.agents import analyze_with_agent

router = APIRouter(
    prefix="/agents",
    tags=["agents"],
)

class AgentQueryRequest(BaseModel):
    agent_type: str # financial, legal, compliance, cross_analysis, risk_scoring
    question: str

@router.post("/analyze")
async def analyze_documents(req: AgentQueryRequest):
    try:
        result = analyze_with_agent(req.agent_type.lower(), req.question)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/report")
async def generate_report():
    try:
        from services.agents import generate_executive_report
        result = generate_executive_report()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

