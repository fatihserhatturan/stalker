<template>
  <div class="flex flex-col h-full bg-gray-900/50">
    <DocumentHeader
      :is-generating-pdf="documentExport.isGeneratingPDF.value"
      :is-generating-word="documentExport.isGeneratingWord.value"
      @copy="handleCopy"
      @download-pdf="handleDownloadPDF"
      @download-word="handleDownloadWord"
      @close="$emit('close-document')"
    />

    <VisualToggle
      v-if="visualData"
      :is-expanded="showVisualComponents"
      :has-dynamic-data="!!visualData"
      @toggle="showVisualComponents = !showVisualComponents"
    >
      <VisualComponents
        :visual-data="visualData"
        @close="showVisualComponents = false"
      />
    </VisualToggle>

    <DocumentContent
      :document-content="documentContent"
      :is-loading="isLoading"
      :error="error"
    />

    <NotificationComponent :notification="notifications.notification.value" />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useDocumentExport } from '@/composables/useDocumentExport'
import { useNotifications } from '@/composables/useNotifications'

import DocumentHeader from './document/DocumentHeader.vue'
import VisualToggle from './document/VisualToggle.vue'
import DocumentContent from './document/DocumentContent.vue'
import VisualComponents from './VisualComponents.vue'
import NotificationComponent from './ui/NotificationComponent.vue'

const props = defineProps({
  documentContent: {
    type: String,
    default: ''
  },
  sessionId: {
    type: String,
    default: ''
  },
  visualData: {
    type: Object,
    default: () => null
  }
})

defineEmits(['close-document'])

const documentExport = useDocumentExport()
const notifications = useNotifications()

const isLoading = ref(false)
const error = ref('')
const showVisualComponents = ref(false)

const handleCopy = () => {
  documentExport.copyToClipboard(props.documentContent)
}

const handleDownloadPDF = () => {
  documentExport.downloadPDF(props.documentContent)
}

const handleDownloadWord = () => {
  documentExport.downloadWord()
}

watch(() => props.documentContent, (newContent) => {
  if (newContent) {
    isLoading.value = false
    error.value = ''
  }
}, { immediate: true })

watch(() => props.visualData, (newVisualData) => {
  if (newVisualData) {
    showVisualComponents.value = true
  }
}, { immediate: true })
</script>
