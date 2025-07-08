import docx
import PyPDF2
from io import BytesIO
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FileService:
    ALLOWED_EXTENSIONS = ['.txt', '.md', '.pdf', '.docx', '.doc']
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    MAX_TEMPLATE_SIZE = 5 * 1024 * 1024  # 5MB

    def validate_file(self, filename: str, file_size: int, is_template: bool = False) -> bool:
        max_size = self.MAX_TEMPLATE_SIZE if is_template else self.MAX_FILE_SIZE

        if file_size > max_size:
            max_mb = max_size / (1024 * 1024)
            raise ValueError(f"Dosya boyutu {max_mb}MB'dan büyük olamaz")

        file_extension = '.' + filename.split('.')[-1].lower() if '.' in filename else ''

        if file_extension not in self.ALLOWED_EXTENSIONS:
            raise ValueError(f"Desteklenmeyen dosya formatı. İzin verilen formatlar: {', '.join(self.ALLOWED_EXTENSIONS)}")

        return True

    def extract_text_from_file(self, file_content: bytes, filename: str) -> str:
        try:
            file_extension = '.' + filename.split('.')[-1].lower() if '.' in filename else ''

            if file_extension in ['.txt', '.md']:
                return self._extract_text_file(file_content)
            elif file_extension == '.pdf':
                return self._extract_pdf_file(file_content)
            elif file_extension in ['.docx', '.doc']:
                return self._extract_word_file(file_content)
            else:
                raise ValueError(f"Desteklenmeyen dosya formatı: {file_extension}")

        except Exception as e:
            logger.error(f"Error extracting text from file {filename}: {str(e)}")
            raise e

    def _extract_text_file(self, file_content: bytes) -> str:
        return file_content.decode('utf-8')

    def _extract_pdf_file(self, file_content: bytes) -> str:
        pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text

    def _extract_word_file(self, file_content: bytes) -> str:
        doc = docx.Document(BytesIO(file_content))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text

    def create_file_info(self, filename: str, content: str, file_extension: str, is_template: bool = False) -> dict:
        return {
            "filename": filename,
            "content": content,
            "uploaded_at": datetime.now().isoformat(),
            "file_type": file_extension,
            "is_template": is_template
        }

    def get_file_extension(self, filename: str) -> str:
        return '.' + filename.split('.')[-1].lower() if '.' in filename else ''
