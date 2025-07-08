from core.prompts import SYSTEM_PROMPT_TEMPLATE

class PromptService:
    def __init__(self, session_service):
        self.session_service = session_service

    def get_enhanced_prompt(self, session_id: str) -> str:
        if session_id not in self.session_service.analysis_context:
            return SYSTEM_PROMPT_TEMPLATE

        context = self.session_service.analysis_context[session_id]
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

        enhanced_prompt += self._get_phase_specific_strategy(phase, missing_areas)
        enhanced_prompt += self._get_uploaded_files_info(session_id)

        return enhanced_prompt

    def _get_phase_specific_strategy(self, phase: str, missing_areas: list) -> str:
        if phase == "discovery":
            return """
- Temel proje anlayışını oluşturmaya odaklan
- Geniş sorular sorarak genel resmi çiz
- Kullanıcının ana motivasyonunu keşfet
"""
        elif phase == "clarification":
            limited_missing = missing_areas[:2] if len(missing_areas) > 2 else missing_areas
            return f"""
- Eksik alanları ({', '.join(limited_missing)}) detaylandır
- Belirsiz noktalarda netleştirici sorular sor
- Spesifik örnekler ve senaryolar talep et
"""
        else:
            return """
- Son detayları tamamla
- Tutarlılık kontrolü yap
- Doküman hazırlığı için son kontroller
"""

    def _get_uploaded_files_info(self, session_id: str) -> str:
        files = self.session_service.get_uploaded_files(session_id)

        if not files:
            return ""

        info = "\n**Yüklenen Dosyalar:**\n"
        for file_info in files:
            info += f"- {file_info['filename']} ({file_info['file_type']}) - {file_info['uploaded_at']}\n"

        return info
