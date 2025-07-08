import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationSummaryBufferMemory
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.schema import HumanMessage
from core.prompts import SYSTEM_PROMPT_TEMPLATE, DOCUMENT_GENERATION_PROMPT, DETAILED_ANALYSIS_PROMPT, FILE_ANALYSIS_PROMPT
import logging
from datetime import datetime
import docx
import PyPDF2
from io import BytesIO

load_dotenv()

logger = logging.getLogger(__name__)

# Session bazlı memory, analiz durumu ve doküman tracking
chat_histories = {}
analysis_context = {}
session_documents = {}
uploaded_files = {}  # Yüklenen dosyaları saklar

def get_memory_for_session(session_id: str) -> ConversationSummaryBufferMemory:
    """Verilen session_id için optimize edilmiş hafızayı alır veya oluşturur."""
    if session_id not in chat_histories:
        logger.info(f"Creating new memory for session: {session_id}")

        chat_histories[session_id] = ConversationSummaryBufferMemory(
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
            "analysis_phase": "discovery",
            "has_uploaded_files": False
        }

        session_documents[session_id] = []
        uploaded_files[session_id] = []

    return chat_histories[session_id]

def save_document_to_session(session_id: str, document_content: str, document_title: str = None):
    """Dokümanı session'a kaydeder."""
    if session_id not in session_documents:
        session_documents[session_id] = []

    document = {
        "id": f"doc_{len(session_documents[session_id]) + 1}_{int(datetime.now().timestamp())}",
        "title": document_title or f"Analiz Dokümanı {len(session_documents[session_id]) + 1}",
        "content": document_content,
        "created_at": datetime.now().isoformat(),
        "type": "analysis_document"
    }

    session_documents[session_id].append(document)
    logger.info(f"Document saved to session {session_id}: {document['id']}")
    return document

def get_session_documents(session_id: str) -> list:
    """Session'a ait dokümanları döndürür."""
    return session_documents.get(session_id, [])

def get_document_by_id(session_id: str, document_id: str) -> dict:
    """Session'dan belirli bir dokümanı döndürür."""
    documents = session_documents.get(session_id, [])
    for doc in documents:
        if doc["id"] == document_id:
            return doc
    return None

def extract_text_from_file(file_content: bytes, filename: str, file_extension: str) -> str:
    """Dosyadan metin çıkarır."""
    try:
        if file_extension in ['.txt', '.md']:
            return file_content.decode('utf-8')

        elif file_extension == '.pdf':
            pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text

        elif file_extension in ['.docx', '.doc']:
            doc = docx.Document(BytesIO(file_content))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text

        else:
            raise ValueError(f"Desteklenmeyen dosya formatı: {file_extension}")

    except Exception as e:
        logger.error(f"Error extracting text from file: {str(e)}")
        raise e

async def process_uploaded_file(session_id: str, file_content: bytes, filename: str, file_extension: str):
    """Yüklenen dosyayı analiz eder ve session'a ekler."""
    try:
        # Dosyadan metin çıkar
        extracted_text = extract_text_from_file(file_content, filename, file_extension)

        # Dosya bilgilerini session'a kaydet
        if session_id not in uploaded_files:
            uploaded_files[session_id] = []

        file_info = {
            "filename": filename,
            "content": extracted_text,
            "uploaded_at": datetime.now().isoformat(),
            "file_type": file_extension
        }

        uploaded_files[session_id].append(file_info)

        # Analysis context'i güncelle
        if session_id in analysis_context:
            analysis_context[session_id]["has_uploaded_files"] = True

        # Dosyayı AI ile analiz et
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set!")

        model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.3,
            google_api_key=google_api_key,
            convert_system_message_to_human=True
        )

        analysis_prompt = f"""
{FILE_ANALYSIS_PROMPT}

**Dosya Adı:** {filename}
**Dosya İçeriği:**
{extracted_text[:8000]}  # İlk 8000 karakteri analiz et
"""

        prompt = ChatPromptTemplate.from_messages([
            ("human", analysis_prompt)
        ])

        chain = prompt | model | StrOutputParser()
        analysis_result = await chain.ainvoke({})

        # Analiz sonucunu memory'ye ekle
        memory = get_memory_for_session(session_id)
        memory.save_context(
            {"input": f"Dosya yüklendi: {filename}"},
            {"output": f"Dosya analizi tamamlandı:\n\n{analysis_result}"}
        )

        logger.info(f"File processed and analyzed for session: {session_id}")
        return analysis_result

    except Exception as e:
        logger.error(f"Error processing uploaded file: {str(e)}")
        raise e

