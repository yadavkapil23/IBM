from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.agents import analyze_with_agent

router = APIRouter(
    prefix="/agents",
    tags=["agents"],
)

class AgentQueryRequest(BaseModel):
    agent_type: str # financial, legal, compliance, cross_analysis
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
