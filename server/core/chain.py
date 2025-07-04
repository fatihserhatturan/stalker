import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationSummaryBufferMemory
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from core.prompts import SYSTEM_PROMPT_TEMPLATE, DOCUMENT_GENERATION_PROMPT, DETAILED_ANALYSIS_PROMPT
import logging

load_dotenv()

logger = logging.getLogger(__name__)

# Session bazlı memory ve analiz durumu tracking
chat_histories = {}
analysis_context = {}

def get_memory_for_session(session_id: str) -> ConversationSummaryBufferMemory:
    """Verilen session_id için optimize edilmiş hafızayı alır veya oluşturur."""
    if session_id not in chat_histories:
        logger.info(f"Creating new memory for session: {session_id}")

        # Daha verimli memory kullanımı için SummaryBufferMemory
        chat_histories[session_id] = ConversationSummaryBufferMemory(
            llm=ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",  # Summary için daha hızlı model
                temperature=0.1,
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                convert_system_message_to_human=True
            ),
            memory_key="history",
            return_messages=True,
            max_token_limit=2000,  # Uzun konuşmalarda summary yapar
            moving_summary_buffer="Önceki konuşma özeti: "
        )

        # Analiz durumu tracking başlat
        analysis_context[session_id] = {
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
            "analysis_phase": "discovery"  # discovery, clarification, completion
        }

    return chat_histories[session_id]

def update_analysis_context(session_id: str, user_message: str, ai_response: str):
    """Analiz durumunu günceller ve hangi bilgilerin toplandığını takip eder."""
    if session_id not in analysis_context:
        return

    context = analysis_context[session_id]
    context["message_count"] += 1

    # Basit keyword analizi ile toplanan bilgileri işaretle
    user_lower = user_message.lower()

    if any(keyword in user_lower for keyword in ["proje", "sistem", "uygulama", "platform", "çözüm"]):
        context["collected_info"]["proje_tanimi"] = True

    if any(keyword in user_lower for keyword in ["kullanıcı", "müşteri", "hedef", "kitle", "departman"]):
        context["collected_info"]["hedef_kitle"] = True

    if any(keyword in user_lower for keyword in ["mevcut", "şu anda", "problem", "sorun", "eksik"]):
        context["collected_info"]["mevcut_durum"] = True

    if any(keyword in user_lower for keyword in ["teknoloji", "teknik", "sistem", "entegrasyon", "veritabanı"]):
        context["collected_info"]["teknik_gereksinimler"] = True

    if any(keyword in user_lower for keyword in ["başarı", "hedef", "kpi", "metrik", "ölçüm"]):
        context["collected_info"]["basari_kriterleri"] = True

    if any(keyword in user_lower for keyword in ["süre", "zaman", "bütçe", "kaynak", "tarih"]):
        context["collected_info"]["zaman_butce"] = True

    if any(keyword in user_lower for keyword in ["risk", "engel", "sorun", "zorluk", "kısıt"]):
        context["collected_info"]["riskler"] = True

    # Analiz fazını güncelle
    completed_areas = sum(context["collected_info"].values())

    if completed_areas < 3:
        context["analysis_phase"] = "discovery"
    elif completed_areas < 6:
        context["analysis_phase"] = "clarification"
    else:
        context["analysis_phase"] = "completion"

def get_enhanced_prompt(session_id: str) -> str:
    """Session durumuna göre optimize edilmiş prompt döndürür."""
    if session_id not in analysis_context:
        return SYSTEM_PROMPT_TEMPLATE

    context = analysis_context[session_id]
    collected = context["collected_info"]
    phase = context["analysis_phase"]

    # Eksik olan alanları belirle
    missing_areas = [area for area, collected_status in collected.items() if not collected_status]

    enhanced_prompt = SYSTEM_PROMPT_TEMPLATE + f"""

**Mevcut Analiz Durumu:**
- Toplanan Bilgi Alanları: {sum(collected.values())}/7
- Analiz Fazı: {phase}
- Eksik Alanlar: {', '.join(missing_areas) if missing_areas else 'Tümü tamamlandı'}
- Mesaj Sayısı: {context["message_count"]}

**Soru Stratejisi:**
"""

    if phase == "discovery":
        enhanced_prompt += """
- Temel proje anlayışını oluşturmaya odaklan
- Geniş sorular sorarak genel resmi çiz
- Kullanıcının ana motivasyonunu keşfet
"""
    elif phase == "clarification":
        enhanced_prompt += f"""
- Eksik alanları ({', '.join(missing_areas[:2])}) detaylandır
- Belirsiz noktalarda netleştirici sorular sor
- Spesifik örnekler ve senaryolar talep et
"""
    else:
        enhanced_prompt += """
- Son detayları tamamla
- Tutarlılık kontrolü yap
- Doküman hazırlığı için son kontroller
"""

    return enhanced_prompt

