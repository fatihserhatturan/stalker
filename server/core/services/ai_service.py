import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema import HumanMessage
from core.prompts import SYSTEM_PROMPT_TEMPLATE, DETAILED_ANALYSIS_PROMPT, FILE_ANALYSIS_PROMPT
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set!")

    def _create_model(self, temperature=0.7, model_name="gemini-2.5-flash"):
        return ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            google_api_key=self.google_api_key,
            convert_system_message_to_human=True
        )

    async def process_conversation(self, enhanced_prompt: str, user_message: str, history: list):
        try:
            model = self._create_model()

            prompt = ChatPromptTemplate.from_messages([
                ("human", f"{enhanced_prompt}\n\nKullanıcı Mesajı: {user_message}")
            ])

            chain = prompt | model | StrOutputParser()

            result = await chain.ainvoke({})

            logger.info(f"AI conversation processed successfully")
            return result

        except Exception as e:
            logger.error(f"Error in AI conversation processing: {str(e)}")
            raise e

    async def analyze_file(self, filename: str, content: str):
        try:
            model = self._create_model(temperature=0.3)

            analysis_prompt = f"""
{FILE_ANALYSIS_PROMPT}

**Dosya Adı:** {filename}
**Dosya İçeriği:**
{content[:8000]}
"""

            prompt = ChatPromptTemplate.from_messages([
                ("human", analysis_prompt)
            ])

            chain = prompt | model | StrOutputParser()
            result = await chain.ainvoke({})

            logger.info(f"File analysis completed for: {filename}")
            return result

        except Exception as e:
            logger.error(f"Error in file analysis: {str(e)}")
            raise e

    async def generate_analysis_document(self, conversation_history: str, uploaded_files_content: str,
                                       template_content: str = None, use_template: bool = False):
        try:
            model = self._create_model(temperature=0.3)

            if use_template and template_content:
                detailed_prompt = f"""
SADECE template formatını kullanarak analiz dokümanı üret. Hiçbir ek açıklama veya giriş cümlesi ekleme.

TEMPLATE:
{template_content[:2000]}

KONUŞMA:
{conversation_history[:1000]}

Template formatını koru, boş alanları konuşmadaki bilgilerle doldur. SADECE doküman içeriğini çıktı olarak ver.
"""
            else:
                detailed_prompt = f"""
{DETAILED_ANALYSIS_PROMPT}

**Konuşma Geçmişi:**
{conversation_history}

{uploaded_files_content}

Yukarıdaki konuşma geçmişini ve yüklenen dosyaları analiz ederek topladığın bilgiler ile kapsamlı bir Ön Analiz Dokümanı hazırla.
Eksik bilgiler için [BİLGİ GEREKLİ] notasyonunu kullan.
SADECE doküman markdown içeriğini çıktı olarak ver, hiçbir ek açıklama ekleme.
"""

            prompt = ChatPromptTemplate.from_messages([
                ("human", detailed_prompt)
            ])

            chain = prompt | model | StrOutputParser()
            result = await chain.ainvoke({})

            logger.info(f"Analysis document generated successfully")
            return result

        except Exception as e:
            logger.error(f"Error generating analysis document: {str(e)}")
            raise e

    async def generate_visual_data(self, conversation_history: str):
        try:
            model = self._create_model(temperature=0.1)

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

            messages = [HumanMessage(content=simple_prompt)]
            ai_response = await model.agenerate([messages])
            result_text = ai_response.generations[0][0].text.strip()

            logger.info(f"Visual data generated successfully")
            return result_text

        except Exception as e:
            logger.error(f"Error generating visual data: {str(e)}")
            raise e
