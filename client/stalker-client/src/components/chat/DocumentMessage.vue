<template>
  <div class="flex items-start space-x-4">
    <div class="flex-shrink-0">
      <div class="w-10 h-10 rounded-full bg-gradient-to-r from-emerald-600 to-teal-700 flex items-center justify-center shadow-lg">
        <DocumentTextIcon class="w-5 h-5 text-white" />
      </div>
    </div>

    <div class="relative max-w-2xl rounded-2xl px-4 py-3 bg-gray-800 border border-gray-700/50 text-gray-100 shadow-lg transition-all duration-200 hover:border-emerald-400">
      <div class="space-y-2">
        <div class="flex items-center space-x-2">
          <DocumentTextIcon class="w-4 h-4 text-emerald-400" />
          <span class="text-sm font-medium text-emerald-400">Analiz Dokümanı Oluşturuldu</span>
        </div>

        <div class="bg-gray-700/30 rounded-lg p-3 border border-gray-600/30">
          <h4 class="text-sm font-medium text-white mb-1">{{ document.title }}</h4>
          <p class="text-xs text-gray-300 mb-2">{{ formatDate(document.created_at) }}</p>

          <button
            @click="$emit('open-document', document)"
            class="inline-flex items-center space-x-1 px-3 py-1 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs transition-colors"
          >
            <DocumentTextIcon class="w-3 h-3" />
            <span>Dokümanı Görüntüle</span>
          </button>
        </div>
      </div>

      <div class="absolute top-4 -left-1 w-2 h-2 bg-gray-800 border-l border-b border-gray-700/50 transform rotate-45"></div>
    </div>
  </div>
</template>

<script setup>
import { DocumentTextIcon } from '@heroicons/vue/24/outline'

defineProps({
  document: {
    type: Object,
    required: true
  }
})

defineEmits(['open-document'])

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('tr-TR', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>
