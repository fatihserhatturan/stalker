from fastapi import HTTPException, UploadFile
from core.business.file_manager import FileManager
import logging

logger = logging.getLogger(__name__)

class FileHandler:
    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager

    async def handle_file_upload(self, file: UploadFile, session_id: str) -> dict:
        try:
            logger.info(f"File upload request for session: {session_id}, file: {file.filename}")

            file_content = await file.read()

            if len(file_content) > 10 * 1024 * 1024:
                raise HTTPException(status_code=413, detail="Dosya boyutu 10MB'dan büyük olamaz")

            analysis_result = await self.file_manager.process_uploaded_file(
                session_id, file_content, file.filename, is_template=False
            )

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
            logger.error(f"Error in file upload handler: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Dosya yüklenirken bir hata oluştu: {str(e)}"
            )

    async def handle_template_upload(self, file: UploadFile, session_id: str) -> dict:
        try:
            logger.info(f"Template upload request for session: {session_id}, file: {file.filename}")

            file_content = await file.read()

            if len(file_content) > 5 * 1024 * 1024:
                raise HTTPException(status_code=413, detail="Template dosyası 5MB'dan büyük olamaz")

            await self.file_manager.process_uploaded_file(
                session_id, file_content, file.filename, is_template=True
            )

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
            logger.error(f"Error in template upload handler: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Template yüklenirken bir hata oluştu: {str(e)}"
            )
