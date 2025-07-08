import json
import logging

logger = logging.getLogger(__name__)

class VisualDataService:
    def parse_visual_data(self, ai_response_text: str) -> dict:
        try:
            json_start = ai_response_text.find('{')
            json_end = ai_response_text.rfind('}') + 1

            if json_start == -1 or json_end == 0:
                raise json.JSONDecodeError("JSON bulunamadı", ai_response_text, 0)

            clean_json = ai_response_text[json_start:json_end]
            visual_data = json.loads(clean_json)

            self._validate_visual_data(visual_data)

            logger.info(f"Visual data successfully parsed from AI response")
            return visual_data

        except Exception as e:
            logger.error(f"AI data generation failed, using fallback: {str(e)}")
            return self.generate_fallback_data()

    def _validate_visual_data(self, visual_data: dict):
        required_keys = ['orgChart', 'workflow', 'timeline', 'riskAnalysis', 'resources', 'cost']
        if not all(key in visual_data for key in required_keys):
            raise ValueError("Eksik JSON anahtarları")

    def generate_fallback_data(self) -> dict:
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
                    {"month": "Ay 1", "planned": 100000, "actual": 105000},
                    {"month": "Ay 2", "planned": 100000, "actual": 95000},
                    {"month": "Ay 3", "planned": 100000, "actual": 110000}
                ]
            }
        }

    def generate_smart_fallback_data(self, conversation_history: str) -> dict:
        text_lower = conversation_history.lower()

        is_ecommerce = any(keyword in text_lower for keyword in ['e-ticaret', 'online', 'ödeme', 'sepet', 'ürün'])

        if is_ecommerce:
            return self._generate_ecommerce_data()
        else:
            return self.generate_fallback_data()

    def _generate_ecommerce_data(self) -> dict:
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
                    {"month": "Ay 1", "planned": 100000, "actual": 105000},
                    {"month": "Ay 2", "planned": 100000, "actual": 95000},
                    {"month": "Ay 3", "planned": 100000, "actual": 110000},
                    {"month": "Ay 4", "planned": 100000, "actual": 115000},
                    {"month": "Ay 5", "planned": 100000, "actual": 98000},
                    {"month": "Ay 6", "planned": 100000, "actual": 102000}
                ]
            }
        }
