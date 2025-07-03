import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from core.prompts import SYSTEM_PROMPT_TEMPLATE, DOCUMENT_GENERATION_PROMPT
import logging

load_dotenv()

logger = logging.getLogger(__name__)

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

    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set!")

    try:
        model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            temperature=0.7,
            google_api_key=google_api_key,
            convert_system_message_to_human=True
        )

        prompt = ChatPromptTemplate.from_messages([
            MessagesPlaceholder(variable_name="history"),
            ("human", f"{SYSTEM_PROMPT_TEMPLATE}\n\nKullanıcı Mesajı: {{input}}")
        ])

        chain = prompt | model | StrOutputParser()

        logger.info("Conversational chain created successfully")
        return chain

    except Exception as e:
        logger.error(f"Error creating conversational chain: {str(e)}")
        raise e

async def generate_sample_document():
    """Rastgele örnek doküman oluşturan fonksiyon."""

    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set!")

    try:
        model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            temperature=0.8,
            google_api_key=google_api_key,
            convert_system_message_to_human=True
        )

        prompt = ChatPromptTemplate.from_messages([
            ("human", DOCUMENT_GENERATION_PROMPT)
        ])

        chain = prompt | model | StrOutputParser()

        result = await chain.ainvoke({})

        logger.info("Sample document generated successfully")
        return result

    except Exception as e:
        logger.error(f"Error generating sample document: {str(e)}")
        raise e
