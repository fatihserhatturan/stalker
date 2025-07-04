import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from core.schemas import ChatRequest, ChatResponse, DocumentRequest, DocumentResponse
from core.chain import (
    process_conversation,
    generate_sample_document,
    generate_detailed_analysis_document,
    get_analysis_status
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Business Analyst API",
    description="A professional API for the AI Business Analyst Hackathon Project",
    version="1.0.0"
)

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
    Gelişmiş context tracking ve memory management ile.
    """
    try:
        logger.info(f"Chat request received for session: {request.session_id}")

        # Yeni gelişmiş process_conversation fonksiyonunu kullan
        result = await process_conversation(request.session_id, request.message)

        logger.info(f"Chat response generated for session: {request.session_id}")

        return ChatResponse(
            answer=result,
            session_id=request.session_id
        )

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Sohbet işlenirken bir hata oluştu: {str(e)}"
        )

@app.get("/analysis-status/{session_id}")
async def get_session_analysis_status(session_id: str):
    """
    Session için analiz durumunu döndüren endpoint.
    Hangi bilgilerin toplandığını ve completion oranını gösterir.
    """
    try:
        logger.info(f"Analysis status request for session: {session_id}")

        status = get_analysis_status(session_id)

        return {
            "session_id": session_id,
            "status": status
        }

    except Exception as e:
        logger.error(f"Error getting analysis status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analiz durumu alınırken hata oluştu: {str(e)}"
        )

@app.post("/generate-document", response_model=DocumentResponse)
async def generate_document(request: DocumentRequest):
    """
    Rastgele örnek doküman oluşturan endpoint.
    """
    try:
        logger.info(f"Sample document generation request received for session: {request.session_id}")

        document_content = await generate_sample_document()

        logger.info(f"Sample document generated successfully for session: {request.session_id}")

        return DocumentResponse(
            document_content=document_content,
            session_id=request.session_id,
            document_type="markdown"
        )

    except Exception as e:
        logger.error(f"Error in document generation endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Doküman oluşturulurken bir hata oluştu: {str(e)}"
        )

@app.post("/generate-analysis-document", response_model=DocumentResponse)
async def generate_analysis_document(request: DocumentRequest):
    """
    Session konuşma geçmişine dayalı gerçek analiz dokümanı oluşturan endpoint.
    Kullanıcı ile yapılan konuşmalardan toplanan bilgileri kullanır.
    """
    try:
        logger.info(f"Analysis document generation request received for session: {request.session_id}")

        # Analiz durumunu kontrol et
        status = get_analysis_status(request.session_id)

        if "error" in status:
            raise HTTPException(
                status_code=404,
                detail="Session bulunamadı veya konuşma geçmişi yok"
            )

        # Session'daki konuşma geçmişinden analiz dokümanı oluştur
        document_content = await generate_detailed_analysis_document(request.session_id)

        logger.info(f"Analysis document generated successfully for session: {request.session_id}")

        return DocumentResponse(
            document_content=document_content,
            session_id=request.session_id,
            document_type="markdown"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in analysis document generation endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analiz dokümanı oluşturulurken bir hata oluştu: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
