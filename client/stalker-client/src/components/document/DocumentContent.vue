<template>
  <div class="flex-1 overflow-hidden">
    <DocumentLoadingState v-if="isLoading" />
    <DocumentErrorState v-else-if="error" :error="error" />
    <DocumentMarkdownView v-else :content="documentContent" />
  </div>
</template>

<script setup>
import DocumentLoadingState from './DocumentLoadingState.vue'
import DocumentErrorState from './DocumentErrorState.vue'
import DocumentMarkdownView from './DocumentMarkdownView.vue'

defineProps({
  documentContent: String,
  isLoading: Boolean,
  error: String
})
</script>
