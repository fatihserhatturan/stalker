<template>
  <div class="mt-3 flex items-center space-x-2 p-3 bg-gray-700/50 rounded-lg">
    <DocumentTextIcon class="w-5 h-5 text-purple-400" />
    <span class="text-sm text-gray-300 flex-1">{{ file.name }}</span>

    <button
      @click="$emit('upload')"
      :disabled="isUploading"
      class="px-3 py-1 bg-purple-600 hover:border-purple-400 text-white text-xs rounded-md transition-all duration-200 disabled:bg-gray-600 disabled:cursor-not-allowed border border-transparent"
    >
      {{ isUploading ? 'Yükleniyor...' : 'Yükle' }}
    </button>

    <button
      @click="$emit('remove')"
      :disabled="isUploading"
      class="text-gray-400 hover:text-gray-200 hover:border hover:border-gray-400 rounded transition-all duration-200 p-1 disabled:cursor-not-allowed"
    >
      <XMarkIcon class="w-4 h-4" />
    </button>
  </div>
</template>

<script setup>
import { DocumentTextIcon, XMarkIcon } from '@heroicons/vue/24/outline'

defineProps({
  file: Object,
  isUploading: Boolean
})

defineEmits(['upload', 'remove'])
</script>
