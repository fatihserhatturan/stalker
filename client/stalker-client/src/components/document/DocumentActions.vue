<template>
  <div class="flex items-center space-x-2">
    <DownloadDropdown
      :is-generating-pdf="isGeneratingPdf"
      :is-generating-word="isGeneratingWord"
      @download-pdf="$emit('download-pdf')"
      @download-word="$emit('download-word')"
    />

    <button
      @click="$emit('copy')"
      class="flex items-center space-x-1 px-3 py-2 bg-gray-700 border border-gray-600 hover:border-gray-400 text-white rounded-lg transition-colors text-sm"
    >
      <ClipboardDocumentIcon class="w-4 h-4" />
      <span>Kopyala</span>
    </button>

    <button
      @click="$emit('close')"
      class="p-2 text-gray-400 border border-transparent hover:border-gray-500 rounded-lg transition-colors"
    >
      <XMarkIcon class="w-4 h-4" />
    </button>
  </div>
</template>

<script setup>
import { ClipboardDocumentIcon, XMarkIcon } from '@heroicons/vue/24/outline'
import DownloadDropdown from './DownloadDropdown.vue'

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
