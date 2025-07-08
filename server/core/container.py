from core.services.ai_service import AIService
from core.services.session_service import SessionService
from core.services.file_service import FileService
from core.services.prompt_service import PromptService
from core.services.visual_data_service import VisualDataService
from core.business.chat_manager import ChatManager
from core.business.file_manager import FileManager
from core.business.document_manager import DocumentManager

class Container:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Container, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def _initialize(self):
        if self._initialized:
            return

        self._session_service = SessionService()
        self._ai_service = AIService()
        self._file_service = FileService()
        self._prompt_service = PromptService(self._session_service)
        self._visual_data_service = VisualDataService()

        self._chat_manager = ChatManager(
            self._ai_service,
            self._session_service,
            self._prompt_service
        )

        self._file_manager = FileManager(
            self._ai_service,
            self._session_service,
            self._file_service
        )

        self._document_manager = DocumentManager(
            self._ai_service,
            self._session_service,
            self._visual_data_service
        )

        self._initialized = True

    @property
    def session_service(self):
        self._initialize()
        return self._session_service

    @property
    def ai_service(self):
        self._initialize()
        return self._ai_service

    @property
    def file_service(self):
        self._initialize()
        return self._file_service

    @property
    def prompt_service(self):
        self._initialize()
        return self._prompt_service

    @property
    def visual_data_service(self):
        self._initialize()
        return self._visual_data_service

    @property
    def chat_manager(self):
        self._initialize()
        return self._chat_manager

    @property
    def file_manager(self):
        self._initialize()
        return self._file_manager

    @property
    def document_manager(self):
        self._initialize()
        return self._document_manager

def get_container():
    return Container()
