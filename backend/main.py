from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import upload, query, agents

app = FastAPI(
    title="AI Due Diligence Platform",
    description="API for processing company documents",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev purposes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api/v1")
app.include_router(query.router, prefix="/api/v1")
app.include_router(agents.router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok"}