def update_analysis_context(session_id: str, user_message: str, ai_response: str):
    """Analiz durumunu günceller ve hangi bilgilerin toplandığını takip eder."""
    if session_id not in analysis_context:
        return

    context = analysis_context[session_id]
    context["message_count"] += 1

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
    has_files = context.get("has_uploaded_files", False)

    missing_areas = [area for area, collected_status in collected.items() if not collected_status]

    enhanced_prompt = SYSTEM_PROMPT_TEMPLATE + f"""

**Mevcut Analiz Durumu:**
- Toplanan Bilgi Alanları: {sum(collected.values())}/7
- Analiz Fazı: {phase}
- Eksik Alanlar: {', '.join(missing_areas) if missing_areas else 'Tümü tamamlandı'}
- Mesaj Sayısı: {context["message_count"]}
- Yüklenen Dosya Var: {'Evet' if has_files else 'Hayır'}

**Soru Stratejisi:**
"""

    if has_files:
        enhanced_prompt += """
- Yüklenen dosyalardaki bilgileri dikkate al
- Eksik bilgileri dosya içeriğine dayanarak netleştir
- Dosyadaki teknik detayları analiz sonuçlarında kullan
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

    # Yüklenen dosya bilgilerini ekle
    if has_files and session_id in uploaded_files:
        enhanced_prompt += f"""

