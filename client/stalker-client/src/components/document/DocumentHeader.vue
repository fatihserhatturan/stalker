<template>
  <div class="bg-gray-800/80 backdrop-blur-md border-b border-gray-700/50 shadow-lg">
    <div class="px-6 py-4 h-[80px]">
      <div class="flex items-center justify-between">
        <DocumentTitle />
        <DocumentActions
          @copy="$emit('copy')"
          @download-pdf="$emit('download-pdf')"
          @download-word="$emit('download-word')"
          @close="$emit('close')"
          :is-generating-pdf="isGeneratingPdf"
          :is-generating-word="isGeneratingWord"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import DocumentTitle from './DocumentTitle.vue'
import DocumentActions from './DocumentActions.vue'

defineProps({
  isGeneratingPdf: Boolean,
  isGeneratingWord: Boolean
})

defineEmits([
  'copy',
  'download-pdf',
  'download-word',
  'close'
])
</script>
