import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from core.schemas import ChatRequest, ChatResponse, DocumentRequest, DocumentResponse
from core.chain import (
    process_conversation,
    generate_detailed_analysis_document,
    generate_visual_data_from_session,  # Bu satırı ekleyin
    get_analysis_status,
    get_session_documents,
    get_document_by_id,
    process_uploaded_file,
    extract_text_from_file,
    uploaded_files
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

@app.post("/upload-file")
async def upload_file(
    file: UploadFile = File(...),
    session_id: str = Form(...)
):
    """
    Proje dosyalarını yüklemek için endpoint.
    """
    try:
        logger.info(f"File upload request for session: {session_id}, file: {file.filename}")

        # Dosya boyutu kontrolü (10MB limit)
        file_content = await file.read()
        if len(file_content) > 10 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="Dosya boyutu 10MB'dan büyük olamaz")

        # Dosya tipini kontrol et
        allowed_extensions = ['.txt', '.md', '.pdf', '.docx', '.doc']
        file_extension = '.' + file.filename.split('.')[-1].lower() if '.' in file.filename else ''

        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Desteklenmeyen dosya formatı. İzin verilen formatlar: {', '.join(allowed_extensions)}"
            )

        # Dosyayı işle ve analiz et
        analysis_result = await process_uploaded_file(session_id, file_content, file.filename, file_extension)

        logger.info(f"File processed successfully for session: {session_id}")

        return {
            "message": "Dosya başarıyla yüklendi ve analiz edildi",
            "session_id": session_id,
            "filename": file.filename,
            "analysis": analysis_result
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in file upload endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Dosya yüklenirken bir hata oluştu: {str(e)}"
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

@app.get("/session-documents/{session_id}")
async def get_documents_for_session(session_id: str):
    """
    Session'a ait dokümanları döndüren endpoint.
    """
    try:
        logger.info(f"Documents request for session: {session_id}")

        documents = get_session_documents(session_id)

        return {
            "session_id": session_id,
            "documents": documents
        }

    except Exception as e:
        logger.error(f"Error getting session documents: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Session dokümanları alınırken hata oluştu: {str(e)}"
        )

@app.get("/document/{session_id}/{document_id}")
async def get_document(session_id: str, document_id: str):
    """
    Belirli bir dokümanı döndüren endpoint.
    """
    try:
        logger.info(f"Document request: {document_id} for session: {session_id}")

        document = get_document_by_id(session_id, document_id)

        if not document:
            raise HTTPException(
                status_code=404,
                detail="Doküman bulunamadı"
            )

        return {
            "session_id": session_id,
            "document": document
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting document: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Doküman alınırken hata oluştu: {str(e)}"
        )

@app.post("/generate-analysis-document", response_model=DocumentResponse)
async def generate_analysis_document(request: DocumentRequest):
    """
    Session konuşma geçmişine dayalı gerçek analiz dokümanı oluşturan endpoint.
    Template yüklenmişse template kullanır, yoksa default format kullanır.
    """
    try:
        logger.info(f"Analysis document generation request received for session: {request.session_id}")

        status = get_analysis_status(request.session_id)

        if "error" in status:
            raise HTTPException(
                status_code=404,
                detail="Session bulunamadı veya konuşma geçmişi yok"
            )

        # Template kullanım kontrolü
        use_template = getattr(request, 'use_template', False)

        document_content = await generate_detailed_analysis_document(request.session_id, use_template)

        logger.info(f"Analysis document generated successfully for session: {request.session_id} (Template: {use_template})")

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


@app.post("/generate-visual-data")
async def generate_visual_data(request: ChatRequest):
    """
    Session konuşma geçmişine dayalı görsel bileşenler için dinamik veri üretir.
    """
    try:
        logger.info(f"Visual data generation request for session: {request.session_id}")

        visual_data = await generate_visual_data_from_session(request.session_id)

        # Visual data'yı detaylı logla
        logger.info(f"Generated visual data structure for session {request.session_id}:")
        logger.info(f"- orgChart: {len(visual_data.get('orgChart', {}).get('roles', []))} roles, {len(visual_data.get('orgChart', {}).get('connections', []))} connections")
        logger.info(f"- workflow: {len(visual_data.get('workflow', {}).get('steps', []))} steps, {len(visual_data.get('workflow', {}).get('connections', []))} connections")
        logger.info(f"- timeline: {len(visual_data.get('timeline', {}).get('phases', []))} phases")
        logger.info(f"- riskAnalysis: {len(visual_data.get('riskAnalysis', {}).get('risks', []))} risks")
        logger.info(f"- resources: {len(visual_data.get('resources', {}).get('distribution', []))} resource types")
        logger.info(f"- cost: {len(visual_data.get('cost', {}).get('timeline', []))} cost periods")

        # Cost verilerini detaylı logla
        cost_data = visual_data.get('cost', {}).get('timeline', [])
        if cost_data:
            logger.info(f"Cost timeline details:")
            for i, cost_item in enumerate(cost_data[:3]):  # İlk 3 ayı logla
                logger.info(f"  {cost_item.get('month', f'Period {i+1}')}: Planned={cost_item.get('planned', 'N/A')}, Actual={cost_item.get('actual', 'N/A')}")
        else:
            logger.warning(f"No cost data found in visual_data for session {request.session_id}")

        # Tam veri yapısını logla (sadece anahtarları)
        logger.info(f"Visual data keys: {list(visual_data.keys())}")

        logger.info(f"Visual data generated successfully for session: {request.session_id}")

        return {
            "session_id": request.session_id,
            "visual_data": visual_data
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in visual data generation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Görsel veri üretilirken hata oluştu: {str(e)}"
        )

@app.post("/upload-template")
async def upload_template(
    file: UploadFile = File(...),
    session_id: str = Form(...),
    is_template: str = Form("true")
):
    """
    Template dosyalarını yüklemek için endpoint.
    """
    try:
        logger.info(f"Template upload request for session: {session_id}, file: {file.filename}")

        # Dosya boyutu kontrolü (5MB limit template için)
        file_content = await file.read()
        if len(file_content) > 5 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="Template dosyası 5MB'dan büyük olamaz")

        # Template dosya tipini kontrol et
        allowed_extensions = ['.txt', '.md', '.docx', '.doc']
        file_extension = '.' + file.filename.split('.')[-1].lower() if '.' in file.filename else ''

        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Desteklenmeyen template formatı. İzin verilen formatlar: {', '.join(allowed_extensions)}"
            )

        # Template işleme işini chain.py'ye devret
        from core.chain import process_template_upload
        result = await process_template_upload(session_id, file_content, file.filename, file_extension)

        logger.info(f"Template processed successfully for session: {session_id}")

        return {
            "message": "Template başarıyla yüklendi",
            "session_id": session_id,
            "filename": file.filename,
            "template_loaded": True
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in template upload endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Template yüklenirken bir hata oluştu: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
