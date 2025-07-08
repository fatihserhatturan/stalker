import { ref} from 'vue'
import { useApi } from './useApi'

export function useChat() {
  const { get, post } = useApi()

  const sessionId = ref(`session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`)
  const messages = ref([
    {
      id: 1,
      text: 'Merhaba! Ben projenizin ön analizini yapmak için buradayım. Proje fikrinizi detaylıca anlatırsanız, kapsamlı bir analiz hazırlayabilirim.\n\n💡 İpucu: Eğer mevcut bir projeniz varsa, proje dokümanlarınızı (PDF, Word, tekst dosyaları) yükleyerek daha detaylı analiz yapabilirim!',
      author: 'ai'
    }
  ])
  const isLoading = ref(false)
  const suggestions = ref([])

  const sendMessage = async (messageText) => {
    messages.value.push({
      id: Date.now(),
      text: messageText,
      author: 'user'
    })

    isLoading.value = true
    suggestions.value = []

    try {
      const response = await post('/chat', {
        session_id: sessionId.value,
        message: messageText
      })

      messages.value.push({
        id: Date.now() + 1,
        text: response.answer,
        author: 'ai'
      })

      generateSuggestions(messageText)

      return response
    } catch (error) {
      messages.value.push({
        id: Date.now() + 1,
        text: 'Üzgünüm, şu anda bir teknik sorun yaşıyorum. Lütfen biraz sonra tekrar deneyin.',
        author: 'ai'
      })
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const generateSuggestions = async (userMessage) => {
    try {
      const response = await post('/chat', {
        session_id: sessionId.value + '_suggestions',
        message: `Kullanıcı bu mesajı gönderdi: "${userMessage}". Bu mesaja AI nasıl yanıt verebilir ona göre kullanıcının AI yanıtına verebileceği 3 farklı mantıklı devam önerisi sun. Her öneri farklı bir perspektiften yaklaşsın ve sadece önerileri ver, açıklama yapma. Öneriler şu formatta olsun:
1. [öneri metni]
2. [öneri metni]
3. [öneri metni]`
      })

      const parsedSuggestions = response.answer
        .split('\n')
        .filter(line => line.match(/^\d+\./))
        .map(line => line.replace(/^\d+\.\s*/, '').trim())
        .filter(suggestion => suggestion.length > 0)
        .slice(0, 3)

      if (parsedSuggestions.length > 0) {
        suggestions.value = parsedSuggestions
      }
    } catch (error) {
      console.error('Error generating suggestions:', error)
    }
  }

  const getAnalysisStatus = async () => {
    try {
      return await get(`/analysis-status/${sessionId.value}`)
    } catch (error) {
      console.error('Error loading analysis status:', error)
      return null
    }
  }

  return {
    sessionId,
    messages,
    isLoading,
    suggestions,
    sendMessage,
    getAnalysisStatus,
  }
}