**Yüklenen Dosyalar:**
"""
        for file_info in uploaded_files[session_id]:
            enhanced_prompt += f"- {file_info['filename']} ({file_info['file_type']}) - {file_info['uploaded_at']}\n"

    return enhanced_prompt

def get_conversational_chain():
    """Gelişmiş hafıza ve context-aware prompt ile yapılandırılmış chain döndürür."""

    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set!")

    try:
        model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7,
            google_api_key=google_api_key,
            convert_system_message_to_human=True
        )

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

        enhanced_prompt = get_enhanced_prompt(session_id)

        result = await chain.ainvoke({
            "enhanced_prompt": enhanced_prompt,
            "input": user_message,
            "history": memory.chat_memory.messages
        })

        memory.save_context(
            {"input": user_message},
            {"output": result}
        )

        update_analysis_context(session_id, user_message, result)

        logger.info(f"Conversation processed for session: {session_id}")
        return result

    except Exception as e:
        logger.error(f"Error processing conversation: {str(e)}")
        raise e

async def generate_detailed_analysis_document(session_id: str, use_template: bool = False):
    """Session geçmişine dayalı detaylı analiz dokümanı oluşturur ve session'a kaydeder."""

    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set!")

    try:
        memory = get_memory_for_session(session_id)

        model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.3,
            google_api_key=google_api_key,
            convert_system_message_to_human=True
        )

        conversation_history = ""
        for message in memory.chat_memory.messages:
            if hasattr(message, 'content'):
                role = "Kullanıcı" if message.type == "human" else "AI"
                conversation_history += f"{role}: {message.content}\n\n"

        # Template kontrolü
        template_content = ""
        template_used = False

        if use_template and session_id in uploaded_files:
            for file_info in uploaded_files[session_id]:
                if file_info.get("is_template", False):
                    template_content = file_info['content']
                    template_used = True
                    logger.info(f"Template found and will be used: {file_info['filename']}")
                    break

        # Yüklenen proje dosyalarını ekle (template hariç)
        uploaded_files_content = ""
        if session_id in uploaded_files and uploaded_files[session_id]:
            uploaded_files_content = "\n**Yüklenen Dosyalar:**\n"
            for file_info in uploaded_files[session_id]:
                if not file_info.get("is_template", False):  # Template dosyasını hariç tut
                    uploaded_files_content += f"\n**Dosya: {file_info['filename']}**\n"
                    uploaded_files_content += f"İçerik: {file_info['content'][:2000]}...\n"

        # Template kullanılacaksa özel prompt, yoksa prompts.py'daki template
        if template_used and template_content:
            detailed_prompt = f"""
SADECE template formatını kullanarak analiz dokümanı üret. Hiçbir ek açıklama veya giriş cümlesi ekleme.

TEMPLATE:
{template_content[:2000]}

KONUŞMA:
{conversation_history[:1000]}

Template formatını koru, boş alanları konuşmadaki bilgilerle doldur. SADECE doküman içeriğini çıktı olarak ver.
"""
            document_title = f"Template Bazlı Analiz Dokümanı - {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        else:
            # prompts.py'daki DETAILED_ANALYSIS_PROMPT template'ini kullan
            detailed_prompt = f"""
{DETAILED_ANALYSIS_PROMPT}

**Konuşma Geçmişi:**
{conversation_history}

{uploaded_files_content}

Yukarıdaki konuşma geçmişini ve yüklenen dosyaları analiz ederek topladığın bilgiler ile kapsamlı bir Ön Analiz Dokümanı hazırla.
Eksik bilgiler için [BİLGİ GEREKLİ] notasyonunu kullan.
SADECE doküman markdown içeriğini çıktı olarak ver, hiçbir ek açıklama ekleme.
"""
            document_title = f"Proje Analiz Dokümanı - {datetime.now().strftime('%d.%m.%Y %H:%M')}"

        prompt = ChatPromptTemplate.from_messages([
            ("human", detailed_prompt)
        ])

        chain = prompt | model | StrOutputParser()
        result = await chain.ainvoke({})

        # Sonuçtan sadece markdown dokümanı kısmını al
        # Eğer model ekstra metin eklediyse temizle
        lines = result.split('\n')
        document_start = -1

        # Doküman başlığını bul
        for i, line in enumerate(lines):
            if 'ÖN ANALİZ DOKÜMANI' in line or line.strip().startswith('# ') or template_used:
                document_start = i
                break

        if document_start >= 0:
            result = '\n'.join(lines[document_start:])

        # Başında ve sonunda gereksiz metinleri temizle
        result = result.strip()

        saved_document = save_document_to_session(session_id, result, document_title)

        logger.info(f"Detailed analysis document generated and saved for session: {session_id} (Template used: {template_used})")
        return result

    except Exception as e:
        logger.error(f"Error generating detailed analysis: {str(e)}")
        raise e

