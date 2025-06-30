from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from core.prompts import SYSTEM_PROMPT_TEMPLATE

load_dotenv()

# Sohbet hafızasını yönetmek için global bir sözlük (basit bir session yönetimi)
# Production'da bu Redis gibi bir veritabanı olmalıdır.
chat_histories = {}

def get_memory_for_session(session_id: str) -> ConversationBufferMemory:
    """Verilen session_id için hafızayı alır veya oluşturur."""
    if session_id not in chat_histories:
        chat_histories[session_id] = ConversationBufferMemory(
            memory_key="history", return_messages=True
        )
    return chat_histories[session_id]

def get_conversational_chain() -> LLMChain:
    """Hafıza ve prompt ile yapılandırılmış bir LLM zinciri döndürür."""

    # 1. Modeli tanımla
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.8)

    # 2. Dinamik Prompt Şablonunu Oluştur
    # Bu şablon, sistem mesajını, sohbet geçmişini ve kullanıcı girdisini birleştirir.
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT_TEMPLATE),
        MessagesPlaceholder(variable_name="history"), # Hafızadaki mesajlar buraya gelecek
        ("human", "{input}") # Kullanıcının son mesajı buraya gelecek
    ])

    # 3. LLM Zincirini Oluştur
    # Bu zincir, prompt'u, modeli ve hafızayı birbirine bağlar.
    chain = LLMChain(
        llm=model,
        prompt=prompt,
        verbose=True, # Terminalde zincirin ne yaptığını görmek için
    )

    return chain
