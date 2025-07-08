<template>
  <div class="border-b border-gray-700/50 bg-gray-800/40">
    <div class="max-w-4xl mx-auto px-6 py-4">
      <div class="bg-gray-800/60 border border-gray-700/50 rounded-xl p-4">
        <div class="flex items-center justify-between mb-3">
          <h3 class="text-sm font-medium text-white flex items-center space-x-2">
            <DocumentIcon class="w-4 h-4 text-orange-400" />
            <span>Doküman Template Yükle</span>
          </h3>
          <button
            @click="$emit('close')"
            class="text-gray-400 hover:text-gray-200 hover:border hover:border-gray-400 rounded transition-all duration-200 p-1"
          >
            <XMarkIcon class="w-4 h-4" />
          </button>
        </div>

        <div v-if="!templateFile" class="space-y-3">
          <FileDropZone
            @files-dropped="handleFileDrop"
            @file-selected="handleFileSelect"
            accept=".txt,.md,.docx,.doc"
            :is-dropping="isDropping"
            message="Template dosyası seç veya buraya sürükle"
            help="Desteklenen formatlar: Word, Markdown, Text"
            color="orange"
          />
        </div>

        <div v-else class="space-y-3">
          <div class="flex items-center space-x-2 p-3 bg-orange-500/10 border border-orange-500/20 rounded-lg">
            <DocumentIcon class="w-5 h-5 text-orange-400" />
            <span class="text-sm text-orange-300 flex-1">{{ templateFile.name }}</span>
            <button
              @click="removeTemplate"
              class="text-gray-400 hover:text-gray-200 hover:border hover:border-gray-400 rounded transition-all duration-200 p-1"
            >
              <XMarkIcon class="w-4 h-4" />
            </button>
          </div>
          <p class="text-xs text-gray-400">
            ✓ Template yüklendi. Doküman oluşturulurken bu template kullanılacak.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { DocumentIcon, XMarkIcon } from '@heroicons/vue/24/outline'
import FileDropZone from './FileDropZone.vue'

defineProps({
  templateFile: Object
})

const emit = defineEmits([
  'close',
  'template-selected',
  'template-removed'
])

const isDropping = ref(false)

const handleFileDrop = (files) => {
  if (files.length > 0) {
    emit('template-selected', files[0])
  }
}

const handleFileSelect = (file) => {
  emit('template-selected', file)
}

const removeTemplate = () => {
  emit('template-removed')
}
</script>