async def generate_visual_data_from_session(session_id: str):
    """Session geçmişine dayalı görsel bileşenler için dinamik veri üretir."""

    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set!")

    try:
        # Session'ın varlığını kontrol et
        if session_id not in chat_histories:
            raise ValueError(f"Session {session_id} bulunamadı")

        memory = get_memory_for_session(session_id)

        model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.1,
            google_api_key=google_api_key,
            convert_system_message_to_human=True
        )

        # Konuşma geçmişini al
        conversation_history = ""
        for message in memory.chat_memory.messages:
            if hasattr(message, 'content'):
                role = "Kullanıcı" if message.type == "human" else "AI"
                conversation_history += f"{role}: {message.content}\n\n"

        # Yüklenen dosya bilgilerini ekle
        uploaded_files_content = ""
        if session_id in uploaded_files and uploaded_files[session_id]:
            uploaded_files_content = "\n**Yüklenen Dosyalar:**\n"
            for file_info in uploaded_files[session_id]:
                uploaded_files_content += f"\n**Dosya: {file_info['filename']}**\n"
                uploaded_files_content += f"İçerik: {file_info['content'][:2000]}...\n"

        # JSON parse et
        import json
        try:
            # AI'dan veri iste - doğru LangChain kullanımı
            simple_prompt = f"""
Proje bilgilerine dayalı JSON veri oluştur:

PROJE BİLGİLERİ:
{conversation_history[:2000]}

ÇIKTİ: Sadece geçerli JSON formatında yanıt ver. MUTLAKA bu EXACT formatı kullan:

{{
  "orgChart": {{
    "roles": [{{"id": "pm", "title": "Proje Müdürü", "color": "#3b82f6"}}],
    "connections": [{{"from": "pm", "to": "dev"}}]
  }},
  "workflow": {{
    "steps": [{{"id": "step1", "title": "Analiz", "color": "#3b82f6"}}],
    "connections": [{{"from": "step1", "to": "step2"}}]
  }},
  "timeline": {{
    "phases": [{{"name": "Analiz", "planned": 15, "actual": 18}}]
  }},
  "riskAnalysis": {{
    "risks": [{{"name": "Risk1", "probability": 3, "impact": 4, "color": "#ef4444"}}]
  }},
  "resources": {{
    "distribution": [{{"role": "Developer", "percentage": 50, "color": "#3b82f6"}}]
  }},
  "cost": {{
    "timeline": [{{"month": "Ay 1", "planned": 50000, "actual": 55000}}]
  }}
}}

ÖNEMLİ: cost.timeline array'inde MUTLAKA "month", "planned", "actual" anahtarlarını kullan!
"""

            # LangChain ChatGoogleGenerativeAI için doğru kullanım
            messages = [HumanMessage(content=simple_prompt)]
            ai_response = await model.agenerate([messages])
            result_text = ai_response.generations[0][0].text.strip()

            logger.info(f"AI response received: {result_text[:200]}...")

            # JSON'u bul ve parse et
            json_start = result_text.find('{')
            json_end = result_text.rfind('}') + 1

            if json_start == -1 or json_end == 0:
                raise json.JSONDecodeError("JSON bulunamadı", result_text, 0)

            clean_json = result_text[json_start:json_end]
            visual_data = json.loads(clean_json)

            # Veri doğrulaması
            required_keys = ['orgChart', 'workflow', 'timeline', 'riskAnalysis', 'resources', 'cost']
            if not all(key in visual_data for key in required_keys):
                raise ValueError("Eksik JSON anahtarları")

            logger.info(f"Visual data successfully generated from AI for session: {session_id}")
            return visual_data

        except Exception as e:
            logger.error(f"AI data generation failed, using fallback: {str(e)}")
            logger.error(f"AI response was: {result_text if 'result_text' in locals() else 'No response'}")

            # Konuşma geçmişine dayalı akıllı fallback
            fallback_data = generate_smart_fallback_data(conversation_history)
            return fallback_data

    except Exception as e:
        logger.error(f"Error generating visual data: {str(e)}")
        raise e

