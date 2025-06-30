import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from core.schemas import ChatRequest, ChatResponse
from core.chain import get_conversational_chain, get_memory_for_session
import logging

# Logging konfigürasyonu
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI uygulamasını başlat
app = FastAPI(
    title="AI Business Analyst API",
    description="A professional API for the AI Business Analyst Hackathon Project",
    version="1.0.0"
)

# CORS middleware ekle
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """API'nin çalıştığını doğrulayan basit endpoint"""
    return {"message": "AI Business Analyst API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Sağlık kontrolü endpoint'i"""
    return {"status": "healthy", "service": "AI Business Analyst"}

@app.post("/chat", response_model=ChatResponse)
async def chat_with_analyst(request: ChatRequest):
    """
    Kullanıcı ile sohbeti yöneten ana API endpoint'i.
    """
    try:
        logger.info(f"Chat request received for session: {request.session_id}")

        # İlgili session için hafızayı al
        memory = get_memory_for_session(request.session_id)

        # Sohbet zincirini oluştur
        chain = get_conversational_chain()

        # Chain'i çalıştır
        result = await chain.ainvoke({
            "input": request.message,
            "history": memory.chat_memory.messages
        })

        # Hafızaya kaydet
        memory.save_context(
            {"input": request.message},
            {"output": result}
        )

        logger.info(f"Chat response generated for session: {request.session_id}")

        return ChatResponse(
            answer=result,  # result artık doğrudan string
            session_id=request.session_id
        )

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Sohbet işlenirken bir hata oluştu: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
