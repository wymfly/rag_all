from typing import Dict, List, Optional
from datetime import datetime
import uuid
from app.models.kb_models import KnowledgeBaseCreate, KnowledgeBaseRead

# In-memory store for knowledge bases
_knowledge_bases: Dict[str, KnowledgeBaseRead] = {}

def create_kb(kb_create: KnowledgeBaseCreate) -> KnowledgeBaseRead:
    """
    Creates a new knowledge base and stores it in memory.
    """
    kb_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    # Create an instance of KnowledgeBaseRead
    # Pydantic v2 uses model_dump() instead of dict()
    knowledge_base_data = kb_create.model_dump()
    
    knowledge_base = KnowledgeBaseRead(
        id=kb_id,
        created_at=now,
        updated_at=now,
        **knowledge_base_data
    )
    
    _knowledge_bases[kb_id] = knowledge_base
    return knowledge_base

def get_kb(kb_id: str) -> Optional[KnowledgeBaseRead]:
    """
    Retrieves a knowledge base by its ID from the in-memory store.
    """
    return _knowledge_bases.get(kb_id)

def list_kbs() -> List[KnowledgeBaseRead]:
    """
    Lists all knowledge bases currently in the in-memory store.
    """
    return list(_knowledge_bases.values())

# Optional: A function to update a KB (not in the original plan for this step, but good for future)
# from app.models.kb_models import KnowledgeBaseUpdate # Assuming this model would exist
# def update_kb(kb_id: str, kb_update: KnowledgeBaseUpdate) -> Optional[KnowledgeBaseRead]:
#     if kb_id in _knowledge_bases:
#         kb = _knowledge_bases[kb_id]
#         update_data = kb_update.model_dump(exclude_unset=True) # exclude_unset to only update provided fields
#         for key, value in update_data.items():
#             setattr(kb, key, value)
#         kb.updated_at = datetime.utcnow()
#         _knowledge_bases[kb_id] = kb
#         return kb
#     return None

# Optional: A function to delete a KB
# def delete_kb(kb_id: str) -> bool:
#     if kb_id in _knowledge_bases:
#         del _knowledge_bases[kb_id]
#         return True
#     return False

if __name__ == '__main__':
    # Basic test cases (for local verification)
    print("--- Testing Knowledge Base Service ---")

    # Test create_kb
    print("\n1. Creating new knowledge bases...")
    kb_create_1_data = KnowledgeBaseCreate(name="Medical Research KB", description="KB for medical research papers.", domain="medical")
    kb_1 = create_kb(kb_create_1_data)
    print(f"   Created KB 1: ID={kb_1.id}, Name='{kb_1.name}', Domain='{kb_1.domain}'")
    
    kb_create_2_data = KnowledgeBaseCreate(name="Legal Documents Archive", domain="legal")
    kb_2 = create_kb(kb_create_2_data)
    print(f"   Created KB 2: ID={kb_2.id}, Name='{kb_2.name}', Description='{kb_2.description}'")

    # Test list_kbs
    print("\n2. Listing all knowledge bases...")
    all_kbs = list_kbs()
    print(f"   Found {len(all_kbs)} KBs:")
    for kb_item in all_kbs:
        print(f"   - ID: {kb_item.id}, Name: '{kb_item.name}'")
    
    assert len(all_kbs) == 2

    # Test get_kb
    print("\n3. Retrieving knowledge bases by ID...")
    retrieved_kb_1 = get_kb(kb_1.id)
    if retrieved_kb_1:
        print(f"   Retrieved KB 1: Name='{retrieved_kb_1.name}', Matches created: {retrieved_kb_1.id == kb_1.id}")
        assert retrieved_kb_1.id == kb_1.id
    else:
        print(f"   Error: KB 1 with ID '{kb_1.id}' not found.")
        assert False, "KB 1 not found"

    non_existent_id = str(uuid.uuid4())
    retrieved_non_existent_kb = get_kb(non_existent_id)
    if retrieved_non_existent_kb is None:
        print(f"   Correctly returned None for non-existent KB ID: '{non_existent_id}'")
        assert True
    else:
        print(f"   Error: Expected None for non-existent KB ID, but got: {retrieved_non_existent_kb}")
        assert False, "Expected None for non-existent KB"

    print("\n--- Knowledge Base Service Tests Completed ---")
