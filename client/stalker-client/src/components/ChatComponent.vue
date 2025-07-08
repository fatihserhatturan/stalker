<template>
  <div class="flex h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black">
    <div
      :class="[
        'flex flex-col transition-all duration-500 ease-in-out',
        showDocument ? 'w-1/2' : 'w-full'
      ]"
    >
      <ChatHeader
        :is-loading="chat.isLoading.value"
        :is-connected="isConnected"
        :is-image-generation-enabled="isImageGenerationEnabled"
        :has-template="!!fileUpload.templateFile.value"
        :show-progress="chat.messages.value.length > 1"
        :completion-rate="completionRate"
        @toggle-image-generation="toggleImageGeneration"
        @toggle-template-upload="toggleTemplateUpload"
      />

      <TemplateUpload
        v-if="showTemplateUpload"
        :template-file="fileUpload.templateFile.value"
        @close="showTemplateUpload = false"
        @template-selected="handleTemplateSelected"
        @template-removed="handleTemplateRemoved"
      />

      <MessageList
        ref="messageListRef"
        :messages="chat.messages.value"
        :suggestions="chat.suggestions.value"
        :session-documents="document.sessionDocuments.value"
        :is-loading="chat.isLoading.value"
        :is-generating-document="document.isGenerating.value"
        :is-uploading-file="fileUpload.isUploading.value"
        :is-connected="isConnected"
        :template-file="fileUpload.templateFile.value"
        @suggestion-selected="handleSuggestionSelected"
        @document-opened="handleDocumentOpened"
      />

      <DocumentGenerateButton
        v-if="chat.messages.value.length > 2 && !showDocument"
        :is-generating="document.isGenerating.value"
        :is-connected="isConnected"
        :is-loading="chat.isLoading.value"
        :template-file="fileUpload.templateFile.value"
        :is-image-generation-enabled="isImageGenerationEnabled"
        @generate="handleGenerateDocument"
      />

      <MessageInput
        v-model="newMessage"
        ref="messageInputRef"
        :is-loading="chat.isLoading.value"
        :is-connected="isConnected"
        :show-file-upload="showFileUpload"
        :selected-file="fileUpload.selectedFile.value"
        :is-uploading="fileUpload.isUploading.value"
        @submit="handleSendMessage"
        @toggle-file-upload="toggleFileUpload"
        @file-selected="handleFileSelected"
        @file-removed="handleFileRemoved"
        @upload-file="handleUploadFile"
      />
    </div>

    <div
      v-if="showDocument"
      class="w-1/2 border-l border-gray-700/50 bg-gray-900/50 backdrop-blur-md transition-all duration-500 ease-in-out transform translate-x-0"
    >
      <DocumentViewer
        :document-content="document.documentContent.value"
        :session-id="chat.sessionId.value"
        :visual-data="isImageGenerationEnabled ? document.visualData.value : null"
        @close-document="handleCloseDocument"
      />
    </div>

    <NotificationComponent :notification="notifications.notification.value" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useChat } from '@/composables/useChat'
import { useFileUpload } from '@/composables/useFileUpload'
import { useDocument } from '@/composables/useDocument'
import { useNotifications } from '@/composables/useNotifications'
import { useApi } from '@/composables/useApi'

import ChatHeader from './chat/ChatHeader.vue'
import TemplateUpload from './file/TemplateUpload.vue'
import MessageList from './chat/MessageList.vue'
import DocumentGenerateButton from './document/DocumentGenerateButton.vue'
import MessageInput from './chat/MessageInput.vue'
import DocumentViewer from './DocumentViewer.vue'
import NotificationComponent from './ui/NotificationComponent.vue'

const chat = useChat()
const fileUpload = useFileUpload()
const document = useDocument()
const notifications = useNotifications()
const { get } = useApi()

const messageListRef = ref(null)
const messageInputRef = ref(null)

const newMessage = ref('')
const isConnected = ref(true)
const isImageGenerationEnabled = ref(false)
const showTemplateUpload = ref(false)
const showFileUpload = ref(false)
const showDocument = ref(false)
const analysisStatus = ref(null)

const completionRate = computed(() => {
  if (!analysisStatus.value || isNaN(analysisStatus.value.completion_rate)) {
    return 0
  }
  return Math.round(analysisStatus.value.completion_rate)
})

const checkConnection = async () => {
  try {
    const response = await get('/health')
    isConnected.value = !!response
    return !!response
  } catch (error) {
    isConnected.value = false
    return false
  }
}

