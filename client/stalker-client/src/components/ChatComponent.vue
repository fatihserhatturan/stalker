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
        <div class="max-w-4xl mx-auto px-6 py-4 h-[80px]">
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

            <!-- İlerleme ve Doküman Kontrolleri -->
            <div class="flex items-center space-x-3">
              <!-- İlerleme Göstergesi -->
              <div v-if="analysisStatus && messages.length > 1" class="flex items-center space-x-2 px-3 py-1 bg-gray-800/60 rounded-lg border border-gray-700/30">
                <div class="w-2 h-2 rounded-full" :class="getStatusColor()"></div>
                <span class="text-xs text-gray-300">{{ Math.round(analysisStatus.completion_rate) }}%</span>
              </div>

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
                    'relative max-w-2xl rounded-2xl px-4 py-3 shadow-lg transition-all duration-200 hover:border-blue-400',
                    msg.author === 'ai'
                      ? 'bg-gray-800 border border-gray-700/50 text-gray-100'
                      : 'bg-gradient-to-r from-emerald-600 to-teal-700 text-white border border-transparent hover:border-emerald-300'
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

              <!-- Dokümanları göster -->
              <div v-if="sessionDocuments.length > 0" class="space-y-3">
                <div class="text-center">
                  <div class="inline-flex items-center px-3 py-1 bg-emerald-600/20 text-emerald-400 rounded-full text-xs">
                    <DocumentTextIcon class="w-3 h-3 mr-1" />
                    Oluşturulan Dokümanlar
                  </div>
                </div>

                <div
                  v-for="doc in sessionDocuments"
                  :key="doc.id"
                  @click="openDocument(doc)"
                  class="bg-gray-800/60 border border-gray-700/50 rounded-xl p-4 cursor-pointer hover:border-emerald-500 transition-all duration-200"
                >
                  <div class="flex items-start space-x-3">
                    <div class="p-2 bg-gradient-to-r from-emerald-600 to-teal-700 rounded-lg shadow-lg">
                      <DocumentTextIcon class="w-4 h-4 text-white" />
                    </div>
                    <div class="flex-1 min-w-0">
                      <h4 class="text-sm font-medium text-white truncate">{{ doc.title }}</h4>
                      <p class="text-xs text-gray-400 mt-1">{{ formatDocumentDate(doc.created_at) }}</p>
                      <p class="text-xs text-emerald-400 mt-1">Görüntülemek için tıklayın</p>
                    </div>
                  </div>
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

            <div v-if="isUploadingFile" class="flex items-start space-x-4">
              <div class="flex-shrink-0">
                <div class="w-10 h-10 rounded-full bg-gradient-to-r from-purple-600 to-pink-700 flex items-center justify-center shadow-lg">
                  <ArrowUpTrayIcon class="w-5 h-5 text-white" />
                </div>
              </div>
              <div class="relative bg-gray-800 border border-gray-700/50 rounded-2xl px-4 py-3 shadow-lg">
                <div class="flex items-center space-x-2">
                  <div class="inline-block animate-spin rounded-full h-4 w-4 border-b-2 border-purple-400"></div>
                  <span class="text-xs text-gray-400 ml-2">Dosya yükleniyor ve analiz ediliyor...</span>
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
      <div v-if="messages.length > 2 && !showDocument" class="px-6 py-4">
        <div class="max-w-4xl mx-auto">
          <div class="flex items-center justify-center mb-4">
            <button
              @click="generateAnalysisDocument"
              :disabled="isGeneratingDocument || !isConnected || isLoading"
              class="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-emerald-600 to-teal-700 hover:border-emerald-400 text-white rounded-xl transition-all duration-200 disabled:from-gray-600 disabled:to-gray-600 disabled:cursor-not-allowed border border-transparent"
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

      <!-- Mesaj Giriş Alanı ve Dosya Yükleme -->
      <div class="px-6 py-4">
        <div class="max-w-4xl mx-auto">
          <!-- Dosya Yükleme Alanı -->
          <div v-if="showFileUpload" class="mb-4 p-4 bg-gray-800/60 border border-gray-700/50 rounded-xl">
            <div class="flex items-center justify-between mb-3">
              <h3 class="text-sm font-medium text-white">Proje Dosyası Yükle</h3>
              <button
                @click="showFileUpload = false"
                class="text-gray-400 hover:text-gray-200 hover:border hover:border-gray-400 rounded transition-all duration-200 p-1"
              >
                <XMarkIcon class="w-4 h-4" />
              </button>
            </div>

            <div
              @drop="handleFileDrop"
              @dragover.prevent
              @dragenter.prevent
              class="border-2 border-dashed border-gray-600 rounded-lg p-6 text-center hover:border-purple-500 transition-all duration-200 cursor-pointer"
              :class="{ 'border-purple-500 bg-purple-500/10': isDragging }"
            >
              <input
                ref="fileInput"
                type="file"
                accept=".txt,.md,.pdf,.docx,.doc"
                @change="handleFileSelect"
                class="hidden"
              />

              <div class="space-y-2">
                <ArrowUpTrayIcon class="w-8 h-8 text-gray-400 mx-auto" />
                <p class="text-sm text-gray-300">
                  <button
                    @click="$refs.fileInput?.click()"
                    class="text-purple-400 hover:text-purple-300 hover:border-b hover:border-purple-300 transition-all duration-200"
                  >
                    Dosya seç
                  </button>
                  veya buraya sürükle
                </p>
                <p class="text-xs text-gray-500">
                  Desteklenen formatlar: PDF, Word, Markdown, Text
                </p>
              </div>
            </div>

            <div v-if="selectedFile" class="mt-3 flex items-center space-x-2 p-3 bg-gray-700/50 rounded-lg">
              <DocumentTextIcon class="w-5 h-5 text-purple-400" />
              <span class="text-sm text-gray-300 flex-1">{{ selectedFile.name }}</span>
              <button
                @click="uploadFile"
                :disabled="isUploadingFile"
                class="px-3 py-1 bg-purple-600 hover:border-purple-400 text-white text-xs rounded-md transition-all duration-200 disabled:bg-gray-600 disabled:cursor-not-allowed border border-transparent"
              >
                {{ isUploadingFile ? 'Yükleniyor...' : 'Yükle' }}
              </button>
              <button
                @click="selectedFile = null"
                class="text-gray-400 hover:text-gray-200 hover:border hover:border-gray-400 rounded transition-all duration-200 p-1"
              >
                <XMarkIcon class="w-4 h-4" />
              </button>
            </div>
          </div>

          <form @submit.prevent="sendMessage" class="relative">
            <div class="relative flex items-end">
              <textarea
                v-model="newMessage"
                ref="messageInput"
                placeholder="Proje fikrinizi detaylıca anlatın..."
                :disabled="isLoading || !isConnected"
                rows="2"
                class="w-full pl-4 pr-20 py-3 bg-gray-800 border border-gray-700 rounded-xl text-sm placeholder-gray-400 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 disabled:bg-gray-900 disabled:text-gray-500 shadow-lg resize-none overflow-y-auto scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-transparent"
                :style="{ maxHeight: '120px', minHeight: '48px' }"
                @input="adjustTextareaHeight"
                @keydown.enter.prevent="handleEnterKey"
              />

              <!-- Dosya Yükleme Butonu -->
              <button
                type="button"
                @click="showFileUpload = !showFileUpload"
                :disabled="isLoading || !isConnected"
                class="absolute right-12 bottom-3 p-2 text-gray-400 hover:text-purple-400 hover:border hover:border-purple-400 rounded transition-all duration-200 disabled:text-gray-600 disabled:cursor-not-allowed"
                title="Dosya Yükle"
              >
                <PaperClipIcon class="w-4 h-4" />
              </button>

              <button
                type="submit"
                :disabled="isLoading || newMessage.trim() === '' || !isConnected"
                class="absolute right-2 bottom-3 p-2 bg-gradient-to-r from-blue-600 to-purple-700 text-white rounded-lg hover:border-blue-400 transition-all duration-200 disabled:from-gray-600 disabled:to-gray-600 disabled:cursor-not-allowed border border-transparent"
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
import { ref, nextTick, onMounted, onUnmounted, watch } from 'vue'
import {
  CpuChipIcon,
  UserIcon,
  PaperAirplaneIcon,
  ExclamationTriangleIcon,
  DocumentTextIcon,
  PaperClipIcon,
  ArrowUpTrayIcon,
  XMarkIcon,
} from '@heroicons/vue/24/outline'
import DocumentViewer from './DocumentViewer.vue'

