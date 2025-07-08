from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationSummaryBufferMemory
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)

class SessionService:
    def __init__(self):
        self.chat_histories = {}
        self.analysis_context = {}
        self.session_documents = {}
        self.uploaded_files = {}

    def get_memory_for_session(self, session_id: str) -> ConversationSummaryBufferMemory:
        if session_id not in self.chat_histories:
            logger.info(f"Creating new memory for session: {session_id}")

            self.chat_histories[session_id] = ConversationSummaryBufferMemory(
                llm=ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash",
                    temperature=0.1,
                    google_api_key=os.getenv("GOOGLE_API_KEY"),
                    convert_system_message_to_human=True
                ),
                memory_key="history",
                return_messages=True,
                max_token_limit=2000,
                moving_summary_buffer="Önceki konuşma özeti: "
            )

            self._initialize_analysis_context(session_id)

        return self.chat_histories[session_id]

    def _initialize_analysis_context(self, session_id: str):
        self.analysis_context[session_id] = {
            "collected_info": {
                "proje_tanimi": False,
                "hedef_kitle": False,
                "mevcut_durum": False,
                "teknik_gereksinimler": False,
                "basari_kriterleri": False,
                "zaman_butce": False,
                "riskler": False
            },
            "message_count": 0,
            "analysis_phase": "discovery",
            "has_uploaded_files": False
        }

        self.session_documents[session_id] = []
        self.uploaded_files[session_id] = []

    def save_context(self, session_id: str, user_input: str, ai_output: str):
        memory = self.get_memory_for_session(session_id)
        memory.save_context(
            {"input": user_input},
            {"output": ai_output}
        )

    def update_analysis_context(self, session_id: str, user_message: str, ai_response: str):
        if session_id not in self.analysis_context:
            return

        context = self.analysis_context[session_id]
        context["message_count"] += 1

        user_lower = user_message.lower()

        keyword_mapping = {
            "proje_tanimi": ["proje", "sistem", "uygulama", "platform", "çözüm"],
            "hedef_kitle": ["kullanıcı", "müşteri", "hedef", "kitle", "departman"],
            "mevcut_durum": ["mevcut", "şu anda", "problem", "sorun", "eksik"],
            "teknik_gereksinimler": ["teknoloji", "teknik", "sistem", "entegrasyon", "veritabanı"],
            "basari_kriterleri": ["başarı", "hedef", "kpi", "metrik", "ölçüm"],
            "zaman_butce": ["süre", "zaman", "bütçe", "kaynak", "tarih"],
            "riskler": ["risk", "engel", "sorun", "zorluk", "kısıt"]
        }

        for category, keywords in keyword_mapping.items():
            if any(keyword in user_lower for keyword in keywords):
                context["collected_info"][category] = True

        completed_areas = sum(context["collected_info"].values())

        if completed_areas < 3:
            context["analysis_phase"] = "discovery"
        elif completed_areas < 6:
            context["analysis_phase"] = "clarification"
        else:
            context["analysis_phase"] = "completion"

    def get_analysis_status(self, session_id: str) -> dict:
        if session_id not in self.analysis_context:
            return {"error": "Session not found"}

        context = self.analysis_context[session_id]
        completion_rate = sum(context["collected_info"].values()) / 7 * 100

        documents = self.get_session_documents(session_id)

        return {
            "completion_rate": completion_rate,
            "phase": context["analysis_phase"],
            "message_count": context["message_count"],
            "collected_areas": context["collected_info"],
            "ready_for_document": completion_rate >= 70,
            "documents": documents,
            "has_uploaded_files": context.get("has_uploaded_files", False),
            "uploaded_files_count": len(self.uploaded_files.get(session_id, []))
        }

    def save_document_to_session(self, session_id: str, document_content: str, document_title: str = None):
        if session_id not in self.session_documents:
            self.session_documents[session_id] = []

        document = {
            "id": f"doc_{len(self.session_documents[session_id]) + 1}_{int(datetime.now().timestamp())}",
            "title": document_title or f"Analiz Dokümanı {len(self.session_documents[session_id]) + 1}",
            "content": document_content,
            "created_at": datetime.now().isoformat(),
            "type": "analysis_document"
        }

        self.session_documents[session_id].append(document)
        logger.info(f"Document saved to session {session_id}: {document['id']}")
        return document

    def get_session_documents(self, session_id: str) -> list:
        return self.session_documents.get(session_id, [])

    def get_document_by_id(self, session_id: str, document_id: str) -> dict:
        documents = self.session_documents.get(session_id, [])
        for doc in documents:
            if doc["id"] == document_id:
                return doc
        return None

    def add_uploaded_file(self, session_id: str, file_info: dict):
        if session_id not in self.uploaded_files:
            self.uploaded_files[session_id] = []

        self.uploaded_files[session_id].append(file_info)

        if session_id in self.analysis_context:
            self.analysis_context[session_id]["has_uploaded_files"] = True

    def get_uploaded_files(self, session_id: str) -> list:
        return self.uploaded_files.get(session_id, [])

    def get_conversation_history(self, session_id: str) -> str:
        memory = self.get_memory_for_session(session_id)
        conversation_history = ""

        for message in memory.chat_memory.messages:
            if hasattr(message, 'content'):
                role = "Kullanıcı" if message.type == "human" else "AI"
                conversation_history += f"{role}: {message.content}\n\n"

        return conversation_history

    def get_uploaded_files_content(self, session_id: str) -> str:
        uploaded_files_content = ""
        files = self.get_uploaded_files(session_id)

        if files:
            uploaded_files_content = "\n**Yüklenen Dosyalar:**\n"
            for file_info in files:
                if not file_info.get("is_template", False):
                    uploaded_files_content += f"\n**Dosya: {file_info['filename']}**\n"
                    uploaded_files_content += f"İçerik: {file_info['content'][:2000]}...\n"

        return uploaded_files_content

    def get_template_content(self, session_id: str) -> str:
        files = self.get_uploaded_files(session_id)

        for file_info in files:
            if file_info.get("is_template", False):
                return file_info['content']

        return ""