def generate_smart_fallback_data(conversation_history: str):
    """Konuşma geçmişine dayalı akıllı fallback veri oluştur"""

    # Konuşmadaki anahtar kelimeleri analiz et
    text_lower = conversation_history.lower()

    # Proje türünü belirle
    is_ecommerce = any(keyword in text_lower for keyword in ['e-ticaret', 'online', 'ödeme', 'sepet', 'ürün'])
    is_mobile = any(keyword in text_lower for keyword in ['mobil', 'android', 'ios', 'uygulama'])
    is_web = any(keyword in text_lower for keyword in ['web', 'website', 'react', 'vue'])

    # Ekip büyüklüğünü tahmin et
    team_indicators = {
        'küçük': ['freelance', '1-2', 'tek', 'basit'],
        'orta': ['3-5', 'ekip', 'orta', 'normal'],
        'büyük': ['enterprise', 'büyük', '10+', 'kurumsal']
    }

    team_size = 'orta'  # varsayılan
    for size, indicators in team_indicators.items():
        if any(indicator in text_lower for indicator in indicators):
            team_size = size
            break

    # Proje süresini tahmin et
    duration_months = 6  # varsayılan
    if any(word in text_lower for word in ['hızlı', 'acil', '1 ay', '2 ay']):
        duration_months = 2
    elif any(word in text_lower for word in ['6 ay', 'altı ay']):
        duration_months = 6
    elif any(word in text_lower for word in ['1 yıl', 'uzun']):
        duration_months = 12

    # Bütçeyi tahmin et
    budget_per_month = 100000  # varsayılan TL
    if any(word in text_lower for word in ['600.000', '600000', 'altı yüz bin']):
        budget_per_month = 100000
    elif any(word in text_lower for word in ['küçük', 'sınırlı', 'az']):
        budget_per_month = 50000
    elif any(word in text_lower for word in ['büyük', 'yüksek', 'enterprise']):
        budget_per_month = 200000

    # Dinamik veri oluştur
    if is_ecommerce:
        return {
            "orgChart": {
                "roles": [
                    {"id": "pm", "title": "Proje Müdürü", "color": "#3b82f6"},
                    {"id": "frontend", "title": "Frontend Developer", "color": "#10b981"},
                    {"id": "backend", "title": "Backend Developer", "color": "#f59e0b"},
                    {"id": "designer", "title": "UI/UX Designer", "color": "#8b5cf6"},
                    {"id": "qa", "title": "QA Engineer", "color": "#ef4444"},
                    {"id": "devops", "title": "DevOps Engineer", "color": "#06b6d4"}
                ],
                "connections": [
                    {"from": "pm", "to": "frontend"},
                    {"from": "pm", "to": "backend"},
                    {"from": "pm", "to": "designer"},
                    {"from": "pm", "to": "qa"},
                    {"from": "pm", "to": "devops"}
                ]
            },
            "workflow": {
                "steps": [
                    {"id": "analysis", "title": "Analiz ve Tasarım", "color": "#3b82f6"},
                    {"id": "frontend_dev", "title": "Frontend Geliştirme", "color": "#10b981"},
                    {"id": "backend_dev", "title": "Backend Geliştirme", "color": "#f59e0b"},
                    {"id": "integration", "title": "Entegrasyon", "color": "#8b5cf6"},
                    {"id": "testing", "title": "Test ve QA", "color": "#ef4444"},
                    {"id": "deployment", "title": "Yayınlama", "color": "#06b6d4"}
                ],
                "connections": [
                    {"from": "analysis", "to": "frontend_dev"},
                    {"from": "analysis", "to": "backend_dev"},
                    {"from": "frontend_dev", "to": "integration"},
                    {"from": "backend_dev", "to": "integration"},
                    {"from": "integration", "to": "testing"},
                    {"from": "testing", "to": "deployment"}
                ]
            },
            "timeline": {
                "phases": [
                    {"name": "Analiz ve Tasarım", "planned": 21, "actual": 25},
                    {"name": "Frontend Geliştirme", "planned": 56, "actual": 52},
                    {"name": "Backend Geliştirme", "planned": 70, "actual": 65},
                    {"name": "Ödeme Entegrasyonu", "planned": 14, "actual": 18},
                    {"name": "Test ve QA", "planned": 28, "actual": 32},
                    {"name": "Deployment", "planned": 7, "actual": 8}
                ]
            },
            "riskAnalysis": {
                "risks": [
                    {"name": "Ödeme Entegrasyonu Zorlukları", "probability": 3, "impact": 4, "color": "#ef4444"},
                    {"name": "Yüksek Trafik Performansı", "probability": 4, "impact": 3, "color": "#f59e0b"},
                    {"name": "Güvenlik Açıkları", "probability": 2, "impact": 5, "color": "#8b5cf6"},
                    {"name": "Mobil Uyumluluk", "probability": 3, "impact": 3, "color": "#10b981"},
                    {"name": "Tecrübeli Developer Eksikliği", "probability": 4, "impact": 4, "color": "#ef4444"}
                ]
            },
            "resources": {
                "distribution": [
                    {"role": "Frontend Developer", "percentage": 28, "color": "#3b82f6"},
                    {"role": "Backend Developer", "percentage": 32, "color": "#10b981"},
                    {"role": "UI/UX Designer", "percentage": 18, "color": "#f59e0b"},
                    {"role": "DevOps Engineer", "percentage": 12, "color": "#8b5cf6"},
                    {"role": "QA Engineer", "percentage": 10, "color": "#ef4444"}
                ]
            },
            "cost": {
                "timeline": [
                    {"month": f"Ay {i+1}", "planned": budget_per_month, "actual": budget_per_month + (i * 5000 - 10000)}
                    for i in range(duration_months)
                ]
            }
        }
    else:
        # Genel proje için varsayılan veri
        return {
            "orgChart": {
                "roles": [
                    {"id": "pm", "title": "Proje Müdürü", "color": "#3b82f6"},
                    {"id": "dev", "title": "Geliştirici", "color": "#10b981"},
                    {"id": "qa", "title": "Test Uzmanı", "color": "#f59e0b"}
                ],
                "connections": [
                    {"from": "pm", "to": "dev"},
                    {"from": "pm", "to": "qa"}
                ]
            },
            "workflow": {
                "steps": [
                    {"id": "analysis", "title": "Analiz", "color": "#3b82f6"},
                    {"id": "development", "title": "Geliştirme", "color": "#10b981"},
                    {"id": "testing", "title": "Test", "color": "#f59e0b"}
                ],
                "connections": [
                    {"from": "analysis", "to": "development"},
                    {"from": "development", "to": "testing"}
                ]
            },
            "timeline": {
                "phases": [
                    {"name": "Analiz", "planned": 15, "actual": 18},
                    {"name": "Geliştirme", "planned": 45, "actual": 40},
                    {"name": "Test", "planned": 15, "actual": 18}
                ]
            },
            "riskAnalysis": {
                "risks": [
                    {"name": "Teknik Zorluklar", "probability": 3, "impact": 4, "color": "#ef4444"},
                    {"name": "Zaman Kısıtı", "probability": 4, "impact": 3, "color": "#f59e0b"}
                ]
            },
            "resources": {
                "distribution": [
                    {"role": "Geliştirici", "percentage": 60, "color": "#3b82f6"},
                    {"role": "Test Uzmanı", "percentage": 40, "color": "#10b981"}
                ]
            },
            "cost": {
                "timeline": [
                    {"month": f"Ay {i+1}", "planned": budget_per_month, "actual": budget_per_month + 5000}
                    for i in range(duration_months)
                ]
            }
        }

