<template>
  <div class="flex h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black">
    <!-- Chat Bölümü -->
    <div
      :class="[
        'flex flex-col transition-all duration-500 ease-in-out',
        showDocument ? 'w-1/2' : 'w-full'
      ]"
    >
      <!-- Header -->
      <div class="relative bg-gray-900/80 backdrop-blur-md border-b border-gray-700/50 shadow-lg">
        <div class="max-w-4xl mx-auto px-6 py-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="p-2 bg-gradient-to-r from-blue-600 to-purple-700 rounded-xl shadow-lg">
                <CpuChipIcon class="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 class="text-xl font-semibold text-white">AI Business Analyst</h1>
                <p class="text-sm text-gray-300">Proje analiz asistanınız</p>
              </div>
            </div>

            <!-- Doküman varsa kapat butonu -->
            <div v-if="showDocument" class="flex items-center space-x-2">
              <button
                @click="closeDocument"
                class="flex items-center space-x-2 px-3 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors"
              >
                <XMarkIcon class="w-4 h-4" />
                <span>Dokümanı Kapat</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Mesajlar -->
      <div class="flex-1 overflow-hidden">
        <div class="h-full max-w-4xl mx-auto">
          <div
            ref="messageList"
            class="h-full overflow-y-auto px-6 py-6 space-y-6 scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-transparent"
          >
            <div class="space-y-6">
              <div
                v-for="msg in messages"
                :key="msg.id"
                :class="['flex items-start space-x-4', msg.author === 'user' ? 'flex-row-reverse space-x-reverse' : '']"
              >
                <div class="flex-shrink-0">
                  <div
                    :class="[
                      'w-10 h-10 rounded-full flex items-center justify-center shadow-lg transition-all duration-200',
                      msg.author === 'ai'
                        ? 'bg-gradient-to-r from-blue-600 to-purple-700 text-white'
                        : 'bg-gradient-to-r from-emerald-600 to-teal-700 text-white'
                    ]"
                  >
                    <UserIcon v-if="msg.author === 'user'" class="w-5 h-5" />
                    <CpuChipIcon v-else class="w-5 h-5" />
                  </div>
                </div>

                <div
                  :class="[
                    'relative max-w-2xl rounded-2xl px-4 py-3 shadow-lg transition-all duration-200 hover:shadow-xl',
                    msg.author === 'ai'
                      ? 'bg-gray-800 border border-gray-700/50 text-gray-100'
                      : 'bg-gradient-to-r from-emerald-600 to-teal-700 text-white'
                  ]"
                >
                  <p :class="['text-sm leading-relaxed whitespace-pre-wrap', msg.author === 'ai' ? 'text-gray-100' : 'text-white']">
                    {{ msg.text }}
                  </p>
                  <div
                    :class="[
                      'absolute top-4 w-2 h-2 transform rotate-45',
                      msg.author === 'ai'
                        ? '-left-1 bg-gray-800 border-l border-b border-gray-700/50'
                        : '-right-1 bg-gradient-to-r from-emerald-600 to-teal-700'
                    ]"
                  ></div>
                </div>
              </div>
            </div>

            <div v-if="isLoading" class="flex items-start space-x-4">
              <div class="flex-shrink-0">
                <div class="w-10 h-10 rounded-full bg-gradient-to-r from-blue-600 to-purple-700 flex items-center justify-center shadow-lg">
                  <CpuChipIcon class="w-5 h-5 text-white" />
                </div>
              </div>
              <div class="relative bg-gray-800 border border-gray-700/50 rounded-2xl px-4 py-3 shadow-lg">
                <div class="flex items-center space-x-2">
                  <div class="flex space-x-1">
                    <div class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 0s;"></div>
                    <div class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 0.15s;"></div>
                    <div class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 0.3s;"></div>
                  </div>
                  <span class="text-xs text-gray-400 ml-2">AI analiz yapıyor...</span>
                </div>
                <div class="absolute top-4 -left-1 w-2 h-2 bg-gray-800 border-l border-b border-gray-700/50 transform rotate-45"></div>
              </div>
            </div>

            <div v-if="isGeneratingDocument" class="flex items-start space-x-4">
              <div class="flex-shrink-0">
                <div class="w-10 h-10 rounded-full bg-gradient-to-r from-emerald-600 to-teal-700 flex items-center justify-center shadow-lg">
                  <DocumentTextIcon class="w-5 h-5 text-white" />
                </div>
              </div>
              <div class="relative bg-gray-800 border border-gray-700/50 rounded-2xl px-4 py-3 shadow-lg">
                <div class="flex items-center space-x-2">
                  <div class="inline-block animate-spin rounded-full h-4 w-4 border-b-2 border-emerald-400"></div>
                  <span class="text-xs text-gray-400 ml-2">Analiz dokümanı oluşturuluyor...</span>
                </div>
                <div class="absolute top-4 -left-1 w-2 h-2 bg-gray-800 border-l border-b border-gray-700/50 transform rotate-45"></div>
              </div>
            </div>

            <div v-if="!isConnected" class="text-center py-4">
              <div class="inline-flex items-center px-4 py-2 bg-red-600/20 text-red-400 rounded-lg text-sm">
                <ExclamationTriangleIcon class="w-4 h-4 mr-2" />
                Backend'e bağlantı kurulamıyor. Lütfen sunucunun çalıştığından emin olun.
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Doküman Oluşturma Butonu -->
      <div v-if="messages.length > 2 && !showDocument" class="bg-gray-900/60 backdrop-blur-md border-t border-gray-700/30 px-6 py-4">
        <div class="max-w-4xl mx-auto">
          <div class="flex items-center justify-center mb-4">
            <button
              @click="generateAnalysisDocument"
              :disabled="isGeneratingDocument || !isConnected || isLoading"
              class="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-emerald-600 to-teal-700 hover:from-emerald-700 hover:to-teal-800 text-white rounded-xl transition-all duration-200 disabled:from-gray-600 disabled:to-gray-600 disabled:cursor-not-allowed shadow-lg hover:shadow-xl transform hover:scale-105 disabled:transform-none"
            >
              <DocumentTextIcon class="w-5 h-5" />
              <span>{{ isGeneratingDocument ? 'Doküman Oluşturuluyor...' : 'Analiz Dokümanı Oluştur' }}</span>
            </button>
          </div>
          <div class="text-center">
            <p class="text-xs text-gray-400">
              Sohbet geçmişinize dayanarak detaylı bir ön analiz dokümanı oluşturulacak
            </p>
          </div>
        </div>
      </div>

      <!-- Mesaj Giriş Alanı -->
      <div class="bg-gray-900/80 backdrop-blur-md border-t border-gray-700/50">
        <div class="max-w-4xl mx-auto px-6 py-4">
          <form @submit.prevent="sendMessage" class="relative">
            <div class="relative flex items-center">
              <input
                v-model="newMessage"
                ref="messageInput"
                type="text"
                placeholder="Proje fikrinizi detaylıca anlatın..."
                :disabled="isLoading || !isConnected"
                class="w-full pl-4 pr-12 py-3 bg-gray-800 border border-gray-700 rounded-xl text-sm placeholder-gray-400 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 disabled:bg-gray-900 disabled:text-gray-500 shadow-lg"
                @keydown.enter.prevent="sendMessage"
              />
              <button
                type="submit"
                :disabled="isLoading || newMessage.trim() === '' || !isConnected"
                class="absolute right-2 p-2 bg-gradient-to-r from-blue-600 to-purple-700 text-white rounded-lg hover:from-blue-700 hover:to-purple-800 transition-all duration-200 disabled:from-gray-600 disabled:to-gray-600 disabled:cursor-not-allowed shadow-lg hover:shadow-xl transform hover:scale-105 disabled:transform-none"
              >
                <PaperAirplaneIcon class="w-4 h-4" />
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Document Viewer Bölümü -->
    <div
      v-if="showDocument"
      class="w-1/2 border-l border-gray-700/50 bg-gray-900/50 backdrop-blur-md transition-all duration-500 ease-in-out transform translate-x-0"
    >
      <DocumentViewer
        :document-content="documentContent"
        :session-id="sessionId"
        @close-document="closeDocument"
      />
    </div>

    <!-- Bildirim -->
    <div
      v-if="notification.show"
      :class="[
        'fixed top-4 right-4 px-4 py-2 rounded-lg shadow-lg transition-all duration-300 z-50',
        notification.type === 'success' ? 'bg-green-600 text-white' : 'bg-red-600 text-white'
      ]"
    >
      {{ notification.message }}
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, onUnmounted } from 'vue'
import {
  CpuChipIcon,
  UserIcon,
  PaperAirplaneIcon,
  ExclamationTriangleIcon,
  DocumentTextIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'
import DocumentViewer from './DocumentViewer.vue'

const messages = ref([
  {
    id: 1,
    text: 'Merhaba! Ben projenizin ön analizini yapmak için buradayım. Proje fikrinizi detaylıca anlatırsanız, kapsamlı bir analiz hazırlayabilirim.',
    author: 'ai'
  }
])
const newMessage = ref('')
const isLoading = ref(false)
const isGeneratingDocument = ref(false)
const isConnected = ref(true)
const sessionId = ref(`session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`)
const messageList = ref(null)
const messageInput = ref(null)

// Document viewer state
const showDocument = ref(false)
const documentContent = ref('')

const notification = ref({
  show: false,
  message: '',
  type: 'success'
})

const API_BASE_URL = 'http://localhost:8000'

const showNotification = (message, type = 'success') => {
  notification.value = { show: true, message, type }
  setTimeout(() => {
    notification.value.show = false
  }, 3000)
}

const scrollToBottom = async () => {
  await nextTick()
  const list = messageList.value
  if (list) {
    list.scrollTop = list.scrollHeight
  }
}

const focusInput = () => {
  nextTick(() => {
    if (messageInput.value) {
      messageInput.value.focus()
    }
  })
}

const checkConnection = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    })
    isConnected.value = response.ok
    return response.ok
  } catch (error) {
    isConnected.value = false
    return false
  }
}

