import uvicorn
from fastapi import FastAPI
from core.schemas import ChatRequest, ChatResponse
from core.chain import get_conversational_chain, get_memory_for_session

# FastAPI uygulamasını başlat
app = FastAPI(
    title="AI Business Analyst API",
    description="A professional API for the AI Business Analyst Hackathon Project",
    version="1.0.0"
)

@app.post("/chat", response_model=ChatResponse)
async def chat_with_analyst(request: ChatRequest):
    """
    Kullanıcı ile sohbeti yöneten ana API endpoint'i.
    Session ID'ye göre sohbet geçmişini hatırlar.
    """
    # İlgili session için hafızayı al
    memory = get_memory_for_session(request.session_id)

    # Sohbet zincirini oluştur
    chain = get_conversational_chain()

    # Zinciri, kullanıcının mesajı ve hafıza ile birlikte çalıştır
    result = await chain.ainvoke({
        "input": request.message,
        "history": memory.chat_memory.messages
    })

    # Yapay zekanın cevabını hafızaya ekle
    memory.save_context({"input": request.message}, {"output": result["text"]})

    return ChatResponse(
        answer=result["text"],
        session_id=request.session_id
    )

# Bu dosya doğrudan çalıştırıldığında uvicorn sunucusunu başlatmak için
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