const loadAnalysisStatus = async () => {
  try {
    const response = await chat.getAnalysisStatus()
    if (response && !response.error) {
      analysisStatus.value = response.status
    }
  } catch (error) {
    console.error('Error loading analysis status:', error)
  }
}

const toggleImageGeneration = () => {
  isImageGenerationEnabled.value = !isImageGenerationEnabled.value
}

const toggleTemplateUpload = () => {
  showTemplateUpload.value = !showTemplateUpload.value
}

const toggleFileUpload = () => {
  showFileUpload.value = !showFileUpload.value
}

const handleTemplateSelected = async (file) => {
  try {
    fileUpload.setTemplateFile(file)
    await fileUpload.uploadTemplate(file, chat.sessionId.value)
    notifications.showNotification('Template başarıyla yüklendi!', 'success')
    showTemplateUpload.value = false
  } catch (error) {
    notifications.showNotification(error.message, 'error')
    fileUpload.removeTemplate()
  }
}

const handleTemplateRemoved = () => {
  fileUpload.removeTemplate()
  notifications.showNotification('Template kaldırıldı', 'success')
}

const handleFileSelected = (file) => {
  try {
    fileUpload.setSelectedFile(file)
  } catch (error) {
    notifications.showNotification(error.message, 'error')
  }
}

const handleFileRemoved = () => {
  fileUpload.removeSelectedFile()
}

const handleUploadFile = async () => {
  try {
    const response = await fileUpload.uploadProjectFile(
      fileUpload.selectedFile.value,
      chat.sessionId.value
    )

    chat.messages.value.push({
      id: Date.now(),
      text: `📁 Dosya yüklendi: ${fileUpload.selectedFile.value.name}`,
      author: 'user'
    })

    chat.messages.value.push({
      id: Date.now() + 1,
      text: response.analysis,
      author: 'ai'
    })

    showFileUpload.value = false
    await loadAnalysisStatus()
    notifications.showNotification('Dosya başarıyla yüklendi ve analiz edildi!', 'success')
    messageListRef.value?.scrollToBottom()
  } catch (error) {
    notifications.showNotification(`Dosya yüklenirken hata: ${error.message}`, 'error')
  }
}

const handleSuggestionSelected = (suggestion) => {
  newMessage.value = suggestion
  chat.suggestions.value = []
  messageInputRef.value?.focusInput()
}

const handleSendMessage = async () => {
  const messageText = newMessage.value
  newMessage.value = ''

  try {
    await chat.sendMessage(messageText)
    await loadAnalysisStatus()
    isConnected.value = true
  } catch (error) {
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      isConnected.value = false
      notifications.showNotification('Backend sunucusuna bağlanılamıyor. Lütfen sunucunun çalıştığından emin olun.', 'error')
    } else {
      notifications.showNotification(`Hata: ${error.message}`, 'error')
    }
  } finally {
    messageInputRef.value?.focusInput()
  }
}

const handleGenerateDocument = async () => {
  try {
    const promises = [
      document.generateAnalysisDocument(
        chat.sessionId.value,
        !!fileUpload.templateFile.value
      )
    ]

    if (isImageGenerationEnabled.value) {
      promises.push(document.generateVisualData(chat.sessionId.value))
    }

    await Promise.all(promises)

    showDocument.value = true
    notifications.showNotification(
      fileUpload.templateFile.value
        ? 'Template ile analiz dokümanı başarıyla oluşturuldu!'
        : 'Analiz dokümanı başarıyla oluşturuldu!',
      'success'
    )

    if (isImageGenerationEnabled.value) {
      notifications.showNotification('Görsel veriler başarıyla oluşturuldu!', 'success')
    }
  } catch (error) {
    notifications.showNotification(`Doküman oluşturulurken hata: ${error.message}`, 'error')
  }
}

const handleDocumentOpened = async (doc) => {
  try {
    const documentData = await document.loadDocument(chat.sessionId.value, doc.id)
    document.documentContent.value = documentData.content
    showDocument.value = true
  } catch (error) {
    notifications.showNotification('Doküman yüklenirken hata oluştu', 'error')
  }
}

const handleCloseDocument = () => {
  showDocument.value = false
  document.clearDocument()
}

onMounted(async () => {
  await checkConnection()
  await document.loadSessionDocuments(chat.sessionId.value)
  await loadAnalysisStatus()
  messageInputRef.value?.focusInput()

  const connectionChecker = setInterval(checkConnection, 30000)

  onUnmounted(() => {
    clearInterval(connectionChecker)
  })
})
</script>
