from core.services.ai_service import AIService
from core.services.session_service import SessionService
from core.services.visual_data_service import VisualDataService
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DocumentManager:
    def __init__(self, ai_service: AIService = None, session_service: SessionService = None,
                 visual_data_service: VisualDataService = None):
        self.ai_service = ai_service or AIService()
        self.session_service = session_service or SessionService()
        self.visual_data_service = visual_data_service or VisualDataService()

    async def generate_analysis_document(self, session_id: str, use_template: bool = False) -> str:
        try:
            conversation_history = self.session_service.get_conversation_history(session_id)
            uploaded_files_content = self.session_service.get_uploaded_files_content(session_id)
            template_content = self.session_service.get_template_content(session_id) if use_template else None

            document_content = await self.ai_service.generate_analysis_document(
                conversation_history=conversation_history,
                uploaded_files_content=uploaded_files_content,
                template_content=template_content,
                use_template=use_template
            )

            document_content = self._clean_document_content(document_content)

            document_title = self._generate_document_title(use_template)

            self.session_service.save_document_to_session(session_id, document_content, document_title)

            logger.info(f"Analysis document generated and saved for session: {session_id} (Template used: {use_template})")
            return document_content

        except Exception as e:
            logger.error(f"Error generating analysis document: {str(e)}")
            raise e

    async def generate_visual_data(self, session_id: str) -> dict:
        try:
            if session_id not in self.session_service.chat_histories:
                raise ValueError(f"Session {session_id} bulunamadı")

            conversation_history = self.session_service.get_conversation_history(session_id)

            ai_response_text = await self.ai_service.generate_visual_data(conversation_history)

            visual_data = self.visual_data_service.parse_visual_data(ai_response_text)

            logger.info(f"Visual data successfully generated for session: {session_id}")
            return visual_data

        except Exception as e:
            logger.error(f"Error generating visual data: {str(e)}")
            return self.visual_data_service.generate_smart_fallback_data(
                self.session_service.get_conversation_history(session_id)
            )

    def _clean_document_content(self, content: str) -> str:
        lines = content.split('\n')
        document_start = -1

        for i, line in enumerate(lines):
            if 'ÖN ANALİZ DOKÜMANI' in line or line.strip().startswith('# '):
                document_start = i
                break

        if document_start >= 0:
            content = '\n'.join(lines[document_start:])

        return content.strip()

    def _generate_document_title(self, use_template: bool) -> str:
        timestamp = datetime.now().strftime('%d.%m.%Y %H:%M')

        if use_template:
            return f"Template Bazlı Analiz Dokümanı - {timestamp}"
        else:
            return f"Proje Analiz Dokümanı - {timestamp}"
