from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class KnowledgeBaseBase(BaseModel):
    name: str = Field(..., description="Name of the knowledge base, e.g., 'Medical Research KB'")
    description: Optional[str] = Field(None, description="Optional description for the knowledge base")
    domain: Optional[str] = Field(None, description="Domain of the knowledge base, e.g., 'medical', 'legal', 'general'")

class KnowledgeBaseCreate(KnowledgeBaseBase):
    pass

class KnowledgeBaseRead(KnowledgeBaseBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier for the knowledge base")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of knowledge base creation")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of last update to the knowledge base")

    class Config:
        from_attributes = True


class FileInfoBase(BaseModel):
    name: str = Field(..., description="Original name of the uploaded file")
    # path: str # We might not want to expose the direct path in the API response for security/abstraction.
                 # This will be an internal detail.
    mime_type: Optional[str] = Field(None, description="MIME type of the file")
    size_bytes: Optional[int] = Field(None, description="Size of the file in bytes")
    # knowledge_base_id: str # This will be implicitly known or handled by the service layer.

class FileInfoRead(FileInfoBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier for the file")
    uploaded_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of file upload")
    status: str = Field("pending", description="Processing status of the file, e.g., 'pending', 'processing', 'processed', 'error'")
    # We might add more fields like error_message if status is 'error'

    class Config:
        from_attributes = True


class KnowledgeBaseWithFiles(KnowledgeBaseRead):
    files: List[FileInfoRead] = []

# Example of how these might be used (for the worker to understand context, not to be added to the file)
# kb_create_data = KnowledgeBaseCreate(name="My Legal Docs", domain="legal")
# kb_read_data = KnowledgeBaseRead(id="uuid-of-kb", name="My Medical KB", domain="medical")
# file_info_data = FileInfoRead(id="uuid-of-file", name="document1.pdf", status="processed")
# kb_with_files_data = KnowledgeBaseWithFiles(id="uuid-of-kb", name="My KB", files=[file_info_data])
