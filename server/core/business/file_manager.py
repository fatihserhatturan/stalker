from core.services.ai_service import AIService
from core.services.session_service import SessionService
from core.services.file_service import FileService
import logging

logger = logging.getLogger(__name__)

class FileManager:
    def __init__(self, ai_service: AIService = None, session_service: SessionService = None,
                 file_service: FileService = None):
        self.ai_service = ai_service or AIService()
        self.session_service = session_service or SessionService()
        self.file_service = file_service or FileService()

    async def process_uploaded_file(self, session_id: str, file_content: bytes,
                                  filename: str, is_template: bool = False) -> str:
        try:
            file_extension = self.file_service.get_file_extension(filename)

            self.file_service.validate_file(filename, len(file_content), is_template)

            extracted_text = self.file_service.extract_text_from_file(file_content, filename)

            file_info = self.file_service.create_file_info(
                filename, extracted_text, file_extension, is_template
            )

            self.session_service.add_uploaded_file(session_id, file_info)

            if not is_template:
                analysis_result = await self.ai_service.analyze_file(filename, extracted_text)

                self.session_service.save_context(
                    session_id,
                    f"Dosya yüklendi: {filename}",
                    f"Dosya analizi tamamlandı:\n\n{analysis_result}"
                )

                logger.info(f"File processed and analyzed for session: {session_id}")
                return analysis_result
            else:
                logger.info(f"Template processed for session: {session_id}")
                return "Template başarıyla yüklendi"

        except Exception as e:
            logger.error(f"Error processing uploaded file: {str(e)}")
            raise e
