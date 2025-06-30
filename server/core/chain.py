import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from core.prompts import SYSTEM_PROMPT_TEMPLATE
import logging

# .env dosyasını yükle
load_dotenv()

logger = logging.getLogger(__name__)

# Sohbet hafızasını yönetmek için global bir sözlük
chat_histories = {}

def get_memory_for_session(session_id: str) -> ConversationBufferMemory:
    """Verilen session_id için hafızayı alır veya oluşturur."""
    if session_id not in chat_histories:
        logger.info(f"Creating new memory for session: {session_id}")
        chat_histories[session_id] = ConversationBufferMemory(
            memory_key="history",
            return_messages=True
        )
    return chat_histories[session_id]

def get_conversational_chain():
    """Hafıza ve prompt ile yapılandırılmış bir chain döndürür."""

    # Google API anahtarını kontrol et
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set!")

    try:
        # 1. Modeli tanımla
        model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            temperature=0.7,
            google_api_key=google_api_key
        )

        # 2. Prompt şablonunu oluştur
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT_TEMPLATE),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])

        # 3. Chain'i oluştur - LLMChain yerine | operatörü kullan
        chain = prompt | model | StrOutputParser()

        logger.info("Conversational chain created successfully")
        return chain

    except Exception as e:
        logger.error(f"Error creating conversational chain: {str(e)}")
        raise e
