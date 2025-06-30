from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id: str  # Her kullanıcının sohbetini ayırt etmek için
    message: str

class ChatResponse(BaseModel):
    answer: str
    session_id: str
