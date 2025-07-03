<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black">
    <div class="relative bg-gray-900/80 backdrop-blur-md border-b border-gray-700/50 shadow-lg">
      <div class="max-w-6xl mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <button
              @click="goBack"
              class="p-2 text-gray-400 hover:text-gray-200 hover:bg-gray-800 rounded-lg transition-colors"
            >
              <ArrowLeftIcon class="w-5 h-5" />
            </button>
            <div class="flex items-center space-x-3">
              <div class="p-2 bg-gradient-to-r from-emerald-600 to-teal-700 rounded-xl shadow-lg">
                <DocumentTextIcon class="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 class="text-xl font-semibold text-white">Proje Analiz Dokümanı</h1>
                <p class="text-sm text-gray-300">Otomatik oluşturulmuş örnek doküman</p>
              </div>
            </div>
          </div>
          <div class="flex items-center space-x-2">
            <button
              @click="downloadDocument"
              class="flex items-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
            >
              <ArrowDownTrayIcon class="w-4 h-4" />
              <span>İndir</span>
            </button>
            <button
              @click="copyToClipboard"
              class="flex items-center space-x-2 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors"
            >
              <ClipboardDocumentIcon class="w-4 h-4" />
              <span>Kopyala</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="isLoading" class="flex items-center justify-center h-96">
      <div class="text-center">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        <p class="mt-4 text-gray-400">Doküman oluşturuluyor...</p>
      </div>
    </div>

    <div v-else-if="error" class="flex items-center justify-center h-96">
      <div class="text-center">
        <ExclamationTriangleIcon class="w-12 h-12 text-red-500 mx-auto mb-4" />
        <h2 class="text-xl font-semibold text-white mb-2">Hata Oluştu</h2>
        <p class="text-gray-400 mb-4">{{ error }}</p>
        <button
          @click="goBack"
          class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
        >
          Geri Dön
        </button>
      </div>
    </div>

    <div v-else class="max-w-6xl mx-auto px-6 py-8">
      <div class="bg-gray-800/50 backdrop-blur-sm rounded-2xl shadow-2xl border border-gray-700/50 overflow-hidden">
        <div class="bg-gradient-to-r from-gray-800 to-gray-700 px-6 py-4 border-b border-gray-600/50">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-2">
              <div class="w-2 h-2 bg-green-400 rounded-full"></div>
              <span class="text-sm text-gray-300">Doküman hazır</span>
            </div>
            <div class="text-sm text-gray-400">
              {{ formatDate(new Date()) }}
            </div>
          </div>
        </div>

        <div class="p-6">
          <div
            v-html="renderedMarkdown"
            class="markdown-content"
          ></div>
        </div>
      </div>
    </div>

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
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  ArrowLeftIcon,
  DocumentTextIcon,
  ArrowDownTrayIcon,
  ClipboardDocumentIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'

const route = useRoute()
const router = useRouter()

const documentContent = ref('')
const isLoading = ref(true)
const error = ref('')
const notification = ref({
  show: false,
  message: '',
  type: 'success'
})

const renderedMarkdown = computed(() => {
  if (!documentContent.value) return ''

  return documentContent.value
    .replace(/^### (.*$)/gm, '<h3>$1</h3>')
    .replace(/^## (.*$)/gm, '<h2>$1</h2>')
    .replace(/^# (.*$)/gm, '<h1>$1</h1>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code>$1</code>')
    .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/^(?!<[h|u|l])/gm, '<p>')
    .replace(/(?<![>])$/gm, '</p>')
    .replace(/<p><\/p>/g, '')
    .replace(/<p>(<[h|u])/g, '$1')
    .replace(/(<\/[h|u]>)<\/p>/g, '$1')
})

const API_BASE_URL = 'http://localhost:8000'

const showNotification = (message, type = 'success') => {
  notification.value = { show: true, message, type }
  setTimeout(() => {
    notification.value.show = false
  }, 3000)
}

const formatDate = (date) => {
  return new Intl.DateTimeFormat('tr-TR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

const goBack = () => {
  router.push('/')
}

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(documentContent.value)
    showNotification('Doküman panoya kopyalandı!', 'success')
  } catch (err) {
    showNotification('Kopyalama işlemi başarısız oldu', 'error')
  }
}

const downloadDocument = () => {
  const blob = new Blob([documentContent.value], { type: 'text/markdown' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `proje-analiz-dokumani-${new Date().toISOString().split('T')[0]}.md`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
  showNotification('Doküman indirildi!', 'success')
}

const loadDocument = async () => {
  try {
    isLoading.value = true
    error.value = ''

    const sessionId = route.query.sessionId || 'default'

    const response = await fetch(`${API_BASE_URL}/generate-document`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        session_id: sessionId
      })
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`)
    }

    const data = await response.json()
    documentContent.value = data.document_content

  } catch (err) {
    console.error('Document loading error:', err)
    error.value = err.message || 'Doküman yüklenirken bir hata oluştu'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadDocument()
})
</script>

<style scoped>
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background-color: rgb(75 85 99);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background-color: rgb(107 114 128);
}

.markdown-content {
  color: #f3f4f6;
  line-height: 1.6;
}

.markdown-content h1 {
  color: #ffffff;
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  margin-top: 2rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #4b5563;
}

.markdown-content h2 {
  color: #60a5fa;
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  margin-top: 2rem;
}

.markdown-content h3 {
  color: #34d399;
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  margin-top: 1.5rem;
}

.markdown-content p {
  color: #f3f4f6;
  margin-bottom: 1rem;
  line-height: 1.7;
}

.markdown-content ul {
  color: #f3f4f6;
  margin: 1rem 0;
  padding-left: 1.5rem;
}

.markdown-content li {
  color: #f3f4f6;
  margin-bottom: 0.5rem;
  line-height: 1.6;
}

.markdown-content strong {
  color: #ffffff;
  font-weight: 600;
}

.markdown-content em {
  color: #d1d5db;
  font-style: italic;
}

.markdown-content code {
  color: #34d399;
  background-color: #1f2937;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-family: 'Courier New', monospace;
  font-size: 0.9em;
}

.markdown-content blockquote {
  border-left: 4px solid #3b82f6;
  background-color: rgba(31, 41, 55, 0.5);
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 0 0.5rem 0.5rem 0;
  color: #e5e7eb;
}

.markdown-content table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
}

.markdown-content th {
  background-color: #374151;
  color: #ffffff;
  padding: 0.75rem;
  text-align: left;
  font-weight: 600;
  border-bottom: 1px solid #4b5563;
}

.markdown-content td {
  background-color: rgba(55, 65, 81, 0.5);
  color: #f3f4f6;
  padding: 0.75rem;
  border-top: 1px solid #4b5563;
}

.markdown-content hr {
  border: none;
  border-top: 1px solid #4b5563;
  margin: 2rem 0;
}

/* İlk başlık için özel stil */
.markdown-content h1:first-child {
  margin-top: 0;
}
</style>
