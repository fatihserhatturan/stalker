from fastapi import HTTPException
from core.schemas import ChatRequest, ChatResponse
from core.business.chat_manager import ChatManager
import logging

logger = logging.getLogger(__name__)

class ChatHandler:
    def __init__(self, chat_manager: ChatManager):
        self.chat_manager = chat_manager

    async def handle_chat(self, request: ChatRequest) -> ChatResponse:
        try:
            logger.info(f"Chat request received for session: {request.session_id}")

            result = await self.chat_manager.process_conversation(request.session_id, request.message)

            logger.info(f"Chat response generated for session: {request.session_id}")

            return ChatResponse(
                answer=result,
                session_id=request.session_id
            )

        except Exception as e:
            logger.error(f"Error in chat handler: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Sohbet işlenirken bir hata oluştu: {str(e)}"
            )

    async def handle_analysis_status(self, session_id: str) -> dict:
        try:
            logger.info(f"Analysis status request for session: {session_id}")

            status = self.chat_manager.get_analysis_status(session_id)

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

    async def handle_session_documents(self, session_id: str) -> dict:
        try:
            logger.info(f"Documents request for session: {session_id}")

            documents = self.chat_manager.get_session_documents(session_id)

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

    async def handle_get_document(self, session_id: str, document_id: str) -> dict:
        try:
            logger.info(f"Document request: {document_id} for session: {session_id}")

            document = self.chat_manager.get_document_by_id(session_id, document_id)

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
