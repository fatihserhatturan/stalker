from fastapi import HTTPException
from core.schemas import DocumentRequest, DocumentResponse, ChatRequest
from core.business.document_manager import DocumentManager
from core.business.chat_manager import ChatManager
import logging

logger = logging.getLogger(__name__)

class DocumentHandler:
    def __init__(self, document_manager: DocumentManager, chat_manager: ChatManager):
        self.document_manager = document_manager
        self.chat_manager = chat_manager

    async def handle_generate_analysis_document(self, request: DocumentRequest) -> DocumentResponse:
        try:
            logger.info(f"Analysis document generation request received for session: {request.session_id}")

            status = self.chat_manager.get_analysis_status(request.session_id)

            if "error" in status:
                raise HTTPException(
                    status_code=404,
                    detail="Session bulunamadı veya konuşma geçmişi yok"
                )

            use_template = getattr(request, 'use_template', False)

            document_content = await self.document_manager.generate_analysis_document(
                request.session_id, use_template
            )

            logger.info(f"Analysis document generated successfully for session: {request.session_id} (Template: {use_template})")

            return DocumentResponse(
                document_content=document_content,
                session_id=request.session_id,
                document_type="markdown"
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in analysis document generation handler: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Analiz dokümanı oluşturulurken bir hata oluştu: {str(e)}"
            )

    async def handle_generate_visual_data(self, request: ChatRequest) -> dict:
        try:
            logger.info(f"Visual data generation request for session: {request.session_id}")

            visual_data = await self.document_manager.generate_visual_data(request.session_id)

            self._log_visual_data_details(visual_data, request.session_id)

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

    def _log_visual_data_details(self, visual_data: dict, session_id: str):
        logger.info(f"Generated visual data structure for session {session_id}:")
        logger.info(f"- orgChart: {len(visual_data.get('orgChart', {}).get('roles', []))} roles, {len(visual_data.get('orgChart', {}).get('connections', []))} connections")
        logger.info(f"- workflow: {len(visual_data.get('workflow', {}).get('steps', []))} steps, {len(visual_data.get('workflow', {}).get('connections', []))} connections")
        logger.info(f"- timeline: {len(visual_data.get('timeline', {}).get('phases', []))} phases")
        logger.info(f"- riskAnalysis: {len(visual_data.get('riskAnalysis', {}).get('risks', []))} risks")
        logger.info(f"- resources: {len(visual_data.get('resources', {}).get('distribution', []))} resource types")
        logger.info(f"- cost: {len(visual_data.get('cost', {}).get('timeline', []))} cost periods")

        cost_data = visual_data.get('cost', {}).get('timeline', [])
        if cost_data:
            logger.info(f"Cost timeline details:")
            for i, cost_item in enumerate(cost_data[:3]):
                logger.info(f"  {cost_item.get('month', f'Period {i+1}')}: Planned={cost_item.get('planned', 'N/A')}, Actual={cost_item.get('actual', 'N/A')}")
        else:
            logger.warning(f"No cost data found in visual_data for session {session_id}")

        logger.info(f"Visual data keys: {list(visual_data.keys())}")