def get_conversational_chain():
    """Gelişmiş hafıza ve context-aware prompt ile yapılandırılmış chain döndürür."""

    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set!")

    try:
        model = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            temperature=0.7,
            google_api_key=google_api_key,
            convert_system_message_to_human=True
        )

        # Dinamik prompt template
        prompt = ChatPromptTemplate.from_messages([
            MessagesPlaceholder(variable_name="history"),
            ("human", "{enhanced_prompt}\n\nKullanıcı Mesajı: {input}")
        ])

        chain = prompt | model | StrOutputParser()

        logger.info("Enhanced conversational chain created successfully")
        return chain

    except Exception as e:
        logger.error(f"Error creating conversational chain: {str(e)}")
        raise e

async def process_conversation(session_id: str, user_message: str):
    """Konuşmayı işler ve context'i günceller."""
    try:
        memory = get_memory_for_session(session_id)
        chain = get_conversational_chain()

        # Enhanced prompt al
        enhanced_prompt = get_enhanced_prompt(session_id)

        result = await chain.ainvoke({
            "enhanced_prompt": enhanced_prompt,
            "input": user_message,
            "history": memory.chat_memory.messages
        })

        # Memory'yi güncelle
        memory.save_context(
            {"input": user_message},
            {"output": result}
        )

        # Analysis context'i güncelle
        update_analysis_context(session_id, user_message, result)

        logger.info(f"Conversation processed for session: {session_id}")
        return result

    except Exception as e:
        logger.error(f"Error processing conversation: {str(e)}")
        raise e

async def generate_detailed_analysis_document(session_id: str):
    """Session geçmişine dayalı detaylı analiz dokümanı oluşturur."""

    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set!")

    try:
        memory = get_memory_for_session(session_id)

        model = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            temperature=0.3,  # Daha tutarlı doküman için düşük temperature
            google_api_key=google_api_key,
            convert_system_message_to_human=True
        )

        # Konuşma geçmişini prompt'a dahil et
        conversation_history = ""
        for message in memory.chat_memory.messages:
            if hasattr(message, 'content'):
                role = "Kullanıcı" if message.type == "human" else "AI"
                conversation_history += f"{role}: {message.content}\n\n"

        detailed_prompt = f"""
{DETAILED_ANALYSIS_PROMPT}

**Konuşma Geçmişi:**
{conversation_history}

Yukarıdaki konuşma geçmişini analiz ederek topladığın bilgiler ile kapsamlı bir Ön Analiz Dokümanı hazırla.
Eksik bilgiler için [BİLGİ GEREKLİ] notasyonunu kullan.
"""

        prompt = ChatPromptTemplate.from_messages([
            ("human", detailed_prompt)
        ])

        chain = prompt | model | StrOutputParser()
        result = await chain.ainvoke({})

        logger.info(f"Detailed analysis document generated for session: {session_id}")
        return result

    except Exception as e:
        logger.error(f"Error generating detailed analysis: {str(e)}")
        raise e


def get_analysis_status(session_id: str) -> dict:
    """Session için analiz durumunu döndürür."""
    if session_id not in analysis_context:
        return {"error": "Session not found"}

    context = analysis_context[session_id]
    completion_rate = sum(context["collected_info"].values()) / 7 * 100

    return {
        "completion_rate": completion_rate,
        "phase": context["analysis_phase"],
        "message_count": context["message_count"],
        "collected_areas": context["collected_info"],
        "ready_for_document": completion_rate >= 70
    }