const messages = ref([
  {
    id: 1,
    text: 'Merhaba! Ben projenizin ön analizini yapmak için buradayım. Proje fikrinizi detaylıca anlatırsanız, kapsamlı bir analiz hazırlayabilirim.\n\n💡 İpucu: Eğer mevcut bir projeniz varsa, proje dokümanlarınızı (PDF, Word, tekst dosyaları) yükleyerek daha detaylı analiz yapabilirim!',
    author: 'ai'
  }
])
const newMessage = ref('')
const isLoading = ref(false)
const isGeneratingDocument = ref(false)
const isUploadingFile = ref(false)
const isConnected = ref(true)
const sessionId = ref(`session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`)
const messageList = ref(null)
const messageInput = ref(null)

// File upload state
const showFileUpload = ref(false)
const selectedFile = ref(null)
const isDragging = ref(false)
const fileInput = ref(null)

// Document viewer state
const showDocument = ref(false)
const documentContent = ref('')
const sessionDocuments = ref([])
const analysisStatus = ref(null)

const isGeneratingVisualData = ref(false)
const visualData = ref(null)

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
      adjustTextareaHeight()
    }
  })
}

const adjustTextareaHeight = () => {
  const textarea = messageInput.value
  if (textarea) {
    textarea.style.height = '48px'
    const scrollHeight = textarea.scrollHeight
    const minHeight = 48
    const maxHeight = 120
    let newHeight = Math.min(Math.max(scrollHeight, minHeight), maxHeight)
    textarea.style.height = newHeight + 'px'
  }
}

