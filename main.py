import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema.messages import HumanMessage, SystemMessage

load_dotenv()

# Model tanımını bu şekilde güncelleyin:
chat_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

messages = [
    SystemMessage(
        content="Sen, bir yazılım projesinin başlangıcında iş birimlerinden gelen talepleri analiz eden, uzman bir 'Yapay Zeka İş Analisti'sin. Görevin, kullanıcıdan gelen üstü kapalı proje fikrini netleştirmek için akıllı ve yönlendirici bir soru sormaktır."
    ),
    HumanMessage(
        content="Merhaba, satış ekibimizin süreçlerini dijitalleştirmek için bir ERP sistemi istiyoruz."
    ),
]

print("Yapay Zeka İş Analisti (Gemini) düşünüyor...")
response = chat_model.invoke(messages)

print("\nAI Cevabı:")
print(response.content)
