from fastapi import APIRouter, UploadFile, File
from typing import List
from services.parser import process_document
from services.rag import index_document

router = APIRouter(
    prefix="/upload",
    tags=["upload"],
)

@router.post("/")
async def upload_documents(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        content = await file.read()
        parsed_data = process_document(file.filename, content)
        
        # Index document in vector database
        chunks_indexed = index_document(
            file.filename, 
            parsed_data.get("text", ""), 
            parsed_data.get("metadata", {})
        )
        
        results.append({
            "filename": file.filename,
            "status": "processed",
            "metadata": parsed_data.get("metadata", {}),
            "chunks_indexed": chunks_indexed,
            "text_preview": parsed_data.get("text", "")[:200]
        })
    return {"results": results}