def get_analysis_status(session_id: str) -> dict:
    """Session için analiz durumunu döndürür."""
    if session_id not in analysis_context:
        return {"error": "Session not found"}

    context = analysis_context[session_id]
    completion_rate = sum(context["collected_info"].values()) / 7 * 100

    documents = get_session_documents(session_id)

    return {
        "completion_rate": completion_rate,
        "phase": context["analysis_phase"],
        "message_count": context["message_count"],
        "collected_areas": context["collected_info"],
        "ready_for_document": completion_rate >= 70,
        "documents": documents,
        "has_uploaded_files": context.get("has_uploaded_files", False),
        "uploaded_files_count": len(uploaded_files.get(session_id, []))
    }

async def process_template_upload(session_id: str, file_content: bytes, filename: str, file_extension: str):
    """Template dosyasını işler ve session'a kaydeder."""
    try:
        # Dosyadan metin çıkar
        template_content = extract_text_from_file(file_content, filename, file_extension)

        # Template bilgilerini session'a kaydet
        if session_id not in uploaded_files:
            uploaded_files[session_id] = []

        # Template olarak işaretle
        template_info = {
            "filename": filename,
            "content": template_content,
            "uploaded_at": datetime.now().isoformat(),
            "file_type": file_extension,
            "is_template": True
        }

        # Mevcut template'i kaldır ve yenisini ekle
        uploaded_files[session_id] = [f for f in uploaded_files[session_id] if not f.get("is_template", False)]
        uploaded_files[session_id].append(template_info)

        logger.info(f"Template processed and saved for session: {session_id}")
        return {"success": True, "filename": filename}

    except Exception as e:
        logger.error(f"Error processing template: {str(e)}")
        raise e

