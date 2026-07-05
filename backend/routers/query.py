from fastapi import APIRouter
from pydantic import BaseModel
from services.rag import query_documents

router = APIRouter(
    prefix="/query",
    tags=["query"],
)

class QueryRequest(BaseModel):
    question: str
    top_k: int = 5

@router.post("/")
async def ask_question(req: QueryRequest):
    results = query_documents(req.question, k=req.top_k)
    return {
        "question": req.question,
        "results": results
    }
