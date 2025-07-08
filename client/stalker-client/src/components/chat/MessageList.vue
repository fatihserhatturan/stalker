<template>
  <div class="flex-1 overflow-hidden">
    <div class="h-full max-w-4xl mx-auto">
      <div
        ref="messageContainer"
        class="h-full overflow-y-auto px-6 py-6 space-y-6 scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-transparent"
      >
        <div class="space-y-6">
          <ChatMessage
            v-for="msg in messages"
            :key="msg.id"
            :message="msg"
          />

          <SuggestionList
            v-if="suggestions.length > 0 && !isLoading"
            :suggestions="suggestions"
            @suggestion-selected="$emit('suggestion-selected', $event)"
          />

          <DocumentMessage
            v-for="doc in sessionDocuments"
            :key="doc.id"
            :document="doc"
            @open-document="$emit('document-opened', $event)"
          />
        </div>

        <LoadingIndicator
          v-if="isLoading"
          message="AI analiz yapıyor..."
        />

        <LoadingIndicator
          v-if="isGeneratingDocument"
          :message="templateFile ? 'Template ile doküman oluşturuluyor...' : 'Analiz dokümanı oluşturuluyor...'"
          color="emerald"
        />

        <LoadingIndicator
          v-if="isUploadingFile"
          message="Dosya yükleniyor ve analiz ediliyor..."
          color="purple"
        />

        <ConnectionError v-if="!isConnected" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'
import ChatMessage from './ChatMessage.vue'
import SuggestionList from './SuggestionList.vue'
import DocumentMessage from './DocumentMessage.vue'
import LoadingIndicator from './LoadingIndicator.vue'
import ConnectionError from './ConnectionError.vue'

defineEmits([
  'suggestion-selected',
  'document-opened'
])

const messageContainer = ref(null)

const props = defineProps({
  messages: Array,
  suggestions: Array,
  sessionDocuments: Array,
  isLoading: Boolean,
  isGeneratingDocument: Boolean,
  isUploadingFile: Boolean,
  isConnected: Boolean,
  templateFile: Object
})

const scrollToBottom = async () => {
  await nextTick()
  const container = messageContainer.value
  if (container) {
    container.scrollTop = container.scrollHeight
  }
}

watch(() => [
  props.messages,
  props.sessionDocuments,
  props.isLoading,
  props.isGeneratingDocument,
  props.isUploadingFile
], scrollToBottom, { deep: true, flush: 'post' })

defineExpose({
  scrollToBottom
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
</style>
