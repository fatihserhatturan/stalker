<template>
  <div class="mb-4 p-4 bg-gray-800/60 border border-gray-700/50 rounded-xl">
    <div class="flex items-center justify-between mb-3">
      <h3 class="text-sm font-medium text-white">Proje Dosyası Yükle</h3>
      <button
        @click="$emit('close')"
        class="text-gray-400 hover:text-gray-200 hover:border hover:border-gray-400 rounded transition-all duration-200 p-1"
      >
        <XMarkIcon class="w-4 h-4" />
      </button>
    </div>

    <FileDropZone
      @files-dropped="handleFileDrop"
      @file-selected="handleFileSelect"
      accept=".txt,.md,.pdf,.docx,.doc"
      :is-dropping="isDropping"
      message="Dosya seç veya buraya sürükle"
      help="Desteklenen formatlar: PDF, Word, Markdown, Text"
      color="purple"
    />

    <SelectedFileDisplay
      v-if="selectedFile"
      :file="selectedFile"
      :is-uploading="isUploading"
      @upload="handleUpload"
      @remove="removeSelectedFile"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { XMarkIcon } from '@heroicons/vue/24/outline'
import FileDropZone from './FileDropZone.vue'
import SelectedFileDisplay from './SelectedFileDisplay.vue'

defineProps({
  selectedFile: Object,
  isUploading: Boolean
})

const emit = defineEmits([
  'close',
  'file-selected',
  'file-removed',
  'upload-file'
])

const isDropping = ref(false)

const handleFileDrop = (files) => {
  if (files.length > 0) {
    emit('file-selected', files[0])
  }
}

const handleFileSelect = (file) => {
  emit('file-selected', file)
}

const handleUpload = () => {
  emit('upload-file')
}

const removeSelectedFile = () => {
  emit('file-removed')
}
</script>