const sendMessage = async () => {
  const userMessageText = newMessage.value.trim()
  if (!userMessageText || isLoading.value || !isConnected.value) return

  messages.value.push({
    id: Date.now(),
    text: userMessageText,
    author: 'user'
  })

  const currentMessage = newMessage.value
  newMessage.value = ''
  scrollToBottom()
  isLoading.value = true

  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        session_id: sessionId.value,
        message: currentMessage
      })
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`)
    }

    const data = await response.json()

    messages.value.push({
      id: Date.now() + 1,
      text: data.answer,
      author: 'ai'
    })

    isConnected.value = true

  } catch (error) {
    console.error("API Error:", error)

    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      isConnected.value = false
      showNotification('Backend sunucusuna bağlanılamıyor. Lütfen sunucunun çalıştığından emin olun.', 'error')
    } else {
      showNotification(`Hata: ${error.message}`, 'error')
    }

    messages.value.push({
      id: Date.now() + 1,
      text: 'Üzgünüm, şu anda bir teknik sorun yaşıyorum. Lütfen biraz sonra tekrar deneyin.',
      author: 'ai'
    })
  } finally {
    isLoading.value = false
    scrollToBottom()
    focusInput()
  }
}

const generateAnalysisDocument = async () => {
  if (isGeneratingDocument.value || !isConnected.value) return

  isGeneratingDocument.value = true

  try {
    const response = await fetch(`${API_BASE_URL}/generate-analysis-document`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        session_id: sessionId.value
      })
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`)
    }

    const data = await response.json()

    // Dokümanı sağ panelde göster
    documentContent.value = data.document_content
    showDocument.value = true

    showNotification('Analiz dokümanı başarıyla oluşturuldu!', 'success')

  } catch (error) {
    console.error("Document generation error:", error)
    showNotification(`Doküman oluşturulurken hata: ${error.message}`, 'error')
  } finally {
    isGeneratingDocument.value = false
  }
}

const closeDocument = () => {
  showDocument.value = false
  documentContent.value = ''
}

onMounted(async () => {
  await checkConnection()
  focusInput()

  const connectionChecker = setInterval(checkConnection, 30000)

  onUnmounted(() => {
    clearInterval(connectionChecker)
  })
})
</script>

<style scoped>
.scrollbar-thin::-webkit-scrollbar {
  width: 6px;
}

.scrollbar-thin::-webkit-scrollbar-track {
  background: transparent;
}

.scrollbar-thin::-webkit-scrollbar-thumb {
  background-color: rgb(75 85 99);
  border-radius: 3px;
}

.scrollbar-thin::-webkit-scrollbar-thumb:hover {
  background-color: rgb(107 114 128);
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message-enter-active {
  animation: slideInUp 0.3s ease-out;
}

@keyframes bounce {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-10px);
  }
}

.animate-bounce {
  animation: bounce 1.4s infinite;
}

input:focus {
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

button:hover:not(:disabled) {
  transform: translateY(-1px);
}

button:active:not(:disabled) {
  transform: translateY(0);
}
</style>
