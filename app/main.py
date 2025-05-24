from fastapi import FastAPI
from app.api.knowledge_base import router as kb_router # Import the router

app = FastAPI(title="Enterprise RAG System") # Added title

@app.get("/")
async def root():
    return {"message": "Welcome to the Enterprise RAG System!"} # Changed message slightly

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Include the knowledge base API router
app.include_router(kb_router, prefix="/api/v1")
