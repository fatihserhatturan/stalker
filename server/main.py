import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from core.schemas import ChatRequest, ChatResponse, DocumentRequest, DocumentResponse
from core.chain import get_conversational_chain, get_memory_for_session, generate_sample_document
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
    """
    try:
        logger.info(f"Chat request received for session: {request.session_id}")

        memory = get_memory_for_session(request.session_id)

        chain = get_conversational_chain()

        result = await chain.ainvoke({
            "input": request.message,
            "history": memory.chat_memory.messages
        })

        memory.save_context(
            {"input": request.message},
            {"output": result}
        )

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

@app.post("/generate-document", response_model=DocumentResponse)
async def generate_document(request: DocumentRequest):
    """
    Rastgele örnek doküman oluşturan endpoint.
    """
    try:
        logger.info(f"Document generation request received for session: {request.session_id}")

        document_content = await generate_sample_document()

        logger.info(f"Document generated successfully for session: {request.session_id}")

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
