from core.services.ai_service import AIService
from core.services.session_service import SessionService
from core.services.prompt_service import PromptService
import logging

logger = logging.getLogger(__name__)

class ChatManager:
    def __init__(self, ai_service: AIService = None, session_service: SessionService = None,
                 prompt_service: PromptService = None):
        self.ai_service = ai_service or AIService()
        self.session_service = session_service or SessionService()
        self.prompt_service = prompt_service or PromptService(self.session_service)

    async def process_conversation(self, session_id: str, user_message: str) -> str:
        try:
            memory = self.session_service.get_memory_for_session(session_id)
            enhanced_prompt = self.prompt_service.get_enhanced_prompt(session_id)

            result = await self.ai_service.process_conversation(
                enhanced_prompt=enhanced_prompt,
                user_message=user_message,
                history=memory.chat_memory.messages
            )

            self.session_service.save_context(session_id, user_message, result)
            self.session_service.update_analysis_context(session_id, user_message, result)

            logger.info(f"Conversation processed for session: {session_id}")
            return result

        except Exception as e:
            logger.error(f"Error processing conversation: {str(e)}")
            raise e

    def get_analysis_status(self, session_id: str) -> dict:
        return self.session_service.get_analysis_status(session_id)

    def get_session_documents(self, session_id: str) -> list:
        return self.session_service.get_session_documents(session_id)

    def get_document_by_id(self, session_id: str, document_id: str) -> dict:
        return self.session_service.get_document_by_id(session_id, document_id)
