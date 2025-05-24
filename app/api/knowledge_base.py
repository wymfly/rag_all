from typing import List
from fastapi import APIRouter, HTTPException, status
# Removed Depends as it's not used in this version, can be added later if needed.

from app.models.kb_models import KnowledgeBaseCreate, KnowledgeBaseRead
from app.knowledge_base import kb_service 

router = APIRouter(
    prefix="/knowledge_bases",
    tags=["Knowledge Bases"]
)

@router.post("/", response_model=KnowledgeBaseRead, status_code=status.HTTP_201_CREATED)
async def create_knowledge_base_api(kb_create: KnowledgeBaseCreate):
    """
    Creates a new knowledge base.
    """
    # The kb_service.create_kb function is expected to handle its own errors
    # or return a valid KnowledgeBaseRead object.
    # If kb_service.create_kb could raise specific exceptions that need
    # different HTTP error codes, that handling would go here.
    return kb_service.create_kb(kb_create)

@router.get("/{kb_id}", response_model=KnowledgeBaseRead)
async def get_knowledge_base_api(kb_id: str):
    """
    Retrieves a specific knowledge base by its ID.
    """
    kb = kb_service.get_kb(kb_id)
    if kb is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Knowledge Base with ID '{kb_id}' not found"
        )
    return kb

@router.get("/", response_model=List[KnowledgeBaseRead])
async def list_knowledge_bases_api():
    """
    Lists all available knowledge bases.
    """
    # kb_service.list_kbs() is expected to return a list (possibly empty)
    return kb_service.list_kbs()

# Example of how to integrate this router into app/main.py (for context, not for this file):
# from app.api import knowledge_base as kb_api_router # Renamed to avoid conflict if main.py also has 'router'
# app.include_router(kb_api_router.router, prefix="/api/v1") # Or similar, e.g. app.include_router(router)
# It's common to use a more descriptive variable name for the imported router if app/main.py has its own 'router'.
# Or, in app/main.py directly:
# from app.api.knowledge_base import router as knowledge_base_router
# app.include_router(knowledge_base_router) # if prefix is already handled in APIRouter
