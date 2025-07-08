import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from core.schemas import ChatRequest, ChatResponse, DocumentRequest, DocumentResponse
from core.handlers.chat_handler import ChatHandler
from core.handlers.file_handler import FileHandler
from core.handlers.document_handler import DocumentHandler
from core.container import get_container
import logging

load_dotenv()

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

container = get_container()
chat_handler = ChatHandler(container.chat_manager)
file_handler = FileHandler(container.file_manager)
document_handler = DocumentHandler(container.document_manager, container.chat_manager)

@app.get("/")
async def root():
    return {"message": "AI Business Analyst API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AI Business Analyst"}

@app.post("/chat", response_model=ChatResponse)
async def chat_with_analyst(request: ChatRequest):
    return await chat_handler.handle_chat(request)

@app.post("/upload-file")
async def upload_file(
    file: UploadFile = File(...),
    session_id: str = Form(...)
):
    return await file_handler.handle_file_upload(file, session_id)

@app.post("/upload-template")
async def upload_template(
    file: UploadFile = File(...),
    session_id: str = Form(...),
    is_template: str = Form("true")
):
    return await file_handler.handle_template_upload(file, session_id)

@app.get("/analysis-status/{session_id}")
async def get_session_analysis_status(session_id: str):
    return await chat_handler.handle_analysis_status(session_id)

@app.get("/session-documents/{session_id}")
async def get_documents_for_session(session_id: str):
    return await chat_handler.handle_session_documents(session_id)

@app.get("/document/{session_id}/{document_id}")
async def get_document(session_id: str, document_id: str):
    return await chat_handler.handle_get_document(session_id, document_id)

@app.post("/generate-analysis-document", response_model=DocumentResponse)
async def generate_analysis_document(request: DocumentRequest):
    return await document_handler.handle_generate_analysis_document(request)

@app.post("/generate-visual-data")
async def generate_visual_data(request: ChatRequest):
    return await document_handler.handle_generate_visual_data(request)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
