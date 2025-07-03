from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    answer: str
    session_id: str

class DocumentRequest(BaseModel):
    session_id: str

class DocumentResponse(BaseModel):
    document_content: str
    session_id: str
    document_type: str