const handleEnterKey = (event) => {
  if (event.shiftKey) {
    return
  } else {
    event.preventDefault()
    sendMessage()
  }
}

const formatDocumentDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('tr-TR', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
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

const loadAnalysisStatus = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/analysis-status/${sessionId.value}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    })

    if (response.ok) {
      const data = await response.json()
      analysisStatus.value = data.status
    }
  } catch (error) {
    console.error('Error loading analysis status:', error)
  }
}

const getStatusColor = () => {
  if (!analysisStatus.value) return 'bg-gray-500'
  const rate = analysisStatus.value.completion_rate
  if (rate < 30) return 'bg-red-400'
  if (rate < 70) return 'bg-yellow-400'
  return 'bg-green-400'
}

const loadSessionDocuments = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/session-documents/${sessionId.value}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    })

    if (response.ok) {
      const data = await response.json()
      sessionDocuments.value = data.documents || []
      scrollToBottom()
    }
  } catch (error) {
    console.error('Error loading session documents:', error)
  }
}

const openDocument = async (doc) => {
  try {
    const response = await fetch(`${API_BASE_URL}/document/${sessionId.value}/${doc.id}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    })

    if (response.ok) {
      const data = await response.json()
      documentContent.value = data.document.content
      showDocument.value = true
    } else {
      showNotification('Doküman yüklenirken hata oluştu', 'error')
    }
  } catch (error) {
    console.error('Error loading document:', error)
    showNotification('Doküman yüklenirken hata oluştu', 'error')
  }
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    validateAndSetFile(file)
  }
}

const handleFileDrop = (event) => {
  event.preventDefault()
  isDragging.value = false

  const files = event.dataTransfer.files
  if (files.length > 0) {
    validateAndSetFile(files[0])
  }
}

const validateAndSetFile = (file) => {
  const allowedTypes = [
    'text/plain',
    'text/markdown',
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/msword'
  ]

  const allowedExtensions = ['.txt', '.md', '.pdf', '.docx', '.doc']
  const fileExtension = '.' + file.name.split('.').pop().toLowerCase()

  if (file.size > 10 * 1024 * 1024) {
    showNotification('Dosya boyutu 10MB\'dan büyük olamaz', 'error')
    return
  }

  if (!allowedTypes.includes(file.type) && !allowedExtensions.includes(fileExtension)) {
    showNotification('Desteklenmeyen dosya formatı. İzin verilen formatlar: PDF, Word, Markdown, Text', 'error')
    return
  }

  selectedFile.value = file
}

const uploadFile = async () => {
  if (!selectedFile.value || isUploadingFile.value) return

  isUploadingFile.value = true

  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    formData.append('session_id', sessionId.value)

    const response = await fetch(`${API_BASE_URL}/upload-file`, {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`)
    }

    const data = await response.json()

    messages.value.push({
      id: Date.now(),
      text: `📁 Dosya yüklendi: ${selectedFile.value.name}`,
      author: 'user'
    })

    messages.value.push({
      id: Date.now() + 1,
      text: data.analysis,
      author: 'ai'
    })

    selectedFile.value = null
    showFileUpload.value = false

    await loadAnalysisStatus()

    showNotification('Dosya başarıyla yüklendi ve analiz edildi!', 'success')

  } catch (error) {
    console.error("File upload error:", error)
    showNotification(`Dosya yüklenirken hata: ${error.message}`, 'error')
  } finally {
    isUploadingFile.value = false
    scrollToBottom()
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

    await loadAnalysisStatus()
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
  isGeneratingVisualData.value = true

  try {
    // Paralel olarak doküman ve görsel veri üret
    const [documentResponse, visualResponse] = await Promise.allSettled([
      fetch(`${API_BASE_URL}/generate-analysis-document`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          session_id: sessionId.value
        })
      }),
      fetch(`${API_BASE_URL}/generate-visual-data`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          session_id: sessionId.value,
          message: "generate_visual_data"
        })
      })
    ])

    // Doküman sonucunu işle
    if (documentResponse.status === 'fulfilled' && documentResponse.value.ok) {
      const documentData = await documentResponse.value.json()
      documentContent.value = documentData.document_content
      showDocument.value = true
      await loadSessionDocuments()
      showNotification('Analiz dokümanı başarıyla oluşturuldu!', 'success')
    } else {
      const error = documentResponse.reason || 'Doküman oluşturulamadı'
      showNotification(`Doküman oluşturulurken hata: ${error}`, 'error')
    }

    // Görsel veri sonucunu işle
    if (visualResponse.status === 'fulfilled' && visualResponse.value.ok) {
      const visualResponseData = await visualResponse.value.json()
      visualData.value = visualResponseData.visual_data
      showNotification('Görsel veriler başarıyla oluşturuldu!', 'success')
    } else {
      console.error('Visual data generation failed:', visualResponse.reason)
      visualData.value = null
    }

  } catch (error) {
    console.error("Document/Visual generation error:", error)
    showNotification(`İşlem sırasında hata: ${error.message}`, 'error')
  } finally {
    isGeneratingDocument.value = false
    isGeneratingVisualData.value = false
  }
}

const closeDocument = () => {
  showDocument.value = false
  documentContent.value = ''
}

onMounted(async () => {
  await checkConnection()
  await loadSessionDocuments()
  await loadAnalysisStatus()
  focusInput()

  const connectionChecker = setInterval(checkConnection, 30000)

  const unwatchMessage = watch(newMessage, () => {
    nextTick(() => {
      adjustTextareaHeight()
    })
  })

  onUnmounted(() => {
    clearInterval(connectionChecker)
    unwatchMessage()
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
  border-color: currentColor;
}

button:active:not(:disabled) {
  transform: none;
}
</style>
